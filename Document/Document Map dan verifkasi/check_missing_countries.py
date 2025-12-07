#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Find which database countries are missing from GeoJSON entirely
"""

import requests
import psycopg2

# Database config
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "iqbal",
    "database": "world_happines_v2"
}

# Get GeoJSON countries
print("Downloading GeoJSON...")
geojson_url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json'
response = requests.get(geojson_url)
geojson_data = response.json()
geojson_names = set(f['properties']['name'] for f in geojson_data['features'])

# Get DB countries
print("Querying database...")
conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT country_name FROM country ORDER BY country_name")
db_countries = [row[0] for row in cursor.fetchall()]
conn.close()

# Mapping dictionary
COUNTRY_NAME_MAPPING = {
    'United States': 'United States of America',
    'Trinidad & Tobago': 'Trinidad and Tobago',
    'Czechia': 'Czech Republic',
    'North Macedonia': 'Macedonia',
    'Serbia': 'Republic of Serbia',
    'Turkiye': 'Turkey',
    'Palestinian Territories': 'Palestine',
    'State of Palestine': 'Palestine',
    'Argelia': 'Algeria',
    'Comoros': 'Comoros',
    'Congo (Kinshasa)': 'Dem. Rep. Congo',
    'Congo (Brazzaville)': 'Congo',
    'Eswatini': 'Swaziland',
    'Mauritius': 'Mauritius',
    'Tanzania': 'United Republic of Tanzania',
    'Hong Kong': 'Hong Kong S.A.R.',
    'Hong Kong S.A.R. of China': 'Hong Kong S.A.R.',
    'Taiwan Province of China': 'Taiwan',
    'Maldives': 'Maldives',
    'Malta': 'Malta',
    'Singapore': 'Singapore',
    'North Cyprus': 'North Cyprus',
    'Somaliland region': 'Somalia',
}

print("\nCounting match success:")
print("="*70)

matched = 0
no_mapping = 0
missing_in_geojson = []

for db_name in db_countries:
    # Get GeoJSON name from mapping
    if db_name in COUNTRY_NAME_MAPPING:
        geojson_name = COUNTRY_NAME_MAPPING[db_name]
    else:
        geojson_name = db_name
        no_mapping += 1
    
    # Check if it exists in GeoJSON
    if geojson_name in geojson_names:
        matched += 1
    else:
        missing_in_geojson.append((db_name, geojson_name))

print(f"Successfully mapped: {matched}/175")
print(f"Missing from GeoJSON: {len(missing_in_geojson)}")
print(f"Without mapping applied: {no_mapping}")

if missing_in_geojson:
    print("\nCountries missing from GeoJSON file:")
    print("="*70)
    for db_name, geojson_name in sorted(missing_in_geojson):
        print(f"  {db_name:40} -> {geojson_name}")
