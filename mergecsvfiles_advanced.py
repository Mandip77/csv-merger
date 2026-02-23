import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
try:
    import ttkbootstrap as tb
    from ttkbootstrap import Style as TBStyle
    USE_TTB = True
except Exception:
    tb = None
    TBStyle = None
    USE_TTB = False
from pathlib import Path
import pandas as pd
import threading
import json
from datetime import datetime
import chardet
import os
import subprocess


class Tooltip:
    """Simple tooltip for Tk widgets."""
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.id = None
        self.tip = None
        widget.bind('<Enter>', self.schedule)
        widget.bind('<Leave>', self.hide)

    def schedule(self, _=None):
        self.hide()
        self.id = self.widget.after(self.delay, self.show)

    def show(self):
        if self.tip or not self.text:
            return
        x, y, cx, cy = self.widget.bbox('insert') if hasattr(self.widget, 'bbox') else (0,0,0,0)
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 20
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        label = ttk.Label(self.tip, text=self.text, background='#ffffe0', relief='solid', borderwidth=1)
        label.pack(ipadx=6, ipady=2)

    def hide(self, _=None):
        if self.id:
            try:
                self.widget.after_cancel(self.id)
            except Exception:
                pass
            self.id = None
        if self.tip:
            try:
                self.tip.destroy()
            except Exception:
                pass
            self.tip = None


class AdvancedCSVMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV File Merger Pro - Advanced Edition")
        self.root.geometry("1200x850")
        self.root.resizable(True, True)
        
        # Configure style
        if USE_TTB and TBStyle is not None:
            style = TBStyle(theme='flatly')
        else:
            style = ttk.Style()
            style.theme_use('clam')
        # Polish default fonts and paddings for a cleaner look
        default_font = ("Segoe UI", 10)
        try:
            style.configure('.', font=default_font)
            style.configure('TButton', padding=6)
            style.configure('TLabel', padding=4)
            style.configure('TFrame', padding=6)
            style.configure('TNotebook.Tab', padding=[12, 6])
        except Exception:
            pass
        
        # Variables
        self.selected_files = []
        self.output_filename = tk.StringVar(value='merged_data.csv')
        self.sort_option = tk.StringVar(value='date')
        self.sort_column = tk.StringVar(value='')
        self.sort_order = tk.StringVar(value='ascending')
        self.export_format = tk.StringVar(value='csv')
        self.duplicate_strategy = tk.StringVar(value='keep_all')
        self.remove_duplicate_rows = tk.BooleanVar(value=False)
        self.duplicate_row_keep = tk.StringVar(value='first')
        self.missing_data_strategy = tk.StringVar(value='keep')
        self.merge_type = tk.StringVar(value='concatenate')
        self.join_column_left = tk.StringVar(value='')
        self.join_column_right = tk.StringVar(value='')
        
        self.selected_columns = {}  # {file_path: [selected_columns]}
        self.column_mapping = {}  # {original_name: new_name}
        self.filters = []  # [{column, operator, value}]
        self.validation_rules = []  # [{column, rule_type, params}]
        self.recent_files = self.load_recent_files()
        self.batch_configs = self.load_batch_configs()
        self.output_dir = tk.StringVar(value=str(Path.cwd()))
        self.settings = self.load_settings()

        self.create_widgets()
        try:
            if self.settings.get('show_onboarding', True):
                self.show_onboarding()
        except Exception:
            pass
    
    def load_recent_files(self):
        """Load recent merge operations"""
        config_file = Path(__file__).parent / 'recent_merges.json'
        try:
            if config_file.exists():
                with open(config_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def save_recent_files(self):
        """Save recent merge operations"""
        config_file = Path(__file__).parent / 'recent_merges.json'
        try:
            with open(config_file, 'w') as f:
                json.dump(self.recent_files[:10], f, indent=2)
        except:
            pass
    
    def create_widgets(self):
        """Create main GUI with notebook tabs"""
        # Create menubar
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Open Output Folder...', command=self.open_output_folder, accelerator='Ctrl+Shift+O')
        file_menu.add_command(label='Save Settings', command=self.save_settings, accelerator='Ctrl+S')
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.root.quit)
        menubar.add_cascade(label='File', menu=file_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label='User Guide', command=self.show_help_docs)
        help_menu.add_command(label='Keyboard Shortcuts', command=self.show_shortcuts)
        help_menu.add_command(label='Report Issue', command=self.report_issue)
        help_menu.add_separator()
        help_menu.add_command(label='About', command=lambda: messagebox.showinfo('About', 'CSV Merger Pro - Advanced\nPolished UI'))
        menubar.add_cascade(label='Help', menu=help_menu)
        self.root.config(menu=menubar)

        # Toolbar (quick actions)
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=8, pady=(8, 0))
        self.btn_add_files = ttk.Button(toolbar, text='➕ Add Files', command=self.add_csv_files)
        self.btn_add_files.pack(side=tk.LEFT, padx=6)
        self.btn_add_folder = ttk.Button(toolbar, text='📁 Add Folder', command=self.add_folder_files)
        self.btn_add_folder.pack(side=tk.LEFT, padx=6)
        self.btn_preview = ttk.Button(toolbar, text='👁️ Preview', command=self.generate_preview)
        self.btn_preview.pack(side=tk.LEFT, padx=6)
        self.btn_merge = ttk.Button(toolbar, text='▶ Merge', command=self.start_merge)
        self.btn_merge.pack(side=tk.LEFT, padx=6)

        # Tooltips for toolbar
        try:
            Tooltip(self.btn_add_files, 'Add CSV files (Ctrl+O)')
            Tooltip(self.btn_add_folder, 'Add all CSV files from a folder (Ctrl+F)')
            Tooltip(self.btn_preview, 'Generate merged preview (Ctrl+P)')
            Tooltip(self.btn_merge, 'Run merge now (Ctrl+M)')
        except Exception:
            pass

        # Keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.add_csv_files())
        self.root.bind('<Control-f>', lambda e: self.add_folder_files())
        self.root.bind('<Control-p>', lambda e: self.generate_preview())
        self.root.bind('<Control-m>', lambda e: self.start_merge())
        self.root.bind('<Control-s>', lambda e: self.save_settings())

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: File Selection
        self.create_file_selection_tab()
        
        # Tab 2: Column Management
        self.create_column_management_tab()
        
        # Tab 3: Data Filtering & Validation
        self.create_filtering_tab()
        
        # Tab 4: Merge & Export Options
        self.create_merge_options_tab()
        
        # Tab 5: Preview & Statistics
        self.create_preview_tab()
        
        # Tab 6: Batch Processing
        self.create_batch_tab()
    
    def create_file_selection_tab(self):
        """Tab 1: File Selection and Configuration"""
        tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(tab, text="📁 Files & Settings")
        
        # Header
        ttk.Label(tab, text="Step 1: Select CSV Files", font=("Segoe UI", 14, "bold")).pack(anchor=tk.W, pady=(0, 15))
        
        # File buttons
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Button(btn_frame, text="➕ Add CSV Files", command=self.add_csv_files, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="📁 Add Folder", command=self.add_folder_files, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑 Clear All", command=self.clear_all_files, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="📜 Recent Files", command=self.show_recent_files, width=15).pack(side=tk.LEFT, padx=5)
        
        # File list
        list_frame = ttk.LabelFrame(tab, text="Selected Files", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Use Treeview for a cleaner multi-column file list
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.files_tree = ttk.Treeview(list_frame, columns=('name', 'path'), show='headings', height=8)
        self.files_tree.heading('name', text='Filename')
        self.files_tree.heading('path', text='Folder')
        self.files_tree.column('name', width=260)
        self.files_tree.column('path', width=520)
        self.files_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.files_tree.yview)
        self.files_tree.bind('<Delete>', lambda e: self.remove_selected_files())
        self.files_tree.bind('<Double-1>', lambda e: self.open_selected_file())
        self.files_tree.bind('<Button-3>', self.show_files_context_menu)
        
        self.file_count_label = ttk.Label(tab, text="No files selected", foreground="gray")
        self.file_count_label.pack(anchor=tk.W)
        
        # Output filename
        config_frame = ttk.LabelFrame(tab, text="Output Configuration", padding="10")
        config_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(config_frame, text="Output filename:", font=("Segoe UI", 9)).pack(anchor=tk.W)
        ttk.Entry(config_frame, textvariable=self.output_filename, width=60).pack(fill=tk.X, pady=(5, 0))
        # Output directory chooser
        out_dir_frame = ttk.Frame(config_frame)
        out_dir_frame.pack(fill=tk.X, pady=(8, 0))
        ttk.Label(out_dir_frame, text="Output folder:").pack(side=tk.LEFT)
        ttk.Entry(out_dir_frame, textvariable=self.output_dir, width=48).pack(side=tk.LEFT, padx=(8, 6))
        ttk.Button(out_dir_frame, text='Browse...', command=self.browse_output_dir).pack(side=tk.LEFT)
        
        # Encoding info
        encoding_frame = ttk.LabelFrame(tab, text="File Encoding", padding="10")
        encoding_frame.pack(fill=tk.X)
        
        ttk.Label(encoding_frame, text="Encoding will be auto-detected for each file", foreground="gray", font=("Segoe UI", 9)).pack(anchor=tk.W)
        ttk.Button(encoding_frame, text="🔍 Detect Encodings", command=self.detect_encodings, width=20).pack(anchor=tk.W)
    
    def create_column_management_tab(self):
        """Tab 2: Column Selection & Mapping"""
        tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(tab, text="📋 Columns")
        
        ttk.Label(tab, text="Step 2: Manage Columns", font=("Segoe UI", 14, "bold")).pack(anchor=tk.W, pady=(0, 15))
        
        # Column selection frame
        select_frame = ttk.LabelFrame(tab, text="Column Selection", padding="10")
        select_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(select_frame, text="Select columns to include (leave empty = all columns)", font=("Segoe UI", 9)).pack(anchor=tk.W)
        ttk.Button(select_frame, text="🔍 Configure Columns...", command=self.open_column_selector, width=25).pack(anchor=tk.W, pady=(5, 0))
        
        self.selected_cols_text = tk.Text(select_frame, height=5, width=60, state='disabled', bg='#f5f5f5')
        self.selected_cols_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Column mapping frame
        mapping_frame = ttk.LabelFrame(tab, text="Column Mapping (Rename/Unify)", padding="10")
        mapping_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        ttk.Label(mapping_frame, text="Map different column names to same column", font=("Segoe UI", 9)).pack(anchor=tk.W)
        ttk.Button(mapping_frame, text="🗺️ Set Column Mapping...", command=self.open_column_mapping, width=25).pack(anchor=tk.W, pady=(5, 0))
        
        self.mapping_text = tk.Text(mapping_frame, height=6, width=60, state='disabled', bg='#f5f5f5')
        self.mapping_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Duplicate column handling
        dup_frame = ttk.LabelFrame(tab, text="Duplicate Column Handling", padding="10")
        dup_frame.pack(fill=tk.X)
        
        ttk.Radiobutton(dup_frame, text="Keep all (rename with suffix _0, _1, etc.)", variable=self.duplicate_strategy, value='keep_all').pack(anchor=tk.W)
        ttk.Radiobutton(dup_frame, text="Keep first occurrence", variable=self.duplicate_strategy, value='first').pack(anchor=tk.W)
        ttk.Radiobutton(dup_frame, text="Keep last occurrence", variable=self.duplicate_strategy, value='last').pack(anchor=tk.W)
        ttk.Radiobutton(dup_frame, text="Merge duplicate columns (concatenate values)", variable=self.duplicate_strategy, value='merge').pack(anchor=tk.W)
    
    def create_filtering_tab(self):
        """Tab 3: Data Filtering & Validation"""
        tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(tab, text="🔍 Filtering & Validation")
        
        ttk.Label(tab, text="Step 3: Filter & Validate Data", font=("Segoe UI", 14, "bold")).pack(anchor=tk.W, pady=(0, 15))
        
        # Filtering frame
        filter_frame = ttk.LabelFrame(tab, text="Data Filtering", padding="10")
        filter_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(filter_frame, text="Apply filters before merging (e.g., date range, column values)", font=("Segoe UI", 9)).pack(anchor=tk.W)
        ttk.Button(filter_frame, text="➕ Add Filter...", command=self.add_filter, width=20).pack(anchor=tk.W, pady=(5, 0))
        
        self.filters_text = tk.Text(filter_frame, height=6, width=80, state='disabled', bg='#f5f5f5', font=("Courier", 9))
        self.filters_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        self.clear_filters_btn = ttk.Button(filter_frame, text="🗑 Clear All Filters", command=self.clear_filters, width=20)
        self.clear_filters_btn.pack(anchor=tk.W, pady=(5, 0))
        
        # Missing data handling
        missing_frame = ttk.LabelFrame(tab, text="Missing Data Handling", padding="10")
        missing_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Radiobutton(missing_frame, text="Keep empty values", variable=self.missing_data_strategy, value='keep').pack(anchor=tk.W)
        ttk.Radiobutton(missing_frame, text="Drop rows with missing data", variable=self.missing_data_strategy, value='drop').pack(anchor=tk.W)
        ttk.Radiobutton(missing_frame, text="Fill with 0", variable=self.missing_data_strategy, value='zero').pack(anchor=tk.W)
        ttk.Radiobutton(missing_frame, text="Fill with 'N/A'", variable=self.missing_data_strategy, value='na').pack(anchor=tk.W)
        ttk.Radiobutton(missing_frame, text="Forward fill (use previous value)", variable=self.missing_data_strategy, value='ffill').pack(anchor=tk.W)
        ttk.Radiobutton(missing_frame, text="Backward fill (use next value)", variable=self.missing_data_strategy, value='bfill').pack(anchor=tk.W)
        
        # Validation rules
        valid_frame = ttk.LabelFrame(tab, text="Data Validation Rules", padding="10")
        valid_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(valid_frame, text="Set validation rules to check data quality", font=("Segoe UI", 9)).pack(anchor=tk.W)
        ttk.Button(valid_frame, text="✔️ Add Validation Rule...", command=self.add_validation_rule, width=25).pack(anchor=tk.W, pady=(5, 0))
        
        self.validation_text = tk.Text(valid_frame, height=6, width=80, state='disabled', bg='#f5f5f5', font=("Courier", 9))
        self.validation_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
    
    def create_merge_options_tab(self):
        """Tab 4: Merge & Export Options"""
        tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(tab, text="⚙️ Merge Options")
        
        ttk.Label(tab, text="Step 4: Configure Merge & Export", font=("Segoe UI", 14, "bold")).pack(anchor=tk.W, pady=(0, 15))
        
        # Merge type
        merge_frame = ttk.LabelFrame(tab, text="Merge Type", padding="10")
        merge_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Radiobutton(merge_frame, text="Concatenate (stack all rows)", variable=self.merge_type, value='concatenate', command=self.on_merge_type_change).pack(anchor=tk.W)
        ttk.Radiobutton(merge_frame, text="Join on column (SQL-like)", variable=self.merge_type, value='join', command=self.on_merge_type_change).pack(anchor=tk.W)
        
        # Join configuration
        self.join_frame = ttk.LabelFrame(tab, text="Join Configuration", padding="10")
        self.join_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(self.join_frame, text="Join Column (Left):", font=("Segoe UI", 9)).grid(row=0, column=0, sticky=tk.W)
        ttk.Combobox(self.join_frame, textvariable=self.join_column_left, width=20, state='readonly').grid(row=0, column=1, padx=5)
        
        ttk.Label(self.join_frame, text="Join Column (Right):", font=("Segoe UI", 9)).grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        ttk.Combobox(self.join_frame, textvariable=self.join_column_right, width=20, state='readonly').grid(row=1, column=1, padx=5, pady=(5, 0))
        
        self.join_frame.pack_forget()  # Hide by default
        
        # Duplicate row removal
        dup_row_frame = ttk.LabelFrame(tab, text="Duplicate Row Handling", padding="10")
        dup_row_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Checkbutton(dup_row_frame, text="Remove duplicate rows", variable=self.remove_duplicate_rows).pack(anchor=tk.W)
        ttk.Label(dup_row_frame, text="Keep:").pack(anchor=tk.W, padx=(20, 0))
        ttk.Combobox(dup_row_frame, textvariable=self.duplicate_row_keep, values=['first', 'last'], width=12, state='readonly').pack(anchor=tk.W, padx=20)
        
        # Sorting
        sort_frame = ttk.LabelFrame(tab, text="Sorting", padding="10")
        sort_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Radiobutton(sort_frame, text="No sorting", variable=self.sort_option, value='none').pack(anchor=tk.W)
        ttk.Radiobutton(sort_frame, text="Auto-detect date column", variable=self.sort_option, value='date').pack(anchor=tk.W)
        ttk.Radiobutton(sort_frame, text="Custom column", variable=self.sort_option, value='custom').pack(anchor=tk.W)
        
        sort_config_frame = ttk.Frame(sort_frame)
        sort_config_frame.pack(fill=tk.X, padx=20, pady=(5, 0))
        
        ttk.Label(sort_config_frame, text="Column:").pack(side=tk.LEFT)
        self.sort_column_combo = ttk.Combobox(sort_config_frame, textvariable=self.sort_column, width=30, state='readonly')
        self.sort_column_combo.pack(side=tk.LEFT, padx=(5, 20))
        
        ttk.Label(sort_config_frame, text="Order:").pack(side=tk.LEFT)
        ttk.Radiobutton(sort_config_frame, text="Ascending", variable=self.sort_order, value='ascending').pack(side=tk.LEFT, padx=(5, 20))
        ttk.Radiobutton(sort_config_frame, text="Descending", variable=self.sort_order, value='descending').pack(side=tk.LEFT)
        
        # Export format
        export_frame = ttk.LabelFrame(tab, text="Export Format", padding="10")
        export_frame.pack(fill=tk.X)
        
        ttk.Radiobutton(export_frame, text="CSV", variable=self.export_format, value='csv').pack(anchor=tk.W)
        ttk.Radiobutton(export_frame, text="Excel (.xlsx)", variable=self.export_format, value='excel').pack(anchor=tk.W)
        ttk.Radiobutton(export_frame, text="JSON", variable=self.export_format, value='json').pack(anchor=tk.W)
        ttk.Radiobutton(export_frame, text="TSV (Tab-separated)", variable=self.export_format, value='tsv').pack(anchor=tk.W)
        
        # Run merge now
        ttk.Button(tab, text="▶ Run Merge Now", command=self.start_merge, width=20).pack(pady=(15, 0))
    
    def create_preview_tab(self):
        """Tab 5: Preview & Statistics"""
        tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(tab, text="👁️ Preview & Statistics")
        
        ttk.Label(tab, text="Step 5: Preview & Review", font=("Segoe UI", 14, "bold")).pack(anchor=tk.W, pady=(0, 15))
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(tab, text="Data Statistics", padding="10")
        stats_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Button(stats_frame, text="📊 Show Statistics...", command=self.show_statistics, width=25).pack(anchor=tk.W)
        
        # Preview frame
        preview_frame = ttk.LabelFrame(tab, text="Data Preview (First 20 rows)", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(preview_frame, text="👁️ Generate Preview", command=self.generate_preview, width=25).pack(anchor=tk.W, pady=(0, 5))
        
        scrollbar = ttk.Scrollbar(preview_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.preview_text = tk.Text(preview_frame, height=25, width=120, yscrollcommand=scrollbar.set, bg='white', font=("Courier New", 8))
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.preview_text.yview)
        
        # Info label
        ttk.Label(tab, text="Tip: Generate preview before merging to verify configuration", foreground="gray", font=("Segoe UI", 9)).pack(anchor=tk.W, pady=(10, 0))
    
    def create_batch_tab(self):
        """Tab 6: Batch Processing & History"""
        tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(tab, text="⚡ Batch & History")
        
        ttk.Label(tab, text="Batch Processing & History", font=("Segoe UI", 14, "bold")).pack(anchor=tk.W, pady=(0, 15))
        
        # Batch frame
        batch_frame = ttk.LabelFrame(tab, text="Batch Processing", padding="10")
        batch_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(batch_frame, text="Save current configuration and run multiple merges", font=("Segoe UI", 9)).pack(anchor=tk.W)
        
        batch_btn_frame = ttk.Frame(batch_frame)
        batch_btn_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(batch_btn_frame, text="💾 Save Config", command=self.save_batch_config, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(batch_btn_frame, text="📂 Load Config", command=self.load_batch_config, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(batch_btn_frame, text="🚀 Run Batch", command=self.run_batch_merge, width=15).pack(side=tk.LEFT, padx=5)
        
        self.batch_text = tk.Text(batch_frame, height=6, width=100, state='disabled', bg='#f5f5f5', font=("Courier", 9))
        self.batch_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Recent files frame
        recent_frame = ttk.LabelFrame(tab, text="Recent Merge Operations", padding="10")
        recent_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(recent_frame, text="Previously merged files", font=("Segoe UI", 9)).pack(anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(recent_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.recent_listbox = tk.Listbox(recent_frame, height=10, yscrollcommand=scrollbar.set, font=("Courier New", 9))
        self.recent_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.recent_listbox.yview)
        
        self.update_recent_list()
        self.update_batch_display()

        # Status bar
        self.status_var = tk.StringVar(value='Ready')
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def update_status(self, text):
        try:
            self.status_var.set(text)
        except Exception:
            pass
    
    def on_merge_type_change(self):
        """Show/hide join configuration based on merge type"""
        if self.merge_type.get() == 'join':
            self.join_frame.pack(fill=tk.X, pady=(0, 15), after=self.join_frame.master.winfo_children()[0])
        else:
            self.join_frame.pack_forget()
    
    def add_csv_files(self):
        """Add individual CSV files"""
        files = filedialog.askopenfilenames(title="Select CSV files", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if files:
            for file in files:
                file_path = Path(file)
                if file_path not in self.selected_files:
                    self.selected_files.append(file_path)
            self.update_file_list()
            self.log_to_app(f"✓ Added {len(files)} file(s)\n")
            self.update_column_options()
    
    def add_folder_files(self):
        """Add all CSV files from a folder"""
        directory = filedialog.askdirectory(title="Select folder containing CSV files")
        if directory:
            dir_path = Path(directory)
            csv_files = list(dir_path.glob('*.csv'))
            if not csv_files:
                messagebox.showwarning("No Files", f"No CSV files found in {directory}")
                return
            
            added_count = 0
            for csv_file in csv_files:
                if csv_file not in self.selected_files:
                    self.selected_files.append(csv_file)
                    added_count += 1
            
            self.update_file_list()
            self.log_to_app(f"✓ Added {added_count} file(s) from folder\n")
            self.update_column_options()
    
    def show_recent_files(self):
        """Show recent files dialog"""
        if not self.recent_files:
            messagebox.showinfo("No History", "No recent merge operations found")
            return
        
        # Create a simple selection window
        recent_window = tk.Toplevel(self.root)
        recent_window.title("Recent Files")
        recent_window.geometry("500x400")
        
        ttk.Label(recent_window, text="Select recent files to add:", font=("Segoe UI", 10)).pack(anchor=tk.W, padx=10, pady=10)
        
        listbox = tk.Listbox(recent_window, font=("Courier New", 9))
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        for item in self.recent_files:
            listbox.insert(tk.END, item['output_path'])
        
        def add_selected():
            for idx in listbox.curselection():
                file_path = Path(self.recent_files[idx]['output_path'])
                if file_path.exists() and file_path not in self.selected_files:
                    self.selected_files.append(file_path)
            self.update_file_list()
            recent_window.destroy()
        
        ttk.Button(recent_window, text="Add Selected", command=add_selected, width=20).pack(pady=10)
    
    def remove_selected_files(self):
        """Remove selected files from list"""
        selected = self.files_tree.selection()
        if not selected:
            messagebox.showinfo("Tip", "Select files to remove first")
            return

        # remove by stored path value
        paths_to_remove = [self.files_tree.item(item, 'values')[1] for item in selected]
        for p in paths_to_remove:
            try:
                ppath = Path(p)
                self.selected_files = [sf for sf in self.selected_files if sf != ppath]
            except Exception:
                continue

        self.update_file_list()
        self.log_to_app(f"✓ Removed {len(selected)} file(s)\n")
        self.update_column_options()
    
    def clear_all_files(self):
        """Clear all selected files"""
        if not self.selected_files:
            return
        self.selected_files.clear()
        self.update_file_list()
        self.log_to_app("✓ Cleared all files\n")
        self.update_column_options()
    
    def update_file_list(self):
        """Update file listbox"""
        # clear tree
        for row in self.files_tree.get_children():
            self.files_tree.delete(row)
        for file in self.selected_files:
            self.files_tree.insert('', tk.END, values=(file.name, str(file.parent)))
        
        count = len(self.selected_files)
        self.file_count_label.config(text=f"{count} file(s) selected" if count > 0 else "No files selected")

    def open_selected_file(self):
        """Open the first selected file using the OS default application"""
        sel = self.files_tree.selection()
        if not sel:
            return
        item = sel[0]
        vals = self.files_tree.item(item, 'values')
        if not vals:
            return
        filename, folder = vals[0], vals[1]
        full = Path(folder) / filename
        try:
            if os.name == 'nt':
                os.startfile(str(full))
            else:
                subprocess.run(['open' if os.name == 'darwin' else 'xdg-open', str(full)])
        except Exception as e:
            messagebox.showerror('Error', f'Could not open file: {e}')

    def open_folder_of_item(self, folder):
        try:
            if os.name == 'nt':
                os.startfile(folder)
            else:
                subprocess.run(['open' if os.name == 'darwin' else 'xdg-open', folder])
        except Exception as e:
            messagebox.showerror('Error', f'Could not open folder: {e}')

    def show_files_context_menu(self, event):
        iid = self.files_tree.identify_row(event.y)
        if not iid:
            return
        # select the row under pointer
        self.files_tree.selection_set(iid)
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label='Open File', command=self.open_selected_file)
        menu.add_command(label='Open Folder', command=lambda: self.open_folder_of_item(self.files_tree.item(iid, 'values')[1]))
        menu.add_separator()
        menu.add_command(label='Remove', command=self.remove_selected_files)
        menu.tk_popup(event.x_root, event.y_root)
    
    def detect_encodings(self):
        """Detect encoding of each file"""
        if not self.selected_files:
            messagebox.showwarning("Warning", "Select files first")
            return
        
        encoding_info = "Detected Encodings:\n" + "="*50 + "\n"
        for file in self.selected_files:
            try:
                with open(file, 'rb') as f:
                    result = chardet.detect(f.read())
                    encoding = result.get('encoding', 'Unknown')
                    confidence = result.get('confidence', 0)
                    encoding_info += f"{file.name}: {encoding} (confidence: {confidence:.1%})\n"
            except Exception as e:
                encoding_info += f"{file.name}: Error - {e}\n"
        
        # Show in messagebox
        info_window = tk.Toplevel(self.root)
        info_window.title("File Encodings")
        info_window.geometry("600x400")
        
        text_widget = scrolledtext.ScrolledText(info_window, width=70, height=20, font=("Courier New", 9))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert('1.0', encoding_info)
        text_widget.config(state='disabled')
    
    def open_column_selector(self):
        """Open column selection dialog"""
        if not self.selected_files:
            messagebox.showwarning("Warning", "Select files first")
            return
        
        # Try to load all unique columns
        all_columns = set()
        for file in self.selected_files:
            try:
                df = pd.read_csv(file)
                all_columns.update(df.columns)
            except:
                pass
        
        if not all_columns:
            messagebox.showerror("Error", "Could not read columns from files")
            return
        
        col_window = tk.Toplevel(self.root)
        col_window.title("Column Selection")
        col_window.geometry("500x500")
        
        ttk.Label(col_window, text="Select columns to include:", font=("Segoe UI", 10)).pack(anchor=tk.W, padx=10, pady=10)
        
        col_frame = ttk.Frame(col_window)
        col_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(col_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(col_frame, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar.set, font=("Segoe UI", 9))
        listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        for col in sorted(all_columns):
            listbox.insert(tk.END, col)
        
        def save_columns():
            selected = [listbox.get(i) for i in listbox.curselection()]
            self.selected_columns = {str(f): selected for f in self.selected_files}
            
            self.selected_cols_text.config(state='normal')
            self.selected_cols_text.delete('1.0', tk.END)
            if selected:
                self.selected_cols_text.insert('1.0', f"{len(selected)} columns selected:\n" + ', '.join(selected))
            else:
                self.selected_cols_text.insert('1.0', "All columns will be included")
            self.selected_cols_text.config(state='disabled')
            
            col_window.destroy()
        
        ttk.Button(col_window, text="✓ Save Selection", command=save_columns, width=20).pack(pady=10)
    
    def open_column_mapping(self):
        """Open column mapping dialog"""
        map_window = tk.Toplevel(self.root)
        map_window.title("Column Mapping")
        map_window.geometry("600x500")
        
        ttk.Label(map_window, text="Map original column names to new names:", font=("Segoe UI", 10)).pack(anchor=tk.W, padx=10, pady=10)
        
        # Mapping entries
        map_frame = ttk.Frame(map_window)
        map_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(map_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.map_text = tk.Text(map_frame, height=15, width=70, yscrollcommand=scrollbar.set, font=("Courier New", 9))
        self.map_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.map_text.yview)
        
        self.map_text.insert('1.0', "# Format: original_name -> new_name\n# Example:\n# date -> Date\n# value -> Amount\n")
        
        def save_mapping():
            mapping_text = self.map_text.get('1.0', tk.END)
            self.column_mapping = {}
            for line in mapping_text.split('\n'):
                if line.strip() and not line.startswith('#'):
                    parts = line.split('->')
                    if len(parts) == 2:
                        self.column_mapping[parts[0].strip()] = parts[1].strip()
            
            self.mapping_text.config(state='normal')
            self.mapping_text.delete('1.0', tk.END)
            if self.column_mapping:
                for orig, new in self.column_mapping.items():
                    self.mapping_text.insert(tk.END, f"{orig} → {new}\n")
            else:
                self.mapping_text.insert('1.0', "No mapping configured")
            self.mapping_text.config(state='disabled')
            
            map_window.destroy()
        
        ttk.Button(map_window, text="✓ Save Mapping", command=save_mapping, width=20).pack(pady=10)
    
    def add_filter(self):
        """Add data filter"""
        filter_window = tk.Toplevel(self.root)
        filter_window.title("Add Filter")
        filter_window.geometry("500x300")
        
        ttk.Label(filter_window, text="Add filtering rule:", font=("Segoe UI", 10)).pack(anchor=tk.W, padx=10, pady=10)
        
        ttk.Label(filter_window, text="Column:").pack(anchor=tk.W, padx=10)
        column_var = tk.StringVar()
        ttk.Entry(filter_window, textvariable=column_var, width=40).pack(anchor=tk.W, padx=10)
        
        ttk.Label(filter_window, text="Operator:").pack(anchor=tk.W, padx=10, pady=(10, 0))
        operator_var = tk.StringVar(value='==')
        ttk.Combobox(filter_window, textvariable=operator_var, values=['==', '!=', '>', '<', '>=', '<=', 'contains'], width=20, state='readonly').pack(anchor=tk.W, padx=10)
        
        ttk.Label(filter_window, text="Value:").pack(anchor=tk.W, padx=10, pady=(10, 0))
        value_var = tk.StringVar()
        ttk.Entry(filter_window, textvariable=value_var, width=40).pack(anchor=tk.W, padx=10)
        
        def add_filter_rule():
            rule = {
                'column': column_var.get(),
                'operator': operator_var.get(),
                'value': value_var.get()
            }
            self.filters.append(rule)
            self.update_filters_display()
            filter_window.destroy()
        
        ttk.Button(filter_window, text="✓ Add Filter", command=add_filter_rule, width=20).pack(pady=10)
    
    def update_filters_display(self):
        """Update filter display"""
        self.filters_text.config(state='normal')
        self.filters_text.delete('1.0', tk.END)
        for i, f in enumerate(self.filters, 1):
            self.filters_text.insert(tk.END, f"{i}. {f['column']} {f['operator']} {f['value']}\n")
        self.filters_text.config(state='disabled')
    
    def clear_filters(self):
        """Clear all filters"""
        self.filters.clear()
        self.update_filters_display()
        self.log_to_app("✓ Cleared all filters\n")
    
    def add_validation_rule(self):
        """Add validation rule"""
        val_window = tk.Toplevel(self.root)
        val_window.title("Add Validation Rule")
        val_window.geometry("500x350")
        
        ttk.Label(val_window, text="Add validation rule:", font=("Segoe UI", 10)).pack(anchor=tk.W, padx=10, pady=10)
        
        ttk.Label(val_window, text="Column:").pack(anchor=tk.W, padx=10)
        column_var = tk.StringVar()
        ttk.Entry(val_window, textvariable=column_var, width=40).pack(anchor=tk.W, padx=10)
        
        ttk.Label(val_window, text="Rule Type:").pack(anchor=tk.W, padx=10, pady=(10, 0))
        rule_var = tk.StringVar(value='not_empty')
        ttk.Combobox(val_window, textvariable=rule_var, values=['not_empty', 'numeric', 'email', 'date', 'unique'], width=20, state='readonly').pack(anchor=tk.W, padx=10)
        
        def add_validation():
            rule = {
                'column': column_var.get(),
                'rule_type': rule_var.get()
            }
            self.validation_rules.append(rule)
            self.update_validation_display()
            val_window.destroy()
        
        ttk.Button(val_window, text="✓ Add Rule", command=add_validation, width=20).pack(pady=10)
    
    def update_validation_display(self):
        """Update validation display"""
        self.validation_text.config(state='normal')
        self.validation_text.delete('1.0', tk.END)
        for i, r in enumerate(self.validation_rules, 1):
            self.validation_text.insert(tk.END, f"{i}. Column '{r['column']}' must be {r['rule_type']}\n")
        self.validation_text.config(state='disabled')
    
    def update_column_options(self):
        """Update column options for sorting"""
        if not self.selected_files:
            self.sort_column_combo['values'] = []
            return
        
        try:
            df = pd.read_csv(self.selected_files[0])
            self.sort_column_combo['values'] = list(df.columns)
        except:
            pass

    def browse_output_dir(self):
        """Open dialog to choose output folder"""
        directory = filedialog.askdirectory(title='Select output folder')
        if directory:
            self.output_dir.set(directory)
    
    def save_batch_config(self):
        """Save batch configuration"""
        config = {
            'timestamp': datetime.now().isoformat(),
            'files': [str(f) for f in self.selected_files],
            'output': self.output_filename.get(),
            'sort_option': self.sort_option.get(),
            'sort_column': self.sort_column.get(),
            'export_format': self.export_format.get(),
            'filters': self.filters,
            'column_mapping': self.column_mapping
        }
        self.batch_configs.append(config)
        # persist to disk
        try:
            cfg_path = Path(__file__).parent / 'batch_configs.json'
            with open(cfg_path, 'w', encoding='utf-8') as fh:
                json.dump(self.batch_configs, fh, indent=2)
        except Exception:
            pass
        self.update_batch_display()
        messagebox.showinfo("Success", "Configuration saved for batch processing")

    def load_batch_configs(self):
        """Load batch configs from disk if present"""
        cfg_path = Path(__file__).parent / 'batch_configs.json'
        try:
            if cfg_path.exists():
                with open(cfg_path, 'r', encoding='utf-8') as fh:
                    return json.load(fh)
        except Exception:
            pass
        return []
    
    def load_batch_config(self):
        """Load batch configuration"""
        if not self.batch_configs:
            messagebox.showwarning("Warning", "No saved configurations")
            return

        # let user pick one of the saved configs to load into UI
        win = tk.Toplevel(self.root)
        win.title('Load Batch Configuration')
        win.geometry('600x400')

        ttk.Label(win, text='Select a configuration to load:', font=("Segoe UI", 10)).pack(anchor=tk.W, padx=10, pady=10)
        listbox = tk.Listbox(win, font=("Courier New", 9))
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        for i, cfg in enumerate(self.batch_configs, 1):
            listbox.insert(tk.END, f"{i}. {cfg.get('timestamp', '')}: {len(cfg.get('files', []))} files → {cfg.get('output', '')}")

        def do_load():
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning('Warning', 'Select a configuration first')
                return
            cfg = self.batch_configs[sel[0]]
            # apply to UI
            try:
                self.selected_files = [Path(p) for p in cfg.get('files', [])]
                self.update_file_list()
                self.output_filename.set(cfg.get('output', self.output_filename.get()))
                self.sort_option.set(cfg.get('sort_option', self.sort_option.get()))
                self.sort_column.set(cfg.get('sort_column', self.sort_column.get()))
                self.export_format.set(cfg.get('export_format', self.export_format.get()))
                self.filters = cfg.get('filters', self.filters)
                self.column_mapping = cfg.get('column_mapping', self.column_mapping)
                self.update_batch_display()
                messagebox.showinfo('Loaded', 'Configuration loaded into UI')
            except Exception as e:
                messagebox.showerror('Error', f'Could not load config: {e}')
            finally:
                win.destroy()

        btn_frame = ttk.Frame(win)
        btn_frame.pack(fill=tk.X, padx=10, pady=8)
        ttk.Button(btn_frame, text='Load', command=do_load).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text='Cancel', command=win.destroy).pack(side=tk.LEFT, padx=8)
    
    def run_batch_merge(self):
        """Run batch merge with saved configs"""
        if not self.batch_configs:
            messagebox.showwarning('Warning', 'No batch configurations to run')
            return

        def worker():
            total = len(self.batch_configs)
            for idx, cfg in enumerate(self.batch_configs, 1):
                try:
                    self.update_status(f'Running batch {idx}/{total}...')
                    files = [Path(p) for p in cfg.get('files', [])]
                    # Apply config to UI state for the run
                    self.output_filename.set(cfg.get('output', self.output_filename.get()))
                    self.sort_option.set(cfg.get('sort_option', self.sort_option.get()))
                    self.sort_column.set(cfg.get('sort_column', self.sort_column.get()))
                    self.export_format.set(cfg.get('export_format', self.export_format.get()))
                    self.filters = cfg.get('filters', self.filters)
                    self.column_mapping = cfg.get('column_mapping', self.column_mapping)
                    # perform merge (synchronous) for this config
                    self.perform_merge_and_export(files)
                except Exception as e:
                    self.log_to_app(f'Batch job {idx} failed: {e}\n')
                    continue
            self.update_status('Ready')
            messagebox.showinfo('Batch Complete', 'Batch processing finished')

        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
    
    def update_batch_display(self):
        """Update batch display"""
        self.batch_text.config(state='normal')
        self.batch_text.delete('1.0', tk.END)
        for i, cfg in enumerate(self.batch_configs, 1):
            self.batch_text.insert(tk.END, f"{i}. {cfg['timestamp']}: {len(cfg['files'])} files → {cfg['output']}\n")
        self.batch_text.config(state='disabled')

    # -----------------
    # Settings & Help
    # -----------------
    def load_settings(self):
        cfg_path = Path(__file__).parent / 'settings.json'
        try:
            if cfg_path.exists():
                with open(cfg_path, 'r', encoding='utf-8') as fh:
                    return json.load(fh)
        except Exception:
            pass
        return {'show_onboarding': True}

    def save_settings(self):
        cfg_path = Path(__file__).parent / 'settings.json'
        try:
            with open(cfg_path, 'w', encoding='utf-8') as fh:
                json.dump(self.settings, fh, indent=2)
            messagebox.showinfo('Saved', 'Settings saved')
        except Exception as e:
            messagebox.showerror('Error', f'Could not save settings: {e}')

    def show_onboarding(self):
        win = tk.Toplevel(self.root)
        win.title('Welcome to CSV Merger Pro')
        win.geometry('600x360')
        ttk.Label(win, text='Welcome — Quick Start', font=("Segoe UI", 14, 'bold')).pack(anchor=tk.W, padx=12, pady=12)
        txt = (
            '1) Add CSV files or a folder (toolbar or File menu)\n'
            '2) Configure columns, mappings and filters in the Columns & Filtering tabs\n'
            '3) Generate a Preview to verify your configuration\n'
            '4) Choose an output folder and filename, then click Merge\n\n'
            'Keyboard shortcuts: Ctrl+O Add files, Ctrl+F Add folder, Ctrl+P Preview, Ctrl+M Merge'
        )
        msg = scrolledtext.ScrolledText(win, height=10, width=70, font=("Segoe UI", 10))
        msg.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 6))
        msg.insert('1.0', txt)
        msg.config(state='disabled')
        var = tk.BooleanVar(value=not self.settings.get('show_onboarding', True))
        chk = ttk.Checkbutton(win, text="Don't show this again", variable=var)
        chk.pack(anchor=tk.W, padx=12, pady=(0, 8))

        def close():
            try:
                self.settings['show_onboarding'] = not var.get()
            except Exception:
                pass
            try:
                self.save_settings()
            except Exception:
                pass
            win.destroy()

        ttk.Button(win, text='Got it', command=close).pack(pady=(0, 12))

    def show_help_docs(self):
        help_text = (
            'CSV Merger Pro - Help\n\n'
            '1. Add files: Use the toolbar or File > Open to add CSVs.\n'
            '2. Columns: Select and map columns across files.\n'
            '3. Filters: Apply row filters before merging.\n'
            '4. Preview: Generate a preview to validate settings.\n'
            '5. Merge: Choose an output folder and filename, then Merge.\n\n'
            'For more details visit the project README or report issues from Help > Report Issue.'
        )
        w = tk.Toplevel(self.root)
        w.title('User Guide')
        w.geometry('700x500')
        txt = scrolledtext.ScrolledText(w, font=("Segoe UI", 10))
        txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        txt.insert('1.0', help_text)
        txt.config(state='disabled')

    def show_shortcuts(self):
        text = (
            'Keyboard Shortcuts:\n\n'
            'Ctrl+O  — Add CSV files\n'
            'Ctrl+F  — Add folder\n'
            'Ctrl+P  — Preview\n'
            'Ctrl+M  — Merge\n'
            'Ctrl+S  — Save settings\n'
        )
        messagebox.showinfo('Shortcuts', text)

    def report_issue(self):
        # open a browser to a placeholder issues page or mailto link
        try:
            import webbrowser
            webbrowser.open('https://github.com/your-repo/csvmerger/issues')
        except Exception:
            messagebox.showinfo('Report', 'Please report issues at https://github.com/your-repo/csvmerger/issues')

    def open_output_folder(self):
        path = self.output_dir.get() or ''
        if not path:
            messagebox.showwarning('No folder', 'No output folder selected')
            return
        try:
            if os.name == 'nt':
                os.startfile(path)
            else:
                subprocess.run(['open' if os.name == 'darwin' else 'xdg-open', path])
        except Exception as e:
            messagebox.showerror('Error', f'Could not open folder: {e}')
    
    def update_recent_list(self):
        """Update recent files list"""
        self.recent_listbox.delete(0, tk.END)
        for item in self.recent_files:
            self.recent_listbox.insert(tk.END, f"{item['timestamp']}: {item['output_path']}")
    
    def generate_preview(self):
        """Generate a preview of the merged dataset (applies current config)."""
        if not self.selected_files:
            messagebox.showwarning("Warning", "Select files first")
            return

        try:
            self.preview_text.config(state='normal')
            self.preview_text.delete('1.0', tk.END)
            self.preview_text.insert('1.0', "Generating merged preview...\n")
            self.preview_text.config(state='disabled')
            self.root.update()

            dfs = []
            for f in self.selected_files:
                try:
                    with open(f, 'rb') as fh:
                        raw = fh.read()
                        enc = chardet.detect(raw).get('encoding') or 'utf-8'
                    df = pd.read_csv(f, encoding=enc)
                    df = self.apply_column_selection_and_mapping(df, f)
                    df = self.apply_filters_to_df(df)
                    df = self.handle_missing_data(df)
                    dfs.append(df)
                except Exception as e:
                    # Log but continue
                    self.log_to_app(f"Failed to read {f.name} for preview: {e}\n")
                    continue

            if not dfs:
                messagebox.showerror("Error", "No data available for preview (all reads failed)")
                return

            # Create merged sample
            merged = pd.concat(dfs, ignore_index=True, sort=False)

            # Apply sorting if requested (preview mirrors final behavior)
            if self.sort_option.get() == 'date':
                # detect a date column
                date_cols = [c for c in merged.columns if 'date' in c.lower() or 'time' in c.lower()]
                if date_cols:
                    try:
                        merged[date_cols[0]] = pd.to_datetime(merged[date_cols[0]], errors='coerce')
                        merged = merged.sort_values(by=date_cols[0]).reset_index(drop=True)
                    except Exception:
                        pass
            elif self.sort_option.get() == 'custom' and self.sort_column.get() in merged.columns:
                try:
                    asc = self.sort_order.get() == 'ascending'
                    merged = merged.sort_values(by=self.sort_column.get(), ascending=asc).reset_index(drop=True)
                except Exception:
                    pass

            # Show merged preview (first 20 rows)
            self.preview_text.config(state='normal')
            self.preview_text.delete('1.0', tk.END)
            header = f"Merged Preview ({len(self.selected_files)} files) - first 20 rows\n"
            header += "=" * 120 + "\n\n"
            self.preview_text.insert(tk.END, header)
            try:
                self.preview_text.insert(tk.END, merged.head(20).to_string())
            except Exception:
                # Fallback: show columns and row count
                self.preview_text.insert(tk.END, f"Columns: {list(merged.columns)}\nRows: {len(merged)}")

            footer = f"\n\nTotal rows (merged): {len(merged):,}\nTotal columns: {len(merged.columns)}\n"
            self.preview_text.insert(tk.END, footer)
            self.preview_text.config(state='disabled')

        except Exception as e:
            messagebox.showerror("Error", f"Could not generate preview: {e}")
    
    def show_statistics(self):
        """Show data statistics"""
        if not self.selected_files:
            messagebox.showwarning("Warning", "Select files first")
            return
        
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Data Statistics")
        stats_window.geometry("700x600")
        
        text_widget = scrolledtext.ScrolledText(stats_window, width=80, height=30, font=("Courier New", 9))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        stats = "DATA STATISTICS\n" + "="*80 + "\n\n"
        
        total_rows = 0
        for file in self.selected_files:
            try:
                df = pd.read_csv(file)
                total_rows += len(df)
                
                stats += f"File: {file.name}\n"
                stats += f"  Rows: {len(df)}\n"
                stats += f"  Columns: {len(df.columns)}\n"
                stats += f"  Column Names: {', '.join(df.columns)}\n"
                stats += f"  Data Types:\n"
                for col, dtype in df.dtypes.items():
                    stats += f"    {col}: {dtype}\n"
                stats += f"  Missing Values:\n"
                for col in df.columns:
                    missing = df[col].isna().sum()
                    if missing > 0:
                        stats += f"    {col}: {missing}\n"
                stats += "\n"
            except Exception as e:
                stats += f"Error reading {file.name}: {e}\n\n"
        
        stats += f"\nTOTAL ROWS (all files): {total_rows}\n"
        
        text_widget.insert('1.0', stats)
        text_widget.config(state='disabled')
    
    # -----------------
    # Merge helpers
    # -----------------
    def apply_filters_to_df(self, df):
        for f in self.filters:
            try:
                if f['operator'] == '==':
                    df = df[df[f['column']] == f['value']]
                elif f['operator'] == '!=':
                    df = df[df[f['column']] != f['value']]
                elif f['operator'] == '>':
                    df = df[df[f['column']] > float(f['value'])]
                elif f['operator'] == '<':
                    df = df[df[f['column']] < float(f['value'])]
                elif f['operator'] == '>=':
                    df = df[df[f['column']] >= float(f['value'])]
                elif f['operator'] == '<=':
                    df = df[df[f['column']] <= float(f['value'])]
                elif f['operator'] == 'contains':
                    df = df[df[f['column']].astype(str).str.contains(f['value'], na=False)]
            except Exception:
                continue
        return df

    def apply_column_selection_and_mapping(self, df, file_path):
        # If selected_columns configured, use them (selection stored per-file)
        sel = []
        if self.selected_columns:
            sel = self.selected_columns.get(str(file_path), [])
        if sel:
            cols = [c for c in sel if c in df.columns]
            df = df.loc[:, cols]

        # Apply mapping
        if self.column_mapping:
            rename_map = {k: v for k, v in self.column_mapping.items() if k in df.columns}
            if rename_map:
                df = df.rename(columns=rename_map)
        return df

    def handle_missing_data(self, df):
        s = self.missing_data_strategy
        if s == 'drop':
            return df.dropna()
        if s == 'zero':
            return df.fillna(0)
        if s == 'na':
            return df.fillna('N/A')
        if s == 'ffill':
            return df.fillna(method='ffill')
        if s == 'bfill':
            return df.fillna(method='bfill')
        return df

    def start_merge(self):
        if not self.selected_files:
            messagebox.showwarning('Warning', 'Select at least one CSV file to merge')
            return
        # run merge in background
        thread = threading.Thread(target=self.perform_merge_and_export, args=(list(self.selected_files),))
        thread.daemon = True
        thread.start()
        self.update_status('Merging...')

    def perform_merge_and_export(self, files):
        self.log_to_app('=== Merge started ===\n')
        try:
            dfs = []
            date_columns = set()
            for i, f in enumerate(files, 1):
                try:
                    with open(f, 'rb') as fh:
                        raw = fh.read()
                        enc = chardet.detect(raw).get('encoding') or 'utf-8'
                    df = pd.read_csv(f, encoding=enc)
                    df = self.apply_column_selection_and_mapping(df, f)
                    df = self.apply_filters_to_df(df)
                    df = self.handle_missing_data(df)
                    dfs.append(df)
                    for col in df.columns:
                        if 'date' in col.lower() or 'time' in col.lower():
                            date_columns.add(col)
                    self.log_to_app(f"{i}. Loaded {f.name}: rows={len(df)}, cols={len(df.columns)}\n")
                except Exception as e:
                    self.log_to_app(f"{i}. Failed to read {f.name}: {e}\n")
                    continue

            if not dfs:
                self.log_to_app('No dataframes loaded, aborting merge.\n')
                return

            # Merge
            if self.merge_type.get() == 'concatenate':
                merged = pd.concat(dfs, ignore_index=True, sort=False)
            else:
                # simple join sequence using first file as base
                merged = dfs[0]
                left_col = self.join_column_left.get() or None
                right_col = self.join_column_right.get() or None
                for other in dfs[1:]:
                    try:
                        merged = merged.merge(other, left_on=left_col, right_on=right_col, how='outer')
                    except Exception as e:
                        self.log_to_app(f'Join failed between frames: {e}\n')

                # Duplicate column strategies
                try:
                    dup_names = [name for name in merged.columns if list(merged.columns).count(name) > 1]
                    if dup_names:
                        strategy = self.duplicate_strategy.get()
                        self.log_to_app(f'Duplicate columns detected: {set(dup_names)} (strategy={strategy})\n')
                        if strategy == 'keep_all':
                            # rename duplicates to keep all but make unique names by suffixing occurrence index
                            counts = {}
                            new_cols = []
                            for col in merged.columns:
                                cnt = counts.get(col, 0)
                                if list(merged.columns).count(col) > 1:
                                    new_name = f"{col}_{cnt}"
                                    counts[col] = cnt + 1
                                    new_cols.append(new_name)
                                else:
                                    new_cols.append(col)
                            merged.columns = new_cols
                        elif strategy in ('first', 'last'):
                            to_drop = []
                            cols = list(merged.columns)
                            for name in set(dup_names):
                                positions = [i for i, c in enumerate(cols) if c == name]
                                if strategy == 'first':
                                    keep_idx = positions[0]
                                    drop_idxs = positions[1:]
                                else:
                                    keep_idx = positions[-1]
                                    drop_idxs = positions[:-1]
                                drop_cols = [cols[i] for i in drop_idxs]
                                to_drop.extend(drop_cols)
                            if to_drop:
                                merged = merged.drop(columns=to_drop)
                                self.log_to_app(f'Dropped duplicate columns: {to_drop}\n')
                        elif strategy == 'merge':
                            # For each duplicate name, concatenate non-null unique values per row (separated by ' | ')
                            cols = list(merged.columns)
                            for name in set(dup_names):
                                positions = [i for i, c in enumerate(cols) if c == name]
                                dup_cols = [cols[i] for i in positions]
                                try:
                                    def merge_row_values(row):
                                        vals = [str(v) for v in row if pd.notna(v)]
                                        # unique preserving order
                                        seen = []
                                        out = []
                                        for v in vals:
                                            if v not in seen:
                                                seen.append(v)
                                                out.append(v)
                                        return ' | '.join(out) if out else pd.NA

                                    merged[name] = merged[dup_cols].apply(merge_row_values, axis=1)
                                    # drop other duplicate columns except the first occurrence
                                    drop_cols = dup_cols[1:]
                                    merged = merged.drop(columns=drop_cols)
                                    self.log_to_app(f'Merged duplicate columns for: {name} -> kept {dup_cols[0]}\n')
                                except Exception as e:
                                    self.log_to_app(f'Failed to merge duplicate columns for {name}: {e}\n')
                except Exception as e:
                    self.log_to_app(f'Error handling duplicate columns: {e}\n')

            # Duplicate rows removal if requested
            if getattr(self, 'remove_duplicate_rows', None) and self.remove_duplicate_rows.get():
                keep = getattr(self, 'duplicate_row_keep', None) and self.duplicate_row_keep.get() or 'first'
                try:
                    before = len(merged)
                    merged = merged.drop_duplicates(keep=keep).reset_index(drop=True)
                    after = len(merged)
                    self.log_to_app(f'Removed duplicate rows: before={before}, after={after}\n')
                except Exception as e:
                    self.log_to_app(f'Could not remove duplicate rows: {e}\n')

            # Sorting
            if self.sort_option.get() == 'date' and date_columns:
                date_col = list(date_columns)[0]
                try:
                    merged[date_col] = pd.to_datetime(merged[date_col], errors='coerce')
                    merged = merged.sort_values(by=date_col).reset_index(drop=True)
                    self.log_to_app(f'Sorted by detected date column: {date_col}\n')
                except Exception as e:
                    self.log_to_app(f'Could not sort by date column: {e}\n')
            elif self.sort_option.get() == 'custom' and self.sort_column.get():
                col = self.sort_column.get()
                if col in merged.columns:
                    asc = self.sort_order.get() == 'ascending'
                    try:
                        merged = merged.sort_values(by=col, ascending=asc).reset_index(drop=True)
                        self.log_to_app(f'Sorted by column {col} ({"asc" if asc else "desc"})\n')
                    except Exception as e:
                        self.log_to_app(f'Could not sort by {col}: {e}\n')

            # Export
            out_fmt = self.export_format.get()
            output_filename = self.output_filename.get() or 'merged_data'
            # choose output dir: user-selected folder if provided, else first file's parent
            out_dir = Path(self.output_dir.get()) if self.output_dir.get() else files[0].parent
            if isinstance(out_dir, str):
                out_dir = Path(out_dir)
            if not out_dir.exists():
                try:
                    out_dir.mkdir(parents=True, exist_ok=True)
                except Exception:
                    out_dir = files[0].parent
            if out_fmt == 'csv':
                out_path = out_dir / (output_filename if output_filename.endswith('.csv') else output_filename + '.csv')
                merged.to_csv(out_path, index=False)
            elif out_fmt == 'tsv':
                out_path = out_dir / (output_filename if output_filename.endswith('.tsv') else output_filename + '.tsv')
                merged.to_csv(out_path, index=False, sep='\t')
            elif out_fmt == 'excel':
                out_path = out_dir / (output_filename if output_filename.endswith('.xlsx') else output_filename + '.xlsx')
                merged.to_excel(out_path, index=False)
            elif out_fmt == 'json':
                out_path = out_dir / (output_filename if output_filename.endswith('.json') else output_filename + '.json')
                merged.to_json(out_path, orient='records', date_format='iso')
            else:
                out_path = out_dir / (output_filename + '.csv')
                merged.to_csv(out_path, index=False)

            self.log_to_app(f'Exported merged file to: {out_path}\n')
            self.log_to_app(f'Total rows: {len(merged):,}, Total columns: {len(merged.columns)}\n')

            # Save recent
            try:
                self.recent_files.insert(0, {'timestamp': datetime.now().isoformat(), 'output_path': str(out_path), 'rows': len(merged)})
                self.save_recent_files()
                self.update_recent_list()
            except:
                pass

        except Exception as e:
            self.log_to_app(f'Error during merge: {e}\n')
        finally:
            self.log_to_app('=== Merge finished ===\n')
            try:
                self.update_status('Ready')
            except Exception:
                pass

    def log_to_app(self, message):
        """Write log messages to preview_text and batch_text areas"""
        try:
            # preview_text exists; append log there
            if hasattr(self, 'preview_text'):
                self.preview_text.config(state='normal')
                self.preview_text.insert(tk.END, message)
                self.preview_text.see(tk.END)
                self.preview_text.config(state='disabled')
            # also append to batch_text if available
            if hasattr(self, 'batch_text'):
                self.batch_text.config(state='normal')
                self.batch_text.insert(tk.END, message)
                self.batch_text.see(tk.END)
                self.batch_text.config(state='disabled')
        except Exception:
            pass


def main():
    # If ttkbootstrap is available, use tb.Window for a modern look
    if USE_TTB and tb is not None:
        root = tb.Window(themename='flatly')
    else:
        root = tk.Tk()
    app = AdvancedCSVMergerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
