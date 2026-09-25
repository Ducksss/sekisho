#!/usr/bin/env bash
# Link skills from .agents/ into each agent's native skills directory.
#
#   .agents/scripts/link-skills.sh         create, repair and prune the symlinks
#   .agents/scripts/link-skills.sh check   change nothing; exit 1 if a shared skill's link is
#                                          missing, wrong, dangling or not staged (pre-commit)
#
# Shared skills (.agents/skills/) get committed symlinks. Private skills
# (.agents/skills-local/) get machine-local symlinks that are kept out of git through
# .git/info/exclude. Written for bash 3.2, the macOS default: no associative arrays.
set -euo pipefail

AGENTS_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$AGENTS_DIR/.." && pwd)"
TARGETS=(".claude/skills" ".cursor/skills")
MODE="${1:-apply}"
case "$MODE" in
    apply | check) ;;
    *) echo "usage: $0 [check]" >&2; exit 2 ;;
esac

IN_GIT=false
git -C "$REPO_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1 && IN_GIT=true
problems=0

problem() {
    echo "link-skills: $1" >&2
    problems=$((problems + 1))
}

exclude_locally() {
    $IN_GIT || return 0
    local exclude
    exclude="$(git -C "$REPO_ROOT" rev-parse --git-path info/exclude)"
    case "$exclude" in /*) ;; *) exclude="$REPO_ROOT/$exclude" ;; esac
    mkdir -p "$(dirname "$exclude")"
    grep -qxF "/$1" "$exclude" 2>/dev/null || echo "/$1" >>"$exclude"
}

for skill_dir in "$AGENTS_DIR"/skills-local/*/; do
    [ -d "$skill_dir" ] || continue
    name="$(basename "$skill_dir")"
    if [ -d "$AGENTS_DIR/skills/$name" ]; then
        echo "link-skills: '$name' is in both skills/ and skills-local/; rename one" >&2
        exit 1
    fi
done

for target_dir in "${TARGETS[@]}"; do
    for source in skills skills-local; do
        for skill_dir in "$AGENTS_DIR/$source"/*/; do
            [ -d "$skill_dir" ] || continue
            name="$(basename "$skill_dir")"
            rel="$target_dir/$name"
            link_path="$REPO_ROOT/$rel"
            link_target="../../.agents/$source/$name"

            if [ -L "$link_path" ] && [ "$(readlink "$link_path")" = "$link_target" ]; then
                if [ "$MODE" = check ] && [ "$source" = skills ] && $IN_GIT &&
                    ! git -C "$REPO_ROOT" ls-files --error-unmatch "$rel" >/dev/null 2>&1; then
                    problem "$rel is not staged (git add $rel)"
                fi
                continue
            fi
            if [ -e "$link_path" ] && [ ! -L "$link_path" ]; then
                echo "link-skills: $rel exists but is not a symlink; move it into .agents/$source/" >&2
                exit 1
            fi
            if [ "$MODE" = check ]; then
                # Private skills are machine-local, so a missing link is not a repo problem.
                [ "$source" = skills ] && problem "$rel is missing or points elsewhere (run .agents/scripts/link-skills.sh)"
                continue
            fi
            mkdir -p "$REPO_ROOT/$target_dir"
            ln -sfn "$link_target" "$link_path"
            [ "$source" = skills-local ] && exclude_locally "$rel"
            echo "Linked: $rel -> $link_target"
        done
    done

    # Prune links into .agents/ whose skill is gone. No trailing slash on the glob, so
    # dangling links (which are not directories) still match.
    for link_path in "$REPO_ROOT/$target_dir"/*; do
        [ -L "$link_path" ] || continue
        link_target="$(readlink "$link_path")"
        case "$link_target" in ../../.agents/skills/* | ../../.agents/skills-local/*) ;; *) continue ;; esac
        [ -d "$link_path" ] && continue
        rel="$target_dir/$(basename "$link_path")"
        if [ "$MODE" = check ]; then
            case "$link_target" in
                ../../.agents/skills/*) problem "$rel points to a deleted skill (run .agents/scripts/link-skills.sh)" ;;
            esac
        else
            rm "$link_path"
            echo "Pruned: $rel"
        fi
    done
done

[ "$problems" -eq 0 ]
