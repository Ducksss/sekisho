<a id="readme-top"></a>

<p align="center">
  <img src="docs/assets/wordmark.svg" alt="Sekisho — Agent payment checkpoint" width="400">
</p>

<p align="center">
  <strong>Screen before signing.</strong><br>
  Wallet evidence, deterministic decisions, and human review for AI agent payments.
</p>

<p align="center">
  <a href="https://getsekisho.vercel.app">Website</a> ·
  <a href="#getting-started">Try locally</a> ·
  <a href="docs/api.md">API reference</a> ·
  <a href="PITCH_PLAN.md">Demo plan</a> ·
  <a href="https://github.com/Ducksss/sekisho/issues">Report an issue</a>
</p>

<p align="center">
  <a href="https://github.com/Ducksss/sekisho/actions/workflows/ci.yml">CI checks</a> ·
  <a href="LICENSE">MIT licensed</a>
</p>

![Before the agent signs. A luminous glass checkpoint represents the policy boundary before payment.](docs/assets/banner.png)

**Build status:** the gate, contracts, Python SDK, agents, MCP server, demo scripts,
and console are implemented and locally tested. You can explore the console without
credentials. Live deployment and the complete testnet rehearsal are still pending;
see the [readiness checklist](docs/readiness.md). The [public website](https://getsekisho.vercel.app)
includes a guided synthetic payment walkthrough and a tested SDK example. Live
screening and payment execution still require local setup.

<details>
<summary>Table of contents</summary>

- [About Sekisho](#about-sekisho)
- [Console walkthrough](#console-walkthrough)
- [Built with](#built-with)
- [Getting started](#getting-started)
- [Usage](#usage)
- [How it works](#how-it-works)
- [Verification](#verification)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)

</details>

## About Sekisho

An agent can buy an API response with USDC before a person sees the destination wallet.
Sekisho (関所, an Edo-era road checkpoint) puts a policy decision between that payment
request and the signature. It screens the counterparty with Intercepta, the Chainalysis
sanctions oracle, and a bounded source-of-funds trace.

| Verdict | Payment behavior |
|---|---|
| **ALLOW** | The payer hook may sign the x402 payment; the seller screens the payer before acceptance. |
| **HOLD** | Payment is held for review; the demo can deposit USDC into escrow for an officer to release or refund. |
| **BLOCK** | The payer hook refuses to sign; the payee hook refuses acceptance. |

The policy decides; AI only explains. Missing required screening data produces at least
HOLD. Registry attestations and officer overrides go through Curvegrid MultiBaas, while
the console lets reviewers compare the exact report bytes with the onchain report hash.

This is a **testnet demo policy**, not a certified AML programme or legal advice. An ALLOW
is a point-in-time policy decision, not a safety guarantee. Screening on mainnet is
read-only; value transfers use Base Sepolia. See [integration limits](docs/SETUP.md#integration-details-and-limits).

## Console walkthrough

**Actual console, synthetic data.** These screenshots were captured from the running
fixture preview. Balances, provider results, and transactions shown are simulated, not
evidence of live screening or settlement. The purple fixture banner stays visible.

![Decision feed with allowed, held, and blocked payments, plus the officer review queue.](docs/assets/console-decisions.png)

<details>
<summary>Case review and treasury screenshots</summary>

**Case review:** inspect the screening timeline and record a release or refund decision.

![Held case with screening evidence and the officer decision panel.](docs/assets/console-case.png)

**Treasury:** distinguish current balances from cumulative escrow exposure and releases.

![Treasury balances, exposure by payee, released totals, and the counterparty book.](docs/assets/console-treasury.png)

</details>

## Built with

| Layer | Technology |
|---|---|
| Gate | Python 3.11, FastAPI, Pydantic, SQLite, server-sent events |
| Console | Next.js 16, React 19, TypeScript, SWR, viem |
| Contracts | Solidity, Foundry, OpenZeppelin; registry and USDC escrow |
| Agent integration | Python SDK, x402 payer/payee hooks, MCP server |
| Screening adapters | Intercepta, Chainalysis sanctions oracle, Blockscout source tracing |
| Onchain operations | Curvegrid MultiBaas writes, webhooks, indexed events, Event Queries |

Adapters are implemented; their live deployment and end-to-end verification remain on
the [roadmap](#roadmap). Exact installed versions are recorded in dependency locks and constraints.

## Getting started

### Explore the console without credentials

Prerequisites: **Git and Node.js 22 with npm**. No wallet or API key is needed.

```bash
git clone https://github.com/Ducksss/sekisho.git
cd sekisho/dashboard
npm ci
npm run dev:fixtures
```

Open [localhost:3000](http://localhost:3000). Look for the **FIXTURE DATA** banner.
The demo controls simulate scenarios in your browser; they do not submit transactions.

### Run the full testnet stack

Follow [Local setup and testnet rehearsal](docs/SETUP.md) for Python 3.11, Foundry,
service credentials, fresh testnet wallets, deployment, webhooks, and smoke checks.
Run `make help` from the repository root for all commands.

The normal console uses live gate data. Stop the fixture process before switching;
submitted builds must leave `NEXT_PUBLIC_USE_FIXTURES` unset or `false`. The running
gate has no mock mode. Keep all private keys and service secrets in the ignored `.env`.

## Usage

In the fixture preview:

1. Open **Live decisions** and use **S1 Clean vendor** or **S3 Sanctioned vendor** to
   compare ALLOW and BLOCK.
2. Run **S2 Mixer-exposed vendor**, open the held case, and inspect its evidence.
3. Enter an officer note and release or refund the simulated hold; check the hold queue.
4. Open **Audit log**, expand a confirmed case, and choose **Verify report**.
5. Open **Treasury** to compare balances with cumulative exposure. Use **Policy** and
   **Integrate** to inspect thresholds and SDK/MCP examples.

For the configured live stack, run `make demo S=S1`, then S3 and S2; review the hold in
the console. `make demo S=all` runs S1–S5 and waits for officer release during S2.
S6 tests fail-closed behavior under explicit timeout fault injection and runs separately.
See the [complete rehearsal sequence](docs/SETUP.md#demo-and-verification) and
[SDK integration guide](sdk/README.md).

## How it works

```text
Treasury Agent → x402 402 → payer hook → Sekisho Gate → policy verdict
                                         ↑                 │
Vendor Agent ← payee hook ← payer wallet  │                 ├ ALLOW → sign, settle
                                         │                 ├ HOLD → escrow → officer
              Intercepta + oracle + trace ┘                 └ BLOCK → no signature
                                                           │
                                   MultiBaas → registry/events/webhooks
                                                           │
                                         Console ← gate API + SSE
```

| Directory | Responsibility |
|---|---|
| [`gate/`](gate/) | Screening, deterministic policy, reports, advisory notes, attestations, SSE |
| [`contracts/`](contracts/) | ComplianceRegistry, ComplianceEscrow, tests, deployment |
| [`sdk/sekisho/`](sdk/sekisho/) | Gate client and x402 hooks |
| [`agents/`](agents/) | Treasury buyer, vendor APIs, rogue payer scenario |
| [`mcp/server.py`](mcp/server.py) | Gate tools for MCP agents |
| [`website/`](website/) | Public static landing page deployed on Vercel |
| [`dashboard/`](dashboard/) | Decisions, review queue, audit, treasury, policy, integration |
| [`scripts/`](scripts/) | Setup, scanning, smoke checks, demo control |

The [PRD](PRD.md) and [API contract](docs/api.md) define the shared schemas. The policy
file is hashed byte for byte. Report verification hashes the served canonical text,
not a reserialized object. Counterparty-supplied text never controls screening.

## Verification

From the repository root after full installation:

```bash
make test
npm --prefix dashboard run lint
npm --prefix dashboard run build
```

Local verification recorded on 26 September 2026: **356 Python tests, 18 contract tests,
and 45 report-hash checks passed**, along with the console build and lint. Browser checks
covered desktop/mobile, review actions, report verification, and recoverable data errors.
See [verification scope and limitations](docs/readiness.md#local-verification) and
[GitHub CI](https://github.com/Ducksss/sekisho/actions/workflows/ci.yml).
These checks do not establish live provider performance or settlement.

## Roadmap

- [x] Gate, deterministic policy, canonical reports, and screening adapters
- [x] Registry and escrow contracts with tests
- [x] x402 payer/payee hooks, agents, MCP, and demo scenarios
- [x] Console review, audit, treasury, policy, and integration flows
- [x] Credential-free fixture preview and local verification
- [ ] Configure live services, fund fresh testnet wallets, and deploy/link contracts
- [ ] Select real counterparties and capture real Intercepta profiles
- [ ] Rehearse S1–S5 twice and S6 separately with indexed onchain evidence
- [ ] Measure live latency, complete human review, and record the narrated demo

The [readiness checklist](docs/readiness.md) is the detailed handoff for the remaining work.
The [pitch plan](PITCH_PLAN.md) covers the ETHGlobal Tokyo 2026 demonstration.

## Contributing

Open an [issue](https://github.com/Ducksss/sekisho/issues) to discuss a change, or send a
focused pull request with validation. Read [AGENTS.md](AGENTS.md) for repository rules.
Keep changes small, preserve fail-closed behavior, and update the gate, SDK, and console
together when a shared schema changes. Do not commit keys, `.env`, or databases.
Record AI assistance and prompts in [docs/ai-usage.md](docs/ai-usage.md).

## License

Distributed under the [MIT License](LICENSE). Third-party dependencies retain their
own licenses; presentation asset provenance is recorded in [docs/assets](docs/assets/README.md).

## Contact

Maintained in [Ducksss/sekisho](https://github.com/Ducksss/sekisho).
For questions or bug reports, use [GitHub Issues](https://github.com/Ducksss/sekisho/issues).

## Acknowledgments

- README structure adapted from [Best-README-Template](https://github.com/othneildrew/Best-README-Template).
- Intercepta, Curvegrid MultiBaas, Chainalysis, Blockscout, and x402 provide the integration surfaces used by this project.
- Atkinson Hyperlegible Next/Mono and Inter Tight provide the console and brand typography through Fontsource.
- [Investflow](https://investflowtemplate.webflow.io/) inspired the [Sekisho visual direction](docs/BRAND-DIRECTION.md); the checkpoint illustration is original.
- [AI usage and committed prompts](docs/ai-usage.md) document the build; the earlier
  [Wallet Audit Trail concept](docs/pitch-deck.md) records the project's provenance.

[Back to top](#readme-top)
