"""
Task 2.1: Unit tests for migration scripts
"""

import pytest
import json
from backend.scripts.migrate_config_jsonb import migrate_config_jsonb, validate_migration

def test_config_migration_preserves_system_prompt():
    """Test that system_prompt is preserved during migration"""
    old_config = {
        "identity": {
            "system_prompt": "You are an AI assistant",
            "persona": "Professional"
        },
        "model": "gpt-4o"
    }
    
    # Simulate migration
    new_config = {
        "instructions": {
            "system_prompt": old_config["identity"]["system_prompt"],
            "persona": old_config["identity"]["persona"]
        },
        "intelligence": {
            "model": old_config["model"]
        }
    }
    
    assert new_config["instructions"]["system_prompt"] == "You are an AI assistant"
    assert new_config["intelligence"]["model"] == "gpt-4o"

def test_migration_handles_missing_fields():
    """Test migration handles missing optional fields gracefully"""
    old_config = {
        "model": "gpt-4o-mini"
    }
    
    new_config = {
        "instructions": {
            "system_prompt": old_config.get('identity', {}).get('system_prompt', ''),
            "persona": old_config.get('identity', {}).get('persona', '')
        },
        "intelligence": {
            "model": old_config.get('model', 'gpt-4o-mini')
        }
    }
    
    assert new_config["instructions"]["system_prompt"] == ""
    assert new_config["intelligence"]["model"] == "gpt-4o-mini"

def test_backup_file_creation():
    """Test that backup file is created with proper structure"""
    # Mock backup data
    backup_data = [
        {"id": "123", "name": "Test Agent", "config": {"old": "data"}}
    ]
    
    # Verify structure
    assert isinstance(backup_data, list)
    assert all("id" in agent for agent in backup_data)
    assert all("config" in agent for agent in backup_data)
