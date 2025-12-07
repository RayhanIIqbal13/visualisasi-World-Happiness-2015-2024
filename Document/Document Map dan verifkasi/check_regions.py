#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Check what regions are in the database
"""

import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "iqbal",
    "database": "world_happines_v2"
}

conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

# Get all regions
cursor.execute("SELECT DISTINCT region_name FROM region ORDER BY region_name")
regions = cursor.fetchall()

print("Regions in database:")
print("="*70)
for i, (region,) in enumerate(regions, 1):
    print(f"{i:2}. {region}")

conn.close()

# Check which regions are missing from color_map
color_map_regions = {
    'Western Europe',
    'Central and Eastern Europe',
    'Northern Europe',
    'Southern Europe',
    'Western Asia',
    'Middle East and North Africa',
    'Sub-Saharan Africa',
    'South Asia',
    'Southeast Asia',
    'East Asia',
    'Latin America and Caribbean',
    'North America',
    'Australia and New Zealand'
}

db_regions = set(r[0] for r in regions)

print("\n\nRegions in database but NOT in color_map:")
print("="*70)
missing = db_regions - color_map_regions
if missing:
    for region in sorted(missing):
        print(f"  - {region}")
else:
    print("  (None - all regions covered)")

print("\n\nRegions in color_map but NOT in database:")
print("="*70)
extra = color_map_regions - db_regions
if extra:
    for region in sorted(extra):
        print(f"  - {region}")
else:
    print("  (None - all colors have corresponding regions)")
