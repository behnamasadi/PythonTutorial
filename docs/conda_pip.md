# Conda, Pip, Pipx & Reproducible Environments 

## TL;DR (quick recipe for mixed conda+pip)
1. **Prefer one ecosystem** (e.g., `conda-forge`) and set `channel_priority: strict`.

   - **defaults**: Maintained by Anaconda, Inc, Often ships **MKL** builds for NumPy/SciPy (good performance on Intel/AMD CPUs). Slightly **slower updates** 

   - **conda-forge**: Large, community-maintained channel; **fast updates** and **very broad coverage**. Consistent toolchains & pinning across packages → fewer ABI mismatches. Typically uses **OpenBLAS** by default (you can switch to MKL if you want).

   - **Mixing them**: You *can* mix, but solver friction increases. If you must:

     * Put **conda-forge first** and set `channel_priority: strict`.
     * Or stay on **defaults** and selectively pull from forge for specific packages (but pin carefully).
     * GPU stacks (e.g., PyTorch, CUDA) sometimes come from dedicated channels (e.g., `pytorch`, `nvidia`). Follow their official install lines, but keep the rest on a single ecosystem.

2. Create env with **conda packages first**, then install **pip‑only** packages.
3. Capture a portable spec with **`environment.yml`** (using `--no-builds`) and include a **`pip:`** subsection with `conda env export --no-builds | grep -v "^prefix:" > environment.yml
`
4. Freeze exact versions per platform with **conda-lock** and share the lock files with `conda-lock -f environment.yml -p linux-64`
5. Recreate with `conda-lock install …` for deterministic results with `conda-lock install --name YOURENV conda-lock.yml`

---

## 1) Concepts & tool roles
- **Conda**: environment + package manager.
- **Anaconda**: a distribution that *includes* Conda and many packages.
- **Pip (inside env)**: install Python packages that aren’t conveniently available via Conda.
- **Pipx (outside envs)**: install global‑ish **CLI tools** in isolated venvs (e.g., `conda-lock`, `pre-commit`).
- **Conda‑lock**: generates lock files for exact, deterministic installs per platform.
- **Conda‑pack**: creates a tarball snapshot of an existing env (good for deployment, not a spec).

---

## 2) Install & PATH basics
### 2.1 Ubuntu/WSL: install Pipx (recommended)
```bash
sudo apt update
sudo apt install -y pipx
pipx ensurepath
exec $SHELL -l   # open a new shell
pipx --version
```
> If you prefer bootstrapping via Python: `sudo apt install -y python3-venv && python3 -m ensurepip --upgrade && python3 -m pip install --user pipx && ~/.local/bin/pipx ensurepath`.

### 2.3 Add Conda to PATH (Linux)
```bash
export PATH="$HOME/anaconda3/bin:$PATH"
```
> Prefer launching Conda by sourcing `conda.sh` from your shell profile rather than hardcoding paths if possible.

### 2.4 Auto‑activating base (optional)
```bash
conda config --show | grep auto_activate_base
conda config --set auto_activate_base false
```

---

## 3) Create & manage environments

### 3.1 Create an environment
```bash
conda create -n myproj -c conda-forge python=3.11
conda activate myproj
# core scientific stack via conda first
conda install numpy pandas scipy
# GPU / PyTorch example (adjust per vendor guidance)
conda install pytorch cudatoolkit=12.1 -c pytorch -c nvidia
# pip‑only packages
python -m pip install fastapi uvicorn[standard]
```

### 3.2 Env location (prefix)
```bash
conda create --prefix /abs/path/to/env python=3.11
```

### 3.4 Listing & updating
```bash
conda info --envs           # list envs
conda list                  # packages in current env
conda update conda          # update conda itself
conda update anaconda       # update distribution meta-package (optional)
conda update --all          # update all packages in current env
conda update -n myproj --all
```

---

## 4) Pip inside Conda envs (the safe way)
- Prefer `python -m pip install package` so you hit the **pip tied to the active interpreter**.
- Avoid `pip install --user` **inside** a conda env (installs outside the env and confuses imports).
- Inspect paths:
```bash
which -a python pip
python -m site --user-base
python -m site --user-site
```
- Show packages & locations:
```bash
pip list
pip freeze
pip show <PACKAGE>
```

### Isolating from user site packages
```bash
unset PYTHONPATH
export PYTHONNOUSERSITE=1
conda activate myproj
python -m site
```

---

## 5) Reproducibility strategies
### 5.1 `environment.yml` (portable spec)
Create from a working env:
```bash
# Portable-ish (keeps versions but drops build hashes)
conda env export --no-builds | grep -v "^prefix:" > environment.yml
```
If you want **minimal** top‑level spec (cleaner, may omit pip):
```bash
conda env export --from-history | grep -v "^prefix:" > environment.yml
```

Add pip entries either directly or through a requirements file. From the active env, capture your pip packages:


#### Why `grep -v "^prefix:"`?

When you do:

```bash
conda env export --no-builds > environment.yml
```

Conda writes a line like:

```
prefix: /home/you/miniconda3/envs/myenv
```

That absolute path is **machine-specific**. If you keep it:

* `conda env create -f environment.yml` may try to create the env at that **exact path**, which will fail (or be undesirable) on other machines.
* It also **leaks your local paths** into the file.

So we strip it:

```bash
conda env export --no-builds | grep -v "^prefix:" > environment.yml
```

#### why  `--no-builds`
It drops build strings (e.g., `py311h123abc_0`) → more portable across platforms while still pinning versions.




### Create/update env from YAML:
```bash
conda env create -f environment.yml
conda env update -n myproj -f environment.yml --prune
```

### 5.2 Lock files with **conda-lock** (deterministic)
Install conda-lock once (via Pipx or a small tools env):
```bash
pipx install conda-lock      # or: conda create -n tools -c conda-forge conda-lock
conda-lock --version
```
Generate locks per platform and commit them:
```bash
conda-lock -f environment.yml -p win-64 -p linux-64
# produces files like: conda-linux-64.lock
```

Recreate **exactly** from the lock:
```bash
conda-lock install -n myproj conda-linux-64.lock   # pick the file for your OS
```

### 5.3 Exact clone (same OS/arch only)
```bash
conda list --explicit > spec.txt
conda create -n clone --file spec.txt
```
Limitations: includes exact builds; doesn’t capture pip. Pair with `pip freeze > requirements.txt` if needed.

### 5.4 Deployable snapshot with **conda-pack**
```bash
conda-pack -n myproj -o myproj.tar.gz
```
Great for shipping a frozen env; not a long‑term spec.

---


## 6) Day‑to‑day workflow (A→Z)
1. Create env with Conda; add pip‑only deps with Pip.
2. Export `environment.yml` and commit.
3. Generate platform locks with `conda-lock` and commit.
4. Teammates/CI: use `conda-lock install …` to recreate exactly.
5. Need a new package? Update YAML → re‑lock → reinstall from lock.

---

## 7) Troubleshooting
### 7.1 `/usr/bin/python3: No module named pip` (Ubuntu)
```bash
# Easiest: install pipx from apt and skip system pip entirely
sudo apt update && sudo apt install -y pipx && pipx ensurepath && exec $SHELL -l

# Or bootstrap system pip
sudo apt update && sudo apt install -y python3-venv
python3 -m ensurepip --upgrade
python3 -m pip install --user --upgrade pip
python3 -m pip --version
```

### 7.2 `pipx` not found after install
Run `pipx ensurepath` and open a new shell. Ensure `~/.local/bin` is on `PATH` (Linux) or the user Scripts dir on Windows.

### 7.3 Mixed channels/solves are slow or fail
Prefer one channel, pin Python version, and avoid unnecessary upgrades. Consider `mamba` for faster solves.

### 7.4 Accidentally used `pip install --user` inside a Conda env
Uninstall the user‑level package (`python -m pip uninstall …` with `PYTHONNOUSERSITE=1` disabled), then reinstall inside the env **without** `--user`.

---