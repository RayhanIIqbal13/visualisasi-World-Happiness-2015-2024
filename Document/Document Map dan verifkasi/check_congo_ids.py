import json
import os

# Check all JSON files for Congo entries
congo_data = {}

for year in range(2015, 2025):
    file_path = f"Data/Json/world_happiness_{year}.json"
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            congo_data[year] = []
            for entry in data:
                if 'congo' in entry['country_name'].lower():
                    congo_data[year].append({
                        'name': entry['country_name'],
                        'country_id': entry['country_id'],
                        'region': entry['region_name']
                    })

print("Congo Entries by Year:")
print("=" * 80)
for year in sorted(congo_data.keys()):
    print(f"\n{year}:")
    for entry in congo_data[year]:
        print(f"  - {entry['name']}: country_id={entry['country_id']}, region={entry['region']}")
