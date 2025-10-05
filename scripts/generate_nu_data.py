"""
N/U Algebra Numerical Validation Dataset Generator

This script reproduces all validation experiments described in:
Martin, E.D. (2025). The NASA Paper & Small Falcon Algebra.

RNG Seed: 20250926
Tolerances: abs=1e-9, rel=1e-12

Generates:
- addition_sweep.csv
- product_sweep.csv
- interval_relation.csv
- interval_relation_with_rel.csv
- chain_experiment.csv
- mc_comparisons.csv
- invariants_grid.csv
- associativity_nominal_diffs.csv
- associativity_nominal_extended.csv
- summary.json
"""

import numpy as np
import pandas as pd
import json
from typing import Tuple
import time

# Set random seed for reproducibility
SEED = 20250926
np.random.seed(SEED)

# Tolerances
ABS_TOL = 1e-9
REL_TOL = 1e-12


class NU:
    """N/U Algebra implementation"""
    
    def __init__(self, n: float, u: float):
        self.n = n
        self.u = max(0, u)  # Ensure non-negative
    
    def __repr__(self):
        return f"NU({self.n}, {self.u})"
    
    def add(self, other: 'NU') -> 'NU':
        """Addition: (n1+n2, u1+u2)"""
        return NU(self.n + other.n, self.u + other.u)
    
    def mul(self, other: 'NU') -> 'NU':
        """Multiplication: (n1*n2, |n1|*u2 + |n2|*u1)"""
        return NU(
            self.n * other.n,
            abs(self.n) * other.u + abs(other.n) * self.u
        )
    
    def scalar(self, a: float) -> 'NU':
        """Scalar multiplication: (a*n, |a|*u)"""
        return NU(a * self.n, abs(a) * self.u)
    
    def catch(self) -> 'NU':
        """Catch operator: (0, |n|+u)"""
        return NU(0, abs(self.n) + self.u)
    
    def flip(self) -> 'NU':
        """Flip operator: (u, |n|)"""
        return NU(self.u, abs(self.n))
    
    def invariant(self) -> float:
        """M(n,u) = |n| + u"""
        return abs(self.n) + self.u


def gaussian_rss(*uncertainties) -> float:
    """Root-sum-square for Gaussian propagation"""
    return np.sqrt(sum(u**2 for u in uncertainties))


def gaussian_product(n1: float, u1: float, n2: float, u2: float) -> float:
    """First-order Gaussian uncertainty propagation for products"""
    return abs(n1 * n2) * np.sqrt((u1/n1)**2 + (u2/n2)**2) if n1 != 0 and n2 != 0 else 0


def interval_product_halfwidth(n1: float, u1: float, n2: float, u2: float) -> float:
    """Exact interval arithmetic half-width for products (n1,n2 >= 0)"""
    # Interval [n1-u1, n1+u1] × [n2-u2, n2+u2]
    corners = [
        (n1 - u1) * (n2 - u2),
        (n1 - u1) * (n2 + u2),
        (n1 + u1) * (n2 - u2),
        (n1 + u1) * (n2 + u2)
    ]
    return (max(corners) - min(corners)) / 2


def generate_addition_sweep(n_cases: int = 8000) -> pd.DataFrame:
    """Test N/U addition vs Gaussian RSS"""
    print("Generating addition sweep...")
    
    results = []
    for i in range(n_cases):
        # Random number of terms (2-50)
        k = np.random.randint(2, 51)
        
        # Generate random N/U pairs
        nominals = np.random.uniform(-100, 100, k)
        uncertainties = np.random.uniform(0.1, 10, k)
        
        # N/U addition
        nu_sum = NU(nominals[0], uncertainties[0])
        for j in range(1, k):
            nu_sum = nu_sum.add(NU(nominals[j], uncertainties[j]))
        
        # Gaussian RSS
        rss_u = gaussian_rss(*uncertainties)
        
        results.append({
            'k': k,
            'sum_u_nu': nu_sum.u,
            'rss_u': rss_u,
            'ratio_nu_over_rss': nu_sum.u / rss_u if rss_u > 0 else np.nan,
            'nu_minus_rss': nu_sum.u - rss_u
        })
    
    return pd.DataFrame(results)


def generate_product_sweep(n_cases: int = 30000) -> pd.DataFrame:
    """Test N/U multiplication vs first-order Gaussian"""
    print("Generating product sweep...")
    
    results = []
    for i in range(n_cases):
        # Generate random pairs
        n1 = np.random.uniform(-100, 100)
        u1 = np.random.uniform(0.1, 10)
        n2 = np.random.uniform(-100, 100)
        u2 = np.random.uniform(0.1, 10)
        
        # N/U multiplication
        nu_prod = NU(n1, u1).mul(NU(n2, u2))
        
        # Gaussian propagation
        gauss_u = gaussian_product(n1, u1, n2, u2)
        
        results.append({
            'n1': n1,
            'u1': u1,
            'n2': n2,
            'u2': u2,
            'u_nu': nu_prod.u,
            'u_gauss': gauss_u,
            'ratio_nu_over_gauss': nu_prod.u / gauss_u if gauss_u > 0 else np.nan,
            'diff_nu_minus_gauss': nu_prod.u - gauss_u
        })
    
    return pd.DataFrame(results)


def generate_interval_relation(n_cases: int = 30000) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Test N/U vs exact interval arithmetic for n1,n2 >= 0"""
    print("Generating interval relation tests...")
    
    results = []
    for i in range(n_cases):
        # Generate positive nominals
        n1 = np.random.uniform(0.1, 100)
        u1 = np.random.uniform(0.01, 10)
        n2 = np.random.uniform(0.1, 100)
        u2 = np.random.uniform(0.01, 10)
        
        # N/U multiplication
        nu_prod = NU(n1, u1).mul(NU(n2, u2))
        
        # Exact interval half-width
        interval_hw = interval_product_halfwidth(n1, u1, n2, u2)
        
        diff = nu_prod.u - interval_hw
        rel_error = abs(diff / interval_hw) if interval_hw > 0 else 0
        
        results.append({
            'n1': n1,
            'u1': u1,
            'n2': n2,
            'u2': u2,
            'u_nu': nu_prod.u,
            'interval_halfwidth': interval_hw,
            'nu_minus_interval': diff
        })
        
        results[-1]['rel_error'] = rel_error
    
    df = pd.DataFrame(results)
    df_basic = df[['n1', 'u1', 'n2', 'u2', 'u_nu', 'interval_halfwidth', 'nu_minus_interval']]
    
    return df_basic, df


def generate_chain_experiment(n_trials: int = 800, lengths: list = [3, 5, 10, 20]) -> pd.DataFrame:
    """Test stability in repeated multiplication"""
    print("Generating chain experiments...")
    
    results = []
    for length in lengths:
        for trial in range(n_trials):
            # Generate random N/U pairs
            pairs = [(np.random.uniform(0.5, 2.0), np.random.uniform(0.01, 0.2)) 
                     for _ in range(length)]
            
            # N/U cumulative product
            nu_prod = NU(pairs[0][0], pairs[0][1])
            for i in range(1, length):
                nu_prod = nu_prod.mul(NU(pairs[i][0], pairs[i][1]))
            
            # Interval cumulative product
            intervals = [(n - u, n + u) for n, u in pairs]
            int_min = intervals[0][0]
            int_max = intervals[0][1]
            for i in range(1, length):
                corners = [
                    int_min * intervals[i][0],
                    int_min * intervals[i][1],
                    int_max * intervals[i][0],
                    int_max * intervals[i][1]
                ]
                int_min = min(corners)
                int_max = max(corners)
            
            interval_hw = (int_max - int_min) / 2
            
            results.append({
                'L': length,
                'nu_u': nu_prod.u,
                'interval_half': interval_hw,
                'ratio_nu_over_interval': nu_prod.u / interval_hw if interval_hw > 0 else np.nan,
                'diff_nu_minus_interval': nu_prod.u - interval_hw
            })
    
    return pd.DataFrame(results)


def generate_mc_comparisons(n_samples: int = 30000) -> pd.DataFrame:
    """Compare N/U bounds to Monte Carlo empirical standard deviations"""
    print("Generating Monte Carlo comparisons...")
    
    distributions = {
        'gaussian': lambda loc, scale, size: np.random.normal(loc, scale, size),
        'uniform': lambda loc, scale, size: np.random.uniform(loc - scale*np.sqrt(3), loc + scale*np.sqrt(3), size),
        'laplace': lambda loc, scale, size: np.random.laplace(loc, scale/np.sqrt(2), size),
        'student_t': lambda loc, scale, size: loc + scale * np.random.standard_t(5, size)
    }
    
    results = []
    pair_id = 0
    
    for dist_name, sampler in distributions.items():
        for _ in range(6):  # 6 pairs per distribution
            # Generate N/U parameters
            a_n = np.random.uniform(-50, 50)
            a_u = np.random.uniform(1, 10)
            b_n = np.random.uniform(-50, 50)
            b_u = np.random.uniform(1, 10)
            
            # N/U product
            nu_prod = NU(a_n, a_u).mul(NU(b_n, b_u))
            
            # Monte Carlo samples
            a_samples = sampler(a_n, a_u, n_samples)
            b_samples = sampler(b_n, b_u, n_samples)
            mc_products = a_samples * b_samples
            mc_std = np.std(mc_products, ddof=1)
            
            results.append({
                'pair_id': pair_id,
                'a_n': a_n,
                'a_u': a_u,
                'b_n': b_n,
                'b_u': b_u,
                'dist': dist_name,
                'mc_std': mc_std,
                'u_nu': nu_prod.u,
                'margin_nu_minus_mc': nu_prod.u - mc_std
            })
            pair_id += 1
    
    return pd.DataFrame(results)


def generate_invariants_grid() -> pd.DataFrame:
    """Test invariant preservation for Catch and Flip operators"""
    print("Generating invariants grid...")
    
    results = []
    
    # Grid of test points
    n_vals = np.linspace(-10, 10, 9)
    u_vals = np.linspace(0, 10, 6)
    
    for n in n_vals:
        for u in u_vals:
            nu_orig = NU(n, u)
            M0 = nu_orig.invariant()
            
            # Test Catch
            nu_catch = nu_orig.catch()
            M_catch = nu_catch.invariant()
            
            # Test Flip
            nu_flip = nu_orig.flip()
            M_flip = nu_flip.invariant()
            
            max_error = max(abs(M0 - M_catch), abs(M0 - M_flip))
            
            results.append({
                'n': n,
                'u': u,
                'M0': M0,
                'M_catch': M_catch,
                'M_flip': M_flip,
                'max_abs_error': max_error
            })
    
    return pd.DataFrame(results)


def generate_associativity_tests(n_cases: int = 20000) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Test associativity of multiplication"""
    print("Generating associativity tests...")
    
    results = []
    
    for i in range(n_cases):
        # Generate three random N/U pairs
        a = NU(np.random.uniform(-100, 100), np.random.uniform(0.1, 10))
        b = NU(np.random.uniform(-100, 100), np.random.uniform(0.1, 10))
        c = NU(np.random.uniform(-100, 100), np.random.uniform(0.1, 10))
        
        # (a * b) * c
        ab = a.mul(b)
        ab_c = ab.mul(c)
        
        # a * (b * c)
        bc = b.mul(c)
        a_bc = a.mul(bc)
        
        # Differences
        nom_diff = ab_c.n - a_bc.n
        abs_diff = abs(nom_diff)
        rel_diff = abs_diff / abs(ab_c.n) if abs(ab_c.n) > 0 else 0
        
        results.append({
            'nominal_lhs': ab_c.n,
            'nominal_rhs': a_bc.n,
            'abs_diff': abs_diff
        })
        
        results[-1]['rel_diff'] = rel_diff
    
    df = pd.DataFrame(results)
    df_basic = df[['nominal_lhs', 'nominal_rhs', 'abs_diff']]
    
    return df_basic, df


def generate_summary(start_time: float, data_dict: dict) -> dict:
    """Generate summary.json with statistics"""
    print("Generating summary...")
    
    addition = data_dict['addition']
    product = data_dict['product']
    interval_rel = data_dict['interval_relation_with_rel']
    chain = data_dict['chain']
    mc = data_dict['mc']
    invariants = data_dict['invariants']
    assoc_ext = data_dict['associativity_extended']
    
    summary = {
        'runtime_sec': time.time() - start_time,
        'addition': {
            'rows': len(addition),
            'min_ratio': float(addition['ratio_nu_over_rss'].min()),
            'median_ratio': float(addition['ratio_nu_over_rss'].median()),
            'max_ratio': float(addition['ratio_nu_over_rss'].max()),
            'min_diff': float(addition['nu_minus_rss'].min()),
            'max_diff': float(addition['nu_minus_rss'].max())
        },
        'product': {
            'rows': len(product),
            'min_ratio': float(product['ratio_nu_over_gauss'].min()),
            'median_ratio': float(product['ratio_nu_over_gauss'].median()),
            'max_ratio': float(product['ratio_nu_over_gauss'].max()),
            'min_diff': float(product['diff_nu_minus_gauss'].min()),
            'max_diff': float(product['diff_nu_minus_gauss'].max())
        },
        'interval_relation': {
            'rows': len(interval_rel),
            'min_diff_nu_minus_interval': float(interval_rel['nu_minus_interval'].min()),
            'max_diff_nu_minus_interval': float(interval_rel['nu_minus_interval'].max()),
            'violations_beyond_tol': int((interval_rel['rel_error'] > REL_TOL).sum())
        },
        'chain': {
            'rows': len(chain),
            'ratio_stats_by_L': {},
            'max_diff': float(chain['diff_nu_minus_interval'].abs().max())
        },
        'monte_carlo': {
            'rows': len(mc),
            'min_margin': float(mc['margin_nu_minus_mc'].min()),
            'median_margin': float(mc['margin_nu_minus_mc'].median()),
            'max_margin': float(mc['margin_nu_minus_mc'].max()),
            'any_mc_exceeds_nu_with_tol': bool((mc['margin_nu_minus_mc'] < -ABS_TOL).any())
        },
        'invariants': {
            'rows': len(invariants),
            'max_abs_error': float(invariants['max_abs_error'].max())
        },
        'associativity_nominal': {
            'rows': len(assoc_ext),
            'max_abs_diff': float(assoc_ext['abs_diff'].max()),
            'median_abs_diff': float(assoc_ext['abs_diff'].median()),
            'violations_beyond_tol': int((assoc_ext['rel_diff'] > REL_TOL).sum())
        },
        'tolerances': {
            'abs': ABS_TOL,
            'rel': REL_TOL
        }
    }
    
    # Chain stats by length
    for L in [3, 5, 10, 20]:
        subset = chain[chain['L'] == L]
        summary['chain']['ratio_stats_by_L'][str(L)] = {
            'count': len(subset),
            'min_ratio': float(subset['ratio_nu_over_interval'].min()),
            'median_ratio': float(subset['ratio_nu_over_interval'].median()),
            'max_ratio': float(subset['ratio_nu_over_interval'].max())
        }
    
    return summary


def main():
    """Generate all validation datasets"""
    start_time = time.time()
    
    print("=" * 60)
    print("N/U Algebra Numerical Validation Dataset Generator")
    print("=" * 60)
    print(f"RNG Seed: {SEED}")
    print(f"Tolerances: abs={ABS_TOL}, rel={REL_TOL}")
    print()
    
    # Generate all datasets
    data = {}
    
    data['addition'] = generate_addition_sweep(8000)
    data['addition'].to_csv('addition_sweep.csv', index=False)
    print(f"✓ addition_sweep.csv ({len(data['addition'])} rows)\n")
    
    data['product'] = generate_product_sweep(30000)
    data['product'].to_csv('product_sweep.csv', index=False)
    print(f"✓ product_sweep.csv ({len(data['product'])} rows)\n")
    
    interval_basic, interval_with_rel = generate_interval_relation(30000)
    data['interval_relation'] = interval_basic
    data['interval_relation_with_rel'] = interval_with_rel
    interval_basic.to_csv('interval_relation.csv', index=False)
    interval_with_rel.to_csv('interval_relation_with_rel.csv', index=False)
    print(f"✓ interval_relation.csv ({len(interval_basic)} rows)")
    print(f"✓ interval_relation_with_rel.csv ({len(interval_with_rel)} rows)\n")
    
    data['chain'] = generate_chain_experiment(800, [3, 5, 10, 20])
    data['chain'].to_csv('chain_experiment.csv', index=False)
    print(f"✓ chain_experiment.csv ({len(data['chain'])} rows)\n")
    
    data['mc'] = generate_mc_comparisons(30000)
    data['mc'].to_csv('mc_comparisons.csv', index=False)
    print(f"✓ mc_comparisons.csv ({len(data['mc'])} rows)\n")
    
    data['invariants'] = generate_invariants_grid()
    data['invariants'].to_csv('invariants_grid.csv', index=False)
    print(f"✓ invariants_grid.csv ({len(data['invariants'])} rows)\n")
    
    assoc_basic, assoc_extended = generate_associativity_tests(20000)
    data['associativity'] = assoc_basic
    data['associativity_extended'] = assoc_extended
    assoc_basic.to_csv('associativity_nominal_diffs.csv', index=False)
    assoc_extended.to_csv('associativity_nominal_extended.csv', index=False)
    print(f"✓ associativity_nominal_diffs.csv ({len(assoc_basic)} rows)")
    print(f"✓ associativity_nominal_extended.csv ({len(assoc_extended)} rows)\n")
    
    # Generate summary
    summary = generate_summary(start_time, data)
    with open('summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"✓ summary.json\n")
    
    print("=" * 60)
    print(f"Total runtime: {summary['runtime_sec']:.2f} seconds")
    print("All datasets generated successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
