import csv
import os
import re
from pathlib import Path

# Config
REPO_ROOT = Path("c:/Github/ScCompLangPackRemix")
STOCK_INI = REPO_ROOT / "4.5.0" / "LIVE" / "stock-global.ini"
PTU_REMIX = REPO_ROOT / "4.5.0" / "PTU" / "data/Localization/english/global.ini"
MANIFEST_CSV = REPO_ROOT / "dry_run_manifest.csv"
OUTPUT_INI = REPO_ROOT / "4.5.0" / "LIVE" / "data" / "Localization" / "english" / "global.ini"

BRANDING_VERSION = "4.5.0 - Dawn of Engineering - BeltaKoda's ScCompLangPackRemix"

def load_ini(path):
    data = {}
    if not path.exists(): return data
    try:
        # Stock files often have BOM, remix files might not. Using utf-8-sig for reading.
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
    desc_key = key.replace("Name", "Desc")
    desc = stock_ini_data.get(desc_key, "").lower()
    
    if "military" in desc: return "Military"
    if "industrial" in desc: return "Industrial"
    if "stealth" in desc: return "Stealth"
    if "competition" in desc: return "Competition"
    if "civilian" in desc: return "Civilian"
    return "Unknown"

def get_prefix(c_type, size, grade, c_class, tracking):
    grade_map = {"1": "A", "2": "B", "3": "C", "4": "D"}
    prefix_grade = grade_map.get(grade, "A")

    if c_type in ["Missile", "Torpedo"]:
        track_map = {
            "Infrared": "IR",
            "Electromagnetic": "EM",
            "CrossSection": "CS"
        }
        return track_map.get(tracking, "MSL")
    
    if c_type == "Bomb":
        return f"B{size}"

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
    print(f"Loading stock data from {STOCK_INI}...")
    stock_data = load_ini(STOCK_INI)
    
    print(f"Loading reference PTU data from {PTU_REMIX}...")
    ptu_data = load_ini(PTU_REMIX)
    
    print(f"Processing manifest from {MANIFEST_CSV}...")
    final_data = stock_data.copy()
    
    # Counter for stats
    counts = {"Verified": 0, "New/Ordnance": 0}

    with open(MANIFEST_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row['key']
            stock_name = stock_data.get(key)
            if not stock_name: continue
            
            ptu_name = ptu_data.get(key)
            
            # 1. Check if we already have a verified remix in PTU
            # We consider it verified if it has a prefix [A-Z]{1,4}[0-9]
            # EXCEPT for ordnance, where we want to apply the NEW functional logic anyway.
            is_ordnance = row['type'] in ["Missile", "Torpedo", "Bomb"]
            
            if ptu_name and ptu_name != stock_name and not is_ordnance:
                # Use the verified PTU remix for standard components
                final_data[key] = ptu_name
                counts["Verified"] += 1
            else:
                # 2. Derive new name for Ordnance or new items
                c_class = get_class_from_desc(key, stock_data)
                tracking = row.get('tracking', 'N/A')
                prefix = get_prefix(row['type'], row['size'], row['grade'], c_class, tracking)
                final_data[key] = f"{prefix} {stock_name}"
                counts["New/Ordnance"] += 1

    # 3. Apply Branding
    print(f"Applying branding: {BRANDING_VERSION}")
    final_data["Frontend_PU_Version"] = BRANDING_VERSION

    # 4. Save final INI
    print(f"Saving remixed INI to {OUTPUT_INI}...")
    OUTPUT_INI.parent.mkdir(parents=True, exist_ok=True)
    
    # Write with utf-8-sig to match Star Citizen expectations
    with open(OUTPUT_INI, 'w', encoding='utf-8-sig') as f:
        for k, v in final_data.items():
            f.write(f"{k}={v}\n")

    print(f"Successfully applied manifest names.")
    print(f" - Preserved {counts['Verified']} verified names from PTU.")
    print(f" - Applied {counts['New/Ordnance']} new/functional names.")

if __name__ == "__main__":
    main()
