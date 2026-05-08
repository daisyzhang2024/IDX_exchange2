import pandas as pd
import numpy as np

# Load your data
df = pd.read_csv("null_CRMLSSold_202401_to_202604.csv")  # or .xlsx, etc.
print("Original Shape:", df.shape)
# Original Shape: (591733, 71) (Sold)
# Original Shape: (852963, 71) (Listing)

# ── 1. Convert date fields to datetime ──────────────────────────────────────
date_cols = ['CloseDate', 'PurchaseContractDate', 'ListingContractDate', 'ContractStatusChangeDate']

for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors='coerce')  # 'coerce' turns unparseable values into NaT


# ── 2. Remove unnecessary or redundant columns ──────────────────────────────
# First, inspect what you have:
print(df.columns.tolist())
print(df.nunique())          # columns with 1 unique value are useless
print(df.isnull().mean())    # columns with >80-90% nulls are often droppable

# Drop columns you've identified as redundant:
cols_to_drop = ['Column1', 'Column2']  # fill in after inspection
df = df.drop(columns=cols_to_drop, errors='ignore')


# ── 3. Handle missing values ─────────────────────────────────────────────────
# Numeric columns → fill with median (robust to outliers)
numeric_cols = df.select_dtypes(include='number').columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

# Categorical columns → fill with mode or a placeholder
cat_cols = df.select_dtypes(include='object').columns
for col in cat_cols:
    df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Unknown')

# Date columns → leave as NaT or drop rows if date is critical
# df = df.dropna(subset=['CloseDate'])  # uncomment if CloseDate must exist


# ── 4. Ensure numeric fields are properly typed ──────────────────────────────
numeric_to_cast = ['ClosePrice', 'LivingArea', 'DaysOnMarket', 'MainLevelBedrooms', 'BathroomsTotalInteger']

for col in numeric_to_cast:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')  # turns bad strings into NaN


# ── 5. Remove or flag invalid numeric values ─────────────────────────────────
# Option A: FLAG them (adds a boolean column, keeps the rows)
df['invalid_ClosePrice']   = df['ClosePrice'] <= 0
df['invalid_LivingArea']   = df['LivingArea'] <= 0
df['invalid_DaysOnMarket'] = df['DaysOnMarket'] < 0
df['invalid_Bedrooms']     = df['MainLevelBedrooms'] < 0
df['invalid_Bathrooms']    = df['BathroomsTotalInteger'] < 0

# Option B: REMOVE them (drops the rows outright)
df = df[df['ClosePrice'] > 0]
df = df[df['LivingArea'] > 0]
df = df[df['DaysOnMarket'] >= 0]
df = df[df['MainLevelBedrooms'] >= 0]
df = df[df['BathroomsTotalInteger'] >= 0]

# ── Save cleaned data ─────────────────────────────────────────────────────────
df.to_csv('cleaned_data_sold_Wk45.csv', index=False)
print("Done! Shape:", df.shape)
# Done! Shape: (591154, 76) (Sold)
# Done! Shape: (852072, 76) (Listing)

# Done! Shape: (615391, 76) (Sold with April data)
# Done! Shape: (891057, 76) (Listing with April data)
