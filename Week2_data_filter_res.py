import pandas as pd

combined_listing = pd.read_csv("combined_CRMLSListing_202401_to_202604.csv")
print("Row count listing (before)", len(combined_listing))
filtered_listing = combined_listing[combined_listing['PropertyType'] == "Residential"]
filtered_listing.to_csv("res_CRMLSListing_202401_to_202604.csv")
print("Row count listing (after)", len(filtered_listing))

combined_sold = pd.read_csv("combined_CRMLSSold_202401_to_202604.csv")
print("Row count sold (before)", len(combined_sold))
filtered_sold = combined_sold[combined_sold['PropertyType'] == "Residential"]
filtered_sold.to_csv("res_CRMLSSold_202401_to_202604.csv")
print("Row count sold (after)", len(filtered_sold))

# Row count listing (before) 852963
# Row count listing (after) 540183
# Row count sold (before) 591733
# Row count sold (after) 397603

# New data from April added
# Row count listing (before) 891983
# Row count listing (after) 566673
# Row count sold (before) 615994
# Row count sold (after) 414184