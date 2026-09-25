# Build and rehearsal readiness

Updated 26 September 2026. Code and local verification do not establish live readiness.

The public project website is deployed at [getsekisho.vercel.app](https://getsekisho.vercel.app).
It provides a labelled, browser-only walkthrough of four synthetic screening scenarios,
fixture screenshots, a tested SDK example, and setup links. It does not host the gate
or execute payments. The console theme now follows the website palette.

## Implemented locally

Gate policy and integrations, registry and escrow contracts, x402 payer/payee hooks,
vendor and treasury agents, spoofed-payer runner, MCP, scenario/control scripts, setup
and smoke scripts. Console includes live decisions, case review, hold queue, audit,
treasury balance/exposure/counterparty views, policy and integration pages.

## Local verification

- Python: 356 tests pass; contracts: 18 pass with `forge test --offline`.
- Console: production build, lint and 45 report-hash checks pass.
- Chromium at 1440×1000 and 390×844: routes render, no document overflow or uncaught
  app errors; fixture review/release updates the queue; report Match/Mismatch and
  premature-release rejection work; audit filtering and keyboard disclosure work.
- Production-mode browser requests intercepted only by the test harness: loading,
  partial data (missing balance stays unavailable), failed read, retry and empty states
  pass. Fixtures are disabled in this build. The deliberate 503 produces the expected
  browser network error and a recoverable UI error.
- Actual gate startup with a temporary database and unavailable dependencies returns
  degraded health and fail-closed HOLD. No signatures or transactions are produced.
- Shared design audit passes; design-document lint has no errors (token-reference
  warnings remain because CSS, rather than the document, owns runtime mappings).

## Website improvement verification (26 September)

The SDK suite passes all 54 tests, including seven tests for
`sdk/examples/screen_before_signing.py`: all three verdicts,
HTTP errors, timeout, and malformed response. Three browser-demo state tests pass.
The generated website excerpts and downloadable example match their source files.
Console production build and lint pass after the shared theme update. Browser QA
covers desktop and 390px mobile flows, keyboard use, scenario resets, simulated release
and refund, BLOCK, and fail-closed HOLD. These are synthetic demonstrations.

`make check-setup` still reports 6/20 checks passing. Intercepta, Blockscout, MultiBaas,
webhook configuration, role-wallet keys and clean/mixer vendor addresses are absent.
No live proof or recording can be produced from this checkout yet.

## Required before calling this complete

- Configure service keys and MultiBaas deployment, webhook URL/secret, and fresh testnet
  wallets. `make check-setup` reports missing values without exposing them.
- Fund gas and buyer test USDC; deploy/link the contracts; save genuine addresses and
  deployment records; register the webhook and saved Event Queries.
- Scan candidates and select a clean vendor, mixer-exposed HOLD vendor, and clean buyer.
  Capture actual Intercepta response bodies and replace the synthetic profile fixtures;
  retain provenance, capture time, HTTP status and verbatim descriptions.
- Run `make smoke` successfully after an event has reached the gate. Check quota >150,
  balances/allowance, oracle self-test, and recent webhook delivery.
- Rehearse S1–S5 twice with a reset between runs, plus S6 under explicit timeout fault
  injection. Prove settlement, escrow release, two-sided screening and browser report
  verification using real indexed events. `all` currently runs S1–S5; S6 is separate.
- Measure latency against the PRD budgets with live dependencies. Tests do not establish
  the p50/p95 performance targets.
- Complete human review in docs/ai-usage.md, publish real integration feedback and team
  details, record the human-narrated video, and complete the submission manually.

No live credentials or funded wallets were available during the local completion pass.
No testnet deployment or money-transfer scenario was executed by that pass. API test
mocks and browser fixtures were used only for automated/local verification.
