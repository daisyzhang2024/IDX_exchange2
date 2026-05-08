import pandas as pd

combined_listing = pd.read_csv("combined_CRMLSListing_202401_to_202604.csv")
combined_sold = pd.read_csv("combined_CRMLSSold_202401_to_202604.csv")

# Filter residential
res_listing = pd.read_csv("res_CRMLSListing_202401_to_202604.csv")
res_sold = pd.read_csv("res_CRMLSSold_202401_to_202604.csv")

# Inspect structure
print(combined_listing.columns)
print(combined_listing.head())
print(combined_sold.columns)
print(combined_sold.head())

# Check property categories (unique properties deliverable)
print(combined_listing['PropertyType'].unique())
print(combined_sold['PropertyType'].unique())

# Validate completeness (null table deliverable)
print(combined_listing.isnull().sum())
print(combined_sold.isnull().sum())

# Missing value report deliverable
listing_nulls = pd.DataFrame({
    'null_count': combined_listing.isnull().sum(),
    'null_rate': combined_listing.isnull().sum() / len(combined_listing)
})

sold_nulls = pd.DataFrame({
    'null_count': combined_sold.isnull().sum(),
    'null_rate': combined_sold.isnull().sum() / len(combined_sold)
})

flag_listing = listing_nulls[listing_nulls["null_rate"] > 0.9]
flag_sold = sold_nulls[sold_nulls["null_rate"] > 0.9]
print(flag_listing)
print(flag_sold)
flag_listing_cols = flag_listing.index.tolist()
flag_sold_cols = flag_sold.index.tolist()
print("Flagged columns (listing)", flag_listing_cols)
print("Flagged columns (sold)", flag_sold_cols)

# Filter for nulls, save in new CSV
wanted_cols_listing = set(combined_listing.columns) - set(flag_listing_cols)
wanted_cols_sold = set(combined_sold.columns) - set(flag_sold_cols)
null_filter_listing = combined_listing[list(wanted_cols_listing)]
null_filter_sold = combined_sold[list(wanted_cols_sold)]
print(null_filter_listing)
print(null_filter_sold)
null_filter_listing.to_csv("null_CRMLSListing_202401_to_202604.csv")
null_filter_sold.to_csv("null_CRMLSSold_202401_to_202604.csv")