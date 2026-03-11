import os
import shutil
from pathlib import Path

# Configuration
SOURCE_FILE = Path(r"4.5.0/PTU/data/Localization/english/global.ini")
# Standard PTU location
PTU_INSTALL_PATH = Path(r"E:\Roberts Space Industries\StarCitizen\PTU")

def install_ptu():
    print("Installing global.ini to PTU...")
    
    if not SOURCE_FILE.exists():
        print(f"Error: Source file not found at {SOURCE_FILE}")
        return

    if not PTU_INSTALL_PATH.exists():
        print(f"Error: Star Citizen PTU installation not found at {PTU_INSTALL_PATH}")
        # Try to find it in alternative locations or ask user? 
        # For now, just report error.
        return

    dest_dir = PTU_INSTALL_PATH / "data" / "Localization" / "english"
    dest_path = dest_dir / "global.ini"

    try:
        if not dest_dir.exists():
            print(f"Creating directory: {dest_dir}")
            dest_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"Copying {SOURCE_FILE} to {dest_path}...")
        shutil.copy2(SOURCE_FILE, dest_path)
        print("Installation successful!")
        
    except Exception as e:
        print(f"Error installing file: {e}")

if __name__ == "__main__":
    install_ptu()
