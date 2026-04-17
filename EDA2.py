import pandas as pd

filtered_null_listings = pd.read_csv("null_CRMLSListing_202401_to_202603.csv")
filtered_null_sold = pd.read_csv("null_CRMLSSold_202401_to_202603.csv")

# Numeric distribution summary for ClosePrice, LivingArea, and DaysOnMarket
print("ClosePrice summary (listings):", filtered_null_listings["ClosePrice"].describe())
print("LivingArea summary (listings):", filtered_null_listings["LivingArea"].describe())
print("DaysOnMarket summary (listings):", filtered_null_listings["DaysOnMarket"].describe())

print("ClosePrice summary (sold):", filtered_null_sold["ClosePrice"].describe())
print("LivingArea summary (sold):", filtered_null_sold["LivingArea"].describe())
print("DaysOnMarket summary (sold):", filtered_null_sold["DaysOnMarket"].describe())