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

The Claude Code skill marketplace is at https://skillsmp.com/. When the user says "look for skills", "skill marketplace", or asks about installable Claude Code skills, this is the source.

- **Install** globally: `bunx skills add -g <owner/repo> --skill <skill-name>`
- **Search**: `bunx skills find <keyword>`
- **Reputation**: report star count as the trust signal (e.g., ⭐ 219.4k)

Skills in this role are declared in `roles/claude/vars/main.yml` under `claude_marketplace_skills` and installed via `roles/claude/tasks/marketplace_skills.yml`.
