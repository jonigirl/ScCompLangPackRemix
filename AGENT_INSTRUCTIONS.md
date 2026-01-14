# Agent Instructions: Star Citizen Language Pack Remix

**Objective**: Maintain and update the compact naming language pack for Star Citizen.

## 🛠️ The "Magic" Workflow (Each Patch)

When a new Star Citizen patch is released, follow these steps:

### 1. Ingest Stock Data
- Obtain the fresh `StockGlobal-[Version]-[Channel].ini` from the extraction tool (C:\SCExtractor).
- Copy it to the repository under `[Version]/[Channel]/stock-global.ini`.

### 2. Identify Changes
- Use `scripts/compare_ini.py` to compare the new stock INI with the previous version's stock INI.
- **Check for**:
    - New ship components/weapons (Look for `item_Name...` keys that aren't in your mapping).
    - Changes to the main menu version string (`Frontend_PU_Version`).

### 3. Apply the Remix
- **Do NOT** crawl Game.dcb unless absolutely necessary for a major mapping update.
- Use a simple Python script to process the 9MB `global.ini` file:
    - **Update Version**: Set `Frontend_PU_Version` to the new patch title + `- ScCompLangPackRemix`.
    - **Apply Prefix**: For all ship component keys, prepend `[Type][Size][Quality]`.
- Ensure all other keys (MFDs, New missions, etc.) remain untouched from the original stock file.

### 4. Deploy & Release
- Install locally for testing.
- Commit to a feature branch → Merge to `main`.
- Push to GitHub and create a Release/Pre-release.

## 🧪 Requirements
- Avoid using complex text editing tools on the 9MB `global.ini`; always use specific Python processing scripts to avoid truncation or encoding errors.
- Always use `utf-8-sig` when reading/writing Star Citizen INI files.
