# N/U Algebra: Conservative Uncertainty Propagation
# 
# This R implementation provides the N/U (Nominal/Uncertainty) Algebra framework
# for propagating explicit uncertainty bounds alongside nominal values.
#
# Reference:
# Martin, Eric D. (2025). The NASA Paper & Small Falcon Algebra.
# DOI: 10.5281/zenodo.17172694

# ==================== Core Operations ====================

#' N/U Addition
#' 
#' Addition operator: (n1, u1) + (n2, u2) = (n1+n2, u1+u2)
#' 
#' @param x Numeric vector c(n, u)
#' @param y Numeric vector c(n, u)
#' @return Numeric vector c(n_result, u_result)
#' @examples
#' NU_add(c(10, 1), c(5, 0.5))  # Returns c(15, 1.5)
NU_add <- function(x, y) {
  if (length(x) != 2 || length(y) != 2) {
    stop("N/U pairs must be length 2 vectors")
  }
  c(n = x[1] + y[1], u = x[2] + y[2])
}

#' N/U Subtraction
#' 
#' Subtraction operator: (n1, u1) - (n2, u2) = (n1-n2, u1+u2)
#' 
#' @param x Numeric vector c(n, u)
#' @param y Numeric vector c(n, u)
#' @return Numeric vector c(n_result, u_result)
NU_sub <- function(x, y) {
  if (length(x) != 2 || length(y) != 2) {
    stop("N/U pairs must be length 2 vectors")
  }
  c(n = x[1] - y[1], u = x[2] + y[2])
}

#' N/U Multiplication
#' 
#' Multiplication: (n1, u1) * (n2, u2) = (n1*n2, |n1|*u2 + |n2|*u1)
#' 
#' @param x Numeric vector c(n, u)
#' @param y Numeric vector c(n, u)
#' @return Numeric vector c(n_result, u_result)
#' @examples
#' NU_mul(c(4.0, 0.1), c(3.0, 0.2))  # Returns c(12.0, 1.1)
NU_mul <- function(x, y) {
  if (length(x) != 2 || length(y) != 2) {
    stop("N/U pairs must be length 2 vectors")
  }
  c(
    n = x[1] * y[1],
    u = abs(x[1]) * y[2] + abs(y[1]) * x[2]
  )
}

#' N/U Scalar Multiplication
#' 
#' Scalar multiplication: a * (n, u) = (a*n, |a|*u)
#' 
#' @param a Scalar value
#' @param x Numeric vector c(n, u)
#' @return Numeric vector c(n_result, u_result)
#' @examples
#' NU_scalar(2.5, c(10, 1))  # Returns c(25.0, 2.5)
NU_scalar <- function(a, x) {
  if (length(x) != 2) {
    stop("N/U pair must be length 2 vector")
  }
  c(n = a * x[1], u = abs(a) * x[2])
}

#' N/U Affine Transformation
#' 
#' Affine: a * (n, u) + b = (a*n + b, |a|*u)
#' 
#' @param a Scale factor
#' @param x Numeric vector c(n, u)
#' @param b Offset (default 0)
#' @return Numeric vector c(n_result, u_result)
NU_affine <- function(a, x, b = 0) {
  if (length(x) != 2) {
    stop("N/U pair must be length 2 vector")
  }
  c(n = a * x[1] + b, u = abs(a) * x[2])
}

# ==================== Special Operators ====================

#' N/U Catch Operator
#' 
#' Catch: C(n, u) = (0, |n| + u)
#' Collapses nominal into uncertainty, preserving invariant M(n,u)
#' 
#' @param x Numeric vector c(n, u)
#' @return Numeric vector c(0, |n|+u)
NU_catch <- function(x) {
  if (length(x) != 2) {
    stop("N/U pair must be length 2 vector")
  }
  c(n = 0, u = abs(x[1]) + x[2])
}

#' N/U Flip Operator
#' 
#' Flip: B(n, u) = (u, |n|)
#' Swaps nominal and uncertainty while preserving invariant M(n,u)
#' 
#' @param x Numeric vector c(n, u)
#' @return Numeric vector c(u, |n|)
NU_flip <- function(x) {
  if (length(x) != 2) {
    stop("N/U pair must be length 2 vector")
  }
  c(n = x[2], u = abs(x[1]))
}

# ==================== Properties ====================

#' N/U Invariant
#' 
#' Compute the uncertainty invariant: M(n, u) = |n| + u
#' This is preserved by Catch and Flip operators
#' 
#' @param x Numeric vector c(n, u)
#' @return Invariant value
NU_invariant <- function(x) {
  if (length(x) != 2) {
    stop("N/U pair must be length 2 vector")
  }
  abs(x[1]) + x[2]
}

#' N/U Lower Bound
#' 
#' Conservative lower bound: n - u
#' 
#' @param x Numeric vector c(n, u)
#' @return Lower bound value
NU_lower <- function(x) {
  if (length(x) != 2) {
    stop("N/U pair must be length 2 vector")
  }
  x[1] - x[2]
}

#' N/U Upper Bound
#' 
#' Conservative upper bound: n + u
#' 
#' @param x Numeric vector c(n, u)
#' @return Upper bound value
NU_upper <- function(x) {
  if (length(x) != 2) {
    stop("N/U pair must be length 2 vector")
  }
  x[1] + x[2]
}

#' N/U Interval
#' 
#' Return interval representation [n-u, n+u]
#' 
#' @param x Numeric vector c(n, u)
#' @return Numeric vector c(lower, upper)
NU_interval <- function(x) {
  if (length(x) != 2) {
    stop("N/U pair must be length 2 vector")
  }
  c(lower = x[1] - x[2], upper = x[1] + x[2])
}

#' N/U Relative Uncertainty
#' 
#' Relative uncertainty: u / |n|
#' 
#' @param x Numeric vector c(n, u)
#' @return Relative uncertainty (Inf if n=0)
NU_relative <- function(x) {
  if (length(x) != 2) {
    stop("N/U pair must be length 2 vector")
  }
  if (x[1] == 0) return(Inf)
  x[2] / abs(x[1])
}

#' N/U Sign Stability Check
#' 
#' Check if sign is stable (|n| > u)
#' 
#' @param x Numeric vector c(n, u)
#' @return Logical TRUE if interval doesn't contain zero
NU_is_sign_stable <- function(x) {
  if (length(x) != 2) {
    stop("N/U pair must be length 2 vector")
  }
  abs(x[1]) > x[2]
}

# ==================== Cumulative Operations ====================

#' Cumulative N/U Sum
#' 
#' Sum multiple N/U pairs
#' 
#' @param ... N/U pairs as c(n, u) vectors
#' @return Cumulative sum as c(n, u)
#' @examples
#' NU_cumsum(c(1, 0.1), c(2, 0.2), c(3, 0.3))
NU_cumsum <- function(...) {
  pairs <- list(...)
  if (length(pairs) == 0) return(c(n = 0, u = 0))
  
  result <- pairs[[1]]
  if (length(pairs) > 1) {
    for (i in 2:length(pairs)) {
      result <- NU_add(result, pairs[[i]])
    }
  }
  result
}

#' Cumulative N/U Product
#' 
#' Product of multiple N/U pairs
#' 
#' @param ... N/U pairs as c(n, u) vectors
#' @return Cumulative product as c(n, u)
#' @examples
#' NU_cumprod(c(2, 0.1), c(3, 0.2), c(4, 0.1))
NU_cumprod <- function(...) {
  pairs <- list(...)
  if (length(pairs) == 0) return(c(n = 1, u = 0))
  
  result <- pairs[[1]]
  if (length(pairs) > 1) {
    for (i in 2:length(pairs)) {
      result <- NU_mul(result, pairs[[i]])
    }
  }
  result
}

#' Weighted Mean of N/U Pairs
#' 
#' Compute weighted mean with uncertainty propagation
#' 
#' @param pairs List of N/U pairs
#' @param weights Optional numeric vector of weights
#' @return Weighted mean as c(n, u)
NU_weighted_mean <- function(pairs, weights = NULL) {
  if (length(pairs) == 0) {
    stop("Cannot compute mean of empty list")
  }
  
  if (is.null(weights)) {
    weights <- rep(1, length(pairs))
  }
  
  if (length(weights) != length(pairs)) {
    stop("Weights must match number of pairs")
  }
  
  total_weight <- sum(weights)
  if (total_weight == 0) {
    stop("Total weight cannot be zero")
  }
  
  # Weighted sum
  weighted_pairs <- mapply(
    function(nu, w) NU_scalar(w, nu),
    pairs, weights,
    SIMPLIFY = FALSE
  )
  weighted_sum <- do.call(NU_cumsum, weighted_pairs)
  
  # Normalize
  NU_scalar(1 / total_weight, weighted_sum)
}

# ==================== Utility Functions ====================

#' Create N/U Pair
#' 
#' Helper to create an N/U pair with validation
#' 
#' @param n Nominal value
#' @param u Uncertainty (will be clamped to >= 0)
#' @return Numeric vector c(n, u)
NU_create <- function(n, u) {
  c(n = as.numeric(n), u = max(0, as.numeric(u)))
}

#' Print N/U Pair
#' 
#' Pretty-print an N/U pair
#' 
#' @param x Numeric vector c(n, u)
#' @param digits Number of digits to display
NU_print <- function(x, digits = 4) {
  if (length(x) != 2) {
    stop("N/U pair must be length 2 vector")
  }
  cat(sprintf("NU(%.{%d}f, %.{%d}f)\n", digits, digits), x[1], x[2])
}

# ==================== Version Info ====================

NU_ALGEBRA_VERSION <- "1.0.0"
NU_ALGEBRA_AUTHOR <- "Eric D. Martin"
NU_ALGEBRA_LICENSE <- "CC BY 4.0"

# ==================== Example Usage ====================

if (FALSE) {  # Don't run on source()
  # Basic operations
  x <- c(10, 1)
  y <- c(5, 0.5)
  
  cat("Addition:\n")
  print(NU_add(x, y))
  
  cat("\nMultiplication:\n")
  print(NU_mul(x, y))
  
  cat("\nScalar multiplication:\n")
  print(NU_scalar(2.5, x))
  
  # Voltage example
  voltage1 <- c(2.00, 0.05)
  voltage2 <- c(1.20, 0.02)
  total_voltage <- NU_add(voltage1, voltage2)
  cat("\nTotal voltage:", total_voltage, "\n")
  
  # Area example
  length <- c(4.0, 0.1)
  width <- c(3.0, 0.2)
  area <- NU_mul(length, width)
  cat("Area:", area, "\n")
  
  # Check sign stability
  cat("\nIs area sign-stable?", NU_is_sign_stable(area), "\n")
}
