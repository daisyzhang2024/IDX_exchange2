import pandas as pd
import matplotlib.pyplot as plt

# combined_listing = pd.read_csv("combined_CRMLSListing_202401_to_202603.csv")
combined_sold = pd.read_csv("combined_CRMLSSold_202401_to_202603.csv")

# combined_listing['ClosePrice'].plot(kind='box')
# plt.title('Boxplot of ClosePrice (Listing)')
# plt.show()

# combined_listing_filter = combined_listing[combined_listing['ClosePrice'] < 2000000]
# combined_listing_filter['ClosePrice'].plot(kind='box')
# plt.title('Boxplot of ClosePrice (Listing with filter)')
# plt.show()

# combined_sold_filter = combined_sold[combined_sold['ClosePrice'] < 2000000]
# combined_sold_filter['ClosePrice'].plot(kind='box')
# plt.title('Boxplot of ClosePrice (Sold with filter)')
# plt.show()

combined_sold_filter = combined_sold[combined_sold['ClosePrice'] < 2000000]
combined_sold_filter['ClosePrice'].plot(kind='hist', bins=10)
plt.title('Histogram of ClosePrice (Sold with filter)')
plt.show()