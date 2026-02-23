# CSV Merger — User Guide & Help Documentation

A comprehensive guide to using CSV Merger for merging, transforming, and exporting CSV files.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Interface Overview](#interface-overview)
3. [File Selection](#file-selection)
4. [Column Management](#column-management)
5. [Filtering Data](#filtering-data)
6. [Merge Options](#merge-options)
7. [Preview & Export](#preview--export)
8. [Batch Processing](#batch-processing)
9. [Troubleshooting](#troubleshooting)
10. [Tips & Tricks](#tips--tricks)

---

## Getting Started

### Installation

**Windows (Recommended):**
1. Download `CSV_Merger_Installer.exe` from GitHub Releases
2. Run the installer
3. Follow the installation wizard (accept defaults)
4. Launch from Start Menu or Desktop shortcut

**From Source (All Platforms):**
```bash
git clone https://github.com/Mandip77/csv-merger
cd csv-merger/practise/csvmerger
pip install -r requirements.txt
python mergecsvfiles_advanced.py
```

### First Launch

On first run, CSV Merger creates:
- `settings.json` — UI preferences
- `batch_configs.json` — Saved merge configurations
- `recent_merges.json` — File history

These files persist in the app directory and enable features like saved configurations.

---

## Interface Overview

CSV Merger uses a **tabbed interface** with 6 main sections:

```
┌─ File Selection ──────────────────────────────────────┐
│ Select and manage CSV files to merge                  │
├─ Column Management ───────────────────────────────────┤
│ Choose and map columns from each file                 │
├─ Filtering ───────────────────────────────────────────┤
│ Apply conditions to filter rows before merge          │
├─ Merge Options ───────────────────────────────────────┤
│ Configure join type, duplicates, sorting              │
├─ Preview ────────────────────────────────────────────┤
│ View sample of merged data before export              │
├─ Batch Processing ────────────────────────────────────┤
│ Save/load configurations for repeated tasks           │
└───────────────────────────────────────────────────────┘
```

### Menu Bar & Toolbar

**Menu Options:**
- **File** — Open recent merges, settings, exit
- **Tools** — Run batch merge, view logs
- **View** — Toggle dark theme (if ttkbootstrap available)
- **Help** — User guide, about, keyboard shortcuts

**Toolbar Buttons:** (left to right)
- 📁 Open file
- ➕ Add files
- ❌ Remove selected file
- 🔄 Refresh file list
- ⚙️ Settings
- 💾 Save configuration
- 🚀 Run merge

**Status Bar:** (bottom)
- Current file count
- Selected merge type
- Processing status

---

## File Selection

### Adding Files

**Method 1: Browse Button**
1. Click the **Browse** button in the File Selection tab
2. Navigate to your CSV files
3. Select one or multiple files (Ctrl+Click for multiple)
4. Confirm selection

**Method 2: Drag and Drop**
1. Open your file explorer
2. Drag CSV files directly into the app window
3. Files are added to the list

**Method 3: Recent Files Menu**
1. Click **File** → **Open Recent**
2. Select from list of recently merged files
3. Files are automatically loaded

### Managing Files

**Viewing Files:**
- Files are displayed in a **Treeview** with:
  - File name
  - File size
  - Last modified date
  - Encoding detected

**Remove Files:**
1. Select file(s) in the list (Ctrl+Click for multiple)
2. Click **Remove** button or press **Delete**
3. Or right-click → **Remove from list**

**Open File Location:**
1. Right-click any file
2. Select **Open folder**
3. Folder opens in Explorer/Finder/File Manager

**Check File Details:**
- Hover mouse over file for preview tooltip (first 5 rows)
- View file size, encoding, column count in status

---

## Column Management

### Understanding Column Selection

Before merging, you choose which columns to include from each file. This lets you:
- ✅ Keep only relevant columns
- ✅ Rename columns for consistency
- ✅ Align columns across files (column mapping)
- ✅ Exclude unnecessary data

### Select Columns

**Step 1: Load Columns**
```
1. Click "Detect Columns" button
2. App reads first row of each file
3. Column list populates with checkboxes
```

**Step 2: Check/Uncheck**
```
✓ "Name"        (keep this column)
✓ "Age"         (keep this column)
☐ "Internal ID" (skip this column)
✓ "Email"       (keep this column)
```

### Rename Columns

**Purpose:** Make column names consistent across files

```
File 1:              File 2:              Mapped:
"Full Name"    →     "Name"         →     "Name"
"Employee Age" →     "Age"          →     "Age"
"Contact Email" →    "Email Addr"   →    "Email"
```

**How to Rename:**
1. Double-click column name in list
2. Type new name
3. Press Enter to confirm

**Smart Auto-Mapping:**
- App suggests matching columns with similar names
- Accept suggestions or manually remap

### Column Mapping (Advanced)

**When Files Have Different Column Names:**

File A columns: `Customer Name`, `Contact Email`, `Industry`
File B columns: `Name`, `Email`, `Sector`

**Mapping:**
```
File A Columns  →  Merged Output
Customer Name   →  Name
Contact Email   →  Email
Industry        →  Sector

File B Columns  →  Merged Output
Name            →  Name
Email           →  Email
Sector          →  Sector
```

---

## Filtering Data

### Add Filters

Filters remove unwanted rows **before merging** to clean data early.

**Step 1: Create Filter**
1. Click **Add Filter** in Filtering tab
2. Choose a column
3. Choose condition (see below)
4. Enter value

**Step 2: Filter Conditions**

| Operator | Example | Meaning |
|----------|---------|---------|
| **equals** | Age = 25 | Exact match |
| **not equals** | City ≠ "NYC" | Exclude value |
| **contains** | Name contains "John" | Substring match |
| **starts with** | Code starts with "US" | Prefix match |
| **>** | Salary > 50000 | Greater than |
| **<** | Date < 2020-01-01 | Less than |
| **>=** | Count >= 10 | Greater or equal |
| **<=** | Price <= 100 | Less or equal |

**Step 3: Apply Filters**
```
Filter 1: Status = "Active"
Filter 2: Amount > 1000
Filter 3: Country contains "USA"

Result: Only rows matching ALL filters included
```

### Multiple Filters

Filters use **AND** logic (all conditions must match):
```
Status = "Active" AND Amount > 1000 AND Country contains "USA"
```

### Remove Filters

1. Select filter in list
2. Click **Remove** button
3. Or click **Clear All** to reset

### Quick Filter Examples

```
▪ Keep only UK rows: Country = "UK"
▪ Exclude test data: Status ≠ "Test"
▪ Amount over $5000: Amount > 5000
▪ Names starting with A: Name starts with "A"
▪ Emails containing gmail: Email contains "@gmail"
```

---

## Merge Options

### Merge Type: Concatenate vs Join

#### **Concatenate (Default)**
- **What:** Stack rows from all files
- **When:** Files have matching columns, you want all rows
- **Result:** Combined row count = sum of all inputs

```
File 1:         File 2:         Result:
Name  Age       Name  Age       Name  Age
Alice 25        Bob   30        Alice 25
Carol 28        David 22        Carol 28
                                Bob   30
                                David 22

(4 rows total)
```

#### **Join**
- **What:** Merge based on common column value (like database join)
- **When:** Files have matching IDs/keys
- **Result:** Rows matching both files combined

```
File 1:                File 2:              Result:
ID  Name  Salary      ID  Department       ID  Name   Salary  Department
1   Alice 50000       1   Engineering      1   Alice  50000   Engineering
2   Bob   60000       3   Sales            2   Bob    60000   (null)
3   Carol 55000                            3   Carol  55000   Sales

(join on ID column)
```

**Join Types:**
- **Inner Join** — Only matching rows (most common)
- **Left Join** — All from File 1 + matching from File 2
- **Right Join** — All from File 2 + matching from File 1
- **Outer Join** — All rows from both files

---

### Handle Missing Data

When files have different columns or missing values:

| Strategy | Effect | When Use |
|----------|--------|----------|
| **Drop Rows** | Remove rows with ANY missing value | Strict data quality |
| **Forward Fill** | Use previous row's value | Time-series data |
| **Interpolate** | 🔢 Estimate numeric values | Numeric columns only |
| **Keep as NULL** | Leave blank/NULL | Preserve unknowns |

**Example:**
```
Original:           Forward Fill:       Interpolate (numeric):
Date   Temp        Date   Temp         Date   Temp
1/1    20°         1/1    20°          1/1    20°
1/2    (missing)   1/2    20°          1/2    25°        ← averaged
1/3    30°         1/3    30°          1/3    30°
```

---

### Duplicate Handling

#### **Duplicate Rows**

Remove identical or similar rows.

**Strategies:**
- **Keep First** — Keep first occurrence, remove repeats
- **Keep Last** — Keep last occurrence, remove repeats
- **Remove All** — Remove all duplicates (risky!)

#### **Duplicate Columns**

When merging creates same-named columns:

**Strategies:**
- **Rename with suffix** — `Name`, `Name_2`, `Name_3`
- **Keep First** — Use first file's column, ignore others
- **Merge/Concatenate** — Combine values: `"Value1, Value2"`

---

### Sorting

Order merged data by specified columns.

**Example:**
```
Sort by: Last Name (A→Z), then First Name (A→Z)

Result:
Last Name  First Name
Adams      John
Adams      Mary
Brown      Paul
Brown      Susan
```

**Steps:**
1. Click **Add Sort Column**
2. Choose column
3. Choose **Ascending** (A→Z) or **Descending** (Z→A)
4. Add multiple sorts for complex ordering

---

## Preview & Export

### Preview

Before exporting, **always preview** the merged data!

**Preview Shows:**
- First 50 rows of merged result
- All columns and values
- Data types detected
- Any NULL/missing values highlighted

**Statistics Displayed:**
- Total rows in result
- Column count
- Data types per column
- Memory footprint

### Export Formats

#### **CSV (Comma-Separated Values)**
- **Best for:** General use, Excel compatibility
- **File size:** Smallest
- **Special chars:** Quoted if needed

#### **TSV (Tab-Separated Values)**
- **Best for:** Tab-delimited legacy systems
- **File size:** Similar to CSV
- **Advantage:** Better with commas in data

#### **XLSX (Excel)**
- **Best for:** Business users, styled output
- **File size:** Medium (compressed)
- **Features:** Limited formatting

#### **JSON (JavaScript Object Notation)**
- **Best for:** APIs, web apps, databases
- **File size:** Medium
- **Advantage:** Preserves data types

### Export Steps

1. **Review Preview** — Check data looks correct
2. **Choose Format** — CSV, TSV, XLSX, or JSON
3. **Choose Location** — Click output directory button
4. **Name File** — Enter filename (extension auto-added)
5. **Click Export** — Run the export
6. **Confirm** — Success message + option to open folder

---

## Batch Processing

### Why Batch?

When doing the same merge repeatedly (daily report, weekly sync):

```
Manual way: 10 clicks × 20 times = 200 clicks
Batch way:  1 click  × 20 times = 20 clicks

Savings: 90% of time!
```

### Save Configuration

**After setting up a merge:**
1. Click **Save Configuration** button
2. Enter name: `"Daily Sales Report"` or `"Weekly Merge"`
3. Click Save
4. Config saved to `batch_configs.json`

**What's Saved:**
- File paths (searches for files)
- Column selections
- Filters
- Merge type
- Sort order
- Export format

### Load Configuration

**To repeat a merge:**
1. Click **Load Configuration** dropdown
2. Select saved config
3. Click **Load**
4. App restores all settings
5. Review preview
6. Click **Run Batch Merge**

### Scheduled Batches (Advanced)

For truly automated batches, use a **task scheduler**:

**Windows:**
```batch
# Create batch_runner.bat
cd C:\path\to\csvmerger
python -c "from mergecsvfiles_advanced import run_batch_merge; run_batch_merge('Daily Sales Report')"
```

Then schedule with **Windows Task Scheduler** to run daily.

**macOS/Linux:**
```bash
# Create cron job
0 9 * * * cd /path/to/csvmerger && python mergecsvfiles_advanced.py --batch "Daily Sales Report"
```

---

## Troubleshooting

### Common Issues & Solutions

#### **"File not found" error**
```
❌ Problem: Can't read CSV file
✅ Solution:
   1. Check file path is correct
   2. Ensure file is not open in another program
   3. Verify you have read permission
   4. Try moving file to simpler path (no special chars)
```

#### **"Encoding error" or "garbled characters"**
```
❌ Problem: Special characters appear wrong
✅ Solution:
   1. Check detected encoding (shown in status)
   2. File might be UTF-8 but app detected Latin-1
   3. Try opening file in Notepad, Save As → UTF-8
   4. Re-add file to app
```

#### **"Column names don't match"**
```
❌ Problem: Files have different column names
✅ Solution:
   1. Use Column Mapping tab
   2. Rename columns to match before merge
   3. Or manually map "Old Name" → "New Name"
```

#### **"Merge result is empty"**
```
❌ Problem: No rows in preview
✅ Solution:
   1. Check your filters (might exclude all rows)
   2. Click "Clear Filters" and retry
   3. Verify files have data (not just headers)
   4. Check join column has matching values
```

#### **"Out of memory" error**
```
❌ Problem: Files too large (>1GB)
✅ Solution:
   1. Close other programs
   2. Filter data first (remove unnecessary rows)
   3. Select fewer columns (skip heavy columns)
   4. Split large file into smaller chunks
   5. Process chunks separately
```

#### **"File permissions denied"**
```
❌ Problem: Can't write to output location
✅ Solution:
   1. Choose different output folder
   2. Right-click folder → Properties → Security
   3. Ensure you have "Write" permission
   4. Try Desktop or Documents folder
```

### Check App Logs

For detailed error info:
1. Click **Tools** menu
2. Select **View Logs**
3. Log file opens showing:
   - What files were read
   - Which columns detected
   - Merge operations performed
   - Any errors or warnings

---

## Tips & Tricks

### Pro Tips

**1. Preview Before Export**
```
Always check preview tab — catches 95% of mistakes
before you export huge files!
```

**2. Use Filters Early**
```
Filter at start → smaller working dataset → faster merge
Filter at end → processes all rows → slower
```

**3. Backup Original Files**
```
Keep originals safe — if merge goes wrong, you have backup
Never merge "in place"
```

**4. Save Successful Configs**
```
Once a merge works well:
1. Save configuration
2. Comment what it does
3. Reuse for future similar data
```

**5. Use Keyboard Shortcuts**
```
Ctrl+O    Open/browse files
Ctrl+E    Export merged data
Ctrl+S    Save configuration
Ctrl+L    Load configuration
F12       Toggle dark theme
```

**6. Test with Small Data First**
```
1. Take 10 rows from each file
2. Test merge settings
3. Once confirmed, run on full data
```

### Advanced Tricks

**Combining Multiple Merges:**
```
Step 1: Merge File A + File B → "temp1.csv"
Step 2: Open temp1.csv + File C
Step 3: Merge again → "final.csv"
Result: A + B + C combined
```

**Handling Different Data Structures:**
```
File A: Name, Age, Email
File B: Name, Age, Phone, Address

Solution: 
1. Select same columns (Name, Age)
2. Map Phone → Email temporarily
3. Merge
4. Manually fix Email column in Excel after
```

**Deduplication Workflow:**
```
1. Merge all files (concatenate)
2. Enable "Remove Duplicate Rows"
3. Choose "Keep First"
4. Export clean data
```

---

## Keyboard Shortcuts Reference

| Shortcut | Action |
|----------|--------|
| **Ctrl+O** | Open/Browse files |
| **Ctrl+E** | Export current preview |
| **Ctrl+S** | Save configuration |
| **Ctrl+L** | Load configuration |
| **Ctrl+R** | Refresh file list |
| **Ctrl+A** | Select all files |
| **Delete** | Remove selected file(s) |
| **F1** | Open help (this guide) |
| **F12** | Toggle dark theme |
| **Tab** | Move to next control |

---

## Frequently Asked Questions

**Q: Can I merge Excel files (.xlsx)?**  
A: Not directly. First convert Excel → CSV using Excel's export feature, then merge.

**Q: What's the maximum file size?**  
A: Depends on RAM. Usually handles files up to 1GB. For larger, split first.

**Q: Can I merge more than 2 files?**  
A: Yes! Select as many as needed. Use concatenate for all-at-once, or merge in batches.

**Q: How do I undo a merge?**  
A: Keep original files; don't save over them. Each export is new file.

**Q: Can I schedule automatic daily merges?**  
A: Yes. Use Windows Task Scheduler or cron (see Batch Processing section).

**Q: How do I prevent duplicate rows?**  
A: In Merge Options tab, enable "Remove Duplicates" → "Keep First".

**Q: Can I encrypt the output CSV?**  
A: CSV doesn't support encryption. Export to XLSX and password-protect.

---

## Contact & Support

- 🐛 **Report bugs**: https://github.com/Mandip77/csv-merger/issues
- 💬 **Ask questions**: https://github.com/Mandip77/csv-merger/discussions
- ⭐ **Request features**: Open an issue with `[FEATURE]` label
- 🤝 **Contribute code**: See CONTRIBUTING.md

---

**Happy merging!** 📊

*CSV Merger v1.0.0 — Open-source desktop CSV transformation tool*
