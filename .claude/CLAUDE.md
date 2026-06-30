# ansible-playbooks

## Linting

Use `uvx ansible-lint` to run ansible-lint (no local install required).

**Always run `uvx ansible-lint` after making any changes** and fix all violations before committing.

## Ansible conventions

### Variable naming — role prefix required

All variables defined within a role (in `vars/main.yml` or via `register:`) must be prefixed with the role name, using underscores (not hyphens). Example: a variable `foo` in role `my_role` must be named `my_role_foo`.

This is enforced by the `var-naming[no-role-prefix]` ansible-lint rule. The only exception is `homedir` in the `facts` role, which is intentionally cross-role and suppressed with `# noqa: var-naming[no-role-prefix]`.

### Role directory names

Role directories must use `snake_case` (underscores only, no hyphens). This is enforced by the `role-name` ansible-lint rule.

## Skill Marketplace

The Claude Code skill marketplace is https://skills.sh/. When the user says "look for skills",
"skill marketplace", or asks about installable Claude Code skills, use this source.

- **Search**: `bunx skills find <keyword>` — only unauthenticated search path; compact output
  (2 lines per result); rank by install count (e.g. 347.8K installs)
- **Reputation**: install count shown in `bunx skills find` output is the trust signal
- To add a skill to this machine, declare it in `roles/claude/vars/main.yml` under
  `claude_marketplace_skills` and run the playbook — do not install ad-hoc
