import pandas as pd
import numpy as np

# Load your data
df = pd.read_csv('Wk45_sold_dateflags.csv')  # or .xlsx, etc.

# ── Geographic Data Checks ────────────────────────────────────────────────────

# California bounding box (approximate)
CA_LAT_MIN, CA_LAT_MAX = 32.5, 42.0
CA_LON_MIN, CA_LON_MAX = -124.5, -114.0


# Flag 1: Missing coordinates (Latitude or Longitude is null)
df['missing_coords_flag'] = df['Latitude'].isna() | df['Longitude'].isna()

# Flag 2: Sentinel null values (Lat = 0 or Lon = 0)
df['zero_coords_flag'] = (df['Latitude'] == 0) | (df['Longitude'] == 0)

# Flag 3: Longitude > 0 (California longitudes must be negative)
df['positive_longitude_flag'] = df['Longitude'] > 0

# Flag 4: Out-of-state or implausible coordinates
df['out_of_state_flag'] = (
    (df['Latitude']  < CA_LAT_MIN) | (df['Latitude']  > CA_LAT_MAX) |
    (df['Longitude'] < CA_LON_MIN) | (df['Longitude'] > CA_LON_MAX)
)

# ── Combined: any geographic issue ───────────────────────────────────────────
df['geo_issue_flag'] = (
    df['missing_coords_flag']   |
    df['zero_coords_flag']      |
    df['positive_longitude_flag'] |
    df['out_of_state_flag']
)

# ── Summary ───────────────────────────────────────────────────────────────────
print("missing_coords_flag:    ", df['missing_coords_flag'].sum())
print("zero_coords_flag:       ", df['zero_coords_flag'].sum())
print("positive_longitude_flag:", df['positive_longitude_flag'].sum())
print("out_of_state_flag:      ", df['out_of_state_flag'].sum())
print("geo_issue_flag (any):   ", df['geo_issue_flag'].sum())

# ── Inspect bad rows ──────────────────────────────────────────────────────────
bad_geo = df[df['geo_issue_flag'] == True]
print(bad_geo[['Latitude', 'Longitude', 'missing_coords_flag', 
               'zero_coords_flag', 'positive_longitude_flag', 'out_of_state_flag']])

df.to_csv('Wk45_sold_geoflags_final.csv')
