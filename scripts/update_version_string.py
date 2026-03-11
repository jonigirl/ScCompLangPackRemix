import sys
import os

file_path = r"4.7.0/PTU/data/Localization/english/global.ini"
# The target string as identified by Select-String
target_substring = "Frontend_PU_Version=4.7.0 - ScCompLangPackRemix"
replacement_string = "Frontend_PU_Version=4.7.0 - Crafting and INventory Gameplay PTU - ScCompLangPackRemix"

print(f"Processing {file_path}...")

if not os.path.exists(file_path):
    print(f"Error: File not found at {file_path}")
    sys.exit(1)

# Read content
try:
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
except UnicodeDecodeError:
    print("UTF-8-SIG decode failed, trying UTF-8...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        print("UTF-8 decode failed, trying Latin-1...")
        with open(file_path, 'r', encoding='latin-1') as f:
            lines = f.readlines()

found = False
new_lines = []
for line in lines:
    if target_substring in line:
        print(f"Found target line: {line.strip()}")
        new_lines.append(replacement_string + "\n")
        found = True
    else:
        new_lines.append(line)

if found:
    # Write back
    with open(file_path, 'w', encoding='utf-8-sig') as f:
        f.writelines(new_lines)
    print("Successfully updated version string.")
else:
    print(f"Error: Target string '{target_substring}' not found in file.")
    sys.exit(1)
