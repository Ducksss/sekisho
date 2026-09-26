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

## Earlier local verification

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

At that earlier pass, `make check-setup` reported 6/20 checks passing. Intercepta, Blockscout, MultiBaas,
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


## MVP implementation verification (26 September 2026, latest pass)

The current local source includes payment/decision binding, $1/payment and $5/run
reservations, Base Sepolia write restrictions, operator authentication, fail-closed
provider responses, complete deduplication inputs, and verified payment/hold receipts.
See [HACKATHON-MVP.md](HACKATHON-MVP.md) for the prioritized acceptance checklist.

- Integrated `.venv/bin/python -m pytest -q`: **446 passed**, Python 3.12.14.
- Foundry `forge test -vv`: **18 passed**, including 256-run fuzz checks.
- Dashboard production build, TypeScript and ESLint passed; report-hash checks **45 passed**.
- Local production console: dummy operator token can be set and is cleared on reload.
  Backend-offline errors render explicitly. This is not a live payment rehearsal.
- MultiBaas API authentication returned HTTP 200; status confirmed chain **84532**.
- Four fresh testnet role wallets exist in the ignored, mode-0600 `.env`. At the latest
  balance check all had zero ETH and the buyer had zero test USDC.
- Intercepta key and testnet funding are still pending. No contracts were deployed and
  no live payment, live Intercepta qualification, or indexed-event rehearsal was completed.

The Python tests use mocked upstream providers. Passing tests does not establish sponsor
qualification. The per-run spending reserve resets on process restart. Human review and
live S1/S3 evidence remain required. Changes are local and have not been pushed upstream.

## Browser finalisation pass (26 September 2026)

The latest implementation adds a guided `/try/` simulation and an opt-in public
runner with durable limits, isolated results, exact preset payment terms, live/fresh
screening checks and independent settlement verification. Console wording separates
policy decisions, request amounts and confirmed financial states. The earlier local
payment/auth/receipt fixes are included in the finalisation publication, rather than
only the branding changes.

Fresh verification:
- Combined Python suite: **459 passed**; final output-copy adjustment rechecked with
  all **13 public-runner tests passing**.
- Dashboard production build/TypeScript and ESLint passed; **45 hash checks passed**.
- Website state tests: **8 passed**; generated examples remain current.
- Real keyless local public API: readiness unavailable, launch HTTP 503, three
  privileged routes HTTP 404. No provider requests or payments made.
- Browser: four labelled scenarios, keyboard activation, correct result focus and
  390/1280px responsive checks; root additionally inspected the desktop trial.
- Deployment YAML parses and Python launcher compiles. Docker is unavailable on this
  machine, so image build/cloud runtime is not yet verified.
- No contract sources changed in this pass; Foundry is unavailable in the current
  environment, so prior contract results above are historical, not a fresh rerun.
- Revised 10-slide deck rendered/inspected with package/layout checks. Live proof
  remains pending; old narration audio was not synced to the revised script.

Hosting: Render account sign-in completed; repository authorization must include
Ducksss/sekisho before its persistent service can be created. Blueprint defaults
public execution off. Credentials, funding, deployed contract/event proof, live
browser tests and team feedback remain outstanding. See FINALISATION-PLAN.md,
PUBLIC-TRIAL.md and LIVE-EVIDENCE.md. This is keyless readiness, not sponsor qualification.

### Later live preflight in the same pass

The team added Intercepta and Blockscout keys. Their authenticated read-only checks
now pass; see LIVE-EVIDENCE.md for successful scans and timeout/rate-limit limits.
Buyer test-USDC balance is 20; all role wallets still need Base Sepolia ETH. MultiBaas
authenticates but has no linked addresses. No transactions have been sent. The deck
now reflects API access verified, payment/attestation proof pending.

Foundry v1.8.3 was obtained from its official release and checksum-verified outside
the repo. A fresh isolated exact-source contract run passed **18 tests**, including
256 runs for each of 2 fuzz tests. It used a stripped environment and no private keys.
GitHub CI for commit 0f2ae6c94dd97aae0015d4038bce1dc75fdd7868 also completed successfully:
https://github.com/Ducksss/sekisho/actions/runs/36239045404 .

### Local x402 payment rehearsal

One 0.05 test-USDC purchase settled through the facilitator and delivered its report.
The initial receipt report encountered a block-indexing delay; reconciling the same
transaction later succeeded and the case is PAID. One live flagged-vendor run passed
S3 with BLOCK, no signature and REFUSED status. Both canonical hashes match. No
registry attestation succeeded: contracts/role gas/hosted browser proof remain pending.
Full timings, identifiers and the initial S1 failure are retained in LIVE-EVIDENCE.md.

### Latest reconciliation status

Two local 0.05 test-USDC purchases have settled, both reconciled to PAID by reporting
the same existing transaction after the initial RPC block lookup failed. The first
bounded retry patch did not fix the live S1 assertion; keep this limitation visible.
Buyer now has 19.90 test USDC. No registry/escrow transactions have been sent.
The updated deck contains the first paid/refused evidence with these limitations.

Receipt refresh now re-fetches the same transaction when a provisional block hash
is unavailable, with tests for changed/placeholder hashes and fail-closed validation.
Both settled receipts pass the revised verifier against the real RPC. First-attempt
confirmation after a fresh payment remains unverified; no third purchase was sent.

Final combined Python run after receipt refresh: **473 passed**. Five trial state
tests also pass; root visually reviewed the recorded evidence panel.
