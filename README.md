# The NASA Paper & Small Falcon Algebra

This project began as part of exploratory research at NASA and has since grown into a broader framework for conservative uncertainty quantification.  
The methods presented here build directly on those early efforts, now formalized as **N/U Algebra**.  

**Citation**:  
Martin, E. D. (2025). *The NASA Paper & Small Falcon Algebra.* Zenodo. https://doi.org/10.5281/zenodo.17172694

---

# N/U Algebra: A Conservative Linear Approach to Uncertainty Propagation

This repository contains the reference implementations of N/U Algebra, a framework for conservative and reproducible uncertainty propagation.  

**Citation**:  
Martin, E. D. (2025). *N/U Algebra: A Conservative Linear Approach to Uncertainty Propagation.* Zenodo.  https://doi.org/10.5281/zenodo.17172694

---

## Overview

N/U Algebra represents every value as an ordered pair **(n, u)** of nominal value and explicit uncertainty. The algebra defines addition, multiplication, and scalar multiplication with rules that guarantee:

- **Conservatism**: propagated uncertainties are never underestimated.  
- **Transparency**: operations are explicit and auditable.  
- **Reproducibility**: results are deterministic given inputs.  

The full theoretical development, proofs, and validation results are provided in the published manuscript (see DOI above).  

---

## Contents

- `nu_algebra.py` — Python implementation of N/U Algebra  
- `nu_algebra.R` — R implementation of N/U Algebra  
- `generate_nu_data.py` — script to reproduce the numerical validation dataset  

---

## Usage

**Python example:**
```python
from nu_algebra import NU

x = NU(10, 1)
y = NU(5, 0.5)

print("x + y =", x.add(y))
print("x * y =", x.mul(y))
print("2 * x =", x.scalar(2))




R Example
source("nu_algebra.R")

x <- c(10, 1)
y <- c(5, 0.5)

cat("x + y =", NU_add(x, y), "\n")
cat("x * y =", NU_mul(x, y), "\n")
cat("2 * x =", NU_scalar(2, x), "\n")

