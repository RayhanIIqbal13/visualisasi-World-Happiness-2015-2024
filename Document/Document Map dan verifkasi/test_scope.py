#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test if COUNTRY_NAME_MAPPING is accessible in halaman_country function
"""

import sys
sys.path.insert(0, r'd:\Kampus ITK\ABD\Tugas Besar - ABD 8 v2')

# Check if COUNTRY_NAME_MAPPING is defined at module level
import ast
import inspect

with open(r'd:\Kampus ITK\ABD\Tugas Besar - ABD 8 v2\app_whr.py', 'r') as f:
    content = f.read()

# Find line numbers
lines = content.split('\n')
for i, line in enumerate(lines[220:280], start=220):
    if 'COUNTRY_NAME_MAPPING' in line:
        print(f"Line {i}: {line}")

print("\n\nSearching for style_function definition:")
for i, line in enumerate(lines[873:885], start=873):
    print(f"Line {i}: {line}")
