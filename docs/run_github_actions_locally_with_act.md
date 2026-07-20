# Running GitHub Actions Locally with `act`

Push, wait for GitHub, watch it fail, fix, push again — that loop is slow.
[`act`](https://github.com/nektos/act) runs your **existing** GitHub Actions
workflows on your own machine inside Docker, using the **same
`.github/workflows/*.yml` files** — no extra config, no duplicated scripts.
Get it green locally, *then* push.

> This is the plain, standard tool most developers use. There is nothing to
> customize: `act` reads the workflow you already have.

---

## 1. Prerequisite: Docker

`act` runs each job in a container, so Docker must be installed and running:

```bash
docker --version      # must succeed
docker ps             # daemon must be up
```

If Docker isn't installed, see https://docs.docker.com/engine/install/.

---

## 2. Install `act`

Pick whichever fits your setup — they all install the same tool:

```bash
# a) One-line install script (Linux/macOS) → installs to a path you give
curl -sSL https://raw.githubusercontent.com/nektos/act/master/install.sh | bash -s -- -b ~/.local/bin

# b) As a GitHub CLI extension (if you already have `gh`)
gh extension install nektos/gh-act      # then run it as:  gh act ...

# c) Package managers
brew install act                        # macOS / Linuxbrew
# Arch:            sudo pacman -S act
# Windows (choco): choco install act-cli
```

Verify:

```bash
act --version
```

---

## 3. First run: choose an image size

The **first** time you run `act`, it asks which runner image to use. Pick
**Medium** — it's the standard `catthehacker/ubuntu` image that has git, curl,
Python, etc. (The choice is saved to `~/.actrc`.)

```
? Please choose the default image you want to use with act:
  - Large   (~17GB, closest to GitHub's runner)
  > Medium  (~500MB, has the common tools)   ← choose this
  - Micro   (~200MB, node only)
```

---

## 4. Everyday commands

```bash
act -l                 # list the jobs act found in .github/workflows
act                    # run the default event (push) — runs all matching jobs
act -j test            # run ONE job by id (recommended)
act pull_request       # simulate a pull_request event instead of push
act -n                 # dry run: print the plan, execute nothing
act -v                 # verbose, when something misbehaves
```

### For THIS repo

The CI here installs the packages and runs `pytest` (`ci.yml`, job id
**`test`**, runner `ubuntu-latest`):

```bash
act -j test
```

This does exactly what GitHub does: set up Python 3.11, `pip install` the
packages, then `pytest`.

---

## 5. The workflow: green locally → push

```bash
act -j test            # 1. run CI locally
# ...fix anything that fails, repeat until green...
git add -A && git commit -m "..."
git push               # 2. push only once it passed locally
```

That's the whole idea — no scripts, no hooks required.

### Optional: make it automatic before every push

If you want the check to run on its own, add a one-line Git `pre-push` hook.
This is optional; `act` on its own is already enough.

```bash
cat > .git/hooks/pre-push <<'EOF'
#!/usr/bin/env bash
act -j test || { echo "❌ local CI failed — push aborted"; exit 1; }
EOF
chmod +x .git/hooks/pre-push
```

Bypass it any time with `git push --no-verify`.

---

## 6. Good to know (limitations)

- **`act` ≈ GitHub, not identical.** It uses `catthehacker` images, not
  GitHub's exact runner image. Close enough to catch the vast majority of
  failures; for maximum parity choose the **Large** image.
- **Linux jobs only.** `act` cannot run `windows-latest` or `macos-latest`
  jobs — only Linux runners.
- **First run is slow** — it pulls the runner image and re-installs pip
  packages. Later runs reuse cached layers and are much faster.
- **Secrets:** pass them with `act -s NAME=value` or `--secret-file` if a
  workflow needs them (this repo's tests don't).

---

## Bonus: the Python-native alternative — `pre-commit`

Many Python projects also use [`pre-commit`](https://pre-commit.com/) for the
*fast* checks (formatting, linting) and keep `act` for the full test run:

```bash
pip install pre-commit
pre-commit run --all-files
```

`act` = "run the whole GitHub workflow"; `pre-commit` = "run quick checks on
each commit". They complement each other. For simply reproducing GitHub CI
locally, `act` is all you need.

---

## TL;DR

```bash
docker ps                 # Docker running?
act -l                    # what jobs exist?
act -j test               # run CI locally  → green? then git push
```
