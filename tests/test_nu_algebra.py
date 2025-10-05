"""
N/U Algebra Unit Tests

Comprehensive test suite for N/U Algebra operations.
Tests all operators, properties, and edge cases.

Reference:
Martin, Eric D. (2025). The NASA Paper & Small Falcon Algebra.
"""

import sys
sys.path.insert(0, '../src')

import pytest
from nu_algebra import NU, cumulative_sum, cumulative_product, weighted_mean


class TestBasicOperations:
    """Test primary N/U algebra operations."""
    
    def test_addition(self):
        """Test addition operator."""
        x = NU(10, 1)
        y = NU(5, 0.5)
        result = x.add(y)
        
        assert result.n == 15
        assert result.u == 1.5
    
    def test_subtraction(self):
        """Test subtraction operator."""
        x = NU(10, 1)
        y = NU(5, 0.5)
        result = x.sub(y)
        
        assert result.n == 5
        assert result.u == 1.5  # Uncertainties add
    
    def test_multiplication(self):
        """Test multiplication operator with absolute values."""
        x = NU(4, 0.1)
        y = NU(3, 0.2)
        result = x.mul(y)
        
        assert result.n == 12
        assert abs(result.u - 1.1) < 1e-10
    
    def test_multiplication_negative_nominals(self):
        """Test multiplication handles negative nominals correctly."""
        x = NU(-4, 0.1)
        y = NU(3, 0.2)
        result = x.mul(y)
        
        assert result.n == -12
        # |n1|*u2 + |n2|*u1 = 4*0.2 + 3*0.1 = 1.1
        assert abs(result.u - 1.1) < 1e-10
    
    def test_scalar_multiplication(self):
        """Test scalar multiplication."""
        x = NU(10, 1)
        result = x.scalar(2.5)
        
        assert result.n == 25
        assert result.u == 2.5
    
    def test_scalar_negative(self):
        """Test scalar multiplication with negative scalar."""
        x = NU(10, 1)
        result = x.scalar(-2)
        
        assert result.n == -20
        assert result.u == 2  # Absolute value
    
    def test_affine_transformation(self):
        """Test affine transformation (ax + b)."""
        x = NU(10, 1)
        result = x.affine(2, 5)
        
        assert result.n == 25  # 2*10 + 5
        assert result.u == 2   # |2|*1


class TestSpecialOperators:
    """Test Catch and Flip operators."""
    
    def test_catch_positive(self):
        """Test Catch operator with positive nominal."""
        x = NU(5, 2)
        caught = x.catch()
        
        assert caught.n == 0
        assert caught.u == 7  # |5| + 2
    
    def test_catch_negative(self):
        """Test Catch operator with negative nominal."""
        x = NU(-5, 2)
        caught = x.catch()
        
        assert caught.n == 0
        assert caught.u == 7  # |-5| + 2
    
    def test_flip_positive(self):
        """Test Flip operator with positive nominal."""
        x = NU(5, 2)
        flipped = x.flip()
        
        assert flipped.n == 2
        assert flipped.u == 5
    
    def test_flip_negative(self):
        """Test Flip operator with negative nominal."""
        x = NU(-5, 2)
        flipped = x.flip()
        
        assert flipped.n == 2
        assert flipped.u == 5  # |-5|
    
    def test_catch_invariant_preservation(self):
        """Test Catch preserves invariant M(n,u)."""
        x = NU(5, 2)
        caught = x.catch()
        
        assert abs(x.invariant() - caught.invariant()) < 1e-10
    
    def test_flip_invariant_preservation(self):
        """Test Flip preserves invariant M(n,u)."""
        x = NU(5, 2)
        flipped = x.flip()
        
        assert abs(x.invariant() - flipped.invariant()) < 1e-10


class TestProperties:
    """Test N/U properties and utility methods."""
    
    def test_invariant(self):
        """Test invariant calculation."""
        x = NU(5, 2)
        assert x.invariant() == 7
        
        y = NU(-5, 2)
        assert y.invariant() == 7
    
    def test_bounds(self):
        """Test lower and upper bounds."""
        x = NU(10, 2)
        
        assert x.lower_bound() == 8
        assert x.upper_bound() == 12
    
    def test_interval(self):
        """Test interval representation."""
        x = NU(10, 2)
        lower, upper = x.interval()
        
        assert lower == 8
        assert upper == 12
    
    def test_relative_uncertainty(self):
        """Test relative uncertainty calculation."""
        x = NU(10, 2)
        assert x.relative_uncertainty() == 0.2
        
        # Test with zero nominal
        zero = NU(0, 1)
        assert zero.relative_uncertainty() == float('inf')
    
    def test_sign_stability_stable(self):
        """Test sign stability for stable case."""
        stable = NU(10, 2)  # |10| > 2
        assert stable.is_sign_stable() is True
    
    def test_sign_stability_unstable(self):
        """Test sign stability for unstable case."""
        unstable = NU(3, 5)  # |3| < 5
        assert unstable.is_sign_stable() is False
    
    def test_sign_stability_boundary(self):
        """Test sign stability at boundary."""
        boundary = NU(5, 5)  # |5| = 5
        assert boundary.is_sign_stable() is False


class TestOperatorOverloading:
    """Test Python operator overloading."""
    
    def test_add_overload(self):
        """Test + operator."""
        a = NU(10, 1)
        b = NU(5, 0.5)
        result = a + b
        
        assert result.n == 15
        assert result.u == 1.5
    
    def test_sub_overload(self):
        """Test - operator."""
        a = NU(10, 1)
        b = NU(5, 0.5)
        result = a - b
        
        assert result.n == 5
        assert result.u == 1.5
    
    def test_mul_overload(self):
        """Test * operator."""
        a = NU(4, 0.1)
        b = NU(3, 0.2)
        result = a * b
        
        assert result.n == 12
        assert abs(result.u - 1.1) < 1e-10
    
    def test_scalar_add(self):
        """Test adding scalar to N/U."""
        a = NU(10, 1)
        result = a + 5
        
        assert result.n == 15
        assert result.u == 1
    
    def test_scalar_mul_left(self):
        """Test left scalar multiplication."""
        a = NU(10, 1)
        result = a * 2.5
        
        assert result.n == 25
        assert result.u == 2.5
    
    def test_scalar_mul_right(self):
        """Test right scalar multiplication."""
        a = NU(10, 1)
        result = 2.5 * a
        
        assert result.n == 25
        assert result.u == 2.5
    
    def test_negation(self):
        """Test unary negation."""
        a = NU(10, 1)
        result = -a
        
        assert result.n == -10
        assert result.u == 1


class TestCumulativeOperations:
    """Test cumulative sum and product functions."""
    
    def test_cumulative_sum(self):
        """Test cumulative sum of multiple pairs."""
        pairs = [NU(1, 0.1), NU(2, 0.2), NU(3, 0.3)]
        result = cumulative_sum(*pairs)
        
        assert result.n == 6
        assert abs(result.u - 0.6) < 1e-10
    
    def test_cumulative_product(self):
        """Test cumulative product of multiple pairs."""
        pairs = [NU(2, 0.1), NU(3, 0.1), NU(4, 0.1)]
        result = cumulative_product(*pairs)
        
        assert result.n == 24
        # Complex calculation - just verify it's positive
        assert result.u > 0
    
    def test_weighted_mean_equal_weights(self):
        """Test weighted mean with equal weights."""
        pairs = [NU(10, 1), NU(12, 1.5), NU(11, 0.8)]
        result = weighted_mean(pairs)
        
        # Equal weights: (10+12+11)/3 = 11
        assert abs(result.n - 11) < 1e-10
        # Uncertainties: (1+1.5+0.8)/3 = 1.1
        assert abs(result.u - 1.1) < 1e-10
    
    def test_weighted_mean_custom_weights(self):
        """Test weighted mean with custom weights."""
        pairs = [NU(10, 1), NU(20, 2)]
        weights = [1, 3]
        result = weighted_mean(pairs, weights)
        
        # Weighted: (1*10 + 3*20)/(1+3) = 70/4 = 17.5
        assert abs(result.n - 17.5) < 1e-10


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_zero_nominal(self):
        """Test operations with zero nominal."""
        x = NU(0, 1)
        y = NU(5, 0.5)
        
        result = x.add(y)
        assert result.n == 5
        
        result = x.mul(y)
        assert result.n == 0
    
    def test_zero_uncertainty(self):
        """Test operations with zero uncertainty."""
        x = NU(10, 0)
        y = NU(5, 0.5)
        
        result = x.add(y)
        assert result.u == 0.5
        
        result = x.mul(y)
        assert result.u == 5  # |10|*0.5 + |5|*0 = 5
    
    def test_negative_uncertainty_clamped(self):
        """Test that negative uncertainty is clamped to 0."""
        x = NU(10, -1)
        assert x.u == 0
    
    def test_large_values(self):
        """Test operations with large values."""
        x = NU(1e10, 1e8)
        y = NU(1e10, 1e8)
        
        result = x.add(y)
        assert result.n == 2e10
        assert result.u == 2e8
    
    def test_small_values(self):
        """Test operations with small values."""
        x = NU(1e-10, 1e-12)
        y = NU(1e-10, 1e-12)
        
        result = x.add(y)
        assert abs(result.n - 2e-10) < 1e-15
        assert abs(result.u - 2e-12) < 1e-15


class TestExamplesFromPaper:
    """Test worked examples from the validation paper."""
    
    def test_example_7_1_voltage_addition(self):
        """Example 7.1: Voltage Addition."""
        v1 = NU(2.00, 0.05)
        v2 = NU(1.20, 0.02)
        total = v1.add(v2)
        
        assert abs(total.n - 3.20) < 1e-10
        assert abs(total.u - 0.07) < 1e-10
    
    def test_example_7_2_area_calculation(self):
        """Example 7.2: Area Calculation."""
        length = NU(4.0, 0.1)
        width = NU(3.0, 0.2)
        area = length.mul(width)
        
        assert abs(area.n - 12.0) < 1e-10
        assert abs(area.u - 1.1) < 1e-10
    
    def test_example_7_3_large_product(self):
        """Example 7.3: Large Product."""
        x = NU(100, 10)
        y = NU(200, 5)
        product = x.mul(y)
        
        assert product.n == 20000
        assert product.u == 2500
    
    def test_example_7_6_work_calculation(self):
        """Example 7.6: Work Calculation."""
        force = NU(10.0, 0.2)
        distance = NU(2.0, 0.05)
        work = force.mul(distance)
        
        assert abs(work.n - 20.0) < 1e-10
        assert abs(work.u - 0.9) < 1e-10
    
    def test_example_7_7_squared_term(self):
        """Example 7.7: Squared Term."""
        p = NU(0.6, 0.02)
        p_squared = p.mul(p)
        
        assert abs(p_squared.n - 0.36) < 1e-10
        assert abs(p_squared.u - 0.024) < 1e-10


class TestAssociativity:
    """Test associativity property."""
    
    def test_addition_associativity(self):
        """Test (a + b) + c = a + (b + c)."""
        a = NU(1, 0.1)
        b = NU(2, 0.2)
        c = NU(3, 0.3)
        
        left = (a.add(b)).add(c)
        right = a.add(b.add(c))
        
        assert abs(left.n - right.n) < 1e-10
        assert abs(left.u - right.u) < 1e-10
    
    def test_multiplication_associativity(self):
        """Test (a * b) * c = a * (b * c)."""
        a = NU(2, 0.1)
        b = NU(3, 0.2)
        c = NU(4, 0.1)
        
        left = (a.mul(b)).mul(c)
        right = a.mul(b.mul(c))
        
        # Nominal should be exactly equal
        assert abs(left.n - right.n) < 1e-10
        # Uncertainty should be equal (within floating point error)
        assert abs(left.u - right.u) < 1e-6


class TestCommutativity:
    """Test commutativity property."""
    
    def test_addition_commutativity(self):
        """Test a + b = b + a."""
        a = NU(10, 1)
        b = NU(5, 0.5)
        
        left = a.add(b)
        right = b.add(a)
        
        assert left.n == right.n
        assert left.u == right.u
    
    def test_multiplication_commutativity(self):
        """Test a * b = b * a."""
        a = NU(4, 0.1)
        b = NU(3, 0.2)
        
        left = a.mul(b)
        right = b.mul(a)
        
        assert abs(left.n - right.n) < 1e-10
        assert abs(left.u - right.u) < 1e-10


class TestMonotonicity:
    """Test monotonicity in uncertainty."""
    
    def test_addition_monotonicity(self):
        """Test that larger u leads to larger result u."""
        base = NU(10, 1)
        small = NU(5, 0.5)
        large = NU(5, 1.0)
        
        result_small = base.add(small)
        result_large = base.add(large)
        
        assert result_large.u > result_small.u
    
    def test_multiplication_monotonicity(self):
        """Test that larger u leads to larger result u."""
        base = NU(10, 1)
        small = NU(5, 0.5)
        large = NU(5, 1.0)
        
        result_small = base.mul(small)
        result_large = base.mul(large)
        
        assert result_large.u > result_small.u


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
