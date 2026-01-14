import csv
import os
import re
from pathlib import Path

# Config
REPO_ROOT = Path("c:/Github/ScCompLangPackRemix")
STOCK_INI = REPO_ROOT / "4.6.0" / "PTU" / "stock-global.ini"
PTU_REMIX = REPO_ROOT / "4.5.0" / "LIVE" / "data/Localization/english/global.ini"
MANIFEST_CSV = REPO_ROOT / "dry_run_manifest_ptu.csv"
OUTPUT_MD = REPO_ROOT / "component_manifest_4.6.0_ptu.md"

def load_ini(path):
    data = {}
    if not path.exists(): return data
    try:
        with open(path, 'r', encoding='utf-8-sig', errors='replace') as f:
            for line in f:
                if '=' in line:
                    parts = line.split('=', 1)
                    if len(parts) == 2:
                        k, v = parts
                        data[k.strip()] = v.strip()
    except Exception as e:
        print(f"Error reading {path}: {e}")
    return data

def get_class_from_desc(key, stock_ini_data):
    # Try to find description key
    desc_key = key.replace("Name", "Desc")
    desc = stock_ini_data.get(desc_key, "").lower()
    
    if "military" in desc: return "Military"
    if "industrial" in desc: return "Industrial"
    if "stealth" in desc: return "Stealth"
    if "competition" in desc: return "Competition"
    if "civilian" in desc: return "Civilian"
    return "Unknown"

def get_prefix(c_type, size, grade, c_class, tracking):
    # Grade mapping for standard components
    grade_map = {"1": "A", "2": "B", "3": "C", "4": "D"}
    prefix_grade = grade_map.get(grade, "A")

    if c_type in ["Missile", "Torpedo"]:
        track_map = {
            "Infrared": "IR",
            "Electromagnetic": "EM",
            "CrossSection": "CS"
        }
        # Finalized: Just the tracking type, no size or grade (roman numerals already in name)
        return track_map.get(tracking, "MSL")
    
    if c_type == "Bomb":
        # Finalized: B[Size], no grade
        return f"B{size}"

    # Standard Components: [Class][Size][Grade]
    class_prefix_map = {
        'Military': 'M',
        'Civilian': 'C',
        'Industrial': 'I',
        'Stealth': 'S',
        'Competition': 'R',
    }
    prefix_class = class_prefix_map.get(c_class, 'C')
    return f"{prefix_class}{size}{prefix_grade}"

def main():
    stock_data = load_ini(STOCK_INI)
    ptu_data = load_ini(PTU_REMIX)
    
    components = {}
    with open(MANIFEST_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row['key']
            if key in components: continue # Deduplicate
            
            # Exclusion logic for ship weapons and turrets
            if row['type'] in ["WeaponGun", "Turret", "TurretBase"]:
                continue
            
            stock_name = stock_data.get(key, "N/A")
            ptu_name = ptu_data.get(key, "N/A")
            
            c_class = get_class_from_desc(key, stock_data)
            tracking = row.get('tracking', 'N/A')
            proposed_prefix = get_prefix(row['type'], row['size'], row['grade'], c_class, tracking)
            proposed_name = f"{proposed_prefix} {stock_name}"
            
            # Status Identification
            if ptu_name == "N/A":
                status = "NEW ITEM"
            elif ptu_name == stock_name:
                status = "NEEDS REMIX"
            # Flexible regex to allow IR/EM/CS/BOMB prefixes as Verified if they follow the pattern
            elif re.match(r"^([A-Z]{1,4})\d[A-Z]\s", ptu_name):
                status = "VERIFIED"
                proposed_name = ptu_name # Keep existing remix
            else:
                status = "REMIXED (MISMATCH?)"
            
            components[key] = {
                "Type": row['type'],
                "Size": row['size'],
                "Grade": row['grade'],
                "Class": c_class,
                "Tracking": tracking,
                "Stock": stock_name,
                "Proposed": proposed_name,
                "Status": status
            }

    # Sort
    sorted_comps = sorted(components.values(), key=lambda x: (x['Type'], x['Size'], x['Stock']))

    with open(OUTPUT_MD, 'w', encoding='utf-8') as f:
        f.write("# Component Manifest: 4.5.0 LIVE\n\n")
        f.write("This table compares the **4.5.0 LIVE Stock** with your **Verified 4.5.0 PTU Remix**.\n")
        f.write("Missiles and Torpedoes now use functional prefixes (**IR/EM/CS**) and Bombs use (**BOMB**).\n\n")
        f.write("| Type | S | G | Tracking | Class | Stock Name | Proposed Remix | Status |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for c in sorted_comps:
            f.write(f"| {c['Type']} | {c['Size']} | {c['Grade']} | {c['Tracking']} | {c['Class']} | {c['Stock']} | **{c['Proposed']}** | {c['Status']} |\n")

    print(f"Generated manifest with {len(sorted_comps)} unique items.")

if __name__ == "__main__":
    main()
