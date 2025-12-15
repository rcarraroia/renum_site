#!/usr/bin/env python3
"""
Obter valores de enum reais do banco
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from config.supabase import supabase_admin

try:
    print("🔍 OBTENDO VALORES DE ENUM REAIS")
    print("=" * 40)
    
    # Chunk types
    chunk_types = supabase_admin.table('agent_memory_chunks').select('chunk_type').execute()
    unique_chunk_types = list(set(r['chunk_type'] for r in chunk_types.data if r['chunk_type']))
    print(f"📝 Chunk types: {sorted(unique_chunk_types)}")
    
    # Pattern types (se houver)
    pattern_types = supabase_admin.table('agent_behavior_patterns').select('pattern_type').execute()
    unique_pattern_types = list(set(r['pattern_type'] for r in pattern_types.data if r['pattern_type']))
    print(f"🎯 Pattern types: {sorted(unique_pattern_types)}")
    
    # Snapshot types
    snapshot_types = supabase_admin.table('agent_knowledge_snapshots').select('snapshot_type').execute()
    unique_snapshot_types = list(set(r['snapshot_type'] for r in snapshot_types.data if r['snapshot_type']))
    print(f"📸 Snapshot types: {sorted(unique_snapshot_types)}")
    
    print(f"\n✅ Valores obtidos com sucesso!")
    
except Exception as e:
    print(f"❌ Erro: {e}")