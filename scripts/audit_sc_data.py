import os
import sys
import configparser
try:
    import scdatatools
    from scdatatools.sc import StarCitizen
except ImportError as e:
    print(f"scdatatools import failed: {e}")
    sys.exit(1)

# Configuration
REPO_ROOT = r"e:\Github\ScCompLangPackRemix"
# Known SC install paths to check
SC_PATHS = [
    r"C:\Program Files\Roberts Space Industries\StarCitizen",
    r"D:\Program Files\Roberts Space Industries\StarCitizen",
    r"E:\Roberts Space Industries\StarCitizen",
]

def find_sc_install():
    """Finds the Star Citizen installation path."""
    print("Searching for Star Citizen installation...")
    
    # Check common paths
    for path in SC_PATHS:
        if os.path.exists(path):
            # Check for LIVE or PTU
            if os.path.exists(os.path.join(path, "LIVE")):
                return os.path.join(path, "LIVE")
            if os.path.exists(os.path.join(path, "PTU")):
                return os.path.join(path, "PTU")
    
    return None

def parse_ini(file_path):
    """Parses the global.ini file into a dictionary."""
    print(f"Parsing {file_path}...")
    data = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line:
                    key, value = line.split('=', 1)
                    data[key.strip()] = value.strip()
    except UnicodeDecodeError:
        print("UTF-8 failed, trying utf-16")
        with open(file_path, 'r', encoding='utf-16') as f:
            for line in f:
                if '=' in line:
                    key, value = line.split('=', 1)
                    data[key.strip()] = value.strip()
    print(f"Loaded {len(data)} entries from INI.")
    return data

def generate_expected_name(name, size, grade, type_str):
    """
    Generates the expected name based on the remix format: [Type][Size][Grade] [Name]
    """
    type_map = {
        "Military": "M",
        "Industrial": "I",
        "Civilian": "C",
        "Competition": "R",
        "Stealth": "S"
    }
    
    type_code = type_map.get(type_str, "?")
    return f"{type_code}{size}{grade} {name}"

def main():
    # 1. Find SC Install
    sc_path = find_sc_install()
    if not sc_path:
        print("Could not find Star Citizen installation.")
        return

    print(f"Found Star Citizen at: {sc_path}")

    # 2. Initialize scdatatools
    try:
        sc = StarCitizen(sc_path)
        print("Initialized StarCitizen API.")
    except Exception as e:
        print(f"Failed to initialize scdatatools: {e}")
        return

    # 3. Explore available managers
    print("Exploring scdatatools managers...")
    print(f"Available attributes: {[attr for attr in dir(sc) if not attr.startswith('_')]}")
    
    # Try localization
    if hasattr(sc, 'localization'):
        print("\nExploring localization data...")
        loc = sc.localization
        print(f"Localization type: {type(loc)}")
        print(dir(loc))
        
        # Try to find component names
        # Localization files usually have keys like "item_Name_SHLD_..."
        if hasattr(loc, 'data') or hasattr(loc, 'strings'):
            data = loc.data if hasattr(loc, 'data') else loc.strings
            print(f"\nLocalization has {len(data)} entries.")
            
            # Search for shield component names
            print("\nSearching for shield component names...")
            shield_keys = [k for k in list(data.keys())[:1000] if 'shield' in k.lower() and 'item_name' in k.lower()]
            print(f"Found {len(shield_keys)} shield name keys (sample of first 1000).")
            
            for key in shield_keys[:5]:
                print(f"  {key}: {data[key]}")
    
    # Alternative: Try using the CLI tool 'scdt' to export data
    print("\n\nAlternative approach needed:")
    print("scdatatools may require using the CLI tool 'scdt' to export component data.")
    print("Or, we could parse the extracted localization .ini files directly."
)

if __name__ == "__main__":
    main()
