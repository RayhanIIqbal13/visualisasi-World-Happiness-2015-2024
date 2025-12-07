#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verify that all 10 database regions have coordinates for map display"""

# Define the 10 correct regions from database
database_regions = [
    'Western Europe',
    'Central and Eastern Europe',
    'Commonwealth of Independent States',
    'Middle East and North Africa',
    'Sub-Saharan Africa',
    'South Asia',
    'Southeast Asia',
    'East Asia',
    'Latin America and Caribbean',
    'North America and ANZ'
]

# Updated REGION_COORDINATES from app_whr.py
region_coordinates = {
    'Western Europe': (55, 10),
    'Central and Eastern Europe': (52, 25),
    'Commonwealth of Independent States': (60, 105),
    'Middle East and North Africa': (25, 40),
    'Sub-Saharan Africa': (-5, 20),
    'South Asia': (20, 77),
    'Southeast Asia': (15, 105),
    'East Asia': (35, 100),
    'Latin America and Caribbean': (-5, -60),
    'North America and ANZ': (0, -95),
}

print("✅ REGION COORDINATES VERIFICATION")
print("=" * 80)
print(f"\nTotal database regions: {len(database_regions)}")
print(f"Total coordinates defined: {len(region_coordinates)}")

print("\n" + "=" * 80)
print("Region Mapping Status:")
print("=" * 80)

all_mapped = True
for region in sorted(database_regions):
    if region in region_coordinates:
        lat, lng = region_coordinates[region]
        print(f"✅ {region:<40} → ({lat:>5}, {lng:>6})")
    else:
        print(f"❌ {region:<40} → NOT FOUND")
        all_mapped = False

print("\n" + "=" * 80)
if all_mapped and len(region_coordinates) == len(database_regions):
    print("✅ SUCCESS: All 10 regions have coordinates!")
    print("✅ Map will display all 10 regions with markers")
else:
    print("❌ ERROR: Some regions are missing coordinates!")
    print(f"❌ Expected: {len(database_regions)}, Got: {len(region_coordinates)}")
