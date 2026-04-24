import pandas as pd
import numpy as np

# Load your data
df = pd.read_csv("cleaned_data_sold_Wk45.csv")  # or .xlsx, etc.

# ── Date Consistency Checks ───────────────────────────────────────────────────

# Make sure dates are already in datetime format (from previous step)
# df['CloseDate'] = pd.to_datetime(df['CloseDate'], errors='coerce')
# df['PurchaseContractDate'] = pd.to_datetime(df['PurchaseContractDate'], errors='coerce')
# df['ListingContractDate'] = pd.to_datetime(df['ListingContractDate'], errors='coerce')


# Flag 1: Listing date is AFTER close date (should be before)
df['listing_after_close_flag'] = df['ListingContractDate'] > df['CloseDate']

# Flag 2: Purchase contract date is AFTER close date (should be before)
df['purchase_after_close_flag'] = df['PurchaseContractDate'] > df['CloseDate']

# Flag 3: Any part of the timeline goes negative/backwards
# i.e. Listing → Purchase → Close order is violated anywhere
df['negative_timeline_flag'] = (
    (df['ListingContractDate'] > df['PurchaseContractDate']) |  # listing after purchase
    (df['ListingContractDate'] > df['CloseDate'])             |  # listing after close
    (df['PurchaseContractDate'] > df['CloseDate'])               # purchase after close
)


# ── Review how many violations exist ─────────────────────────────────────────
print("listing_after_close_flag:  ", df['listing_after_close_flag'].sum())
print("purchase_after_close_flag: ", df['purchase_after_close_flag'].sum())
print("negative_timeline_flag:    ", df['negative_timeline_flag'].sum())

# ── Optionally inspect the bad rows ──────────────────────────────────────────
bad_rows = df[df['negative_timeline_flag'] == True]
print(bad_rows[['ListingContractDate', 'PurchaseContractDate', 'CloseDate']])

df.to_csv('Wk45_sold_dateflags.csv')