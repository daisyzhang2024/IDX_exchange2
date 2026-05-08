import pandas as pd
import numpy as np

# Load your data
df = pd.read_csv('Wk45_listing_geoflags_final.csv')  # or .xlsx, etc.

# ── Column Checks ────────────────────────────────────────────────────

# printing columns
print("Columns in the dataset:")
print("ClosePrice" in df.columns.tolist())

# # See all columns with duplicates
# cols = df.columns.tolist()
# dupes = [c for c in cols if c.endswith('.1')]
# print("Columns with .1 suffix:", dupes)

# # Check if .1 version matches the original
# print(df[['ListPrice', 'ListPrice.1']].head())

df = df[[col for col in df.columns if not col.endswith('.1')]]
df = df.drop(columns=['Unnamed: 0.2', 'Unnamed: 0'], errors='ignore')

# Feature 1: Price Ratio (ClosePrice / ListPrice)
# measures negotiation strength
df['price_ratio'] = df['ClosePrice'] / df['ListPrice']

# Feature 2: Price per sq ft (ClosePrice / LivingArea)
# normalizes price across sizes
df['price_per_sqft'] = df['ClosePrice'] / df['LivingArea']

print(df[df['PurchaseContractDate'].notna()]['PurchaseContractDate'])

# Feature 3: Close Year, Close Month, Close YrMo
# Enables time-series analysis
df["CloseYear"] = df["CloseDate"].str[:4].astype(float)
df["CloseMonth"] = df["CloseDate"].str[5:7].astype(float)
df["CloseYrMo"] = df["CloseDate"].str[:7].str.replace("-", "").astype(float)

# Feature 4: Close to Original List Ratio (ClosePrice / OriginalListPrice)
# Captures full price reduction history
df['close_to_original_ratio'] = df['ClosePrice'] / df['OriginalListPrice']

# Feature 5: Listing to Contract Days (PurchaseContractDate - ListingContractDate)
# Measures time from listing to accepted offer
df['listing_to_contract_days'] = (
    pd.to_datetime(df['PurchaseContractDate'], errors='coerce') - 
    pd.to_datetime(df['ListingContractDate'], errors='coerce')
).dt.days

# Feature 6: Contract to Close Days (CloseDate - PurchaseContractDate)
# escrow and closing period duration
df['contract_to_close_days'] = (
    pd.to_datetime(df['CloseDate'], errors='coerce') - 
    pd.to_datetime(df['PurchaseContractDate'], errors='coerce')
).dt.days

# ── Segment Analysis ───────────────────────────────────────────
# group by PropertyType for summary statistics
segment_summary = df.groupby('PropertyType').agg({
    'price_ratio': ['mean', 'median', 'std'],
    'price_per_sqft': ['mean', 'median', 'std'],
    'DaysOnMarket': ['mean', 'median', 'std'],
    'close_to_original_ratio': ['mean', 'median', 'std'],
    'listing_to_contract_days': ['mean', 'median', 'std'],
    'contract_to_close_days': ['mean', 'median', 'std']
})
print("PropertyType Table:", segment_summary)

# group by PropertySubType for more granular insights
subtype_summary = df.groupby('PropertySubType').agg({
    'price_ratio': ['mean', 'median', 'std'],
    'price_per_sqft': ['mean', 'median', 'std'],
    'DaysOnMarket': ['mean', 'median', 'std'],
    'close_to_original_ratio': ['mean', 'median', 'std'],
    'listing_to_contract_days': ['mean', 'median', 'std'],
    'contract_to_close_days': ['mean', 'median', 'std']
})
print("PropertySubType Table:", subtype_summary)

# group by CountyOrParish for geographic insights
county_summary = df.groupby('CountyOrParish').agg({
    'price_ratio': ['mean', 'median', 'std'],
    'price_per_sqft': ['mean', 'median', 'std'],
    'DaysOnMarket': ['mean', 'median', 'std'],
    'close_to_original_ratio': ['mean', 'median', 'std'],
    'listing_to_contract_days': ['mean', 'median', 'std'],
    'contract_to_close_days': ['mean', 'median', 'std']
})
print("CountyOrParish Table:", county_summary)

# group by MLSAreaMajor for neighborhood-level insights
mls_summary = df.groupby('MLSAreaMajor').agg({
    'price_ratio': ['mean', 'median', 'std'],
    'price_per_sqft': ['mean', 'median', 'std'],
    'DaysOnMarket': ['mean', 'median', 'std'],
    'close_to_original_ratio': ['mean', 'median', 'std'],
    'listing_to_contract_days': ['mean', 'median', 'std'],
    'contract_to_close_days': ['mean', 'median', 'std']
})
print("MLSAreaMajor Table:", mls_summary)

# group by ListOfficeName for agent-level insights
agent_summary = df.groupby('ListOfficeName').agg({
    'price_ratio': ['mean', 'median', 'std'],
    'price_per_sqft': ['mean', 'median', 'std'],
    'DaysOnMarket': ['mean', 'median', 'std'],
    'close_to_original_ratio': ['mean', 'median', 'std'],
    'listing_to_contract_days': ['mean', 'median', 'std'],
    'contract_to_close_days': ['mean', 'median', 'std']
})
print("ListOfficeName Table:", agent_summary)

# group by BuyerOfficeName for buyer agent insights
buyer_agent_summary = df.groupby('BuyerOfficeName').agg({
    'price_ratio': ['mean', 'median', 'std'],
    'price_per_sqft': ['mean', 'median', 'std'],
    'DaysOnMarket': ['mean', 'median', 'std'],
    'close_to_original_ratio': ['mean', 'median', 'std'],
    'listing_to_contract_days': ['mean', 'median', 'std'],
    'contract_to_close_days': ['mean', 'median', 'std']
})
print("BuyerOfficeName Table:", buyer_agent_summary)

# ── Sample Output Table ───────────────────────────────────────────────────────────────────
sample_output = df[['ClosePrice', 'ListPrice', 'price_ratio', 'price_per_sqft', 'DaysOnMarket', 
                    'CloseYear', 'CloseMonth', 'CloseYrMo', 'close_to_original_ratio',
                    'listing_to_contract_days', 'contract_to_close_days']].head(10)
print("Sample Output Table:", sample_output)

# # ── Inspect bad rows ──────────────────────────────────────────────────────────
# bad_geo = df[df['geo_issue_flag'] == True]
# print(bad_geo[['Latitude', 'Longitude', 'missing_coords_flag', 
#                'zero_coords_flag', 'positive_longitude_flag', 'out_of_state_flag']])

# df.to_csv('Wk45_sold_geoflags.csv')
