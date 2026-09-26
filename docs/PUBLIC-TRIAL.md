# Public browser trial

## What works without credentials

`website/try/` is a static, guided simulation. Serve `website/` over HTTP and open
`/try/`. No wallet, key, faucet or provider request is needed. The four scenarios
are synthetic and labelled. A simulation never produces a real transaction link.

The public Python service exposes `/public/readiness`, `/public/runs` and an isolated
run result. It is disabled by default. Live readiness is a configuration gate, not a
claim that providers, funding or contracts have been validated.

```bash
make public-trial
# Other terminal, for the static page:
python3 -m http.server 3112 --directory website
```

The website's `try/config.mjs` contains only the public API base URL. Leave it empty
until the hosted backend is ready. Use HTTPS publicly. Do not put provider keys,
operator tokens, wallet private keys or session capabilities in this file.

## Public-run limits

The initial runner permits only server-selected clean/flagged fictional vendors,
50,000 atomic units of canonical Base Sepolia USDC per purchase, and one signature
per run. It does not expose escrow or officer actions. Decisions bind the actual
recipient, asset, amount and network; unavailable evidence pauses signing.

SQLite persists reservations: at most 20 lifetime runs, 1 test USDC total reserved,
3 runs per browser session and 6 per hashed client IP. Session limits alone are not
identity controls; global caps remain the financial boundary. Reverse proxy IP
handling must be configured carefully; never trust arbitrary forwarded headers.

Every admitted run consumes its allowance even if screening refuses or execution
fails. Restarting must not erase the database. A run interrupted by a hard crash
blocks further signing until an operator reconciles the possible onchain outcome.
There is no public reset endpoint. A run ID is an unguessable read capability: avoid
recording it in public logs or sharing it beyond the demo participant.

Admission also reads the gate’s durable provider counter and requires 50 calls of
headroom below the smaller of INTERCEPTA_QUOTA and INTERCEPTA_RESERVE_FROM. An unreadable
counter disables live admission. Direct live Quick Scan must be enabled, and the
signing decision must be no more than 120 seconds old.

The run limit bounds trials, not exact upstream API calls. A single trial may screen
both parties plus supporting evidence. Monitor the gate's durable provider counter
and preserve quota for the judged demonstration.

## Hosting: Render with a persistent disk

`render.yaml` provisions one Docker service with a 1 GB disk at `/data`, in Singapore.
Only the restricted public runner binds externally. The gate and preset vendor
servers listen on loopback. The privileged treasury controller is not started.

Render requires a paid service for persistent disks. Its published starter price is
$7/month and disk storage $0.25/GB/month (checked 26 September 2026); verify the price
shown before provisioning. Sources: https://render.com/pricing and
https://render.com/docs/disks. Provisioning requires a signed-in Render account and review of the displayed billing
plan; preparing these files alone does not provision or pay for a service.

1. Sign in to Render and connect the Sekisho repository; select its `render.yaml`
   Blueprint. Review the displayed service/disk cost.
2. Keep `PUBLIC_TRIAL_ENABLED=false` and `PUBLIC_TRIAL_LIVE_VERIFIED=false` initially.
3. Add server secrets privately in Render, using `.env.example` as the checklist.
   Never add `.env` to Git or the Docker image. Provider access and wallet funding are
   not tested merely by setting variables.
4. Preserve `DB_PATH=/data/gate.db`, `PUBLIC_TRIAL_DB_PATH=/data/public-trial.db`,
   `SEKISHO_URL=http://127.0.0.1:8000` and one instance. Use only Base Sepolia wallets.
5. Set `PUBLIC_TRIAL_ORIGIN=https://sekisho-phi.vercel.app`. Other marketing aliases
   should link to that canonical trial page instead of broadening CORS blindly.
6. Prove local live S1/S3 and receipt verification first. Set both public trial flags
   to `true` only after reviewing the evidence in [LIVE-EVIDENCE.md](LIVE-EVIDENCE.md).
7. Set the public HTTPS backend URL in `website/try/config.mjs`, deploy the website,
   and repeat the allowed/refused browser acceptance tests.

For another Docker host, use `docker compose -f deploy/compose.yaml up --build -d`.
The local compose port binds to 127.0.0.1; place an HTTPS reverse proxy in front.
The named volume must persist across deploys. Do not scale the SQLite stack across
machines or delete the volume to replenish a budget.

## Operator console, webhooks and attestation

Keep the full gate and console private during the public trial. Use an authenticated
operator network/tunnel for the console. The public trial is not a replacement for
its audit/review screens. Do not expose `/v1/screen`, `/v1/demo/reset` or the treasury
controller without their own quota/access boundary.

If webhook delivery is required to the hosted gate, expose only the authenticated
`POST /webhooks/multibaas` route through a separately configured proxy and retain
signature verification. Do not publish every gate route to obtain webhook ingress.
Receipt and onchain attestation checks remain separate from webhook delivery.
The initial Render blueprint exposes no gate routes; hosted webhook ingress and the
private operator-console connection remain deployment tasks.

## Verification

```bash
.venv/bin/python -m pytest agents/tests/test_public_trial.py -q
.venv/bin/python -m pytest -q
node --test website/try/state.test.mjs
node --test scripts/test-website-demo.mjs
npm --prefix dashboard run lint
npm --prefix dashboard run build
```

A deployment is accepted only when the browser requests the intended HTTPS backend,
no secrets or private console routes are exposed, limits survive restart, and one
real paid purchase plus one live refusal/pause is recorded. Docker build and live
cloud execution still require a Docker runtime or the connected host build system.
