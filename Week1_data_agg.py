import pandas as pd
import glob
import os

# df_1 = pd.read_csv("CRMLSSold202602.csv")
# print(df_1.head())
# print(df_1.columns)
# print(df_1.describe())

# 1. Set your range
start_range = 202401
end_range = 202604

# 2. Get all matching CSV files
def combine_files(string_desc):  # string is "Listing" or "Sold"
    all_files = glob.glob(f'CRMLS{string_desc}*.csv')
    # 3. Filter files based on the numbers in their names
    files_to_combine = []
    for f in all_files:
        # This extracts the digits (YYYYMM) from the filename
        # e.g., 'CRMLSListing202405.csv' -> '202405'
        date_part = ''.join(filter(str.isdigit, f))
        
        if date_part:
            date_val = int(date_part)
            if start_range <= date_val <= end_range:
                files_to_combine.append(f)
    # Sort them so they are combined in chronological order
    files_to_combine.sort()
    # 4. Combine and Export
    if files_to_combine:
        print(f"Combining {len(files_to_combine)} files...")
        combined_df = pd.concat([pd.read_csv(f) for f in files_to_combine])
        
        output_name = f"combined_CRMLS{string_desc}_{start_range}_to_{end_range}.csv"
        combined_df.to_csv(output_name, index=False)
        print(f"Done! Saved as {output_name}")
    else:
        print("No files found within that specific range.")

combine_files("Listing")
combine_files("Sold")