"""
Script para corrigir current_user.get() em todos os arquivos
"""
import os
import re

files_to_fix = [
    "src/api/routes/sub_agents.py",
    "src/api/routes/renus_config.py",
    "src/api/routes/tools.py",
]

for filepath in files_to_fix:
    print(f"Corrigindo {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Substituir current_user.get("role") por current_user.role
    content = content.replace('current_user.get("role")', 'current_user.role')
    
    # Substituir current_user.get("id") por current_user.id
    content = content.replace('current_user.get("id")', 'current_user.id')
    
    # Substituir current_user.get("client_id") por getattr(current_user, "client_id", None)
    content = content.replace('current_user.get("client_id")', 'getattr(current_user, "client_id", None)')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ {filepath} corrigido")

print("\n✅ Todos os arquivos corrigidos!")
