"""
Basic N/U Algebra Operations Examples

This script demonstrates the core functionality of N/U Algebra
with practical examples from the validation paper.

Reference:
Martin, Eric D. (2025). The NASA Paper & Small Falcon Algebra.
"""

import sys
sys.path.insert(0, '../src')
from nu_algebra import NU, cumulative_sum, cumulative_product, weighted_mean


def example_1_voltage_addition():
    """
    Example 7.1 from the paper: Voltage Addition
    
    Adding two voltage measurements with uncertainties.
    """
    print("=" * 60)
    print("Example 1: Voltage Addition")
    print("=" * 60)
    
    v1 = NU(2.00, 0.05)  # 2.00 V ± 0.05 V
    v2 = NU(1.20, 0.02)  # 1.20 V ± 0.02 V
    
    print(f"Voltage 1: {v1}")
    print(f"Voltage 2: {v2}")
    
    total = v1.add(v2)
    print(f"\nTotal voltage: {total}")
    print(f"Result: ({total.n:.2f} V, {total.u:.2f} V)")
    print(f"Interval: [{total.lower_bound():.2f}, {total.upper_bound():.2f}] V")
    
    # Compare to Gaussian RSS
    import math
    gaussian_rss = math.sqrt(0.05**2 + 0.02**2)
    print(f"\nGaussian RSS uncertainty: {gaussian_rss:.4f} V")
    print(f"N/U uncertainty: {total.u:.4f} V")
    print(f"N/U is {total.u/gaussian_rss:.2f}× more conservative")
    print()


def example_2_area_calculation():
    """
    Example 7.2 from the paper: Area Calculation
    
    Computing area with measurement uncertainties.
    """
    print("=" * 60)
    print("Example 2: Area Calculation")
    print("=" * 60)
    
    length = NU(4.0, 0.1)   # 4.0 m ± 0.1 m
    width = NU(3.0, 0.2)    # 3.0 m ± 0.2 m
    
    print(f"Length: {length}")
    print(f"Width: {width}")
    
    area = length.mul(width)
    print(f"\nArea: {area}")
    print(f"Result: ({area.n:.1f} m², {area.u:.1f} m²)")
    print(f"Interval: [{area.lower_bound():.1f}, {area.upper_bound():.1f}] m²")
    print(f"Relative uncertainty: {area.relative_uncertainty():.1%}")
    print(f"Sign stable: {area.is_sign_stable()}")
    print()


def example_3_large_product():
    """
    Example 7.3 from the paper: Large Product
    
    Demonstrates that N/U algebra handles large values correctly.
    """
    print("=" * 60)
    print("Example 3: Large Product")
    print("=" * 60)
    
    x = NU(100, 10)
    y = NU(200, 5)
    
    print(f"X: {x}")
    print(f"Y: {y}")
    
    product = x.mul(y)
    print(f"\nProduct: {product}")
    print(f"Calculation: |100|×5 + |200|×10 = {abs(100)*5 + abs(200)*10}")
    print(f"Result matches: {product.u == 2500}")
    print()


def example_4_multiple_measurements():
    """
    Example 7.5 from the paper: Multiple Measurements
    
    Combining multiple measurements with cumulative sum.
    """
    print("=" * 60)
    print("Example 4: Multiple Measurements")
    print("=" * 60)
    
    measurements = [
        NU(100.0, 2.0),
        NU(105.0, 1.5),
        NU(102.5, 1.0)
    ]
    
    print("Measurements:")
    for i, m in enumerate(measurements, 1):
        print(f"  {i}. {m}")
    
    total = cumulative_sum(*measurements)
    print(f"\nCumulative sum: {total}")
    
    # Compare to Gaussian RSS
    import math
    gaussian_rss = math.sqrt(2.0**2 + 1.5**2 + 1.0**2)
    print(f"\nGaussian RSS uncertainty: {gaussian_rss:.2f}")
    print(f"N/U uncertainty: {total.u:.2f}")
    print(f"Ratio: {total.u/gaussian_rss:.2f}")
    print()


def example_5_work_calculation():
    """
    Example 7.6 from the paper: Work Calculation (Force × Distance)
    """
    print("=" * 60)
    print("Example 5: Work Calculation")
    print("=" * 60)
    
    force = NU(10.0, 0.2)      # 10.0 N ± 0.2 N
    distance = NU(2.0, 0.05)   # 2.0 m ± 0.05 m
    
    print(f"Force: {force}")
    print(f"Distance: {distance}")
    
    work = force.mul(distance)
    print(f"\nWork: {work}")
    print(f"Result: {work.n:.1f} J ± {work.u:.1f} J")
    print()


def example_6_scalar_operations():
    """
    Demonstrate scalar multiplication and affine transformations.
    """
    print("=" * 60)
    print("Example 6: Scalar Operations")
    print("=" * 60)
    
    temperature_c = NU(20, 0.5)  # 20°C ± 0.5°C
    print(f"Temperature (Celsius): {temperature_c}")
    
    # Convert to Fahrenheit: F = 9/5 * C + 32
    temperature_f = temperature_c.affine(9/5, 32)
    print(f"Temperature (Fahrenheit): {temperature_f}")
    print(f"Result: {temperature_f.n:.1f}°F ± {temperature_f.u:.1f}°F")
    
    # Double a measurement
    doubled = temperature_c.scalar(2)
    print(f"\nDoubled: {doubled}")
    print()


def example_7_special_operators():
    """
    Demonstrate Catch and Flip operators with invariant preservation.
    """
    print("=" * 60)
    print("Example 7: Special Operators")
    print("=" * 60)
    
    nu = NU(5, 2)
    print(f"Original: {nu}")
    print(f"Invariant M(n,u) = |n| + u = {nu.invariant()}")
    
    caught = nu.catch()
    print(f"\nCatch: {caught}")
    print(f"Invariant: {caught.invariant()}")
    print(f"Invariant preserved: {nu.invariant() == caught.invariant()}")
    
    flipped = nu.flip()
    print(f"\nFlip: {flipped}")
    print(f"Invariant: {flipped.invariant()}")
    print(f"Invariant preserved: {nu.invariant() == flipped.invariant()}")
    print()


def example_8_operator_overloading():
    """
    Demonstrate Python operator overloading (+, -, *, etc.)
    """
    print("=" * 60)
    print("Example 8: Operator Overloading")
    print("=" * 60)
    
    a = NU(10, 1)
    b = NU(5, 0.5)
    
    print(f"a = {a}")
    print(f"b = {b}")
    
    print(f"\na + b = {a + b}")
    print(f"a - b = {a - b}")
    print(f"a * b = {a * b}")
    print(f"2 * a = {2 * a}")
    print(f"a + 5 = {a + 5}")
    print(f"-a = {-a}")
    print()


def example_9_sign_stability():
    """
    Demonstrate sign stability checking.
    """
    print("=" * 60)
    print("Example 9: Sign Stability")
    print("=" * 60)
    
    stable = NU(10, 2)      # |10| > 2 → stable
    unstable = NU(3, 5)     # |3| < 5 → unstable
    boundary = NU(5, 5)     # |5| = 5 → boundary
    
    for label, nu in [("Stable", stable), ("Unstable", unstable), ("Boundary", boundary)]:
        print(f"{label}: {nu}")
        print(f"  Interval: {nu.interval()}")
        print(f"  Sign stable: {nu.is_sign_stable()}")
        print(f"  |n| > u: {abs(nu.n)} > {nu.u} = {abs(nu.n) > nu.u}")
    print()


def example_10_weighted_mean():
    """
    Compute weighted mean of multiple measurements.
    """
    print("=" * 60)
    print("Example 10: Weighted Mean")
    print("=" * 60)
    
    # Three measurements with different precisions
    measurements = [
        NU(100.0, 2.0),   # Lower precision
        NU(102.0, 1.0),   # Medium precision
        NU(101.0, 0.5)    # High precision
    ]
    
    # Weight inversely by uncertainty (more precise = higher weight)
    weights = [1/m.u for m in measurements]
    
    print("Measurements:")
    for i, (m, w) in enumerate(zip(measurements, weights), 1):
        print(f"  {i}. {m} (weight: {w:.2f})")
    
    mean = weighted_mean(measurements, weights)
    print(f"\nWeighted mean: {mean}")
    
    # Compare to unweighted mean
    unweighted = weighted_mean(measurements)
    print(f"Unweighted mean: {unweighted}")
    print()


def main():
    """Run all examples."""
    examples = [
        example_1_voltage_addition,
        example_2_area_calculation,
        example_3_large_product,
        example_4_multiple_measurements,
        example_5_work_calculation,
        example_6_scalar_operations,
        example_7_special_operators,
        example_8_operator_overloading,
        example_9_sign_stability,
        example_10_weighted_mean
    ]
    
    for example in examples:
        example()
    
    print("=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
