"""
Engineering Applications of N/U Algebra

This script demonstrates N/U Algebra in structural and mechanical engineering
contexts, including stress analysis, safety factors, and load calculations.

Reference:
Martin, Eric D. (2025). The NASA Paper & Small Falcon Algebra.
"""

import sys
sys.path.insert(0, '../src')
from nu_algebra import NU, cumulative_sum, cumulative_product
import math


def print_header(title):
    """Print section header."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def example_1_beam_stress():
    """
    Example 1: Simply Supported Beam - Maximum Bending Stress
    
    Calculate maximum stress in a simply supported beam with point load.
    Formula: σ = (M * c) / I
    where M = (P * L) / 4 (maximum moment at center)
          c = beam depth / 2
          I = moment of inertia
    """
    print_header("Example 1: Beam Stress Analysis")
    
    # Input parameters with uncertainties
    load = NU(5000, 50)          # 5000 N ± 50 N (point load)
    length = NU(2.0, 0.01)       # 2.0 m ± 0.01 m (beam length)
    depth = NU(0.15, 0.001)      # 0.15 m ± 0.001 m (beam depth)
    width = NU(0.10, 0.001)      # 0.10 m ± 0.001 m (beam width)
    
    print(f"Applied Load: {load} N")
    print(f"Beam Length: {length} m")
    print(f"Beam Depth: {depth} m")
    print(f"Beam Width: {width} m")
    
    # Calculate maximum moment: M = PL/4
    moment = load.mul(length).scalar(0.25)
    print(f"\nMaximum Moment: {moment} N·m")
    
    # Calculate section modulus: S = (b*h²)/6
    depth_squared = depth.mul(depth)
    section_modulus = width.mul(depth_squared).scalar(1/6)
    print(f"Section Modulus: {section_modulus} m³")
    
    # Calculate stress: σ = M/S
    # Using σ = M * (1/S) to avoid division
    S_inv = NU(1/section_modulus.n, section_modulus.u / (section_modulus.n**2))
    stress = moment.mul(S_inv)
    
    print(f"\nMaximum Bending Stress: {stress} Pa")
    print(f"Stress Range: [{stress.lower_bound():.0f}, {stress.upper_bound():.0f}] Pa")
    print(f"Relative Uncertainty: {stress.relative_uncertainty():.2%}")
    
    # Safety check against yield strength
    yield_strength = 250e6  # 250 MPa for mild steel
    safety_margin = yield_strength - stress.upper_bound()
    
    print(f"\nYield Strength: {yield_strength:.2e} Pa")
    print(f"Safety Margin (conservative): {safety_margin:.2e} Pa")
    print(f"Safe Design: {safety_margin > 0}")


def example_2_column_buckling():
    """
    Example 2: Column Critical Buckling Load (Euler's Formula)
    
    Calculate critical buckling load for a column.
    Formula: P_cr = (π² * E * I) / (K * L)²
    where E = Young's modulus
          I = moment of inertia
          K = effective length factor
          L = column length
    """
    print_header("Example 2: Column Buckling Analysis")
    
    # Input parameters
    E = NU(200e9, 10e9)          # 200 GPa ± 10 GPa (steel modulus)
    diameter = NU(0.050, 0.001)  # 50 mm ± 1 mm (column diameter)
    length = NU(3.0, 0.02)       # 3.0 m ± 0.02 m (column length)
    K = NU(1.0, 0.05)            # Effective length factor (pinned-pinned)
    
    print(f"Young's Modulus: {E} Pa")
    print(f"Column Diameter: {diameter} m")
    print(f"Column Length: {length} m")
    print(f"Effective Length Factor: {K}")
    
    # Calculate moment of inertia: I = π*d⁴/64
    d_4th = diameter.pow(2).pow(2)  # d⁴ = (d²)²
    I = d_4th.scalar(math.pi / 64)
    print(f"\nMoment of Inertia: {I} m⁴")
    
    # Calculate effective length: L_eff = K * L
    L_eff = K.mul(length)
    L_eff_sq = L_eff.mul(L_eff)
    print(f"Effective Length²: {L_eff_sq} m²")
    
    # Calculate numerator: π² * E * I
    numerator = E.mul(I).scalar(math.pi**2)
    
    # Calculate critical load: P_cr = numerator / L_eff²
    # Using P_cr = numerator * (1/L_eff²)
    L_eff_sq_inv = NU(1/L_eff_sq.n, L_eff_sq.u / (L_eff_sq.n**2))
    P_critical = numerator.mul(L_eff_sq_inv)
    
    print(f"\nCritical Buckling Load: {P_critical} N")
    print(f"Conservative Lower Bound: {P_critical.lower_bound():.0f} N")
    print(f"Relative Uncertainty: {P_critical.relative_uncertainty():.2%}")
    
    # Design recommendation
    applied_load = 5000  # N
    safety_factor_nominal = P_critical.n / applied_load
    safety_factor_conservative = P_critical.lower_bound() / applied_load
    
    print(f"\nApplied Load: {applied_load} N")
    print(f"Safety Factor (nominal): {safety_factor_nominal:.2f}")
    print(f"Safety Factor (conservative): {safety_factor_conservative:.2f}")
    print(f"Meets SF > 2 requirement: {safety_factor_conservative > 2}")


def example_3_thermal_stress():
    """
    Example 3: Thermal Stress in Constrained Bar
    
    Calculate thermal stress in a bar constrained at both ends.
    Formula: σ = E * α * ΔT
    where E = Young's modulus
          α = coefficient of thermal expansion
          ΔT = temperature change
    """
    print_header("Example 3: Thermal Stress Analysis")
    
    # Material properties (steel)
    E = NU(200e9, 5e9)              # 200 GPa ± 5 GPa
    alpha = NU(12e-6, 0.5e-6)       # 12e-6 /°C ± 0.5e-6 /°C
    temp_change = NU(50, 2)         # 50°C ± 2°C increase
    
    print(f"Young's Modulus: {E} Pa")
    print(f"Thermal Expansion Coeff: {alpha} /°C")
    print(f"Temperature Change: {temp_change} °C")
    
    # Calculate thermal stress: σ = E * α * ΔT
    thermal_strain = alpha.mul(temp_change)
    thermal_stress = E.mul(thermal_strain)
    
    print(f"\nThermal Strain: {thermal_strain}")
    print(f"Thermal Stress: {thermal_stress} Pa")
    print(f"Stress Range: [{thermal_stress.lower_bound():.2e}, "
          f"{thermal_stress.upper_bound():.2e}] Pa")
    
    # Convert to MPa for readability
    stress_mpa = thermal_stress.scalar(1e-6)
    print(f"\nThermal Stress: ({stress_mpa.n:.2f} MPa, {stress_mpa.u:.2f} MPa)")
    
    # Check against yield
    yield_strength = 250  # MPa
    is_safe = stress_mpa.upper_bound() < yield_strength
    
    print(f"\nYield Strength: {yield_strength} MPa")
    print(f"Safe (conservative check): {is_safe}")


def example_4_composite_loading():
    """
    Example 4: Combined Axial and Bending Stress
    
    Calculate combined stress in a beam under both axial load and bending.
    Formula: σ_total = σ_axial + σ_bending
    where σ_axial = P/A
          σ_bending = M*c/I
    """
    print_header("Example 4: Combined Loading Analysis")
    
    # Axial load
    axial_force = NU(10000, 100)     # 10 kN ± 100 N
    area = NU(0.01, 0.0001)          # 100 cm² ± 1 cm²
    
    # Bending moment
    moment = NU(500, 10)             # 500 N·m ± 10 N·m
    section_modulus = NU(5e-5, 1e-6) # 50 cm³ ± 1 cm³
    
    print(f"Axial Force: {axial_force} N")
    print(f"Cross-sectional Area: {area} m²")
    print(f"Bending Moment: {moment} N·m")
    print(f"Section Modulus: {section_modulus} m³")
    
    # Calculate axial stress: σ_a = P/A
    area_inv = NU(1/area.n, area.u / (area.n**2))
    axial_stress = axial_force.mul(area_inv)
    print(f"\nAxial Stress: {axial_stress} Pa")
    
    # Calculate bending stress: σ_b = M/S
    S_inv = NU(1/section_modulus.n, section_modulus.u / (section_modulus.n**2))
    bending_stress = moment.mul(S_inv)
    print(f"Bending Stress: {bending_stress} Pa")
    
    # Combined stress (worst case: both tensile on same side)
    total_stress = axial_stress.add(bending_stress)
    print(f"\nTotal Combined Stress: {total_stress} Pa")
    print(f"Conservative Upper Bound: {total_stress.upper_bound():.2e} Pa")
    print(f"Relative Uncertainty: {total_stress.relative_uncertainty():.2%}")
    
    # Von Mises equivalent stress (simplified for uniaxial)
    print(f"\nSign Stability Check: {total_stress.is_sign_stable()}")
    if total_stress.is_sign_stable():
        print("Stress direction is well-defined (no sign uncertainty)")


def example_5_pressure_vessel():
    """
    Example 5: Thin-Walled Pressure Vessel
    
    Calculate hoop stress in a cylindrical pressure vessel.
    Formula: σ_hoop = (P * r) / t
    where P = internal pressure
          r = vessel radius
          t = wall thickness
    """
    print_header("Example 5: Pressure Vessel Analysis")
    
    # Input parameters
    pressure = NU(2e6, 0.1e6)        # 2 MPa ± 0.1 MPa (internal pressure)
    radius = NU(0.5, 0.005)          # 0.5 m ± 5 mm (inner radius)
    thickness = NU(0.010, 0.0005)    # 10 mm ± 0.5 mm (wall thickness)
    
    print(f"Internal Pressure: {pressure} Pa")
    print(f"Vessel Radius: {radius} m")
    print(f"Wall Thickness: {thickness} m")
    
    # Check thin-wall assumption: r/t > 10
    ratio = radius.n / thickness.n
    print(f"\nRadius/Thickness ratio: {ratio:.1f}")
    print(f"Thin-wall assumption valid: {ratio > 10}")
    
    # Calculate hoop stress: σ = (P * r) / t
    numerator = pressure.mul(radius)
    t_inv = NU(1/thickness.n, thickness.u / (thickness.n**2))
    hoop_stress = numerator.mul(t_inv)
    
    print(f"\nHoop Stress: {hoop_stress} Pa")
    stress_mpa = hoop_stress.scalar(1e-6)
    print(f"Hoop Stress: ({stress_mpa.n:.1f} MPa, {stress_mpa.u:.1f} MPa)")
    print(f"Conservative Upper Bound: {stress_mpa.upper_bound():.1f} MPa")
    
    # Design check
    allowable_stress = 150  # MPa
    is_safe = stress_mpa.upper_bound() < allowable_stress
    
    print(f"\nAllowable Stress: {allowable_stress} MPa")
    print(f"Safe Design (conservative): {is_safe}")
    
    # Required safety factor
    if is_safe:
        safety_factor = allowable_stress / stress_mpa.upper_bound()
        print(f"Actual Safety Factor: {safety_factor:.2f}")


def example_6_cantilever_deflection():
    """
    Example 6: Cantilever Beam Deflection
    
    Calculate maximum deflection of a cantilever beam.
    Formula: δ = (P * L³) / (3 * E * I)
    where P = point load at free end
          L = beam length
          E = Young's modulus
          I = moment of inertia
    """
    print_header("Example 6: Cantilever Deflection Analysis")
    
    # Input parameters
    load = NU(1000, 20)              # 1000 N ± 20 N
    length = NU(1.5, 0.01)           # 1.5 m ± 10 mm
    E = NU(70e9, 3e9)                # 70 GPa ± 3 GPa (aluminum)
    I = NU(1e-6, 5e-8)               # Moment of inertia
    
    print(f"Point Load: {load} N")
    print(f"Cantilever Length: {length} m")
    print(f"Young's Modulus: {E} Pa")
    print(f"Moment of Inertia: {I} m⁴")
    
    # Calculate L³
    L_cubed = length.mul(length).mul(length)
    print(f"\nLength³: {L_cubed} m³")
    
    # Calculate numerator: P * L³
    numerator = load.mul(L_cubed)
    
    # Calculate denominator: 3 * E * I
    denominator = E.mul(I).scalar(3)
    
    # Calculate deflection: δ = numerator / denominator
    denom_inv = NU(1/denominator.n, denominator.u / (denominator.n**2))
    deflection = numerator.mul(denom_inv)
    
    print(f"\nMaximum Deflection: {deflection} m")
    deflection_mm = deflection.scalar(1000)
    print(f"Deflection: ({deflection_mm.n:.2f} mm, {deflection_mm.u:.2f} mm)")
    print(f"Conservative Upper Bound: {deflection_mm.upper_bound():.2f} mm")
    
    # Check against deflection limit (L/360 for general structures)
    deflection_limit = (length.n * 1000) / 360  # mm
    is_acceptable = deflection_mm.upper_bound() < deflection_limit
    
    print(f"\nDeflection Limit (L/360): {deflection_limit:.2f} mm")
    print(f"Meets Deflection Criteria: {is_acceptable}")


def example_7_factor_of_safety():
    """
    Example 7: Comprehensive Safety Factor Analysis
    
    Demonstrate proper use of safety factors with N/U bounds.
    Shows the difference between nominal and conservative approaches.
    """
    print_header("Example 7: Safety Factor with Uncertainty")
    
    # Component strength (from testing)
    ultimate_strength = NU(400e6, 20e6)  # 400 MPa ± 20 MPa
    
    # Applied stress (from analysis)
    applied_stress = NU(150e6, 15e6)     # 150 MPa ± 15 MPa
    
    print(f"Ultimate Strength: {ultimate_strength} Pa")
    print(f"Applied Stress: {applied_stress} Pa")
    
    # Nominal safety factor (traditional approach)
    SF_nominal = ultimate_strength.n / applied_stress.n
    print(f"\nNominal Safety Factor: {SF_nominal:.2f}")
    
    # Conservative safety factor (N/U approach)
    # Use worst case: lowest strength / highest stress
    SF_conservative = ultimate_strength.lower_bound() / applied_stress.upper_bound()
    print(f"Conservative Safety Factor: {SF_conservative:.2f}")
    
    # The difference
    SF_reduction = ((SF_nominal - SF_conservative) / SF_nominal) * 100
    print(f"\nSafety Factor Reduction: {SF_reduction:.1f}%")
    
    # Design decisions
    required_SF = 2.0
    print(f"\nRequired Safety Factor: {required_SF}")
    print(f"Nominal approach passes: {SF_nominal > required_SF}")
    print(f"Conservative approach passes: {SF_conservative > required_SF}")
    
    if SF_nominal > required_SF and SF_conservative < required_SF:
        print("\n⚠️  WARNING: Design passes nominal check but fails conservative check!")
        print("   Recommendation: Reduce applied load or increase component strength")


def main():
    """Run all engineering examples."""
    print("\n" + "=" * 70)
    print("N/U ALGEBRA: ENGINEERING APPLICATIONS")
    print("=" * 70)
    print("Reference: Martin, E.D. (2025). The NASA Paper & Small Falcon Algebra")
    
    examples = [
        example_1_beam_stress,
        example_2_column_buckling,
        example_3_thermal_stress,
        example_4_composite_loading,
        example_5_pressure_vessel,
        example_6_cantilever_deflection,
        example_7_factor_of_safety
    ]
    
    for example in examples:
        example()
    
    print("\n" + "=" * 70)
    print("All engineering examples completed successfully!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("1. N/U algebra provides conservative bounds for design verification")
    print("2. Uncertainty propagates through complex engineering calculations")
    print("3. Conservative safety factors account for measurement uncertainty")
    print("4. Sign stability indicates well-defined stress/load directions")
    print("5. All calculations are transparent and auditable")


if __name__ == "__main__":
    main()
