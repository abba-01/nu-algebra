# Validation Datasets

The complete numerical validation dataset (70,000+ test cases) is available on Zenodo:

**DOI**: [10.5281/zenodo.17221863](https://doi.org/10.5281/zenodo.17221863)

## Included Files
- `addition_sweep.csv` (8,000 rows)
- `product_sweep.csv` (30,000 rows)
- `interval_relation.csv` (30,000 rows)
- `chain_experiment.csv` (3,200 rows)
- `mc_comparisons.csv` (24 rows)
- `invariants_grid.csv` (54 rows)
- `associativity_nominal_diffs.csv` (20,000 rows)
- `summary.json`

## Regeneration

To regenerate the datasets locally:
```bash
python scripts/generate_nu_data.py
