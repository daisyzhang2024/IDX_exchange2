import pandas as pd
import numpy as np

# Load your data
df = pd.read_csv('Wk6_sold_features.csv')  # or .xlsx, etc.

# Dataset size and median values before outlier removal
print("Dataset shape before outlier removal:", df.shape)
print("Median ClosePrice before outlier removal:", df['ClosePrice'].median())
print("Median LivingArea before outlier removal:", df['LivingArea'].median())
print("Median DaysOnMarket before outlier removal:", df['DaysOnMarket'].median())

# ── Column Checks ────────────────────────────────────────────────────

# printing columns
print("Columns in the dataset:")
print(df.columns.tolist())

# Flag extreme values (ClosePrice < 0, LivingArea < 0, DaysOnMarket < 0)
df['ClosePrice_extreme'] = df['ClosePrice'] < 0
df['LivingArea_extreme'] = df['LivingArea'] < 0
df['DaysOnMarket_extreme'] = df['DaysOnMarket'] < 0

# Flag outlier columns (ClosePrice, LivingArea, DaysOnMarket)
outlier_columns = ['ClosePrice', 'LivingArea', 'DaysOnMarket']
for col in outlier_columns:
    if col in df.columns:
        # Calculate IQR
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        # Define outlier thresholds
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Flag outliers
        df[f'{col}_outlier_flag'] = (df[col] < lower_bound) | (df[col] > upper_bound)
        
        print(f"{col} outliers: {df[f'{col}_outlier_flag'].sum()}")
    else:
        print(f"Column {col} not found in dataset.")

df.to_csv('Wk7_sold_outliers_flagged.csv')

# Separate filtered dataset with outliers and extreme values removed
df_filtered = df[~(df['ClosePrice_outlier_flag'] | df['LivingArea_outlier_flag'] | df['DaysOnMarket_outlier_flag'] | df['ClosePrice_extreme'] | df['LivingArea_extreme'] | df['DaysOnMarket_extreme'])]
print("Shape after removing outliers and extreme values:", df_filtered.shape)
df_filtered.to_csv('Wk7_sold_outliers_removed.csv')

# Dataset size and median values after outlier removal
print("Dataset shape after outlier removal:", df_filtered.shape)
print("Median ClosePrice after outlier removal:", df_filtered['ClosePrice'].median())
print("Median LivingArea after outlier removal:", df_filtered['LivingArea'].median())
print("Median DaysOnMarket after outlier removal:", df_filtered['DaysOnMarket'].median())