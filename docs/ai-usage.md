# AI usage

ETHGlobal's AI rule asks every project to say where and how AI tools were used, and to
commit the specs, prompts and plans behind AI-generated work. This is Sekisho's record,
kept up to date as the build goes.

## Tools

- **Claude Code** (Claude Opus 5.5, in the Claude desktop app): the lead engineering
  agent. It split the PRD into workstreams, ran parallel subagents for research and
  building, then reviewed, integrated, tested and committed their output. Every commit
  it made carries a `Co-Authored-By: Claude` trailer.
- **Claude** (runtime): the AI analyst writes advisory case notes, and the Treasury Agent
  reasons about which vendor data to buy. Both run behind a provider switch
  (`LLM_PROVIDER`), and the demo also works with `LLM_PROVIDER=none`. The AI never decides
  a verdict: the deterministic policy in `gate/policy/policy.yaml` does.

## Specs, plans and prompts (committed)

| File | What it is |
|---|---|
| [PRD.md](../PRD.md) | Product requirements, written by the team before any code; committed first |
| [PITCH_PLAN.md](../PITCH_PLAN.md) | Pitch and demo plan, written by the team |
| [docs/pitch-deck.md](pitch-deck.md) | The earlier "Wallet Audit Trail" concept that became Sekisho |
| [docs/api.md](api.md) | Gate API contract, written by the lead agent from PRD 9.11 so the workstreams could run in parallel |
| [docs/prompts/](prompts/README.md) | Every prompt: the team's instructions to the lead agent and the lead agent's prompts to each subagent |
| [AGENTS.md](../AGENTS.md) | Standing instructions that every coding agent in this repo reads |

## Where AI wrote code

| Area | Files | How it was made | Team review |
|---|---|---|---|
| Repo structure | `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.pre-commit-config.yaml` | Lead agent, from the agent-agnostic repository guide the team supplied | pending |
| Scaffold | `Makefile`, `.env.example` (PRD Appendix G), packaging, `scripts/gen_wallets.py` | Lead agent | pending |
| Demo policy | `gate/policy/policy.yaml` | PRD Appendix D, byte for byte (hash verified) | pending |
| Contracts | `contracts/src/`, `contracts/test/`, `contracts/script/` | PRD Appendices A to C, which the team had already compiled and tested; installed and re-tested by a subagent (prompt 04) | pending |
| Gate | `gate/sekisho_gate/` | Subagents from PRD Section 9 (prompts 06, 07) | pending |
| SDK and vendor agents | `sdk/`, `agents/vendors/`, `agents/rogue/` | Subagent from PRD 10.1, 10.2, 10.4 (prompt 08) | pending |
| Treasury Agent, demo, MCP | `agents/treasury/`, `scripts/`, `mcp/` | Subagent from PRD 10.3 to 10.5 and 12 (prompt 09) | pending |
| Compliance Console | `dashboard/` | Subagent from PRD 10.6 (prompt 05) | pending |

Before submission, the team replaces each "pending" with who reviewed it, and confirms that
the contracts were deployed and tested by the team.
