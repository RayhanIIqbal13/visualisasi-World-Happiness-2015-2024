#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Remove Jamaica with East Asia region from all JSON files
"""

import json
from pathlib import Path

json_dir = Path("d:\\Kampus ITK\\ABD\\Tugas Besar - ABD 8 v2\\Data\\Json")

print("Removing Jamaica (East Asia) from all JSON files...")
print("="*70)

files_processed = 0
jamaica_removed = 0

for json_file in sorted(json_dir.glob("world_happiness_*.json")):
    # Load JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    original_count = len(data)
    
    # Filter out Jamaica with East Asia region
    filtered_data = [
        item for item in data 
        if not (item.get('country_name') == 'Jamaica' and item.get('region_name') == 'East Asia')
    ]
    
    removed_count = original_count - len(filtered_data)
    
    if removed_count > 0:
        # Save updated JSON
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(filtered_data, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] {json_file.name} - Removed {removed_count} Jamaica (East Asia) entry")
        jamaica_removed += removed_count
    else:
        print(f"[SKIP] {json_file.name} - No Jamaica (East Asia) found")
    
    files_processed += 1

print("\n" + "="*70)
print(f"Total files processed: {files_processed}")
print(f"Total Jamaica (East Asia) entries removed: {jamaica_removed}")
print("Done!")
