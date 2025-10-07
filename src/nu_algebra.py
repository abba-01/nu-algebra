"""
N/U Algebra: Conservative Uncertainty Propagation

This module implements the N/U (Nominal/Uncertainty) Algebra framework
for propagating explicit uncertainty bounds alongside nominal values.

Reference:
Martin, Eric D. (2025). The NASA Paper & Small Falcon Algebra.
DOI: 10.5281/zenodo.17172694
"""

from typing import Union
import math


class NU:
    """
    N/U Algebra: Ordered pair (n, u) where n is nominal and u ≥ 0 is uncertainty.
    
    Attributes:
        n (float): Nominal (central) value
        u (float): Uncertainty bound (always non-negative)
    
    Examples:
        >>> voltage = NU(2.00, 0.05)  # 2.00 V ± 0.05 V
        >>> current = NU(1.20, 0.02)  # 1.20 A ± 0.02 A
        >>> total = voltage.add(current)
        >>> print(total)
        NU(3.20, 0.07)
    """
    
    def __init__(self, n: float, u: float):
        """
        Initialize an N/U pair.
        
        Args:
            n: Nominal value (any real number)
            u: Uncertainty bound (will be clamped to ≥ 0)
        """
        self.n = float(n)
        self.u = max(0.0, float(u))  # Ensure non-negative
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"NU({self.n}, {self.u})"
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"({self.n}, {self.u})"
    
    def __eq__(self, other: 'NU') -> bool:
        """Equality comparison (exact match)."""
        if not isinstance(other, NU):
            return False
        return self.n == other.n and self.u == other.u
    
    # ==================== Primary Operations ====================
    
    def add(self, other: 'NU') -> 'NU':
        """
        Addition operator: (n₁, u₁) ⊕ (n₂, u₂) = (n₁+n₂, u₁+u₂)
        
        Args:
            other: Another N/U pair
        
        Returns:
            New N/U pair with summed nominal and uncertainty
        
        Example:
            >>> NU(10, 1).add(NU(5, 0.5))
            NU(15, 1.5)
        """
        return NU(self.n + other.n, self.u + other.u)
    
    def sub(self, other: 'NU') -> 'NU':
        """
        Subtraction: (n₁, u₁) - (n₂, u₂) = (n₁-n₂, u₁+u₂)
        
        Note: Uncertainty adds because we don't know the correlation.
        
        Example:
            >>> NU(10, 1).sub(NU(5, 0.5))
            NU(5, 1.5)
        """
        return NU(self.n - other.n, self.u + other.u)
    
    def mul(self, other: 'NU') -> 'NU':
        """
        Multiplication: (n₁, u₁) ⊗ (n₂, u₂) = (n₁n₂, |n₁|u₂ + |n₂|u₁)
        
        The absolute values ensure uncertainty remains non-negative
        for all input combinations.
        
        Args:
            other: Another N/U pair
        
        Returns:
            New N/U pair with product nominal and propagated uncertainty
        
        Example:
            >>> NU(4.0, 0.1).mul(NU(3.0, 0.2))
            NU(12.0, 1.1)
        """
        return NU(
            self.n * other.n,
            abs(self.n) * other.u + abs(other.n) * self.u
        )
    
    def scalar(self, a: float) -> 'NU':
        """
        Scalar multiplication: a ⊙ (n, u) = (an, |a|u)
        
        Args:
            a: Scalar multiplier
        
        Returns:
            New N/U pair scaled by a
        
        Example:
            >>> NU(10, 1).scalar(2.5)
            NU(25.0, 2.5)
        """
        return NU(a * self.n, abs(a) * self.u)
    
    def affine(self, a: float, b: float = 0.0) -> 'NU':
        """
        Affine transformation: a ⊙ (n, u) + b = (an+b, |a|u)
        
        Args:
            a: Scale factor
            b: Offset (default 0)
        
        Returns:
            Transformed N/U pair
        
        Example:
            >>> NU(10, 1).affine(2, 5)  # 2x + 5
            NU(25, 2)
        """
        return NU(a * self.n + b, abs(a) * self.u)
    
    # ==================== Special Operators ====================
    
    def catch(self) -> 'NU':
        """
        Catch operator: C(n, u) = (0, |n|+u)
        
        Collapses nominal into uncertainty, preserving the invariant M(n,u).
        Useful when magnitude is known but sign is uncertain.
        
        Returns:
            N/U pair with zero nominal and total magnitude as uncertainty
        
        Example:
            >>> NU(5, 2).catch()
            NU(0, 7)
        """
        return NU(0, abs(self.n) + self.u)
    
    def flip(self) -> 'NU':
        """
        Flip operator: B(n, u) = (u, |n|)
        
        Swaps nominal and uncertainty while preserving the invariant M(n,u).
        The absolute value ensures the new uncertainty is non-negative.
        
        Returns:
            N/U pair with swapped and adjusted components
        
        Example:
            >>> NU(5, 2).flip()
            NU(2, 5)
        """
        return NU(self.u, abs(self.n))
    
    # ==================== Properties ====================
    
    def invariant(self) -> float:
        """
        Uncertainty invariant: M(n, u) = |n| + u
        
        This quantity is preserved by Catch and Flip operators.
        
        Returns:
            The invariant value
        
        Example:
            >>> nu = NU(5, 2)
            >>> nu.invariant()
            7.0
            >>> nu.catch().invariant()
            7.0
        """
        return abs(self.n) + self.u
    
    def lower_bound(self) -> float:
        """Conservative lower bound: n - u"""
        return self.n - self.u
    
    def upper_bound(self) -> float:
        """Conservative upper bound: n + u"""
        return self.n + self.u
    
    def interval(self) -> tuple:
        """
        Return the interval representation [n-u, n+u]
        
        Returns:
            Tuple (lower, upper)
        """
        return (self.lower_bound(), self.upper_bound())
    
    def relative_uncertainty(self) -> float:
        """
        Relative uncertainty: u / |n|
        
        Returns:
            Relative uncertainty (inf if n=0)
        """
        if self.n == 0:
            return float('inf')
        return self.u / abs(self.n)
    
    def is_sign_stable(self) -> bool:
        """
        Check if sign is stable (|n| > u)
        
        Returns:
            True if the interval [n-u, n+u] doesn't contain zero
        """
        return abs(self.n) > self.u
    
    # ==================== Convenience Methods ====================
    
    def __add__(self, other: Union['NU', float]) -> 'NU':
        """Operator overload: nu1 + nu2 or nu + scalar"""
        if isinstance(other, NU):
            return self.add(other)
        return self.affine(1, other)
    
    def __sub__(self, other: Union['NU', float]) -> 'NU':
        """Operator overload: nu1 - nu2 or nu - scalar"""
        if isinstance(other, NU):
            return self.sub(other)
        return self.affine(1, -other)
    
    def __mul__(self, other: Union['NU', float]) -> 'NU':
        """Operator overload: nu1 * nu2 or nu * scalar"""
        if isinstance(other, NU):
            return self.mul(other)
        return self.scalar(other)
    
    def __rmul__(self, other: float) -> 'NU':
        """Right multiplication: scalar * nu"""
        return self.scalar(other)
    
    def __neg__(self) -> 'NU':
        """Negation: -nu"""
        return self.scalar(-1)
    
    def __abs__(self) -> 'NU':
        """Absolute value with uncertainty propagation"""
        return NU(abs(self.n), self.u)
    
    def pow(self, exponent: int) -> 'NU':
        """
        Integer power via repeated multiplication.
        
        Args:
            exponent: Integer exponent (must be >= 1)
        
        Returns:
            N/U pair raised to the power
        
        Example:
            >>> NU(3, 0.1).pow(2)
            NU(9, 0.6)
        """
        if exponent < 1:
            raise ValueError("Only positive integer exponents supported")
        
        result = self
        for _ in range(exponent - 1):
            result = result.mul(self)
        return result


# ==================== Module-Level Functions ====================

def cumulative_sum(*nu_pairs: NU) -> NU:
    """
    Sum multiple N/U pairs: ⊕(x₁, x₂, ..., xₙ)
    
    Args:
        *nu_pairs: Variable number of N/U pairs
    
    Returns:
        Cumulative sum
    
    Example:
        >>> cumulative_sum(NU(1, 0.1), NU(2, 0.2), NU(3, 0.3))
        NU(6, 0.6)
    """
    if not nu_pairs:
        return NU(0, 0)
    
    result = nu_pairs[0]
    for nu in nu_pairs[1:]:
        result = result.add(nu)
    return result


def cumulative_product(*nu_pairs: NU) -> NU:
    """
    Product of multiple N/U pairs: ⊗(x₁, x₂, ..., xₙ)
    
    Args:
        *nu_pairs: Variable number of N/U pairs
    
    Returns:
        Cumulative product
    
    Example:
        >>> cumulative_product(NU(2, 0.1), NU(3, 0.2), NU(4, 0.1))
        NU(24, 5.2)
    """
    if not nu_pairs:
        return NU(1, 0)
    
    result = nu_pairs[0]
    for nu in nu_pairs[1:]:
        result = result.mul(nu)
    return result


def weighted_mean(nu_pairs: list, weights: list = None) -> NU:
    """
    Weighted mean of N/U pairs.
    
    Args:
        nu_pairs: List of N/U pairs
        weights: Optional list of weights (default: equal weights)
    
    Returns:
        Weighted mean as N/U pair
    
    Example:
        >>> data = [NU(10, 1), NU(12, 1.5), NU(11, 0.8)]
        >>> weighted_mean(data)
        NU(11.0, 1.1)
    """
    if not nu_pairs:
        raise ValueError("Cannot compute mean of empty list")
    
    if weights is None:
        weights = [1.0] * len(nu_pairs)
    
    if len(weights) != len(nu_pairs):
        raise ValueError("Weights must match number of N/U pairs")
    
    total_weight = sum(weights)
    if total_weight == 0:
        raise ValueError("Total weight cannot be zero")
    
    # Weighted sum
    weighted_sum = cumulative_sum(*[
        nu.scalar(w) for nu, w in zip(nu_pairs, weights)
    ])
    
    # Normalize by total weight
    return weighted_sum.scalar(1.0 / total_weight)


# ==================== Compatibility Aliases ====================

def NU_add(x: NU, y: NU) -> NU:
    """Functional interface for addition"""
    return x.add(y)


def NU_mul(x: NU, y: NU) -> NU:
    """Functional interface for multiplication"""
    return x.mul(y)


def NU_scalar(a: float, x: NU) -> NU:
    """Functional interface for scalar multiplication"""
    return x.scalar(a)


# ==================== Version Info ====================

__version__ = "3.1.0"
__author__ = "Eric D. Martin"
__license__ = "CC BY 4.0"
