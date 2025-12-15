
import psycopg2
import os
import json
from dotenv import load_dotenv

# Carregar env se necessario, ou usar hardcoded validado
# DATABASE_URL = os.getenv('DATABASE_URL')
DATABASE_URL = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"

print(f"Conectando ao banco... {DATABASE_URL.split('@')[1]}")

conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = False

try:
    cursor = conn.cursor()
    
    print("🗑️  LIMPANDO DADOS ANTIGOS...")
    
    # Deletar tudo (órfãos mesmo)
    cursor.execute("DROP TABLE IF EXISTS sub_agents CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS renus_config CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS isa_commands CASCADE;")
    
    print("✓ Tabelas antigas removidas (sub_agents, renus_config, isa_commands)")
    
    print("\n🏗️  CRIANDO ESTRUTURA NOVA...")
    
    # Ler e executar migration
    with open('backend/migrations/20251213000000_unify_agents.sql', 'r', encoding='utf-8') as f:
        migration_sql = f.read()
    
    cursor.execute(migration_sql)
    
    print("✓ Tabela agents criada e agents de sistema/migrados inseridos via SQL")
    
    # Reforçar criação de AGENTES PADRÃO (caso o SQL tenha falhado ou para garantir os textos corretos)
    print("\n👥 VALIDANDO/ATUALIZANDO AGENTES PADRÃO...")
    
    # RENUS (Upsert para garantir descrição atualizada)
    cursor.execute("""
        INSERT INTO agents (id, role, name, description, config, sicc_enabled)
        VALUES (
            '00000000-0000-0000-0000-000000000001'::uuid,
            'system_orchestrator',
            'RENUS',
            'Orquestrador Global - Conduz entrevistas e qualifica leads',
            jsonb_build_object(
                'model', 'gpt-4o',
                'system_prompt', 'Você é o RENUS, orquestrador principal da plataforma RENUM. Conduz entrevistas de requisitos, qualifica leads e roteia conversas.',
                'temperature', 0.7,
                'max_tokens', 2000,
                'provider', 'openai',
                'tools', jsonb_build_array('supabase_query', 'whatsapp', 'email')
            ),
            true
        )
        ON CONFLICT (id) DO UPDATE SET
            description = EXCLUDED.description,
            config = EXCLUDED.config;
    """)
    print("  ✓ RENUS validado/atualizado")
    
    # ISA (Upsert)
    cursor.execute("""
        INSERT INTO agents (id, role, name, description, config, sicc_enabled)
        VALUES (
            '00000000-0000-0000-0000-000000000002'::uuid,
            'system_supervisor',
            'ISA',
            'Supervisora de Inteligência - Gerencia SICC e executa tarefas administrativas',
            jsonb_build_object(
                'model', 'gpt-4o',
                'system_prompt', 'Você é a ISA, assistente administrativa e supervisora de aprendizado do sistema RENUM. Analisa dados, executa comandos e gerencia o SICC.',
                'temperature', 0.3,
                'max_tokens', 4000,
                'provider', 'openai',
                'tools', jsonb_build_array('supabase_query', 'send_email', 'generate_report')
            ),
            true
        )
        ON CONFLICT (id) DO UPDATE SET
            description = EXCLUDED.description,
            config = EXCLUDED.config;
    """)
    print("  ✓ ISA validada/atualizada")
    
    # Validar
    cursor.execute("""
        SELECT id, role, name, config->>'model' as model
        FROM agents
        ORDER BY role;
    """)
    
    print("\n📊 AGENTES FINAIS NO BANCO:")
    for row in cursor.fetchall():
        print(f"  {row[2]} ({row[1]}): {row[3]}")
    
    # Commit
    conn.commit()
    print("\n✅ MIGRATION COMPLETA - BANCO LIMPO E RECRIADO")
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    conn.rollback()
    raise
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
