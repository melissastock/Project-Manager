# Portfolio operating system

This repository is organized into **eight top-level domains** (cold storage, execution lanes, platform, product lab, recovery, narrative output, and the nested control plane). Each domain folder has a short `README.md` describing how to use it.

## Project Manager control plane

Automation, portfolio manifest, governance scripts, operator documentation, and **pm-portal** live under:

**`Project-Manager/`**

From the repository root, run scripts with:

```bash
python3 Project-Manager/scripts/portfolio_status.py
```

Paths in `Project-Manager/config/repos.json` are relative to this **repository root** (the portfolio workspace), not relative to `Project-Manager/`. Clone or symlink managed child repositories next to `Project-Manager/` as those paths describe.

For friction with Git, CI, Conda, or environment wiring, see **`Project-Manager/docs/operator-friction-log.md`**.

Consulting-first operator workflow (offers, stage gates, payments, web/portal): **`Project-Manager/docs/master-consulting-operator-workflow.md`**.
