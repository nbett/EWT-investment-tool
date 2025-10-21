# EWMC: Elliott Wave × Monte Carlo


Run fully online in **GitHub Codespaces** (no local setup). This project fuses Elliott Wave structure with a state‑conditional Monte Carlo to produce probabilistic target hits, invalidation odds, timing windows, and OTE pullback probabilities.


## Quick start (Codespaces)
1. Open this repo → **Code ▸ Create codespace on main**.
2. Wait for the container to build (installs Python + deps automatically).
3. In the Codespaces terminal, run:
```bash
python examples/run_simulation.py --ticker AAPL --start 2022-01-01 --paths 5000
