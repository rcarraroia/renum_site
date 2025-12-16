"""
Script de Teste Simplificado - SICC Integration (Fase 7)
Cria memorias de teste para os agentes de sistema (RENUS e ISA)
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime

# Load environment
load_dotenv()

# Configuracao Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    print("[ERRO] Variaveis de ambiente SUPABASE_URL ou SUPABASE_SERVICE_ROLE_KEY nao configuradas")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# IDs dos Agentes Sistema 
RENUS_ID = '00000000-0000-0000-0000-000000000001'
ISA_ID = '00000000-0000-0000-0000-000000000002'

# Client ID (buscar dinamicamente)
try:
    client_result = supabase.table('clients').select('id').limit(1).execute()
    CLIENT_ID = client_result.data[0]['id'] if client_result.data else None
except Exception as e:
    print(f"[AVISO] Nao foi possivel buscar client_id: {e}")
    CLIENT_ID = None

def criar_memorias_teste():
    """Cria memorias de teste para RENUS e ISA"""
    
    print("Criando memorias de teste para SICC Integration...")
    print(f"RENUS ID: {RENUS_ID}")
    print(f"ISA ID: {ISA_ID}")
    print(f"Client ID: {CLIENT_ID}")
    print()
    
    # Memorias para RENUS (Orquestrador)
    memorias_renus = [
        {
            'agent_id': RENUS_ID,
            'client_id': CLIENT_ID,
            'chunk_type': 'faq',
            'content': 'Cliente interessado em agentes para clinicas odontologicas geralmente pergunta sobre integracao com sistemas de agendamento e prontuarios eletronicos.',
            'metadata': {
                'source': 'interview',
                'topic': 'healthcare',
                'sentiment': 'positive',
                'keywords': ['clinica', 'odontologia', 'integracao', 'agendamento']
            },
            'source': 'conversation',
            'confidence_score': 0.92,
            'usage_count': 15,
            'last_used_at': datetime.now().isoformat(),
            'version': 1,
            'is_active': True
        },
        {
            'agent_id': RENUS_ID,
            'client_id': CLIENT_ID,
            'chunk_type': 'pattern',
            'content': 'Padrao identificado: Quando cliente menciona "multi-nivel" ou "MMN", o sub-agente Discovery MMN deve ser acionado automaticamente.',
            'metadata': {
                'source': 'isa_analysis',
                'confidence': 0.95,
                'trigger_keywords': ['mmn', 'multi-nivel', 'rede', 'distribuidor']
            },
            'source': 'isa_analysis',
            'confidence_score': 0.95,
            'usage_count': 8,
            'version': 1,
            'is_active': True
        }
    ]
    
    # Memorias para ISA (Supervisor)
    memorias_isa = [
        {
            'agent_id': ISA_ID,
            'client_id': CLIENT_ID,
            'chunk_type': 'insight',
            'content': 'Analise detectou que 78% das queries sobre "banco de dados" sao relacionadas a performance. Recomendacao: criar FAQ dedicado para otimizacao de queries.',
            'metadata': {
                'analysis_type': 'pattern_detection',
                'confidence': 0.87,
                'recommendation': 'create_faq',
                'data_source': 'command_history'
            },
            'source': 'isa_analysis',
            'confidence_score': 0.87,
            'usage_count': 3,
            'version': 1,
            'is_active': True
        },
        {
            'agent_id': ISA_ID,
            'client_id': CLIENT_ID,
            'chunk_type': 'process',
            'content': 'Processo de backup automatico de memorias: executar snapshot toda sexta as 23h, manter ultimos 7 snapshots, comprimir snapshots mais antigos.',
            'metadata': {
                'process_type': 'automation',
                'schedule': 'weekly',
                'retention': 7
            },
            'source': 'manual',
            'confidence_score': 1.0,
            'usage_count': 0,
            'version': 1,
            'is_active': True
        }
    ]
    
    # Inserir memorias no banco
    try:
        # RENUS
        print("Inserindo memorias para RENUS...")
        for mem in memorias_renus:
            result = supabase.table('agent_memory_chunks').insert(mem).execute()
            if result.data:
                print(f"   [OK] Memoria criada: {mem['chunk_type']} - {mem['content'][:50]}...")
            else:
                print(f"   [FALHA] Nao foi possivel criar memoria: {mem['chunk_type']}")
        
        # ISA
        print("\nInserindo memorias para ISA...")
        for mem in memorias_isa:
            result = supabase.table('agent_memory_chunks').insert(mem).execute()
            if result.data:
                print(f"   [OK] Memoria criada: {mem['chunk_type']} - {mem['content'][:50]}...")
            else:
                print(f"   [FALHA] Nao foi possivel criar memoria: {mem['chunk_type']}")
        
        print("\n[SUCESSO] Memorias de teste criadas!")
        
    except Exception as e:
        print(f"[ERRO] Ao criar memorias: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def validar_memorias():
    """Valida que as memorias foram criadas corretamente"""
    
    print("\nValidando memorias criadas...")
    
    try:
        # Contar memorias do RENUS
        renus_memories = supabase.table('agent_memory_chunks')\
            .select('*', count='exact')\
            .eq('agent_id', RENUS_ID)\
            .execute()
        
        print(f"RENUS tem {renus_memories.count} memorias")
        
        # Contar memorias da ISA
        isa_memories = supabase.table('agent_memory_chunks')\
            .select('*', count='exact')\
            .eq('agent_id', ISA_ID)\
            .execute()
        
        print(f"ISA tem {isa_memories.count} memorias")
        
        # Mostrar tipos de chunk
        if renus_memories.data:
            print(f"\nTipos de memoria RENUS:")
            for mem in renus_memories.data:
                print(f"   - {mem['chunk_type']}: {mem['content'][:60]}...")
        
        if isa_memories.data:
            print(f"\nTipos de memoria ISA:")
            for mem in isa_memories.data:
                print(f"   - {mem['chunk_type']}: {mem['content'][:60]}...")
        
        # Validacao
        if renus_memories.count >= 2 and isa_memories.count >= 2:
            print("\n[VALIDACAO OK] Memorias criadas com sucesso!")
            return True
        else:
            print("\n[AVISO] Menos memorias do que esperado foram criadas")
            return False
            
    except Exception as e:
        print(f"[ERRO] Ao validar memorias: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    print("=" * 70)
    print("TESTE DE INTEGRACAO SICC - FASE 7")
    print("=" * 70)
    print()
    
    # Etapa 1: Criar memorias
    if criar_memorias_teste():
        # Etapa 2: Validar
        if validar_memorias():
            print("\n" + "=" * 70)
            print("[SUCESSO] TESTE CONCLUIDO COM SUCESSO!")
            print("=" * 70)
            exit(0)
        else:
            print("\n[AVISO] TESTE CONCLUIDO COM AVISOS")
            exit(1)
    else:
        print("\n[ERRO] TESTE FALHOU")
        exit(1)
