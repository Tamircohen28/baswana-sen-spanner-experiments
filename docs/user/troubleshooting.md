# Troubleshooting

## Import errors after install

Run `make install` to recreate the virtualenv, then `make test`.

## `k` out of range

Baswana-Sen requires `2 <= k <= log(n)`. The experiment runner adjusts k per graph size automatically.

## Greedy comparison too slow

Greedy is O(m·n). Use `run_comparison.py` defaults (n ≤ 1000) or reduce parameters with `--help`.

## Jupyter kernel not found

Activate the project venv before launching Jupyter:

```bash
source .venv/bin/activate
python -m ipykernel install --user --name=baswana-sen
jupyter lab
```
