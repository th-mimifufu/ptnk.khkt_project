# ptnk.khkt_project

## Developer Setup
This guide helps new developers set up the project correctly with **pre-commit**, **pre-push protection**, and local dependencies for all services (`frontend`, `backend`, `ml`).

---

### 1. Clone the repository

```bash
git clone https://github.com/th-mimifufu/ptnk.khkt_project.git
cd ptnk.khkt_project
```

### 2. Install pre-commit and Git hooks

```bash
pip install pre-commit
pre-commit install --hook-type pre-commit
pre-commit install --hook-type pre-push
```

- Enable script permissions (macOS/Linux only)

```bash
chmod +x scripts/prevent_push_main.sh
```
