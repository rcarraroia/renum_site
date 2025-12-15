"""
Fix SICC column names to match real database schema
Sprint 10 - SICC Implementation
"""

import re

# Mapping of old names to new names
MEMORY_MAPPINGS = {
    'memory_type': 'chunk_type',
    'confidence': 'confidence_score',
    'access_count': 'usage_count',
    # Remove: importance (doesn't exist in DB)
}

BEHAVIOR_MAPPINGS = {
    'trigger_conditions': 'trigger_context',
    'actions': 'action_config',
    'usage_count': 'total_applications',
    'successful_uses': 'successful_applications',
    # Remove: pattern_name, description, version, confidence
}

print("="*60)
print("FIXING SICC COLUMN NAMES")
print("="*60)

# Files to update
files_to_update = [
    'src/models/sicc/memory.py',
    'src/models/sicc/behavior.py',
    'src/services/sicc/memory_service.py',
    'src/services/sicc/behavior_service.py',
]

for filepath in files_to_update:
    print(f"\nProcessing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply mappings based on file type
        if 'memory' in filepath:
            for old, new in MEMORY_MAPPINGS.items():
                # Replace in various contexts
                content = re.sub(rf'\b{old}\b', new, content)
                content = content.replace(f'"{old}"', f'"{new}"')
                content = content.replace(f"'{old}'", f"'{new}'")
        
        if 'behavior' in filepath:
            for old, new in BEHAVIOR_MAPPINGS.items():
                content = re.sub(rf'\b{old}\b', new, content)
                content = content.replace(f'"{old}"', f'"{new}"')
                content = content.replace(f"'{old}'", f"'{new}'")
        
        # Write back if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Updated")
        else:
            print(f"  ⏭️  No changes needed")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")

print("\n" + "="*60)
print("✅ COLUMN NAMES FIXED")
print("="*60)
print("\nNext: Manually review and test the changes")
