#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test Country Name Mapping
=========================

Script ini memverifikasi bahwa semua negara yang mismatched sekarang memiliki mapping
dan dapat ditemukan dengan benar di database.
"""

import json
import requests
import psycopg2
from psycopg2.extras import RealDictCursor

# Database configuration (hardcoded since config_whr imports streamlit)
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "iqbal",
    "database": "world_happines_v2"
}

# ============ COUNTRY NAME MAPPING ============
COUNTRY_NAME_MAPPING = {
    # North America
    'United States': 'United States of America',
    'Trinidad & Tobago': 'Trinidad and Tobago',
    
    # Europe
    'Czechia': 'Czech Republic',
    'North Macedonia': 'Macedonia',
    'Serbia': 'Republic of Serbia',
    'Turkiye': 'Turkey',
    'North Cyprus': 'Northern Cyprus',
    
    # Western Asia / Middle East
    'Palestinian Territories': 'West Bank',
    'State of Palestine': 'West Bank',
    
    # Africa
    'Argelia': 'Algeria',
    'Congo (Kinshasa)': 'Democratic Republic of the Congo',
    'Congo (Brazzaville)': 'Republic of the Congo',
    'Somaliland region': 'Somaliland',
    
    # Asia
    'Taiwan Province of China': 'Taiwan',
    
    # Special cases
    'Eswatini': 'Swaziland',
    'Tanzania': 'United Republic of Tanzania',
}

# ============ DOWNLOAD GEOJSON ============
print("Downloading GeoJSON data...")
geojson_url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json'
response = requests.get(geojson_url)
geojson_data = response.json()

# Extract GeoJSON country names
geojson_countries = set()
for feature in geojson_data['features']:
    country_name = feature['properties'].get('name', '')
    if country_name:
        geojson_countries.add(country_name)

print(f"GeoJSON countries loaded: {len(geojson_countries)} countries")

# ============ QUERY DATABASE ============
print("\nQuerying database for all countries...")
try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        SELECT DISTINCT c.country_name, r.region_name 
        FROM country c
        LEFT JOIN region r ON c.region_id = r.region_id
        ORDER BY c.country_name
    """)
    db_countries = cursor.fetchall()
    conn.close()
    
    print(f"Database countries loaded: {len(db_countries)} countries")
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit(1)

# ============ TEST MAPPING ============
print("\n" + "="*70)
print("TESTING COUNTRY NAME MAPPING")
print("="*70)

mapped_successfully = 0
failed_mapping = []

for country in db_countries:
    db_name = country['country_name']
    region = country['region_name']
    
    # Get GeoJSON name from mapping
    if db_name in COUNTRY_NAME_MAPPING:
        geojson_name = COUNTRY_NAME_MAPPING[db_name]
    else:
        geojson_name = db_name
    
    # Check if GeoJSON name exists
    if geojson_name in geojson_countries:
        mapped_successfully += 1
        print(f"[OK] {db_name:40} -> {geojson_name:40} [{region}]")
    else:
        failed_mapping.append({
            'db_name': db_name,
            'geojson_name': geojson_name,
            'region': region
        })
        print(f"[FAIL] {db_name:40} -> {geojson_name:40} NOT FOUND!")

# ============ SUMMARY ============
print("\n" + "="*70)
print("MAPPING TEST SUMMARY")
print("="*70)
print(f"Successfully mapped: {mapped_successfully}/{len(db_countries)}")
print(f"Failed mapping: {len(failed_mapping)}")

if failed_mapping:
    print("\nFailed mappings:")
    for failed in failed_mapping:
        print(f"  - {failed['db_name']} ({failed['region']})")
        print(f"    Attempted mapping: {failed['geojson_name']}")
else:
    print("\nSUCCESS! All countries mapped correctly!")

print("\n" + "="*70)
