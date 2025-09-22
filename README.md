# N/U Algebra

**A Conservative Linear Algebra for Uncertainty Propagation**

This repository provides open, reproducible code for N/U Algebra, as described in the manuscript:

> Martin, E. D. (2025). N/U Algebra: A Conservative Linear Approach to Uncertainty Propagation. ...

- **nu_algebra.py:** Python implementation of N/U Algebra (Nominal/Uncertainty Algebra)
- **nu_algebra.R:** R implementation of N/U Algebra

## Description

N/U Algebra is a conservative, transparent framework for uncertainty propagation. All quantities are represented as ordered pairs (n, u) of nominal value and explicit uncertainty. The algebra supports addition, multiplication, and scalar multiplication, guaranteeing reproducibility and monotonicity.

See the full paper ...... for theory, proofs, and example applications.

## Usage

```python

# Python example
from nu_algebra import NU

x = NU(10, 1)
y = NU(5, 0.5)
print("x + y =", x.add(y))
print("x * y =", x.mul(y))
print("2 * x =", x.scalar(2))

# R example
source("nu_algebra.R")
x <- c(10, 1)
y <- c(5, 0.5)
cat("x + y =", NU_add(x, y), "\n")
cat("x * y =", NU_mul(x, y), "\n")
cat("2 * x =", NU_scalar(2, x), "\n")
License

CC BY 4.0

Author

Eric D. Martin

Manuscript: 
Website: https://ericdmartin.com
