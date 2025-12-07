import json

# Load the mapping from app_whr.py
COUNTRY_NAME_MAPPING = {
    'United States': 'United States of America',
    'Trinidad & Tobago': 'Trinidad and Tobago',
    'Czechia': 'Czech Republic',
    'North Macedonia': 'Macedonia',
    'Serbia': 'Republic of Serbia',
    'Turkiye': 'Turkey',
    'North Cyprus': 'Northern Cyprus',
    'Palestinian Territories': 'West Bank',
    'State of Palestine': 'West Bank',
    'Argelia': 'Algeria',
    'Congo (Kinshasa)': 'Democratic Republic of the Congo',
    'Congo (Brazzaville)': 'Republic of the Congo',
    'Democratic Republic of the Congo': 'Democratic Republic of the Congo',
    'Republic of the Congo': 'Republic of the Congo',
    'Somaliland region': 'Somaliland',
    'Taiwan Province of China': 'Taiwan',
    'Eswatini': 'Swaziland',
    'Tanzania': 'United Republic of Tanzania',
}

# Test the Congo countries
congo_names = [
    'Democratic Republic of the Congo',
    'Republic of the Congo',
    'Congo (Kinshasa)',
    'Congo (Brazzaville)'
]

print("Congo Countries Mapping Test:")
print("=" * 80)
for name in congo_names:
    if name in COUNTRY_NAME_MAPPING:
        geojson_name = COUNTRY_NAME_MAPPING[name]
        print(f"✅ {name}")
        print(f"   → Maps to: {geojson_name}")
    else:
        print(f"❌ {name} - NOT IN MAPPING")
    print()

print("=" * 80)
print("\nVerifying all JSON files have correct Congo names:")
print("=" * 80)

import os
for year in range(2015, 2025):
    file_path = f"Data/Json/world_happiness_{year}.json"
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            congo_found = []
            for entry in data:
                if 'congo' in entry['country_name'].lower():
                    congo_found.append(entry['country_name'])
            
            if congo_found:
                print(f"{year}: {', '.join(set(congo_found))}")
            else:
                print(f"{year}: No Congo found")
