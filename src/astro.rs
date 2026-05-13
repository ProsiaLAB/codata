//! Astronomical constants from IAU 2015 resolution.
//!
//! This module provides astronomical constants as defined by the IAU 2015 Resolution B3.
//! These values are used as standard nominal conversion factors.

use crate::constants::Constant;

/// IAU 2015 constants (Current IAU nominal values).
///
/// These values are defined as nominal conversion constants by IAU 2015 Resolution B3.
pub mod iau2015 {
    use crate::constants::NEWTONIAN_CONSTANT_OF_GRAVITATION as G;

    /// Astronomical Unit (au)
    /// Source: IAU 2012 Resolution B2
    /// Unit: m
    pub const AU_SI: f64 = 149_597_870_700.0;
    /// Astronomical Unit (au) in CGS
    pub const AU_CGS: f64 = AU_SI * 100.0;
    pub const AU: f64 = AU_SI;

    /// Parsec (pc)
    /// Source: IAU 2015 Resolution B2
    /// Defined as (648000 / pi) * au
    /// Unit: m
    pub const PC_SI: f64 = 30_856_775_814_913_673.0;
    /// Parsec (pc) in CGS
    pub const PC_CGS: f64 = PC_SI * 100.0;
    pub const PC: f64 = PC_SI;

    /// Luminosity for bolometric magnitude 0
    /// Source: IAU 2015 Resolution B2
    /// Unit: W
    pub const L_BOL0_SI: f64 = 3.0128e28;
    /// Luminosity for bolometric magnitude 0 in CGS
    pub const L_BOL0_CGS: f64 = L_BOL0_SI * 1e7;
    pub const L_BOL0: f64 = L_BOL0_SI;

    /// Nominal solar luminosity
    /// Source: IAU 2015 Resolution B3
    /// Unit: W
    pub const L_SUN_SI: f64 = 3.828e26;
    /// Nominal solar luminosity in CGS
    pub const L_SUN_CGS: f64 = L_SUN_SI * 1e7;
    pub const L_SUN: f64 = L_SUN_SI;

    /// Nominal solar mass parameter
    /// Source: IAU 2015 Resolution B3
    /// Unit: m^3 s^-2
    pub const GM_SUN_SI: f64 = 1.327_124_4e20;
    /// Nominal solar mass parameter in CGS (cm^3 s^-2)
    pub const GM_SUN_CGS: f64 = GM_SUN_SI * 1e6;
    pub const GM_SUN: f64 = GM_SUN_SI;

    /// Solar mass (derived from `GM_sun` / G)
    /// Unit: kg
    pub const M_SUN_SI: f64 = GM_SUN_SI / G;
    /// Solar mass in CGS (g)
    pub const M_SUN_CGS: f64 = M_SUN_SI * 1000.0;
    pub const M_SUN: f64 = M_SUN_SI;

    /// Nominal solar radius
    /// Source: IAU 2015 Resolution B3
    /// Unit: m
    pub const R_SUN_SI: f64 = 695_700_000.0;
    /// Nominal solar radius in CGS (cm)
    pub const R_SUN_CGS: f64 = R_SUN_SI * 100.0;
    pub const R_SUN: f64 = R_SUN_SI;

    /// Nominal Jupiter mass parameter
    /// Source: IAU 2015 Resolution B3
    /// Unit: m^3 s^-2
    pub const GM_JUP_SI: f64 = 1.266_865_3e17;
    /// Nominal Jupiter mass parameter in CGS (cm^3 s^-2)
    pub const GM_JUP_CGS: f64 = GM_JUP_SI * 1e6;
    pub const GM_JUP: f64 = GM_JUP_SI;

    /// Jupiter mass (derived from `GM_jup` / G)
    /// Unit: kg
    pub const M_JUP_SI: f64 = GM_JUP_SI / G;
    /// Jupiter mass in CGS (g)
    pub const M_JUP_CGS: f64 = M_JUP_SI * 1000.0;
    pub const M_JUP: f64 = M_JUP_SI;

    /// Nominal Jupiter equatorial radius
    /// Source: IAU 2015 Resolution B3
    /// Unit: m
    pub const R_JUP_SI: f64 = 71_492_000.0;
    /// Nominal Jupiter equatorial radius in CGS (cm)
    pub const R_JUP_CGS: f64 = R_JUP_SI * 100.0;
    pub const R_JUP: f64 = R_JUP_SI;

    /// Nominal Earth mass parameter
    /// Source: IAU 2015 Resolution B3
    /// Unit: m^3 s^-2
    pub const GM_EARTH_SI: f64 = 3.986_004e14;
    /// Nominal Earth mass parameter in CGS (cm^3 s^-2)
    pub const GM_EARTH_CGS: f64 = GM_EARTH_SI * 1e6;
    pub const GM_EARTH: f64 = GM_EARTH_SI;

    /// Earth mass (derived from `GM_earth` / G)
    /// Unit: kg
    pub const M_EARTH_SI: f64 = GM_EARTH_SI / G;
    /// Earth mass in CGS (g)
    pub const M_EARTH_CGS: f64 = M_EARTH_SI * 1000.0;
    pub const M_EARTH: f64 = M_EARTH_SI;

    /// Nominal Earth equatorial radius
    /// Source: IAU 2015 Resolution B3
    /// Unit: m
    pub const R_EARTH_SI: f64 = 6_378_100.0;
    /// Nominal Earth equatorial radius in CGS (cm)
    pub const R_EARTH_CGS: f64 = R_EARTH_SI * 100.0;
    pub const R_EARTH: f64 = R_EARTH_SI;
}

// Re-export current nominal values at module level
pub use iau2015::*;

/// Collection of astronomical constants for lookup.
pub const ASTRO_CONSTANTS: &[(&str, Constant)] = &[
    ("Astronomical Unit", Constant { value: AU_SI, uncertainty: 0.0, unit: "m" }),
    ("Parsec", Constant { value: PC_SI, uncertainty: 0.0, unit: "m" }),
    ("Solar luminosity", Constant { value: L_SUN_SI, uncertainty: 0.0, unit: "W" }),
    ("Solar mass", Constant { value: M_SUN_SI, uncertainty: 0.0, unit: "kg" }),
    ("Solar radius", Constant { value: R_SUN_SI, uncertainty: 0.0, unit: "m" }),
    ("Jupiter mass", Constant { value: M_JUP_SI, uncertainty: 0.0, unit: "kg" }),
    ("Jupiter equatorial radius", Constant { value: R_JUP_SI, uncertainty: 0.0, unit: "m" }),
    ("Earth mass", Constant { value: M_EARTH_SI, uncertainty: 0.0, unit: "kg" }),
    ("Earth equatorial radius", Constant { value: R_EARTH_SI, uncertainty: 0.0, unit: "m" }),
];
