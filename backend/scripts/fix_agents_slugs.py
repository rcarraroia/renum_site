
import asyncio
import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH para importar módulos src
backend_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(backend_dir))

from src.config.supabase import supabase_admin

async def fix_agents_slugs():
    """
    Atualiza os slugs dos agentes RENUS e ISA se estiverem faltando.
    """
    print("🔍 Iniciando verificação de slugs dos agentes RENUS e ISA...")
    
    # 1. Corrigir RENUS
    try:
        print("➡️  Verificando RENUS...")
        # Buscar agente RENUS
        response = supabase_admin.table('agents').select('*').eq('name', 'RENUS').execute()
        
        if response.data:
            renus_agent = response.data[0]
            print(f"   Encontrado agente RENUS (ID: {renus_agent['id']})")
            
            if not renus_agent.get('slug'):
                print("   ⚠️  Slug está vazio. Atualizando para 'renus'...")
                update = await asyncio.to_thread(
                    lambda: supabase_admin.table('agents').update({'slug': 'renus'}).eq('id', renus_agent['id']).execute()
                )
                print("   ✅ Slug do RENUS atualizado com sucesso!")
            else:
                print(f"   ✅ Slug já configurado: {renus_agent['slug']}")
        else:
            print("   ❌ Agente RENUS não encontrado no banco de dados.")

    except Exception as e:
        print(f"   ❌ Erro ao processar RENUS: {e}")

    # 2. Corrigir ISA
    try:
        print("\n➡️  Verificando ISA...")
        # Buscar agente ISA
        response = supabase_admin.table('agents').select('*').eq('name', 'ISA').execute()
        
        if response.data:
            isa_agent = response.data[0]
            print(f"   Encontrado agente ISA (ID: {isa_agent['id']})")
            
            if not isa_agent.get('slug'):
                print("   ⚠️  Slug está vazio. Atualizando para 'isa'...")
                update = await asyncio.to_thread(
                     lambda: supabase_admin.table('agents').update({'slug': 'isa'}).eq('id', isa_agent['id']).execute()
                )
                print("   ✅ Slug do ISA atualizado com sucesso!")
            else:
                print(f"   ✅ Slug já configurado: {isa_agent['slug']}")
        else:
            print("   ❌ Agente ISA não encontrado no banco de dados.")

    except Exception as e:
        print(f"   ❌ Erro ao processar ISA: {e}")

    print("\n🏁 Processo concluído.")

if __name__ == "__main__":
    asyncio.run(fix_agents_slugs())
