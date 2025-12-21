"""
Task 2: Create database migration scripts
Migration for existing RENUS/ISA configurations to unified structure
"""

from supabase import create_client
import os
import json
from datetime import datetime

# Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def backup_agents_table():
    """Create backup of agents table before migration"""
    print("📦 Creating backup of agents table...")
    
    agents = supabase.table('agents').select('*').execute()
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'backup_agents_{timestamp}.json'
    
    with open(backup_file, 'w') as f:
        json.dump(agents.data, f, indent=2, default=str)
    
    print(f"✅ Backup created: {backup_file}")
    return backup_file

def migrate_config_jsonb():
    """
    Migrate config JSONB from old structure to new 9-category structure
    Old: { "identity": {...}, "sicc": {...}, "model": "...", ... }
    New: { "instructions": {...}, "intelligence": {...}, ... }
    """
    print("🔄 Migrating config JSONB structure...")
    
    # Get all agents
    agents = supabase.table('agents').select('*').execute()
    
    for agent in agents.data:
        old_config = agent.get('config', {})
        
        # Build new config structure
        new_config = {
            "instructions": {
                "system_prompt": old_config.get('identity', {}).get('system_prompt', '') or old_config.get('system_prompt', ''),
                "persona": old_config.get('identity', {}).get('persona', ''),
                "capabilities": old_config.get('identity', {}).get('capabilities', ''),
                "limitations": old_config.get('identity', {}).get('limitations', ''),
                "welcome_message": old_config.get('identity', {}).get('welcome_message', '')
            },
            "intelligence": {
                "model": old_config.get('model', 'gpt-4o-mini'),
                "provider": old_config.get('provider', 'openai'),
                "temperature": old_config.get('temperature', 0.7),
                "max_tokens": old_config.get('max_tokens', 2000),
                "sicc": old_config.get('sicc', {"enabled": False})
            },
            "tools": {
                "enabled_tools": old_config.get('tools', [])
            },
            "integrations": {},
            "knowledge": {},
            "triggers": {},
            "guardrails": {},
            "sub_agents": {},
            "advanced": {}
        }
        
        # Update agent with new config
        supabase.table('agents').update({
            'config': new_config,
            'updated_at': datetime.now().isoformat()
        }).eq('id', agent['id']).execute()
        
        print(f"✅ Migrated config for agent: {agent['name']}")
    
    print("✅ Config migration complete")

def validate_migration():
    """Validate data integrity after migration"""
    print("🔍 Validating migration...")
    
    agents = supabase.table('agents').select('*').execute()
    
    for agent in agents.data:
        config = agent.get('config', {})
        
        # Check new structure exists
        assert 'instructions' in config, f"Missing 'instructions' in {agent['name']}"
        assert 'intelligence' in config, f"Missing 'intelligence' in {agent['name']}"
        
        # Check system_prompt preserved
        system_prompt = config['instructions'].get('system_prompt')
        assert system_prompt, f"System prompt lost in {agent['name']}"
        
        print(f"✅ Validated: {agent['name']}")
    
    print("✅ Validation complete")

def rollback_migration(backup_file):
    """Rollback migration using backup file"""
    print(f"⏪ Rolling back migration from {backup_file}...")
    
    with open(backup_file, 'r') as f:
        backup_data = json.load(f)
    
    for agent in backup_data:
        supabase.table('agents').update({
            'config': agent['config']
        }).eq('id', agent['id']).execute()
    
    print("✅ Rollback complete")

if __name__ == '__main__':
    print("🚀 Starting migration...")
    
    # Step 1: Backup
    backup_file = backup_agents_table()
    
    # Step 2: Migrate
    migrate_config_jsonb()
    
    # Step 3: Validate
    validate_migration()
    
    print(f"""
✅ Migration completed successfully!

Backup file: {backup_file}
To rollback: python backend/scripts/rollback_migration.py {backup_file}
""")
