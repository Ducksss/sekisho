# .agents/

Agent-agnostic configuration following the [Agent Skills](https://agentskills.io)
open standard and [AGENTS.md](https://agents.md) conventions. Portable assets live
here once and are symlinked into each agent's directory; assets that need a different
format per agent are generated from one source here; agent-specific files stay where
their agent expects them.

## Layout

- `skills/`: shared skills (committed). Each is a directory with a `SKILL.md`.
- `skills-local/`: private skills (gitignored). Their symlinks are kept out of git
  through `.git/info/exclude`, so they never show up as untracked files.
- `mcp/servers.json`: canonical MCP server config.
- `scripts/link-skills.sh`: symlinks skills into `.claude/skills/` and `.cursor/skills/`.
- `scripts/sync-mcp.sh`: renders `servers.json` into `.mcp.json` (Claude Code),
  `.cursor/mcp.json` (Cursor) and `.codex/config.toml` (Codex).

## Adding a skill

1. Create `.agents/skills/<name>/SKILL.md` with `name` (lowercase, hyphens, same as the
   directory) and `description` frontmatter. Keep it under 500 lines and put detail in
   `references/`.
2. Add `references/NOTES.md` with seven sections: Overview, Scope, Key Decisions,
   Key Nuances & Limitations, Future Improvement Ideas, Open Questions, Changelog.
   Every change to the skill gets a new changelog row.
3. Run `.agents/scripts/link-skills.sh`.
4. Commit the skill directory and the new symlinks together.

Third-party skills: `npx skills add <repo>@<skill> -y` installs into `.agents/skills/`
and links `.claude/skills/`. Run `link-skills.sh` afterwards to link the other agents.

## Adding an MCP server

1. Edit `.agents/mcp/servers.json`. Each entry is either
   `{"type": "stdio", "command": ..., "args": [...], "env": {...}}` or
   `{"type": "http", "url": ..., "headers": {...}}`. The script rejects any other field,
   and `${VAR}` interpolation, because each agent handles those differently.
2. Run `.agents/scripts/sync-mcp.sh`.
3. Commit `servers.json` and every generated file together.
4. Codex reads MCP servers from `~/.codex/config.toml`, so each developer also runs
   `.agents/scripts/sync-mcp.sh install-codex` once. It maintains a marked block in that
   file and leaves the rest of it untouched.

## Rules

- Edit skills in `.agents/skills/`, never in `.claude/skills/` or `.cursor/skills/`.
- Edit MCP servers in `.agents/mcp/servers.json`, never in `.mcp.json`,
  `.cursor/mcp.json` or `.codex/config.toml`.
- Agent-specific files (`.claude/settings.json`, `.claude/agents/`, `.cursor/rules/*.mdc`)
  have no cross-agent equivalent: leave them in place. Knowledge that every agent needs
  goes in the root `AGENTS.md` instead.
- Pre-commit runs `link-skills.sh check` and `sync-mcp.sh check`. Enable it once per clone
  with `pre-commit install`.
