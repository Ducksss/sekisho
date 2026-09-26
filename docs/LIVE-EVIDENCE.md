# Live evidence record

**Status: not executed in this finalisation pass.** Keys are assumed unavailable.
Do not replace pending items with unit-test results or simulation screenshots.

## Capture for each real browser run

| Evidence | Allowed purchase | Refusal or pause |
|---|---|---|
| UTC start/end and source commit | Pending | Pending |
| Public run/case identifiers (redact bearer run capability from shared logs) | Pending | Pending |
| Actual recipient and screening network | Pending | Pending |
| Quick Scan HTTP status, timestamp, verbatim traits | Pending | Pending |
| Policy version/hash and decision reason | Pending | Pending |
| Signing result (permitted / no signature) | Pending | Pending |
| Base Sepolia receipt and matching USDC Transfer | Pending | Not expected for refusal |
| Purchased report delivered | Pending | Not expected |
| Canonical report hash consistency | Pending | Pending |
| MultiBaas attestation receipt + indexed Screened event | Pending | Pending |
| Elapsed time and provider calls consumed | Pending | Pending |

A transaction hash alone is not settlement evidence. Match a successful receipt to
the configured buyer, exact preset recipient, canonical test USDC and 50,000 atomic
units. A hash match proves consistency of the served report, not truth of the provider.

## Rehearsal checklist

1. Run `.venv/bin/python scripts/check_setup.py --minimum` (offline config only).
2. Validate credentials and supported real mainnet profiles; do not synthesize clean
   data for an unknown buyer. Set vendor recipients only from reviewed profiles.
3. Confirm Base Sepolia chain 84532, role-wallet balances and contract addresses.
4. Deploy/link contracts, register the webhook and saved MultiBaas queries, and run
   `.venv/bin/python scripts/smoke.py`. Keep all privileged endpoints private.
5. Run S1 and S3 locally; collect actual results. If evidence produces HOLD instead
   of the expected verdict, investigate it; do not edit policy merely for a green demo.
6. Only after this evidence is reviewed, enable the public runner and repeat the
   allowed/refused path through the browser, within its fixed testnet limits.
7. Verify provider 401/429/timeout/malformed data fails closed with controlled tests.
   Do not deliberately exhaust the real sponsor quota.
8. For the separate escrow showcase, prove deposit, officer authorization, fresh
   clearance and release/refund receipts. Public HOLD by itself is not an escrow demo.
9. Replace the pitch proof slide with measured results and record new narration.

## Sponsor feedback (write after live use)

Intercepta: pending actual integration feedback (3–5 lines).
Curvegrid: pending actual API/event-query/webhook feedback.
Team review and names/socials: pending confirmation.
