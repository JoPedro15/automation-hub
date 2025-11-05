# 🧩 Random Stuff

A collection of small, focused Python projects exploring **APIs**, **automation**, and **experiments** — all under one
roof, sharing common tooling and conventions.

## 📁 Structure

| Folder     | Description                                                      |
|------------|------------------------------------------------------------------|
| `common/`  | Shared utilities (e.g., logging, helpers) reused across projects |
| `spotify/` | Lightweight **Spotify Web API client** (Client Credentials flow) |

Each subproject is self-contained with its own:

- `Makefile`
- `pyproject.toml`
- `src/` and `tests/` directories

## ⚙️ Quickstart

```bash
# 1️⃣ Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2️⃣ Install dependencies
make setup

# 3️⃣ Format, lint, and test everything
make fmt
make lint
make test
```

## 🧱 Project Conventions

### Python version: ≥ 3.10

### Layout per project:

```bash
<project>/
├─ src/
│  └─ <package>/
├─ tests/
├─ Makefile
└─ pyproject.toml
```

### Logging

Use common/python/logging_utils.py to keep output consistent across projects.

## 🪄 Adding a New Project

```
mkdir my-new-project && cd my-new-project
mkdir src tests
cp ../spotify/Makefile .
```

Then update:

the import paths

the pyproject.toml (name, dependencies)

and write your first test in tests/

Made with ☕ by João

<div style="text-align: center;">
  <b>Made with ☕ by João</b><br>
</div>