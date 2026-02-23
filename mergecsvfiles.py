import os
import pandas as pd
from pathlib import Path


def merge_csv_files(directory_path, output_filename='merged_data.csv'):
    """
    Merges multiple CSV files from a directory into a single CSV file.
    
    Parameters:
    -----------
    directory_path : str
        Path to the directory containing CSV files
    output_filename : str
        Name of the output merged CSV file (default: 'merged_data.csv')
    
    Returns:
    --------
    bool
        True if successful, False otherwise
    """
    
    try:
        # Convert to Path object for better path handling
        dir_path = Path(directory_path)
        
        # Validate directory exists
        if not dir_path.exists() or not dir_path.is_dir():
            print(f"Error: Directory '{directory_path}' does not exist.")
            return False
        
        # Find all CSV files in the directory
        csv_files = list(dir_path.glob('*.csv'))
        
        if not csv_files:
            print(f"No CSV files found in '{directory_path}'")
            return False
        
        print(f"Found {len(csv_files)} CSV file(s) to merge:")
        for file in csv_files:
            print(f"  - {file.name}")
        
        # Read all CSV files
        dataframes = []
        date_columns = set()
        
        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file)
                
                # Detect potential date columns
                for col in df.columns:
                    if 'date' in col.lower() or 'time' in col.lower():
                        date_columns.add(col)
                
                dataframes.append(df)
                print(f"✓ Loaded: {csv_file.name} ({len(df)} rows, {len(df.columns)} columns)")
            except Exception as e:
                print(f"✗ Error reading {csv_file.name}: {e}")
                continue
        
        if not dataframes:
            print("No CSV files could be loaded successfully.")
            return False
        
        # Rename duplicate columns
        all_columns = {}
        for df in dataframes:
            for col in df.columns:
                if col not in all_columns:
                    all_columns[col] = 1
                else:
                    all_columns[col] += 1
        
        # Create a mapping for duplicate columns
        duplicate_cols = {col: count for col, count in all_columns.items() if count > 1}
        
        # Rename duplicate columns in each dataframe
        for i, df in enumerate(dataframes):
            col_counter = {}
            for col in df.columns:
                if col in duplicate_cols:
                    if col not in col_counter:
                        col_counter[col] = 0
                    else:
                        col_counter[col] += 1
                    
                    # Only rename from the second occurrence onwards
                    if col_counter[col] > 0:
                        new_col_name = f"{col}_{i}"
                        df.rename(columns={col: new_col_name}, inplace=True)
        
        # Merge all dataframes
        print("\nMerging data...")
        merged_df = pd.concat(dataframes, ignore_index=True, sort=False)
        
        # Sort by date columns if detected
        if date_columns:
            for date_col in list(date_columns)[:1]:  # Use the first date column found
                if date_col in merged_df.columns:
                    try:
                        merged_df[date_col] = pd.to_datetime(merged_df[date_col])
                        merged_df = merged_df.sort_values(by=date_col).reset_index(drop=True)
                        print(f"✓ Sorted by date column: {date_col}")
                    except Exception as e:
                        print(f"⚠ Could not sort by {date_col}: {e}")
        
        # Save merged file
        output_path = dir_path / output_filename
        merged_df.to_csv(output_path, index=False)
        
        print(f"\n✓ Successfully merged {len(csv_files)} CSV files")
        print(f"✓ Output file: {output_path}")
        print(f"  - Total rows: {len(merged_df)}")
        print(f"  - Total columns: {len(merged_df.columns)}")
        
        return True
    
    except Exception as e:
        print(f"Error during merge operation: {e}")
        return False


def main():
    """Main function to run the script"""
    import sys
    
    print("=" * 60)
    print("CSV FILE MERGER")
    print("=" * 60)
    
    # Get directory path from command-line arguments or user input
    if len(sys.argv) > 1:
        directory_path = sys.argv[1]
        output_filename = sys.argv[2] if len(sys.argv) > 2 else 'merged_data.csv'
    else:
        # Get user input
        directory_path = input("\nEnter the directory path containing CSV files: ").strip()
        output_filename = input("Enter output filename (default: merged_data.csv): ").strip()
        
        if not output_filename:
            output_filename = 'merged_data.csv'
    
    # Run merge operation
    success = merge_csv_files(directory_path, output_filename)
    
    if success:
        print("\n✓ Merge completed successfully!")
    else:
        print("\n✗ Merge operation failed.")


if __name__ == "__main__":
    main()