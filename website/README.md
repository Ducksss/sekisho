# Sekisho public website

Live: [getsekisho.vercel.app](https://getsekisho.vercel.app).

Static brand and project-information site, deployed separately from the operational
Next.js console. The default /try/ configuration is an explicit simulation and makes no gate requests, wallet connections or payment mutations. An optional limited public runner adapter is disabled until configured.
All product screenshots retain their synthetic-fixture labels. The live backend and
contract rehearsal are tracked in [readiness](../docs/readiness.md).

## Preview

From the repository root:

```bash
python3 -m http.server 3112 --bind 127.0.0.1 --directory website
```

Open `http://localhost:3112`. This is static HTML/CSS with native JavaScript modules; there is no dependency
installation or framework build. The guided simulation never contacts the gate. The source assets and font provenance are in [docs/assets](../docs/assets/README.md).

## Keep examples current

Canonical synthetic cases and scenario copy live in `dashboard/fixtures/`. The
website ships generated excerpts without live flags, addresses, or transaction hashes.
The displayed and downloadable Python example comes from the tested SDK example.

```bash
python3 scripts/build_website_demo.py
python3 scripts/build_website_demo.py --check
node --test scripts/test-website-demo.mjs
.venv/bin/python -m pytest sdk/tests/test_website_example.py -q
```

Use native browser controls to verify all scenarios, back/restart, release/refund,
scenario resets, keyboard focus, copy/download, and mobile layout. With JavaScript
unavailable, the site retains its setup link and readable SDK code.

## Deploy

Vercel project: `sekisho`, scope: `ducksss-projects`, connected to `Ducksss/sekisho`.
The project root is `website`, with static output `.` and no framework build.

Push to `main` to update [getsekisho.vercel.app](https://getsekisho.vercel.app)
automatically after a successful deployment. Pushes to other branches create preview
deployments. The Python gate, operational dashboard, and contracts are outside the
publishing root.

For a manual fallback, run from the repository root; Vercel applies the configured
`website` root:

```bash
vercel link --project sekisho --scope ducksss-projects
vercel deploy --dry --json
vercel deploy --prod --scope ducksss-projects
```

Inspect the dry-run file list before publishing. `.env*` and `.vercel/` are ignored;
no environment variables or secrets are required by this site. The command creates a
static production deployment. Keep the Vercel project root set to `website` for both
Git integration and CLI publication.

## Verification

Desktop and 390px mobile layouts and guided flows reviewed in Chromium; no horizontal overflow.
Verified heading structure, asset paths/dimensions, section anchors, keyboard FAQ,
source/readiness links, and fixture labels. Reduced motion disables smooth scrolling
and transitions; forced colors retain system semantics. Verify production `/`, asset
URLs, and the custom 404 after each deployment.

## Guided browser trial

Open `/try/` for four clearly labelled illustrative branches: allowed, blocked,
human review, and unavailable evidence. Simulation makes no requests to the gate.
The timeline separates evidence, policy, signing and settlement. HOLD never implies
an escrow deposit. Purchased sample content is not live market data.

Run the focused checks with `node --test website/try/state.test.mjs`.

For the live trial, deploy the limited public runner separately, verify its setup
and set `publicRunnerURL` in `try/config.mjs` to its HTTPS origin. **No secrets belong
in this file.** Configure the runner's allowed CORS origin for the website. The adapter
uses `/public/readiness`, `POST /public/runs`, and `GET /public/runs/{run_id}`.
Readiness must explicitly report live Base Sepolia mode before a run can be requested.
Two live presets (`clean`, `flagged`) map to the illustrative choices; unavailable
evidence is simulation-only. Current live evidence controls the actual verdict.

Browser-generated session/idempotency identifiers use sessionStorage. A pending key
survives an ambiguous request failure, so retry does not automatically duplicate a
purchase. Never place run capability IDs in public URLs. No privileged operator token
is accepted by the page. Result data uses textContent, never provider HTML.

Transaction links appear only for runner status `paid` with a valid hash; the runner
must independently validate the Base Sepolia receipt and exact USDC transfer. Seller
content is shown only in that confirmed state. Case and canonical-report data are
rendered only when returned. The report consistency indicator is explicitly a server
check; it is not an independent browser/onchain attestation verification.

Before enabling the adapter, test the real hosted path including origin restrictions,
limits, repeat clicks, concurrent requests, provider failures and restarted processes.
The static site cannot host the gate or its persistent state. No live test is claimed
by the presence of this UI adapter.
