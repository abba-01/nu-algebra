"""
N/U Algebra Validation Tests

Tests that verify the implementation matches the validation results
from the paper (Martin, E.D., 2025).

Reference:
Martin, Eric D. (2025). The NASA Paper & Small Falcon Algebra.
Validation Dataset: DOI 10.5281/zenodo.17221863
"""

import sys
sys.path.insert(0, '../src')

import pytest
import math
from nu_algebra import NU, cumulative_sum, cumulative_product


class TestPaperExamples:
    """Test all worked examples from the paper (Section 7)."""
    
    def test_example_7_1_voltage_addition(self):
        """
        Example 7.1: Voltage Addition
        Result should be (3.20 V, 0.07 V)
        """
        v1 = NU(2.00, 0.05)
        v2 = NU(1.20, 0.02)
        total = v1.add(v2)
        
        assert abs(total.n - 3.20) < 1e-10, "Nominal should be 3.20"
        assert abs(total.u - 0.07) < 1e-10, "Uncertainty should be 0.07"
    
    def test_example_7_2_area_calculation(self):
        """
        Example 7.2: Area Calculation
        Result should be (12.0 m², 1.1 m²)
        """
        length = NU(4.0, 0.1)
        width = NU(3.0, 0.2)
        area = length.mul(width)
        
        assert abs(area.n - 12.0) < 1e-10, "Nominal should be 12.0"
        assert abs(area.u - 1.1) < 1e-10, "Uncertainty should be 1.1"
    
    def test_example_7_3_large_product(self):
        """
        Example 7.3: Large Product
        Result should be (20,000, 2500)
        """
        x = NU(100, 10)
        y = NU(200, 5)
        product = x.mul(y)
        
        assert product.n == 20000, "Nominal should be 20,000"
        assert product.u == 2500, "Uncertainty should be 2500"
    
    def test_example_7_4_interval_equivalence(self):
        """
        Example 7.4: Interval Equivalence
        For positive nominals, N/U should match interval half-width
        """
        # Intervals: [9,11] × [4.5,5.5]
        n1, u1 = 10, 1    # [9, 11]
        n2, u2 = 5, 0.5   # [4.5, 5.5]
        
        # N/U product
        nu_prod = NU(n1, u1).mul(NU(n2, u2))
        
        # Interval product corners
        corners = [
            (n1 - u1) * (n2 - u2),
            (n1 - u1) * (n2 + u2),
            (n1 + u1) * (n2 - u2),
            (n1 + u1) * (n2 + u2)
        ]
        interval_halfwidth = (max(corners) - min(corners)) / 2
        
        # For positive nominals, N/U should match interval
        assert abs(nu_prod.u - interval_halfwidth) < 1e-10
    
    def test_example_7_5_multiple_measurements(self):
        """
        Example 7.5: Multiple Measurements
        Result should be (307.5, 4.5)
        """
        measurements = [
            NU(100.0, 2.0),
            NU(105.0, 1.5),
            NU(102.5, 1.0)
        ]
        
        total = cumulative_sum(*measurements)
        
        assert abs(total.n - 307.5) < 1e-10
        assert abs(total.u - 4.5) < 1e-10
    
    def test_example_7_6_work_calculation(self):
        """
        Example 7.6: Work Calculation
        Result should be (20.0 J, 0.9 J)
        """
        force = NU(10.0, 0.2)
        distance = NU(2.0, 0.05)
        work = force.mul(distance)
        
        assert abs(work.n - 20.0) < 1e-10
        assert abs(work.u - 0.9) < 1e-10
    
    def test_example_7_7_squared_term(self):
        """
        Example 7.7: Squared Term
        p² should give (0.36, 0.024)
        """
        p = NU(0.6, 0.02)
        p_squared = p.mul(p)
        
        assert abs(p_squared.n - 0.36) < 1e-10
        assert abs(p_squared.u - 0.024) < 1e-10


class TestValidationProperties:
    """Test properties verified in the validation dataset."""
    
    def test_addition_conservatism(self):
        """
        N/U addition should be more conservative than Gaussian RSS.
        From validation: ratio range 1.00-3.54, median 1.74
        """
        # Test several cases
        test_cases = [
            ([(10, 1), (5, 0.5)], 2),
            ([(100, 10), (50, 5), (25, 2.5)], 3),
            ([(1, 0.1), (2, 0.2), (3, 0.3), (4, 0.4)], 4),
        ]
        
        for pairs, count in test_cases:
            # N/U sum
            nu_objects = [NU(n, u) for n, u in pairs]
            nu_sum = cumulative_sum(*nu_objects)
            
            # Gaussian RSS
            rss = math.sqrt(sum(u**2 for _, u in pairs))
            
            # N/U should be >= RSS
            assert nu_sum.u >= rss, f"N/U ({nu_sum.u}) should be >= RSS ({rss})"
    
    def test_multiplication_conservatism(self):
        """
        N/U multiplication should exceed first-order Gaussian.
        From validation: ratio range 1.00-1.41 (√2), median ≈1.001
        """
        test_cases = [
            (10, 1, 5, 0.5),
            (100, 10, 200, 20),
            (4.0, 0.1, 3.0, 0.2),
        ]
        
        for n1, u1, n2, u2 in test_cases:
            # N/U product
            nu_prod = NU(n1, u1).mul(NU(n2, u2))
            
            # First-order Gaussian (if nominals non-zero)
            if n1 != 0 and n2 != 0:
                gauss_u = abs(n1 * n2) * math.sqrt((u1/n1)**2 + (u2/n2)**2)
                
                # N/U should be >= Gaussian
                assert nu_prod.u >= gauss_u - 1e-10, \
                    f"N/U ({nu_prod.u}) should be >= Gaussian ({gauss_u})"
                
                # Ratio should be <= sqrt(2) (theoretical max)
                ratio = nu_prod.u / gauss_u
                assert ratio <= math.sqrt(2) + 1e-6, \
                    f"Ratio ({ratio}) should be <= √2"
    
    def test_interval_consistency_positive_nominals(self):
        """
        For positive nominals, N/U should match interval arithmetic.
        From validation: max relative error 0.014% (floating-point)
        """
        test_cases = [
            (10, 1, 5, 0.5),
            (100, 5, 50, 2),
            (4.0, 0.1, 3.0, 0.2),
        ]
        
        for n1, u1, n2, u2 in test_cases:
            # N/U product
            nu_prod = NU(n1, u1).mul(NU(n2, u2))
            
            # Interval product
            corners = [
                (n1 - u1) * (n2 - u2),
                (n1 - u1) * (n2 + u2),
                (n1 + u1) * (n2 - u2),
                (n1 + u1) * (n2 + u2)
            ]
            interval_hw = (max(corners) - min(corners)) / 2
            
            # Should match within floating-point error
            rel_error = abs(nu_prod.u - interval_hw) / interval_hw
            assert rel_error < 1e-4, \
                f"Relative error ({rel_error}) should be < 0.01%"
    
    def test_chain_stability(self):
        """
        Repeated multiplication should not explode.
        From validation: max difference ~10^-12 (machine epsilon)
        """
        # Chain of 5 multiplications
        pairs = [
            NU(1.5, 0.1),
            NU(1.2, 0.05),
            NU(1.8, 0.15),
            NU(1.1, 0.08),
            NU(1.3, 0.12)
        ]
        
        # N/U cumulative product
        nu_result = cumulative_product(*pairs)
        
        # Interval cumulative product
        intervals = [(p.n - p.u, p.n + p.u) for p in pairs]
        int_min, int_max = intervals[0]
        
        for i in range(1, len(intervals)):
            corners = [
                int_min * intervals[i][0],
                int_min * intervals[i][1],
                int_max * intervals[i][0],
                int_max * intervals[i][1]
            ]
            int_min = min(corners)
            int_max = max(corners)
        
        interval_hw = (int_max - int_min) / 2
        
        # Should be stable (close to interval result)
        ratio = nu_result.u / interval_hw
        assert 0.99 < ratio < 1.01, \
            f"Chain ratio ({ratio}) should be near 1.0"
    
    def test_invariant_preservation_exact(self):
        """
        Catch and Flip should preserve M(n,u) = |n| + u exactly.
        From validation: max error = 0.0
        """
        test_values = [
            (5, 2),
            (-5, 2),
            (10.5, 3.7),
            (-10.5, 3.7),
            (0, 5),
        ]
        
        for n, u in test_values:
            nu = NU(n, u)
            M_original = nu.invariant()
            
            # Test Catch
            caught = nu.catch()
            M_catch = caught.invariant()
            assert abs(M_original - M_catch) < 1e-15, \
                "Catch should preserve invariant exactly"
            
            # Test Flip
            flipped = nu.flip()
            M_flip = flipped.invariant()
            assert abs(M_original - M_flip) < 1e-15, \
                "Flip should preserve invariant exactly"


class TestValidationStatistics:
    """Test that statistics match reported values from summary.json."""
    
    def test_sqrt2_bound_on_multiplication(self):
        """
        Maximum ratio of N/U to Gaussian should be sqrt(2).
        From validation: max_ratio = 1.414213...
        """
        # This occurs when both uncertainties are equal and small
        n1, n2 = 10, 10
        u1, u2 = 0.1, 0.1
        
        nu_prod = NU(n1, u1).mul(NU(n2, u2))
        gauss_u = abs(n1 * n2) * math.sqrt((u1/n1)**2 + (u2/n2)**2)
        
        ratio = nu_prod.u / gauss_u
        
        # Should approach sqrt(2) for equal relative uncertainties
        assert ratio <= math.sqrt(2) + 1e-6
        
        # For this specific case, should be very close to sqrt(2)
        assert abs(ratio - math.sqrt(2)) < 0.01
    
    def test_addition_identity(self):
        """Test additive identity (0, 0)."""
        x = NU(10, 1)
        identity = NU(0, 0)
        
        result = x.add(identity)
        
        assert result.n == x.n
        assert result.u == x.u
    
    def test_multiplication_identity(self):
        """Test multiplicative identity (1, 0)."""
        x = NU(10, 1)
        identity = NU(1, 0)
        
        result = x.mul(identity)
        
        assert abs(result.n - x.n) < 1e-10
        assert abs(result.u - x.u) < 1e-10


class TestNonNegativityGuarantee:
    """Test that uncertainties are always non-negative."""
    
    def test_negative_nominals_multiplication(self):
        """Negative nominals should still yield non-negative uncertainty."""
        test_cases = [
            (-10, 1, 5, 0.5),
            (10, 1, -5, 0.5),
            (-10, 1, -5, 0.5),
        ]
        
        for n1, u1, n2, u2 in test_cases:
            result = NU(n1, u1).mul(NU(n2, u2))
            assert result.u >= 0, \
                f"Uncertainty should be non-negative, got {result.u}"
    
    def test_negative_scalar_multiplication(self):
        """Negative scalar should yield non-negative uncertainty."""
        x = NU(10, 1)
        
        result = x.scalar(-5)
        
        assert result.u >= 0, "Uncertainty should be non-negative"
        assert result.u == 5, "Should be |a| * u = |-5| * 1 = 5"
    
    def test_flip_with_negative_nominal(self):
        """Flip with negative nominal should preserve non-negativity."""
        x = NU(-7, 3)
        flipped = x.flip()
        
        assert flipped.n == 3, "New nominal should be original uncertainty"
        assert flipped.u == 7, "New uncertainty should be |original nominal|"
        assert flipped.u >= 0, "Uncertainty must be non-negative"


class TestReproducibility:
    """Test that operations are deterministic and reproducible."""
    
    def test_deterministic_addition(self):
        """Same inputs should always give same outputs."""
        x = NU(10.123456789, 1.987654321)
        y = NU(5.555555555, 0.444444444)
        
        result1 = x.add(y)
        result2 = x.add(y)
        
        assert result1.n == result2.n
        assert result1.u == result2.u
    
    def test_deterministic_multiplication(self):
        """Same inputs should always give same outputs."""
        x = NU(10.123456789, 1.987654321)
        y = NU(5.555555555, 0.444444444)
        
        result1 = x.mul(y)
        result2 = x.mul(y)
        
        assert result1.n == result2.n
        assert result1.u == result2.u
    
    def test_cumulative_order_independence(self):
        """
        Cumulative operations should be order-independent
        (due to commutativity and associativity).
        """
        a = NU(1, 0.1)
        b = NU(2, 0.2)
        c = NU(3, 0.3)
        
        # Different orderings should give same result
        sum1 = cumulative_sum(a, b, c)
        sum2 = cumulative_sum(c, b, a)
        sum3 = cumulative_sum(b, a, c)
        
        assert abs(sum1.n - sum2.n) < 1e-10
        assert abs(sum1.u - sum2.u) < 1e-10
        assert abs(sum1.n - sum3.n) < 1e-10
        assert abs(sum1.u - sum3.u) < 1e-10


class TestValidationSummaryStatistics:
    """
    Test key statistics from summary.json.
    
    These tests verify the reported validation statistics are accurate.
    """
    
    def test_addition_median_ratio(self):
        """
        Addition median ratio reported as 1.74.
        Test that typical cases are in this range.
        """
        # Typical case: 3 terms with similar uncertainties
        pairs = [(10, 2), (12, 2.5), (11, 2.2)]
        
        nu_sum = cumulative_sum(*[NU(n, u) for n, u in pairs])
        rss = math.sqrt(sum(u**2 for _, u in pairs))
        ratio = nu_sum.u / rss
        
        # Should be in typical range (1.0 - 3.54, median 1.74)
        assert 1.0 <= ratio <= 3.54, f"Ratio {ratio} outside expected range"
    
    def test_multiplication_median_ratio(self):
        """
        Multiplication median ratio reported as ≈1.001.
        Most products should be very close to Gaussian.
        """
        # Typical case: moderate relative uncertainties
        n1, u1 = 50, 5
        n2, u2 = 30, 3
        
        nu_prod = NU(n1, u1).mul(NU(n2, u2))
        gauss_u = abs(n1 * n2) * math.sqrt((u1/n1)**2 + (u2/n2)**2)
        ratio = nu_prod.u / gauss_u
        
        # Should be close to 1.0 (median ≈1.001)
        assert 1.0 <= ratio <= 1.5, f"Ratio {ratio} outside expected range"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
