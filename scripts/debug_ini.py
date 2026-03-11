
import os

file_path = r"d:\Github\ScCompLangPackRemix\4.4.0\PTU\data\Localization\english\global.ini"

print(f"Reading {file_path}...")

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
except UnicodeDecodeError:
    print("UTF-8 failed, trying utf-16")
    with open(file_path, 'r', encoding='utf-16') as f:
        lines = f.readlines()
except Exception as e:
    print(f"Error reading file: {e}")
    exit(1)

print(f"Read {len(lines)} lines.")

search_terms = ["Arctic", "XL-1", "QuadraCell", "item_Name"]

for term in search_terms:
    print(f"Searching for '{term}'...")
    count = 0
    for i, line in enumerate(lines):
        if term.lower() in line.lower():
            print(f"Found at line {i+1}: {line.strip()}")
            count += 1
            if count >= 5:
                print("... (stopping after 5 matches)")
                break
    if count == 0:
        print(f"'{term}' NOT FOUND.")
