"""scripts/capture_intercepta.py writes live bodies with their provenance, counts quota,
keeps the key out of stdout and leaves a fixture alone on a failed call (respx only)."""

import importlib.util
import json

import httpx
import pytest

from sekisho_gate.config import REPO_ROOT
from sekisho_gate.screening.cache import QUOTA_KEY, InterceptaCache

pytestmark = pytest.mark.respx(assert_all_called=False)  # unmatched requests still fail

BASE = "https://api.web3antivirus.io/api/public"
CLEAN = "0x1111111111111111111111111111111111111111"
MIXER = "0x2222222222222222222222222222222222222222"
SANCTIONED = "0x098B716B8Aaf21512996dC57EB0615e2383E2f96"
KEY = "live-key-never-printed"
DESCRIPTION = "Intercepta’s own text, with a curly apostrophe"


def load_script():
    spec = importlib.util.spec_from_file_location("capture_intercepta", REPO_ROOT / "scripts" / "capture_intercepta.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


capture = load_script()


@pytest.fixture
def settings(make_settings):
    return make_settings(intercepta_api_key=KEY, vendor_clean_payto=CLEAN, vendor_mixer_payto=MIXER,
                         vendor_sanctioned_payto=SANCTIONED)


def score(description: str = DESCRIPTION) -> dict:
    return {"toxicScore": 0, "traits": [{"name": "fake_phishing_transfer", "risk": 20, "txsCount": 2,
                                         "description": description}]}


def test_writes_live_bodies_with_provenance(respx_mock, settings, tmp_path, capsys):
    route = respx_mock.get(f"{BASE}/v2/extension/account/{CLEAN.lower()}/quick-scan").mock(
        return_value=httpx.Response(200, text=json.dumps(score(), ensure_ascii=False)))
    with httpx.Client() as http:
        code = capture.main(["--only", "clean_quick_scan.json"], http=http, settings=settings, out_dir=tmp_path)
    assert code == 0 and route.call_count == 1
    assert route.calls[0].request.headers["X-API-KEY"] == KEY
    wrapper = json.loads((tmp_path / "clean_quick_scan.json").read_text(encoding="utf-8"))
    meta = wrapper["_meta"]
    assert meta["synthetic"] is False and meta["http_status"] == 200 and wrapper["status"] == 200
    assert meta["address"] == CLEAN and meta["captured_at"].endswith("Z")
    assert meta["endpoint"] == "GET /api/public/v2/extension/account/{address}/quick-scan"
    assert isinstance(meta["latency_ms"], int)
    assert wrapper["response"]["traits"][0]["description"] == DESCRIPTION  # verbatim
    assert InterceptaCache(settings.db_path).value(QUOTA_KEY) == 1
    assert KEY not in capsys.readouterr().out


def test_token_capture_sends_the_mainnet_chain(respx_mock, settings, tmp_path):
    body = {"action": "info", "riskLevel": "neutral", "detectors": []}
    route = respx_mock.get(f"{BASE}/v2/extension/token-intelligence/token/{capture.BASE_USDC.lower()}/risks").mock(
        return_value=httpx.Response(200, json=body))
    with httpx.Client() as http:
        assert capture.main(["--only", "token_base_usdc.json"], http=http, settings=settings, out_dir=tmp_path) == 0
    assert route.calls[0].request.url.params["chainId"] == "8453"
    wrapper = json.loads((tmp_path / "token_base_usdc.json").read_text(encoding="utf-8"))
    assert wrapper["response"] == body and wrapper["_meta"]["endpoint"].endswith("?chainId=8453")


def test_failed_call_leaves_the_fixture_alone(respx_mock, settings, tmp_path, capsys):
    existing = tmp_path / "mixer_quick_scan.json"
    existing.write_text('{"_meta": {"synthetic": true}}\n', encoding="utf-8")
    respx_mock.get(f"{BASE}/v2/extension/account/{MIXER.lower()}/quick-scan").mock(
        return_value=httpx.Response(429, text="Too Many Requests"))
    with httpx.Client() as http:
        code = capture.main(["--only", "mixer_quick_scan.json"], http=http, settings=settings, out_dir=tmp_path)
    assert code == 1
    assert existing.read_text(encoding="utf-8") == '{"_meta": {"synthetic": true}}\n'
    out = capsys.readouterr().out
    assert "HTTP 429" in out and "fixture unchanged" in out and KEY not in out


def test_dry_run_sends_nothing(respx_mock, settings, tmp_path, capsys):
    with httpx.Client() as http:
        assert capture.main(["--dry-run"], http=http, settings=settings, out_dir=tmp_path) == 0
    assert not respx_mock.calls and not list(tmp_path.glob("*.json"))
    assert "5 live Intercepta call(s)" in capsys.readouterr().out


def test_refuses_without_a_key_or_an_address(make_settings, tmp_path):
    no_key = make_settings(intercepta_api_key="", vendor_clean_payto=CLEAN, vendor_mixer_payto=MIXER)
    assert capture.main([], settings=no_key, out_dir=tmp_path) == 2
    no_vendor = make_settings(vendor_clean_payto="", vendor_mixer_payto=MIXER)
    assert capture.main([], settings=no_vendor, out_dir=tmp_path) == 2
