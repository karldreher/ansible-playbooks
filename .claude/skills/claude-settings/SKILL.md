---
name: claude-settings
description: Updates Claude Code settings — permissions, allow list entries, CLAUDE.md guidelines, and default mode — by editing the Ansible role files that generate them. Use this skill whenever the user says "add a permission", "update claude settings", "add an allow list entry", "allow this command", "add to the allow list", "update CLAUDE.md", "change default mode", or any variation of modifying Claude Code configuration. Also triggers when the user wants to allow a new CLI command, add a tool permission, or change how Claude Code behaves by default. Even if the user just says something like "let claude run X without asking", this skill applies.
argument-hint: "[setting change description]"
model: claude-haiku-4-5
---

This role manages Claude Code settings through Ansible — settings aren't edited directly in `~/.claude/`, they're defined in role files and deployed via playbook. This skill knows where each piece lives and how to edit it safely.

Reference documentation:
- Settings: https://code.claude.com/docs/en/settings.md
- Permissions: https://code.claude.com/docs/en/permissions.md

## What lives where

| Setting type | File | Key / location |
|---|---|---|
| Permission allow list | `roles/claude/vars/main.yml` | `claude_settings.permissions.allow` (YAML list) |
| Default mode | `roles/claude/vars/main.yml` | `claude_settings.permissions.defaultMode` |
| Global guidelines | `roles/claude/templates/CLAUDE.md.j2` | Jinja2 template → `~/.claude/CLAUDE.md` |

## Editing the allow list

The allow list in `roles/claude/vars/main.yml` controls which tools and commands Claude can use without asking for permission. Read the file first to see the current entries and section structure.

### Format

Each entry is a string matching one of these patterns:

```yaml
# Bash commands — prefix match with wildcard
- "Bash(command:*)"         # e.g. "Bash(git diff:*)"
- "Bash(command subcommand:*)"  # e.g. "Bash(gh pr create:*)"

# Standalone tools — just the name
- "WebSearch"
```

### Placement rules

The list is organized into labeled sections with comments. Place new entries in the correct section alphabetically. The current sections are:

1. General bash commands (`cat`, `find`, `grep`, `ls`)
2. `gh` CLI commands
3. `git` commands
4. `npm` commands
5. `bun` commands
6. `uv` / Python commands
7. Special tools (`WebSearch`)

If a new entry doesn't fit an existing section, create a new commented section in a logical position.

### Example

To allow `docker ps` and `docker logs`:

```yaml
# Docker read commands.
- "Bash(docker logs:*)"
- "Bash(docker ps:*)"
```

## Editing CLAUDE.md guidelines

The file `roles/claude/templates/CLAUDE.md.j2` is a Jinja2 template that generates the global `~/.claude/CLAUDE.md`. Read it first to understand existing sections and tone.

### How to add a guideline

- Add a new `## Section` with a descriptive heading
- Use concise bullet points — these go into Claude's context window every conversation, so brevity matters
- Place the section in a logical position relative to existing ones
- The template supports Jinja2 syntax if conditional content is needed, but plain markdown is preferred for simple guidelines

## Changing the default mode

The `defaultMode` value in `roles/claude/vars/main.yml` controls Claude's startup behavior. Valid values: `"plan"`, `"normal"`. Edit the existing `defaultMode` key — don't add a second one.

## After making changes

Remind the user that changes won't take effect until the Ansible playbook is run to deploy them. Something like:

> Changes saved to the role files. Run the playbook to deploy them to `~/.claude/`.
