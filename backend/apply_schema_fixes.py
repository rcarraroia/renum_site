"""
Apply all schema fixes to match real database
Sprint 10 - SICC Implementation
"""

import re

print("="*60)
print("APPLYING SCHEMA FIXES")
print("="*60)

# Fix memory.py - remaining occurrences
print("\n[1/4] Fixing memory.py...")
with open('src/models/sicc/memory.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix remaining references
content = content.replace('MemoryType', 'ChunkType')
content = content.replace('access_count', 'usage_count')
content = content.replace('memory_type', 'chunk_type')

# Fix MemoryChunkResponse
content = re.sub(
    r'access_count: int = Field\(default=0, description="Number of times this memory was accessed"\)',
    'usage_count: int = Field(default=0, description="Number of times this memory was used")',
    content
)

with open('src/models/sicc/memory.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("  ✅ memory.py fixed")

# Fix memory_service.py
print("\n[2/4] Fixing memory_service.py...")
with open('src/services/sicc/memory_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace field names in service
replacements = [
    ('memory_type', 'chunk_type'),
    ('confidence', 'confidence_score'),
    ('access_count', 'usage_count'),
    ('MemoryType', 'ChunkType'),
]

for old, new in replacements:
    content = content.replace(f'"{old}"', f'"{new}"')
    content = content.replace(f"'{old}'", f"'{new}'")
    content = content.replace(f'.{old}', f'.{new}')
    content = content.replace(f'data.{old}', f'data.{new}')

# Remove importance field references
content = re.sub(r',\s*"importance":[^,}]+', '', content)
content = re.sub(r'importance[^,\n]+,?\n?', '', content)

# Add client_id to inserts
content = content.replace(
    '"agent_id": str(data.agent_id),',
    '"agent_id": str(data.agent_id),\n                "client_id": str(data.client_id),'
)

with open('src/services/sicc/memory_service.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("  ✅ memory_service.py fixed")

# Fix behavior.py
print("\n[3/4] Fixing behavior.py...")
with open('src/models/sicc/behavior.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove pattern_name and description fields
content = re.sub(r'pattern_name: str = Field\([^)]+\)\n\s*', '', content)
content = re.sub(r'description: str = Field\([^)]+\)\n\s*', '', content)

# Replace field names
replacements = [
    ('trigger_conditions', 'trigger_context'),
    ('actions', 'action_config'),
    ('usage_count', 'total_applications'),
    ('successful_uses', 'successful_applications'),
]

for old, new in replacements:
    content = content.replace(old, new)

# Remove version and confidence fields
content = re.sub(r'version: int = Field\([^)]+\)\n\s*', '', content)
content = re.sub(r'confidence: float = Field\([^)]+\)\n\s*', '', content)

with open('src/models/sicc/behavior.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("  ✅ behavior.py fixed")

# Fix behavior_service.py
print("\n[4/4] Fixing behavior_service.py...")
with open('src/services/sicc/behavior_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace field names
replacements = [
    ('trigger_conditions', 'trigger_context'),
    ('actions', 'action_config'),
    ('usage_count', 'total_applications'),
    ('successful_uses', 'successful_applications'),
    ('pattern_name', 'pattern_type'),  # Use pattern_type as identifier
]

for old, new in replacements:
    content = content.replace(f'"{old}"', f'"{new}"')
    content = content.replace(f"'{old}'", f"'{new}'")
    content = content.replace(f'.{old}', f'.{new}')

# Add client_id to inserts
content = content.replace(
    '"agent_id": str(data.agent_id),',
    '"agent_id": str(data.agent_id),\n                "client_id": str(data.client_id),'
)

# Remove version references
content = re.sub(r'"version":\s*\d+,?\n?\s*', '', content)
content = re.sub(r'version[^,\n]+,?\n?', '', content)

with open('src/services/sicc/behavior_service.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("  ✅ behavior_service.py fixed")

print("\n" + "="*60)
print("✅ ALL FIXES APPLIED")
print("="*60)
print("\nNext: Update __init__.py exports and run validation")
