import pandas as pd
import glob
import os

# Counting row counts before concatenation
# 1. Set your range
start_range = 202401
end_range = 202603

# 2. Get all matching CSV files
def count_rows(string_desc):  # string is "Listing" or "Sold"
    all_files = glob.glob(f'CRMLS{string_desc}*.csv')
    # 3. Filter files based on the numbers in their names
    files_to_count = []
    row_counts = []
    for f in all_files:
        # This extracts the digits (YYYYMM) from the filename
        # e.g., 'CRMLSListing202405.csv' -> '202405'
        date_part = ''.join(filter(str.isdigit, f))
        
        if date_part:
            date_val = int(date_part)
            if start_range <= date_val <= end_range:
                files_to_count.append(f)
    # Sort them so they are combined in chronological order
    files_to_count.sort()
    # 4. Combine and Export
    if files_to_count:
        row_counts = [len(pd.read_csv(f)) for f in files_to_count]
    return row_counts

print("Individual row count (Listing)", count_rows("Listing"))
# Individual row count (Listing) [27454, 27447, 32282, 36503, 38796, 35893, 36340,
# 35305, 34625, 34730, 25128, 19417, 37469, 33983, 38492, 40187, 40271, 26399, 27345,
# 25210, 26923, 27586, 20677, 18773, 35302, 31409, 39017]
print("Sum (Listing)", sum(count_rows("Listing")))
# Sum (Listing) 852963
print("Individual row count (Sold)", count_rows("Sold"))
# Individual row count (Sold) [17976, 19925, 23276, 24640, 26487, 24328, 26240, 24558, 21267,
# 23274, 20279, 20241, 18738, 18702, 21445, 23262, 23154, 22883, 23646, 22972, 22443, 23233,
# 19088, 20538, 16487, 19106, 23545]
print("Sum (Sold)", sum(count_rows("Sold")))
# Sum (Sold) 591733

combined_listing = pd.read_csv('combined_CRMLSListing_202401_to_202603.csv')
combined_sold = pd.read_csv('combined_CRMLSSold_202401_to_202603.csv')
print("Combined row count (Listing)", len(combined_listing))
# Combined row count (Listing) 852963
print("Combined row count (Sold)", len(combined_sold))
# Combined row count (Sold) 591733
