"""Capture live Intercepta responses as the gate's test fixtures (docs/readiness.md).

    .venv/bin/python scripts/capture_intercepta.py             # the .env vendors + Base USDC
    .venv/bin/python scripts/capture_intercepta.py --dry-run   # print the plan, call nothing
    .venv/bin/python scripts/capture_intercepta.py --only mixer_quick_scan.json --mixer 0xabc…

One live, keyed GET per fixture (five by default), counted in the gate's quota table like
every other Intercepta call. Each body goes to gate/tests/data/intercepta/<file> with its
provenance: endpoint, address, capture time (UTC), HTTP status and latency. The body is
stored as parsed JSON, so trait and detector descriptions stay verbatim. A non-200 answer
or a body that is not a JSON object is reported and the existing fixture is left alone.
The API key is never printed.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx
from eth_utils import is_address, to_checksum_address

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sekisho_gate.screening.cache import QUOTA_KEY, InterceptaCache  # noqa: E402
from sekisho_gate.screening.intercepta import PATHS  # noqa: E402

OUT_DIR = ROOT / "gate" / "tests" / "data" / "intercepta"
BASE_USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"  # the token the gate scans for Base Sepolia USDC
TIMEOUT_S = 10.0  # generous: this is a capture, not the gate's 3 s payment budget


def targets(settings: Any, clean: str | None, mixer: str | None, sanctioned: str | None) -> list[dict[str, Any]]:
    clean = clean or settings.vendor_clean_payto
    mixer = mixer or settings.vendor_mixer_payto
    sanctioned = sanctioned or settings.vendor_sanctioned_payto
    return [
        {"file": "clean_quick_scan.json", "kind": "quick_scan", "address": clean,
         "role": "S1 clean vendor (VENDOR_CLEAN_PAYTO)"},
        {"file": "mixer_quick_scan.json", "kind": "quick_scan", "address": mixer,
         "role": "S2 mixer-exposed vendor (VENDOR_MIXER_PAYTO)"},
        {"file": "sanctioned_quick_scan.json", "kind": "quick_scan", "address": sanctioned,
         "role": "S3/S4 sanctioned address (VENDOR_SANCTIONED_PAYTO)"},
        {"file": "impersonation_clean.json", "kind": "impersonation", "address": clean,
         "role": "impersonation check on the S1 clean vendor"},
        {"file": "token_base_usdc.json", "kind": "token", "address": BASE_USDC, "params": {"chainId": "8453"},
         "role": "Scan Token on Base USDC, the mainnet equivalent of Base Sepolia USDC"},
    ]


def endpoint_label(kind: str, params: dict[str, str] | None) -> str:
    query = ("?" + "&".join(f"{k}={v}" for k, v in params.items())) if params else ""
    return f"GET {PATHS[kind]}{query}"


def capture_one(http: httpx.Client, base_url: str, key: str, target: dict[str, Any],
                cache: InterceptaCache) -> tuple[dict[str, Any] | None, str]:
    """One live call. Returns (fixture wrapper, message); the wrapper is None on failure."""
    address = target["address"].lower()
    url = base_url.rstrip("/") + PATHS[target["kind"]].format(address=address)
    cache.incr(QUOTA_KEY)  # counted before it is sent, as the gate does
    captured_at = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    t0 = time.monotonic()
    try:
        resp = http.get(url, params=target.get("params"), timeout=TIMEOUT_S,
                        headers={"X-API-KEY": key, "Accept": "application/json"})
    except httpx.HTTPError as exc:
        return None, f"request failed: {type(exc).__name__}"
    latency_ms = int((time.monotonic() - t0) * 1000)
    if resp.status_code != 200:
        return None, f"HTTP {resp.status_code} in {latency_ms} ms: {resp.text[:300]}"
    try:
        body = json.loads(resp.text)
    except ValueError:
        return None, f"HTTP 200 in {latency_ms} ms, but the body is not JSON: {resp.text[:300]}"
    if not isinstance(body, dict):
        return None, f"HTTP 200 in {latency_ms} ms, but the body is not a JSON object: {resp.text[:300]}"
    meta = {
        "synthetic": False,
        "source": "live Intercepta API response, captured with scripts/capture_intercepta.py",
        "endpoint": endpoint_label(target["kind"], target.get("params")),
        "role": target["role"],
        "address": to_checksum_address(target["address"]),
        "captured_at": captured_at,
        "http_status": resp.status_code,
        "latency_ms": latency_ms,
        "note": "The body is exactly as received, parsed as JSON; descriptions are Intercepta's own text.",
    }
    return {"_meta": meta, "status": resp.status_code, "response": body}, f"HTTP 200 in {latency_ms} ms"


def main(argv: list[str] | None = None, *, http: httpx.Client | None = None, settings: Any = None,
         out_dir: Path = OUT_DIR) -> int:
    parser = argparse.ArgumentParser(description="Capture live Intercepta responses as test fixtures")
    parser.add_argument("--clean", help="S1 vendor address (default VENDOR_CLEAN_PAYTO)")
    parser.add_argument("--mixer", help="S2 vendor address (default VENDOR_MIXER_PAYTO)")
    parser.add_argument("--sanctioned", help="S3 address (default VENDOR_SANCTIONED_PAYTO)")
    parser.add_argument("--only", nargs="+", metavar="FILE", help="capture only these fixture files")
    parser.add_argument("--dry-run", action="store_true", help="print the plan, send nothing")
    args = parser.parse_args(argv)

    if settings is None:
        from sekisho_gate.config import get_settings

        settings = get_settings()
    plan = targets(settings, args.clean, args.mixer, args.sanctioned)
    if args.only:
        unknown = set(args.only) - {t["file"] for t in plan}
        if unknown:
            print(f"unknown fixture file(s): {', '.join(sorted(unknown))}", file=sys.stderr)
            return 2
        plan = [t for t in plan if t["file"] in args.only]
    bad = [t for t in plan if not is_address(t["address"] or "")]
    if bad:
        for t in bad:
            print(f"{t['file']}: no valid address for {t['role']}", file=sys.stderr)
        return 2
    key = settings.intercepta_api_key.get_secret_value().strip()
    if not key and not args.dry_run:
        print("INTERCEPTA_API_KEY is not set in .env: a capture needs a live, keyed call.", file=sys.stderr)
        return 2

    print(f"{'Dry run: ' if args.dry_run else ''}{len(plan)} live Intercepta call(s) -> {out_dir}")
    if args.dry_run:
        for t in plan:
            print(f"  {t['file']}: {endpoint_label(t['kind'], t.get('params'))} for {t['address']} ({t['role']})")
        return 0

    cache = InterceptaCache(settings.db_path)
    own = http is None
    client = http or httpx.Client()
    failures = 0
    try:
        for t in plan:
            wrapper, message = capture_one(client, settings.intercepta_base_url, key, t, cache)
            if wrapper is None:
                failures += 1
                print(f"  FAILED {t['file']} ({t['address']}): {message}; fixture unchanged")
                continue
            path = out_dir / t["file"]
            path.write_text(json.dumps(wrapper, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"  wrote {t['file']} ({t['address']}): {message}")
    finally:
        if own:
            client.close()
    used = cache.value(QUOTA_KEY)
    print(f"Intercepta calls counted so far: {used}/{settings.intercepta_quota}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
