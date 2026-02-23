# CSV Merger — FAQ & Troubleshooting

Quick answers to the most common questions and issues.

## Installation & Setup

### Q: What are the system requirements?
**A:** 
- **OS**: Windows 10+ (macOS/Linux with source installation)
- **RAM**: 2GB minimum (4GB+ for large files)
- **Python**: 3.8 or higher (for source install)
- **Disk**: 100MB for app installation

### Q: How do I uninstall CSV Merger?
**A:** 
- **Windows (Installer)**: Settings → Apps → CSV Merger → Uninstall
- **Portable Exe**: Just delete the folder
- **Source**: Delete the project folder and virtual environment

### Q: Can I run CSV Merger without installing?
**A:** 
Yes! Use the portable `CSV Merger.exe` from the dist folder on GitHub releases, or run from source with Python.

### Q: Do I need an internet connection to use it?
**A:** 
No, the app is completely offline. It works on your local computer without any cloud connection.

---

## File Handling

### Q: What file formats are supported?
**A:** 
**Input**: CSV, TSV
**Output**: CSV, TSV, XLSX (Excel), JSON

For other formats (JSON input, Parquet):
- Convert to CSV first using online tools or Python
- Excel files: Open in Excel → File → Save As → CSV

### Q: Can I merge files from different folders?
**A:** 
Yes! The file browser and drag-drop support files from anywhere. You can even select folders and the app will find CSV files recursively.

### Q: What happens to my original files?
**A:** 
They're NOT modified. Merging creates a new output file. Always keep backups.

### Q: Can I undo a merge?
**A:** 
CSV Merger doesn't save over originals, so reversing is simple: delete the merged file you just created. Originals are safe.

### Q: How do I handle very large files (1GB+)?
**A:** 
1. Split the large file into chunks (100-200 MB each)
2. Merge chunks in smaller batches
3. Or: Use filtering to reduce data first, then merge

**Python script to split large CSV:**
```python
import pandas as pd
df = pd.read_csv('large_file.csv')
for i, chunk in enumerate(pd.read_csv('large_file.csv', chunksize=50000)):
    chunk.to_csv(f'chunk_{i}.csv', index=False)
```

---

## Data & Columns

### Q: How do I handle files with different column names?
**A:** 
Use the **Column Management** tab:
1. Enable "Detect Columns"
2. Rename columns to match
3. Or use "Column Mapping" to align different names
4. Proceed with merge

Example:
```
File A: "Customer Name" → Rename to "Name"
File B: "Name"          → Already "Name"
Result: Both mapped to single "Name" column
```

### Q: What if files have different numbers of columns?
**A:** 
CSV Merger handles this automatically:
1. Selected columns are merged
2. Unselected columns are ignored
3. Missing columns get NULL values in the output
4. Choose "Drop Rows with Missing Values" if strict

### Q: How do I handle special characters (é, ñ, 中)?
**A:** 
CSV Merger auto-detects file encoding (UTF-8, Latin-1, etc.):
1. App shows detected encoding in the File Selection tab
2. If wrong, convert file to UTF-8 first:
   - Open in Notepad
   - File → Save As → Choose UTF-8 encoding
3. Re-add file to app

### Q: Can I merge files with duplicate column names?
**A:** 
The app detects this and offers strategies:
- **Rename with suffix**: `Sales_1`, `Sales_2`
- **Keep First**: Use first file's column
- **Merge Values**: Combine like `"10, 20, 30"`

---

## Merge Operations

### Q: What's the difference between Concatenate and Join?
**A:** 
**Concatenate** (default):
```
Stacks rows: File1 rows + File2 rows = Total rows
(4 + 3 = 7 rows)
No matching needed
```

**Join**:
```
Matches on common key, combines matching rows only
(only rows where ID matches both files)
(1 match, 2 no match = 1 row)
```

Use **Concatenate** when merging similar data. Use **Join** when combining data from different sources with a common ID/key.

### Q: How many files can I merge at once?
**A:** 
Theoretically unlimited, but practically:
- 2-10 files: Instant
- 10-50 files: A few seconds
- 50+ files: Consider merging in batches
- 100+ text recommendation: Use Python script instead

### Q: Can I merge files with different delimiters?
**A:** 
CSV Merger assumes CSV/TSV format. For other delimiters:
1. Open file in Notepad++
2. Find and replace delimiters (e.g., `;` → `,`)
3. Save and re-add to app

### Q: How to merge the same file multiple times (duplicates)?
**A:** 
Select the file multiple times:
1. Click Browse, select File.csv
2. Click Browse again, select same File.csv
3. It's added twice
4. In Merge Options, enable "Remove Duplicates" if needed

---

## Filtering & Cleaning

### Q: How do filters work?
**A:** 
Filters remove rows **before merge** using AND logic:

```
Filter 1: Status = "Active"
Filter 2: Amount > 1000
Filter 3: Date >= "2024-01-01"

Result: Only rows matching ALL THREE filters included
```

### Q: Can I use OR logic instead of AND?
**A:** 
Not in the UI currently, but workaround:
1. Run merge with Filter A
2. Export result
3. Run merge with Filter B
4. Manually combine output files

### Q: How do I handle NULL/missing values?
**A:** 
In Merge Options, choose strategy:
- **Drop Rows**: Remove any row with missing data (strictest)
- **Forward Fill**: Use previous row's value
- **Interpolate**: Estimate numeric values (average)
- **Keep as NULL**: Leave blank (most flexible)

### Q: Can I remove duplicate rows?
**A:** 
Yes! In Merge Options:
1. Enable "Remove Duplicate Rows"
2. Choose strategy:
   - **Keep First**: First occurrence kept
   - **Keep Last**: Last occurrence kept
   - **Remove All**: All duplicates removed (risky!)

---

## Export & Output

### Q: Which export format should I use?
**A:** 
| Format | Best For | When |
|--------|----------|------|
| **CSV** | Most compatible | Default choice |
| **TSV** | Tab-delimited data | Many commas in data |
| **XLSX** | Business users | Excel import needed |
| **JSON** | APIs, databases | Web app integration |

### Q: How do I change the output location?
**A:** 
1. In Preview tab, click **Output Directory** button
2. Browse to folder where to save file
3. Optionally type custom filename
4. Export

### Q: Can I overwrite the original file?
**A:** 
Not recommended! Always export to a different filename:
- Original: `sales_march.csv`
- Merged: `sales_march_merged.csv`

This way you can always revert if needed.

### Q: How do I export without headers?
**A:** 
Currently, headers are always included. Workaround:
1. Export normally
2. Open in Excel
3. Delete first row (headers)
4. Save

*This feature may be added in future versions.*

### Q: Can I append to an existing file?
**A:** 
Not in the app UI, but workaround:
1. Export merged data
2. Open both files in Excel
3. Copy-paste merged data to existing file
4. Save

Or use command line:
```bash
cat file1.csv file2.csv > combined.csv
```

---

## Performance & Optimization

### Q: How long should merging take?
**A:** 
Typical speeds:
- **Small files** (< 1 MB): < 1 second
- **Medium files** (1-50 MB): 1-5 seconds
- **Large files** (50-500 MB): 10-60 seconds
- **Very large** (> 500 MB): Minutes

If slow, try filtering to reduce data first.

### Q: Why is the app slow with large files?
**A:** 
Possible causes:
1. **Low RAM**: Close other programs
2. **Disk issues**: Slow hard drive (SSD is faster)
3. **Complex operations**: Too many filters + joins
4. **Missing columns**: Scanning all columns (select fewer)

**Optimize:**
1. Filter data first
2. Select only needed columns
3. Close other apps
4. Use SSD instead of HDD

### Q: Can I batch process multiple merges?
**A:** 
Yes! Use Batch Processing tab:
1. Configure a merge (files, columns, filters, export)
2. Click **Save Configuration**
3. Name it (e.g., "Daily Report")
4. Later, load config + click **Run Batch Merge**

Saves hours on repetitive tasks!

---

## Batch Processing

### Q: How do I save and reuse a merge configuration?
**A:** 
1. Set up merge exactly how you want
2. Click **Save Configuration** button
3. Name it: `"Weekly Sales Merge"`, etc.
4. Click Save
5. Next time: **Load Configuration** → Select name → **Load**

All settings restored automatically!

### Q: Can I schedule automatic daily merges?
**A:** 

**Windows (Task Scheduler):**
```
1. Click Windows Start
2. Search "Task Scheduler"
3. Create Basic Task
4. Schedule: Daily at 9 AM
5. Action: Start program
6. Program: python
7. Arguments: -c "from mergecsvfiles_advanced import run_batch_merge; run_batch_merge('Daily Sales Report')"
```

**macOS/Linux (Cron):**
```bash
# Edit crontab
crontab -e

# Add line for daily 9 AM merge
0 9 * * * cd /path/to/csvmerger && python mergecsvfiles_advanced.py --batch "Daily Sales Report"
```

### Q: Where are batch configurations saved?
**A:** 
Batch configurations saved in `batch_configs.json` file in the app directory. You can:
- **Backup**: Copy this file to external drive
- **Share**: Send to colleague (they put in their app dir)
- **View**: Open in text editor to see all settings

---

## Troubleshooting Errors

### Q: "File not found" error
**A:** 
```
Cause: File moved, renamed, or deleted
Solution:
1. Check file still exists in same location
2. Re-add file via Browse button
3. Use absolute paths, not relative paths
```

### Q: "Encoding error" (garbled characters)
**A:** 
```
Cause: File in different encoding than detected
Solution:
1. Look at detected encoding in app (shown in status)
2. If wrong, convert file:
   - Right-click file → Open with Notepad
   - File → Save As → UTF-8
   - Try again in CSV Merger
```

### Q: "Out of Memory" error
**A:** 
```
Cause: Files too large for available RAM
Solution:
1. Close other programs (free up RAM)
2. Filter data (reduce rows)
3. Select fewer columns (reduce memory)
4. Split large files into chunks
5. Process chunks separately
```

### Q: "No matching rows" when joining
**A:** 
```
Cause: Join column values don't match exactly
Solution:
1. Check join column is correct
2. Look for case differences: "USA" vs "usa"
3. Check for spaces: "New York " vs "New York"
4. Verify both files have values for join column
5. Use Concatenate instead of Join if not critical
```

### Q: "Column not found" error
**A:** 
```
Cause: Server's typing wrong column name or file structure changed
Solution:
1. Click "Detect Columns" to reload
2. Verify column exists in file
3. Check file open in another program (close it)
4. Try opening file in Notepad to inspect headers
```

### Q: App won't start/crashes
**A:** 
```
Solution:
1. Restart the app
2. Delete settings files:
   - settings.json
   - batch_configs.json
   - recent_merges.json
3. Try running from source: python mergecsvfiles_advanced.py
4. Check Python installed: python --version
5. Reinstall: Download fresh installer
```

---

## Tips & Best Practices

### ✅ DO:
- ✓ Test with small data first
- ✓ Always preview before export
- ✓ Keep backup of original files
- ✓ Use filters to clean data early
- ✓ Save configurations for repeated merges
- ✓ Check output file has expected row count
- ✓ Use meaningful filenames

### ❌ DON'T:
- ✗ Directly edit original CSV files
- ✗ Have file open in Excel while merging
- ✗ Try merging 1000+ files at once
- ✗ Assume filters are applied (check preview!)
- ✗ Export without naming properly
- ✗ Ignore the preview tab
- ✗ Trust data without validation

---

## Getting Help

### Options:

1. **Check this FAQ** — Most common issues answered above

2. **User Guide** — Detailed step-by-step in USER_GUIDE.md

3. **GitHub Issues** — Report bugs
   https://github.com/Mandip77/csv-merger/issues

4. **GitHub Discussions** — Ask questions
   https://github.com/Mandip77/csv-merger/discussions

5. **View Logs** — Click Tools → View Logs for detailed info

---

## Frequently Requested Features

🔜 Coming soon:
- [ ] Python script support for custom transformations
- [ ] Cloud storage integration (Google Drive, OneDrive)
- [ ] Undo/Redo functionality
- [ ] Data validation rules
- [ ] More export formats (Parquet, SQLite)
- [ ] Internationalization (other languages)
- [ ] Auto-update feature

Have a feature request? Open an issue on GitHub!

---

**Still have questions?** Post on GitHub Discussions: https://github.com/Mandip77/csv-merger/discussions

*CSV Merger v1.0.0 — Making CSV merging simple and powerful* 📊
