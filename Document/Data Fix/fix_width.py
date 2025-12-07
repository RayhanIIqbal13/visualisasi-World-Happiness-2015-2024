#!/usr/bin/env python
"""Fix use_container_width to width parameter"""

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace use_container_width=True with width='stretch'
content = content.replace('use_container_width=True', "width='stretch'")
# Replace use_container_width=False with width='content'
content = content.replace('use_container_width=False', "width='content'")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Successfully replaced all use_container_width instances')
