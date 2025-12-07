#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path

json_dir = Path("d:\\Kampus ITK\\ABD\\Tugas Besar - ABD 8 v2\\Data\\Json")

print("Verification - Jamaica entries in all files:")
print("="*70)

for json_file in sorted(json_dir.glob("world_happiness_*.json")):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    jamaica_entries = [x for x in data if x.get('country_name') == 'Jamaica']
    year = json_file.stem.split('_')[-1]
    
    if jamaica_entries:
        for entry in jamaica_entries:
            region = entry.get('region_name')
            ranking = entry.get('ranking')
            print(f"{year}: Jamaica - Region: {region}, Ranking: {ranking}")
    else:
        print(f"{year}: No Jamaica found")
