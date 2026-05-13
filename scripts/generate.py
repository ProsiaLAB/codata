import urllib.request
import re

URL = "https://physics.nist.gov/cuu/Constants/Table/allascii.txt"

def normalize_name(name):
    # Replace special characters with descriptive words
    name = name.replace("/", "_over_")
    name = name.replace("^", "_pow_")
    name = name.replace("(", "_")
    name = name.replace(")", "_")
    # Replace non-alphanumeric with underscores
    name = re.sub(r'[^a-zA-Z0-9]', '_', name)
    # Collapse multiple underscores
    name = re.sub(r'_+', '_', name)
    # Strip leading/trailing underscores
    name = name.strip('_')
    return name.upper()

def parse_line(line):
    if len(line) < 110:
        return None
    
    quantity = line[0:60].strip()
    value_str = line[60:85].strip()
    uncertainty_str = line[85:110].strip()
    unit = line[110:].strip()
    
    if not quantity or quantity == "Quantity":
        return None
    
    # Clean value
    # Remove spaces
    value_str = value_str.replace(" ", "")
    # Remove "..."
    value_str = value_str.replace("...", "")
    
    # Clean uncertainty
    if uncertainty_str == "(exact)":
        uncertainty = 0.0
    else:
        uncertainty_str = uncertainty_str.replace(" ", "")
        try:
            uncertainty = float(uncertainty_str)
        except ValueError:
            uncertainty = 0.0
            
    try:
        value = float(value_str)
    except ValueError:
        return None
        
    return {
        "name": normalize_name(quantity),
        "original_name": quantity,
        "value": value,
        "value_str": value_str,
        "uncertainty": uncertainty,
        "uncertainty_str": uncertainty_str,
        "unit": unit
    }

def format_float(val):
    # Use high precision to avoid truncation
    s = f"{val:.18g}"
    if 'e' in s:
        mantissa, exponent = s.split('e')
    else:
        mantissa, exponent = s, ""

    parts = mantissa.split('.')
    integral = parts[0]
    fractional = parts[1] if len(parts) > 1 else ""
    
    # Integral part: groups of 3 from the right
    new_integral = ""
    for i, char in enumerate(reversed(integral)):
        if i > 0 and i % 3 == 0 and char.isdigit():
            new_integral = "_" + new_integral
        new_integral = char + new_integral
        
    # Fractional part: groups of 3 from the left
    new_fractional = ""
    for i, char in enumerate(fractional):
        if i > 0 and i % 3 == 0:
            new_fractional += "_"
        new_fractional += char
        
    res = new_integral
    if new_fractional:
        res += "." + new_fractional
    elif not exponent:
        # Always include .0 for float literals to avoid mismatched type error (E0308)
        res += ".0"
        
    if exponent:
        # If there was a fractional part, or we just added .0 (not applicable here as exponent exists)
        # But if exponent exists, we don't necessarily need .0 if mantissa has no dot.
        # Actually, rust 1.27+ allows 1e10 as f64, but 1.0e10 is safer.
        if '.' not in res:
            res += ".0"
        res += "e" + exponent
    return res

def get_cgs_multiplier(unit_str):
    if not unit_str:
        return 1.0
    
    # Simple dimensional analysis for CGS conversion
    # SI -> CGS:
    # m -> 100 cm
    # kg -> 1000 g
    # s -> 1 s
    # J -> 1e7 erg
    # W -> 1e7 erg/s
    # Pa -> 10 dyn/cm^2
    # N -> 1e5 dyn
    # T -> 1e4 G
    
    # We'll handle the most common units found in CODATA
    # Pattern matching for units like "m^3 kg^-1 s^-2"
    multiplier = 1.0
    
    # Length
    if "m" in unit_str:
        # Match m, m^2, m^-1, etc.
        m_matches = re.findall(r'm(?:\^([-0-9]+))?', unit_str)
        for p in m_matches:
            p = int(p) if p else 1
            multiplier *= (100.0 ** p)
            
    # Mass
    if "kg" in unit_str:
        kg_matches = re.findall(r'kg(?:\^([-0-9]+))?', unit_str)
        for p in kg_matches:
            p = int(p) if p else 1
            multiplier *= (1000.0 ** p)
    elif "g" in unit_str and "kg" not in unit_str: # e.g. "kg mol^-1"
        pass # g is already CGS-ish but we usually start from kg in SI

    # Energy/Power
    if "J" in unit_str:
        j_matches = re.findall(r'J(?:\^([-0-9]+))?', unit_str)
        for p in j_matches:
            p = int(p) if p else 1
            multiplier *= (1e7 ** p)
    if "W" in unit_str:
        w_matches = re.findall(r'W(?:\^([-0-9]+))?', unit_str)
        for p in w_matches:
            p = int(p) if p else 1
            multiplier *= (1e7 ** p)
            
    # Force
    if "N" in unit_str and "N A^-2" not in unit_str: # Avoid confusion with units like "N A^-2"
         n_matches = re.findall(r'N(?:\^([-0-9]+))?', unit_str)
         for p in n_matches:
             p = int(p) if p else 1
             multiplier *= (1e5 ** p)
             
    # Magnetic field
    if "T" in unit_str:
        t_matches = re.findall(r'T(?:\^([-0-9]+))?', unit_str)
        for p in t_matches:
            p = int(p) if p else 1
            multiplier *= (1e4 ** p)

    return multiplier

def main():
    print(f"Fetching {URL}...")
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8')
    
    lines = content.splitlines()
    constants = []
    for line in lines[4:]: # Skip header
        res = parse_line(line)
        if res:
            res['cgs_multiplier'] = get_cgs_multiplier(res['unit'])
            constants.append(res)
    
    with open("src/constants.rs", "w") as f:
        f.write("// Generated from CODATA 2022 constants data\n")
        f.write("// Source: https://physics.nist.gov/cuu/Constants/Table/allascii.txt\n\n")
        f.write("#![allow(clippy::excessive_precision)]\n\n")
        
        f.write("/// A physical constant value with its uncertainty and unit.\n")
        f.write("#[derive(Debug, Clone, Copy, PartialEq)]\n")
        f.write("pub struct Constant {\n")
        f.write("    pub value: f64,\n")
        f.write("    pub uncertainty: f64,\n")
        f.write("    pub unit: &'static str,\n")
        f.write("}\n\n")
        
        for c in constants:
            # Wrap units in backticks for clippy
            unit_doc = c['unit'].replace("MeV", "`MeV`").replace("GeV", "`GeV`").replace("E_h", "`E_h`")
            name_doc = c['original_name'].replace("MeV", "`MeV`").replace("GeV", "`GeV`").replace("E_h", "`E_h`")
            
            f.write(f"/// {name_doc}\n")
            if c['unit']:
                f.write(f"/// Unit: {unit_doc}\n")
            f.write(f"/// Uncertainty: {c['uncertainty_str']}\n")
            f.write(f"pub const {c['name']}_SI: f64 = {format_float(c['value'])};\n")
            f.write(f"/// {name_doc} (CGS)\n")
            f.write(f"pub const {c['name']}_CGS: f64 = {format_float(c['value'] * c['cgs_multiplier'])};\n")
            f.write(f"pub const {c['name']}: f64 = {c['name']}_SI;\n\n")

        f.write("/// Detailed constant information including value, uncertainty, and unit.\n")
        f.write("#[allow(clippy::unreadable_literal)]\n")
        f.write("pub const CONSTANTS: &[(&str, Constant)] = &[\n")
        for c in constants:
            f.write(f"    (\"{c['original_name']}\", Constant {{ value: {format_float(c['value'])}, uncertainty: {format_float(c['uncertainty'])}, unit: \"{c['unit']}\" }}),\n")
        f.write("];\n")

if __name__ == "__main__":
    main()
