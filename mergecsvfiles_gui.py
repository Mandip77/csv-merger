import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import pandas as pd
import threading


class CSVMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV File Merger Pro")
        self.root.geometry("950x1000")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Set icon if available
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        self.selected_files = []  # List of Path objects for selected CSV files
        self.output_filename = tk.StringVar(value='merged_data.csv')
        self.sort_option = tk.StringVar(value='date')
        self.sort_column = tk.StringVar(value='')
        self.sort_order = tk.StringVar(value='ascending')
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create GUI widgets with professional styling"""
        
        # Main container with padding
        main_container = ttk.Frame(self.root, padding="15")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # ===== HEADER SECTION =====
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            header_frame,
            text="CSV File Merger Pro",
            font=("Segoe UI", 16, "bold")
        )
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Select multiple CSV files from any directory and merge them",
            font=("Segoe UI", 10),
            foreground="gray"
        )
        subtitle_label.pack(side=tk.LEFT, padx=(15, 0))
        
        # ===== FILE SELECTION SECTION =====
        file_select_frame = ttk.LabelFrame(main_container, text="Step 1: Select CSV Files", padding="10")
        file_select_frame.pack(fill=tk.X, pady=(0, 15))
        
        btn_container = ttk.Frame(file_select_frame)
        btn_container.pack(fill=tk.X)
        
        add_files_btn = ttk.Button(
            btn_container,
            text="➕ Add CSV Files...",
            command=self.add_csv_files,
            width=20
        )
        add_files_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        add_folder_btn = ttk.Button(
            btn_container,
            text="📁 Add Folder (all CSV files)...",
            command=self.add_folder_files,
            width=25
        )
        add_folder_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_all_btn = ttk.Button(
            btn_container,
            text="🗑 Clear All",
            command=self.clear_all_files,
            width=12
        )
        clear_all_btn.pack(side=tk.LEFT)
        
        # ===== SELECTED FILES LIST =====
        files_frame = ttk.LabelFrame(main_container, text="Step 2: Selected CSV Files", padding="10")
        files_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # File list with scrollbar
        list_container = ttk.Frame(files_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.files_listbox = tk.Listbox(
            list_container,
            height=10,
            yscrollcommand=scrollbar.set,
            font=("Courier New", 9),
            bg='white',
            selectmode=tk.MULTIPLE
        )
        self.files_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.files_listbox.yview)
        self.files_listbox.bind('<Delete>', self.remove_selected_files)
        
        # File count label
        self.file_count_label = ttk.Label(
            files_frame,
            text="No files selected",
            foreground="gray",
            font=("Segoe UI", 9)
        )
        self.file_count_label.pack(anchor=tk.W, pady=(10, 0))
        
        info_label = ttk.Label(
            files_frame,
            text="Tip: Select files to remove and press Delete, or click 'Clear All' button",
            foreground="gray",
            font=("Segoe UI", 8)
        )
        info_label.pack(anchor=tk.W)
        
        # ===== SORTING OPTIONS SECTION =====
        sort_frame = ttk.LabelFrame(main_container, text="Step 3: Configure Sorting", padding="10")
        sort_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Sort option selection
        sort_option_frame = ttk.Frame(sort_frame)
        sort_option_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(sort_option_frame, text="Sort by:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Radiobutton(
            sort_option_frame,
            text="No sorting (keep original order)",
            variable=self.sort_option,
            value='none',
            command=self.update_sort_options
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Radiobutton(
            sort_option_frame,
            text="Auto-detect date column",
            variable=self.sort_option,
            value='date',
            command=self.update_sort_options
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Radiobutton(
            sort_option_frame,
            text="Custom column",
            variable=self.sort_option,
            value='custom',
            command=self.update_sort_options
        ).pack(side=tk.LEFT)
        
        # Column selection frame
        self.column_select_frame = ttk.Frame(sort_frame)
        self.column_select_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(self.column_select_frame, text="Column:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(0, 5))
        self.column_combo = ttk.Combobox(
            self.column_select_frame,
            textvariable=self.sort_column,
            state='readonly',
            width=30,
            font=("Segoe UI", 9)
        )
        self.column_combo.pack(side=tk.LEFT, padx=(0, 20))
        
        # Sort order
        ttk.Label(self.column_select_frame, text="Order:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Radiobutton(
            self.column_select_frame,
            text="Ascending",
            variable=self.sort_order,
            value='ascending'
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Radiobutton(
            self.column_select_frame,
            text="Descending",
            variable=self.sort_order,
            value='descending'
        ).pack(side=tk.LEFT)
        
        # Disable custom options initially
        self.update_sort_options()
        
        # ===== OUTPUT FILENAME SECTION =====
        output_frame = ttk.LabelFrame(main_container, text="Step 4: Output Configuration", padding="10")
        output_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(output_frame, text="Output filename:", font=("Segoe UI", 9)).pack(anchor=tk.W, pady=(0, 5))
        ttk.Entry(
            output_frame,
            textvariable=self.output_filename,
            width=60,
            font=("Segoe UI", 9)
        ).pack(fill=tk.X)
        
        # ===== STATUS SECTION =====
        status_frame = ttk.LabelFrame(main_container, text="Status & Log", padding="10")
        status_frame.pack(fill=tk.BOTH, expand=False, pady=(0, 15))
        
        # Text widget for output
        self.text_output = tk.Text(
            status_frame,
            height=5,
            width=100,
            state='disabled',
            bg='#f5f5f5',
            font=("Courier New", 8),
            relief=tk.FLAT,
            borderwidth=1
        )
        self.text_output.pack(fill=tk.BOTH, expand=True)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_container,
            mode='indeterminate',
            length=900
        )
        self.progress.pack(fill=tk.X, pady=(0, 15))
        
        # ===== ACTION BUTTONS =====
        btn_frame = ttk.Frame(main_container)
        btn_frame.pack(fill=tk.X)
        
        merge_btn = ttk.Button(
            btn_frame,
            text="▶ Merge Selected Files",
            command=self.merge_files,
            width=30
        )
        merge_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_log_btn = ttk.Button(
            btn_frame,
            text="📋 Clear Log",
            command=self.clear_output,
            width=15
        )
        clear_log_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        exit_btn = ttk.Button(
            btn_frame,
            text="✕ Exit",
            command=self.root.quit,
            width=10
        )
        exit_btn.pack(side=tk.RIGHT)
    
    
    def add_csv_files(self):
        """Open file dialog to select CSV files from any location"""
        files = filedialog.askopenfilenames(
            title="Select CSV files",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if files:
            for file in files:
                file_path = Path(file)
                if file_path not in self.selected_files:
                    self.selected_files.append(file_path)
            self.update_file_list()
            self.log_message(f"✓ Added {len(files)} file(s)\n")
            self.update_column_options()
    
    def add_folder_files(self):
        """Select a folder and add all CSV files from it"""
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
            self.log_message(f"✓ Added {added_count} file(s) from folder: {directory}\n")
            self.update_column_options()
    
    def update_file_list(self):
        """Update the listbox with selected files"""
        self.files_listbox.delete(0, tk.END)
        for file in self.selected_files:
            self.files_listbox.insert(tk.END, f"{file.name} ({file.parent})")
        
        count = len(self.selected_files)
        if count == 0:
            self.file_count_label.config(text="No files selected")
        elif count == 1:
            self.file_count_label.config(text="1 file selected")
        else:
            self.file_count_label.config(text=f"{count} files selected")
    
    def remove_selected_files(self, event=None):
        """Remove selected files from the list"""
        selected_indices = sorted(self.files_listbox.curselection(), reverse=True)
        
        if not selected_indices:
            messagebox.showinfo("Tip", "Please select file(s) to remove first")
            return
        
        for idx in selected_indices:
            self.selected_files.pop(idx)
        
        self.update_file_list()
        self.log_message(f"✓ Removed {len(selected_indices)} file(s)\n")
        self.update_column_options()
    
    def clear_all_files(self):
        """Clear all selected files"""
        if not self.selected_files:
            return
        
        self.selected_files.clear()
        self.update_file_list()
        self.log_message("✓ Cleared all files\n")
        self.update_column_options()
    
    def update_sort_options(self):
        """Enable/disable sort options based on selection"""
        sort_type = self.sort_option.get()
        
        if sort_type == 'custom':
            self.column_combo.config(state='readonly')
        else:
            self.column_combo.config(state='disabled')
    
    def update_column_options(self):
        """Update available columns for custom sorting"""
        if not self.selected_files:
            self.column_combo['values'] = []
            self.sort_column.set('')
            return
        
        try:
            # Read the first file to get column names
            df = pd.read_csv(self.selected_files[0])
            columns = list(df.columns)
            self.column_combo['values'] = columns
            
            if columns and not self.sort_column.get():
                self.sort_column.set(columns[0])
        except Exception as e:
            self.log_message(f"⚠ Could not read columns: {e}\n")
    
    def log_message(self, message):
        """Add message to text output"""
        self.text_output.config(state='normal')
        self.text_output.insert(tk.END, message)
        self.text_output.see(tk.END)
        self.text_output.config(state='disabled')
        self.root.update()
    
    def clear_output(self):
        """Clear the text output"""
        self.text_output.config(state='normal')
        self.text_output.delete('1.0', tk.END)
        self.text_output.config(state='disabled')
    
    def merge_files(self):
        """Merge selected CSV files in a separate thread"""
        if not self.selected_files:
            messagebox.showwarning("Warning", "Please select at least one CSV file to merge!")
            return
        
        # Run merge in background thread
        self.root.after(0, lambda: self._merge_thread(self.selected_files))
    
    def _merge_thread(self, selected_files):
        """Run merge in background thread"""
        thread = threading.Thread(target=self._perform_merge, args=(selected_files,))
        thread.daemon = True
        thread.start()
    
    def _perform_merge(self, selected_files):
        """Perform the actual merge operation"""
        self.progress.start()
        self.log_message("=" * 100 + "\n")
        self.log_message("Starting merge operation...\n\n")
        
        try:
            output_filename = self.output_filename.get() or 'merged_data.csv'
            sort_type = self.sort_option.get()
            sort_order = self.sort_order.get()
            custom_column = self.sort_column.get()
            
            self.log_message(f"📊 Files to merge: {len(selected_files)}\n")
            self.log_message(f"💾 Output: {output_filename}\n")
            self.log_message(f"📈 Sort type: {sort_type}\n")
            if sort_type == 'custom':
                self.log_message(f"📌 Sort column: {custom_column} ({sort_order})\n")
            self.log_message("\n")
            
            # Read all selected CSV files
            dataframes = []
            date_columns = set()
            
            for idx, csv_file in enumerate(selected_files, 1):
                try:
                    df = pd.read_csv(csv_file)
                    
                    # Detect date columns
                    for col in df.columns:
                        if 'date' in col.lower() or 'time' in col.lower():
                            date_columns.add(col)
                    
                    dataframes.append(df)
                    self.log_message(f"  {idx}. ✓ {csv_file.name} ({len(df)} rows, {len(df.columns)} cols)\n")
                except Exception as e:
                    self.log_message(f"  {idx}. ✗ {csv_file.name} - Error: {e}\n")
                    continue
            
            if not dataframes:
                self.log_message("\n❌ No CSV files could be loaded successfully.\n")
                self.progress.stop()
                messagebox.showerror("Error", "Failed to load CSV files.")
                return
            
            self.log_message("\n")
            
            # Handle duplicate columns
            all_columns = {}
            for df in dataframes:
                for col in df.columns:
                    all_columns[col] = all_columns.get(col, 0) + 1
            
            duplicate_cols = {col: count for col, count in all_columns.items() if count > 1}
            
            # Rename duplicates
            for i, df in enumerate(dataframes):
                col_counter = {}
                for col in df.columns:
                    if col in duplicate_cols:
                        col_counter[col] = col_counter.get(col, 0) + 1
                        if col_counter[col] > 1:
                            new_col_name = f"{col}_{i}"
                            df.rename(columns={col: new_col_name}, inplace=True)
            
            if duplicate_cols:
                self.log_message(f"⚠ Duplicate columns renamed: {', '.join(duplicate_cols.keys())}\n\n")
            
            # Merge dataframes
            self.log_message("🔄 Merging data...\n")
            merged_df = pd.concat(dataframes, ignore_index=True, sort=False)
            
            # Apply sorting based on user selection
            if sort_type == 'date' and date_columns:
                for date_col in list(date_columns)[:1]:
                    if date_col in merged_df.columns:
                        try:
                            merged_df[date_col] = pd.to_datetime(merged_df[date_col])
                            merged_df = merged_df.sort_values(by=date_col).reset_index(drop=True)
                            self.log_message(f"📅 Sorted by date column: {date_col}\n")
                        except Exception as e:
                            self.log_message(f"⚠ Could not sort by {date_col}: {e}\n")
            elif sort_type == 'date' and not date_columns:
                self.log_message(f"⚠ No date columns found, keeping original order\n")
            elif sort_type == 'custom' and custom_column:
                if custom_column in merged_df.columns:
                    try:
                        ascending = (sort_order == 'ascending')
                        merged_df = merged_df.sort_values(by=custom_column, ascending=ascending).reset_index(drop=True)
                        self.log_message(f"📌 Sorted by column '{custom_column}' ({sort_order})\n")
                    except Exception as e:
                        self.log_message(f"⚠ Could not sort by {custom_column}: {e}\n")
            else:
                self.log_message(f"⏭ Keeping original order (no sorting applied)\n")
            
            # Save merged file
            # Use the directory of the first file as output location
            output_path = selected_files[0].parent / output_filename
            merged_df.to_csv(output_path, index=False)
            
            self.log_message(f"\n✅ Successfully merged {len(selected_files)} CSV files\n")
            self.log_message(f"📍 Output file: {output_path}\n")
            self.log_message(f"   • Total rows: {len(merged_df):,}\n")
            self.log_message(f"   • Total columns: {len(merged_df.columns)}\n")
            self.log_message("\n" + "=" * 100 + "\n")
            self.log_message("✅ Merge completed successfully!\n")
            
            self.progress.stop()
            messagebox.showinfo(
                "Success",
                f"✅ Merge completed successfully!\n\n"
                f"Rows: {len(merged_df):,}\n"
                f"Columns: {len(merged_df.columns)}\n\n"
                f"Output file:\n{output_path}"
            )
            
        except Exception as e:
            self.log_message(f"\n❌ Error: {e}\n")
            self.progress.stop()
            messagebox.showerror("Error", f"An error occurred:\n{e}")
    
    def log_message(self, message):
        """Add message to text output"""
        self.text_output.config(state='normal')
        self.text_output.insert(tk.END, message)
        self.text_output.see(tk.END)
        self.text_output.config(state='disabled')
        self.root.update()
    
    def clear_output(self):
        """Clear the text output"""
        self.text_output.config(state='normal')
        self.text_output.delete('1.0', tk.END)
        self.text_output.config(state='disabled')


def main():
    root = tk.Tk()
    app = CSVMergerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
