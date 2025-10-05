# Basic N/U Algebra Operations Examples (R)
#
# This script demonstrates the core functionality of N/U Algebra
# with practical examples from the validation paper.
#
# Reference:
# Martin, Eric D. (2025). The NASA Paper & Small Falcon Algebra.

# Load N/U Algebra functions
source("../src/nu_algebra.R")

# Helper function to print section headers
print_header <- function(title) {
  cat("\n")
  cat(paste(rep("=", 60), collapse = ""), "\n")
  cat(title, "\n")
  cat(paste(rep("=", 60), collapse = ""), "\n")
}

# Helper function to print N/U pair nicely
print_nu <- function(label, nu) {
  cat(sprintf("%s: NU(%.4f, %.4f)\n", label, nu[1], nu[2]))
}


# ==============================================================================
# Example 1: Voltage Addition
# ==============================================================================
example_1_voltage_addition <- function() {
  print_header("Example 1: Voltage Addition")
  
  v1 <- c(2.00, 0.05)  # 2.00 V ± 0.05 V
  v2 <- c(1.20, 0.02)  # 1.20 V ± 0.02 V
  
  print_nu("Voltage 1", v1)
  print_nu("Voltage 2", v2)
  
  total <- NU_add(v1, v2)
  cat("\n")
  print_nu("Total voltage", total)
  cat(sprintf("Result: (%.2f V, %.2f V)\n", total[1], total[2]))
  cat(sprintf("Interval: [%.2f, %.2f] V\n", 
              NU_lower(total), NU_upper(total)))
  
  # Compare to Gaussian RSS
  gaussian_rss <- sqrt(0.05^2 + 0.02^2)
  cat(sprintf("\nGaussian RSS uncertainty: %.4f V\n", gaussian_rss))
  cat(sprintf("N/U uncertainty: %.4f V\n", total[2]))
  cat(sprintf("N/U is %.2fx more conservative\n", total[2] / gaussian_rss))
}


# ==============================================================================
# Example 2: Area Calculation
# ==============================================================================
example_2_area_calculation <- function() {
  print_header("Example 2: Area Calculation")
  
  length <- c(4.0, 0.1)   # 4.0 m ± 0.1 m
  width <- c(3.0, 0.2)    # 3.0 m ± 0.2 m
  
  print_nu("Length", length)
  print_nu("Width", width)
  
  area <- NU_mul(length, width)
  cat("\n")
  print_nu("Area", area)
  cat(sprintf("Result: (%.1f m², %.1f m²)\n", area[1], area[2]))
  cat(sprintf("Interval: [%.1f, %.1f] m²\n", 
              NU_lower(area), NU_upper(area)))
  cat(sprintf("Relative uncertainty: %.1f%%\n", 
              NU_relative(area) * 100))
  cat(sprintf("Sign stable: %s\n", NU_is_sign_stable(area)))
}


# ==============================================================================
# Example 3: Large Product
# ==============================================================================
example_3_large_product <- function() {
  print_header("Example 3: Large Product")
  
  x <- c(100, 10)
  y <- c(200, 5)
  
  print_nu("X", x)
  print_nu("Y", y)
  
  product <- NU_mul(x, y)
  cat("\n")
  print_nu("Product", product)
  
  expected_u <- abs(100) * 5 + abs(200) * 10
  cat(sprintf("Calculation: |100|×5 + |200|×10 = %.0f\n", expected_u))
  cat(sprintf("Result matches: %s\n", product[2] == expected_u))
}


# ==============================================================================
# Example 4: Multiple Measurements
# ==============================================================================
example_4_multiple_measurements <- function() {
  print_header("Example 4: Multiple Measurements")
  
  measurements <- list(
    c(100.0, 2.0),
    c(105.0, 1.5),
    c(102.5, 1.0)
  )
  
  cat("Measurements:\n")
  for (i in seq_along(measurements)) {
    cat(sprintf("  %d. ", i))
    print_nu("", measurements[[i]])
  }
  
  total <- do.call(NU_cumsum, measurements)
  cat("\n")
  print_nu("Cumulative sum", total)
  
  # Compare to Gaussian RSS
  uncertainties <- sapply(measurements, function(m) m[2])
  gaussian_rss <- sqrt(sum(uncertainties^2))
  cat(sprintf("\nGaussian RSS uncertainty: %.2f\n", gaussian_rss))
  cat(sprintf("N/U uncertainty: %.2f\n", total[2]))
  cat(sprintf("Ratio: %.2f\n", total[2] / gaussian_rss))
}


# ==============================================================================
# Example 5: Work Calculation
# ==============================================================================
example_5_work_calculation <- function() {
  print_header("Example 5: Work Calculation")
  
  force <- c(10.0, 0.2)      # 10.0 N ± 0.2 N
  distance <- c(2.0, 0.05)   # 2.0 m ± 0.05 m
  
  print_nu("Force", force)
  print_nu("Distance", distance)
  
  work <- NU_mul(force, distance)
  cat("\n")
  print_nu("Work", work)
  cat(sprintf("Result: %.1f J ± %.1f J\n", work[1], work[2]))
}


# ==============================================================================
# Example 6: Scalar Operations
# ==============================================================================
example_6_scalar_operations <- function() {
  print_header("Example 6: Scalar Operations")
  
  temperature_c <- c(20, 0.5)  # 20°C ± 0.5°C
  print_nu("Temperature (Celsius)", temperature_c)
  
  # Convert to Fahrenheit: F = 9/5 * C + 32
  temperature_f <- NU_affine(9/5, temperature_c, 32)
  print_nu("Temperature (Fahrenheit)", temperature_f)
  cat(sprintf("Result: %.1f°F ± %.1f°F\n", temperature_f[1], temperature_f[2]))
  
  # Double a measurement
  doubled <- NU_scalar(2, temperature_c)
  cat("\n")
  print_nu("Doubled", doubled)
}


# ==============================================================================
# Example 7: Special Operators
# ==============================================================================
example_7_special_operators <- function() {
  print_header("Example 7: Special Operators")
  
  nu <- c(5, 2)
  print_nu("Original", nu)
  cat(sprintf("Invariant M(n,u) = |n| + u = %.1f\n", NU_invariant(nu)))
  
  caught <- NU_catch(nu)
  cat("\n")
  print_nu("Catch", caught)
  cat(sprintf("Invariant: %.1f\n", NU_invariant(caught)))
  cat(sprintf("Invariant preserved: %s\n", 
              NU_invariant(nu) == NU_invariant(caught)))
  
  flipped <- NU_flip(nu)
  cat("\n")
  print_nu("Flip", flipped)
  cat(sprintf("Invariant: %.1f\n", NU_invariant(flipped)))
  cat(sprintf("Invariant preserved: %s\n", 
              NU_invariant(nu) == NU_invariant(flipped)))
}


# ==============================================================================
# Example 8: Chaining Operations
# ==============================================================================
example_8_chaining_operations <- function() {
  print_header("Example 8: Chaining Operations")
  
  a <- c(10, 1)
  b <- c(5, 0.5)
  c <- c(2, 0.2)
  
  print_nu("a", a)
  print_nu("b", b)
  print_nu("c", c)
  
  # (a + b) * c
  cat("\n(a + b) * c:\n")
  result1 <- NU_mul(NU_add(a, b), c)
  print_nu("Result", result1)
  
  # a * c + b * c (distributive property check)
  cat("\na * c + b * c:\n")
  result2 <- NU_add(NU_mul(a, c), NU_mul(b, c))
  print_nu("Result", result2)
  
  cat(sprintf("\nNominals equal: %s\n", result1[1] == result2[1]))
  cat(sprintf("N/U is sub-distributive: u1 <= u2: %s\n", 
              result1[2] <= result2[2]))
}


# ==============================================================================
# Example 9: Sign Stability
# ==============================================================================
example_9_sign_stability <- function() {
  print_header("Example 9: Sign Stability")
  
  stable <- c(10, 2)      # |10| > 2 → stable
  unstable <- c(3, 5)     # |3| < 5 → unstable
  boundary <- c(5, 5)     # |5| = 5 → boundary
  
  test_cases <- list(
    list(label = "Stable", nu = stable),
    list(label = "Unstable", nu = unstable),
    list(label = "Boundary", nu = boundary)
  )
  
  for (case in test_cases) {
    cat(sprintf("\n%s: ", case$label))
    print_nu("", case$nu)
    interval <- NU_interval(case$nu)
    cat(sprintf("  Interval: [%.1f, %.1f]\n", interval[1], interval[2]))
    cat(sprintf("  Sign stable: %s\n", NU_is_sign_stable(case$nu)))
    cat(sprintf("  |n| > u: %.0f > %.0f = %s\n", 
                abs(case$nu[1]), case$nu[2], 
                abs(case$nu[1]) > case$nu[2]))
  }
}


# ==============================================================================
# Example 10: Weighted Mean
# ==============================================================================
example_10_weighted_mean <- function() {
  print_header("Example 10: Weighted Mean")
  
  # Three measurements with different precisions
  measurements <- list(
    c(100.0, 2.0),   # Lower precision
    c(102.0, 1.0),   # Medium precision
    c(101.0, 0.5)    # High precision
  )
  
  # Weight inversely by uncertainty (more precise = higher weight)
  weights <- sapply(measurements, function(m) 1 / m[2])
  
  cat("Measurements:\n")
  for (i in seq_along(measurements)) {
    cat(sprintf("  %d. ", i))
    print_nu("", measurements[[i]])
    cat(sprintf("     (weight: %.2f)\n", weights[i]))
  }
  
  mean_weighted <- NU_weighted_mean(measurements, weights)
  cat("\n")
  print_nu("Weighted mean", mean_weighted)
  
  # Compare to unweighted mean
  mean_unweighted <- NU_weighted_mean(measurements)
  print_nu("Unweighted mean", mean_unweighted)
}


# ==============================================================================
# Main Execution
# ==============================================================================
main <- function() {
  cat("\n")
  cat(paste(rep("=", 60), collapse = ""), "\n")
  cat("N/U Algebra Examples in R\n")
  cat(paste(rep("=", 60), collapse = ""), "\n")
  cat("Reference: Martin, E.D. (2025). The NASA Paper & Small Falcon Algebra\n")
  
  examples <- list(
    example_1_voltage_addition,
    example_2_area_calculation,
    example_3_large_product,
    example_4_multiple_measurements,
    example_5_work_calculation,
    example_6_scalar_operations,
    example_7_special_operators,
    example_8_chaining_operations,
    example_9_sign_stability,
    example_10_weighted_mean
  )
  
  for (example_fn in examples) {
    example_fn()
  }
  
  cat("\n")
  cat(paste(rep("=", 60), collapse = ""), "\n")
  cat("All examples completed successfully!\n")
  cat(paste(rep("=", 60), collapse = ""), "\n")
  cat("\n")
}


# Run all examples
if (!interactive()) {
  main()
}


# ==============================================================================
# Interactive Usage Examples
# ==============================================================================

# If running interactively in R console, you can run individual examples:
#
# > source("basic_operations.R")
# > example_1_voltage_addition()
# > example_2_area_calculation()
# etc.
#
# Or run all examples:
# > main()
