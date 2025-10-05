# The NASA Paper & Small Falcon Algebra

**A Conservative Framework for Uncertainty Quantification**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17172694.svg)](https://doi.org/10.5281/zenodo.17172694)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

---

## 📋 Overview

**N/U (Nominal/Uncertainty) Algebra** is a mathematically rigorous framework for propagating explicit uncertainty bounds alongside nominal values in safety-critical systems. Every quantity is represented as an ordered pair **(n, u)** where:
- **n** ∈ ℝ is the nominal (central) value
- **u** ≥ 0 is a nonnegative uncertainty bound

### Key Properties

- ✅ **Conservative Bounds**: Never underestimates uncertainty (validated across 70,000+ test cases)
- ✅ **O(1) Complexity**: Constant-time operations per pair
- ✅ **Deterministic**: Reproducible results without distributional assumptions
- ✅ **Mathematically Proven**: Closure, associativity, monotonicity formally established
- ✅ **Audit-Ready**: Transparent, traceable uncertainty propagation

---

## 🎯 Use Cases

N/U Algebra is designed for domains requiring **conservative, transparent uncertainty quantification**:

- **Aerospace & Engineering**: Safety-critical calculations with guaranteed bounds
- **Metrology**: Measurement uncertainty propagation per JCGM guidelines
- **Psychological Science**: Conservative effect size estimation and replication prediction
- **Regulatory Compliance**: Audit-defensible uncertainty tracking
- **Real-Time Systems**: Low-latency uncertainty propagation

---

## 📊 Validation Results

Extensive numerical validation confirms the algebra's properties:

| Test Category | Cases | Key Finding |
|--------------|-------|-------------|
| **Addition vs Gaussian RSS** | 8,000 | N/U ≥ RSS in 100% of cases (ratio: 1.00–3.54, median 1.74) |
| **Multiplication vs Gaussian** | 30,000 | Ratio range: 1.00–1.41 (√2 cap), median ≈1.001 |
| **Interval Consistency** | 30,000 | Matches interval arithmetic within 0.014% (floating-point error) |
| **Chain Stability** | 3,200 | No error explosion; max difference ~10⁻¹² |
| **Monte Carlo Comparison** | 24 | N/U bounds exceed empirical std across all distributions |
| **Invariant Preservation** | 54 | Perfect conservation (max error: 0.0) |

**Full dataset**: [Zenodo DOI 10.5281/zenodo.17221863](https://doi.org/10.5281/zenodo.17221863)

---

## 🚀 Quick Start

### Python Implementation

```python
from nu_algebra import NU

# Create N/U pairs
voltage1 = NU(2.00, 0.05)  # (2.00 V, ±0.05 V)
voltage2 = NU(1.20, 0.02)  # (1.20 V, ±0.02 V)

# Operations
total = voltage1.add(voltage2)     # (3.20 V, 0.07 V)
print(f"Total voltage: {total}")

# Area calculation
length = NU(4.0, 0.1)
width = NU(3.0, 0.2)
area = length.mul(width)           # (12.0 m², 1.1 m²)
print(f"Area: {area}")

# Scalar multiplication
scaled = voltage1.scalar(2.5)      # (5.00 V, 0.125 V)
```

### R Implementation

```r
source("nu_algebra.R")

# Create N/U pairs
voltage1 <- c(2.00, 0.05)
voltage2 <- c(1.20, 0.02)

# Operations
total <- NU_add(voltage1, voltage2)
cat("Total voltage:", total, "\n")  # (3.20, 0.07)

# Multiplication
length <- c(4.0, 0.1)
width <- c(3.0, 0.2)
area <- NU_mul(length, width)
cat("Area:", area, "\n")            # (12.0, 1.1)
```

---

## 📁 Repository Contents

### Core Implementations
- `nu_algebra.py` — Python implementation with full operator suite
- `nu_algebra.R` — R implementation for statistical workflows
- `generate_nu_data.py` — Reproducibility script for validation dataset

### Documentation
- `README.md` — Numerical validation dataset documentation
- `summary.json` — Machine-readable validation statistics
- `Nominal Uncertainty Algebra Case.txt` — Psychology application framework

### Validation Data (Available on Zenodo)
- `addition_sweep.csv` — 8,000 addition tests vs Gaussian RSS
- `product_sweep.csv` — 30,000 multiplication tests
- `interval_relation.csv` — Interval arithmetic comparison
- `chain_experiment.csv` — Repeated multiplication stability
- `mc_comparisons.csv` — Monte Carlo validation (24 distributions)
- `invariants_grid.csv` — Invariant preservation tests

---

## 📖 Core Operations

### Primary Operations

| Operation | Formula | Example |
|-----------|---------|---------|
| **Addition** | (n₁+n₂, u₁+u₂) | (10,1) ⊕ (5,0.5) = (15, 1.5) |
| **Multiplication** | (n₁n₂, \|n₁\|u₂ + \|n₂\|u₁) | (10,1) ⊗ (5,0.5) = (50, 15) |
| **Scalar** | (an, \|a\|u) | 3 ⊙ (10,1) = (30, 3) |

### Special Operators

| Operator | Formula | Invariant Preserved |
|----------|---------|---------------------|
| **Catch** | C(n,u) = (0, \|n\|+u) | M = \|n\| + u |
| **Flip** | B(n,u) = (u, \|n\|) | M = \|n\| + u |

---

## 🔬 Comparative Analysis

| Method | Assumptions | Complexity | Conservatism | N/U Advantage |
|--------|-------------|------------|--------------|---------------|
| **N/U Algebra** | None | O(1) | High | Deterministic, transparent |
| Gaussian Propagation | Linearity | O(1) | Low | More conservative |
| Monte Carlo | None | O(n) | Variable | Deterministic bounds |
| Interval Arithmetic | None | O(1) | High | Better stability |
| Polynomial Chaos | Smoothness | O(p^d) | Moderate | Much faster |

---

## 📚 Citation

If you use this work, please cite:

```bibtex
@misc{martin2025nasa,
  author       = {Martin, Eric D.},
  title        = {The NASA Paper \& Small Falcon Algebra},
  year         = {2025},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.17172694},
  url          = {https://doi.org/10.5281/zenodo.17172694}
}

@dataset{martin2025validation,
  author       = {Martin, Eric D.},
  title        = {N/U Algebra Numerical Validation Dataset},
  year         = {2025},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.17221863},
  url          = {https://doi.org/10.5281/zenodo.17221863}
}
```

### Author
**Eric D. Martin**  
ORCID: [0009-0006-5944-1742](https://orcid.org/0009-0006-5944-1742)

---

## 🔄 Reproducibility

All numerical results are fully reproducible:

1. **Install dependencies**:
   ```bash
   pip install numpy pandas  # Python
   # or use R with built-in packages
   ```

2. **Run validation**:
   ```bash
   python generate_nu_data.py
   ```

3. **Parameters**:
   - RNG seed: `20250926`
   - Absolute tolerance: `1e-9`
   - Relative tolerance: `1e-12`

---

## 🛠️ Integration Examples

### With Bayesian Methods
Use N/U bounds as initial envelopes for Bayesian updating:
```python
prior_nu = NU(mean_prior, conservative_bound)
# Bayesian update refines within N/U envelope
```

### With Monte Carlo
Use N/U algebra for rapid initial bounds before sampling:
```python
fast_bound = x.mul(y)  # O(1) conservative bound
# Then run MC within envelope if needed
```

### With Machine Learning
Train models to respect N/U constraints:
```python
# Ensure predictions stay within propagated bounds
prediction_nu = model_nu.predict(input_nu)
```

---

## 🤝 Applications

### Aerospace (NASA Context)
- Safety-critical trajectory calculations
- Sensor fusion with guaranteed bounds
- Real-time uncertainty propagation

### Psychology & Social Science
- Conservative effect size estimation
- Replication prediction (see `Nominal Uncertainty Algebra Case.txt`)
- Meta-analysis with transparent uncertainty

### Engineering
- Structural analysis stress/strain bounds
- Measurement uncertainty per JCGM guidelines
- Quality control with audit trails

---

## 📄 License

**CC BY 4.0** — You are free to:
- **Share**: Copy and redistribute the material
- **Adapt**: Remix, transform, and build upon the material

**Under the following terms**:
- **Attribution**: You must give appropriate credit and link to the license

---

## 🔗 Related Resources

- **Validation Dataset**: [Zenodo 10.5281/zenodo.17221863](https://doi.org/10.5281/zenodo.17221863)
- **JCGM Guidelines**: [GUM 2008](https://www.bipm.org/en/publications/guides/gum)
- **Interval Arithmetic Standard**: [IEEE 1788-2015](https://standards.ieee.org/standard/1788-2015.html)

---

## 📞 Contact & Support

For questions, issues, or collaboration:
- **Issues**: Open a GitHub issue in this repository
- **Email**: Contact via ORCID profile
- **Citation Questions**: See CITATION.cff file

---

**Built on the principle**: *Never claim more certainty than your measurements support.* More. Or Less.
