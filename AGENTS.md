# AGENTS.md

Ansible role that installs and configures a Mumble server (murmur) and optionally mumble-web on Debian (bookworm, trixie).

## Layout

- `defaults/main.yml`: all role variables with defaults (documented in `README.md`)
- `tasks/`, `handlers/`, `templates/`: role logic; `meta/main.yml` holds Galaxy metadata and the `geerlingguy.nodejs` dependency (used when `mumble_web` is true)
- `requirements.yml`: role and collection dependencies
- `molecule/default/`: Molecule scenario (Docker driver) with `prepare.yml`, `converge.yml` and a goss-style spec in `tests/`

## Checks

- `ansible-lint .` must pass (default configuration, no repo config); install `requirements.yml` first with `ansible-galaxy install -r requirements.yml`
- `molecule test` runs the role in a systemd Docker container; CI uses the shared `systemli/github-ansible-workflow` on Debian 12 and 13
- `ansible-lint` creates `.ansible/`; it is git ignored, never commit it

## Conventions

- Use fully qualified module names, quoted octal `mode` values and `true`/`false` booleans
- Give every task a `name`
- Role variables are prefixed `murmur_` (server) or `mumble_web` (web client); document new ones in `defaults/main.yml` and the README

## Commits and PRs

- Write in English, use conventional commit titles (`feat:`, `fix:`, `chore:`, `ci:`; `!` for breaking changes)
- The PR title sets the release-drafter label (`enhancement`, `bug`, `chore`, `breaking`); a breaking change bumps the major version
- Open PRs as draft and fill in `.github/pull_request_template.md`: what changed and why, plus a breaking changes section if needed
- Do not list changed files or claim test results in the description; CI covers that
