"""
Análise Completa do Banco de Dados para Implementação do SICC
Sistema de Inteligência Corporativa Contínua
"""
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime


# Credenciais do Supabase
DB_CONFIG = {
    'host': 'db.vhixvzaxswphwoymdhgg.supabase.co',
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres',
    'password': 'BD5yEMQ9iDMOkeGW'
}


def connect_db():
    """Conecta ao banco de dados"""
    return psycopg2.connect(**DB_CONFIG)


def analyze_tables(conn):
    """Lista todas as tabelas e suas estruturas"""
    print("\n" + "="*80)
    print("📊 ANÁLISE DE TABELAS EXISTENTES")
    print("="*80)
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        # Listar todas as tabelas
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cur.fetchall()
        
        print(f"\n✅ Total de tabelas encontradas: {len(tables)}\n")
        
        table_details = {}
        
        for table in tables:
            table_name = table['table_name']
            print(f"\n📋 Tabela: {table_name}")
            print("-" * 80)
            
            # Estrutura da tabela
            cur.execute("""
                SELECT 
                    column_name, 
                    data_type, 
                    is_nullable,
                    column_default,
                    character_maximum_length
                FROM information_schema.columns 
                WHERE table_name = %s
                ORDER BY ordinal_position;
            """, (table_name,))
            columns = cur.fetchall()
            
            print(f"Colunas ({len(columns)}):")
            for col in columns:
                nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
                default = f" DEFAULT {col['column_default']}" if col['column_default'] else ""
                max_len = f"({col['character_maximum_length']})" if col['character_maximum_length'] else ""
                print(f"  - {col['column_name']}: {col['data_type']}{max_len} {nullable}{default}")
            
            # Contar registros
            cur.execute(f"SELECT COUNT(*) as count FROM {table_name};")
            count = cur.fetchone()['count']
            print(f"\n📊 Registros: {count}")
            
            table_details[table_name] = {
                'columns': len(columns),
                'records': count,
                'structure': columns
            }
        
        return table_details


def analyze_indexes(conn):
    """Analisa índices existentes"""
    print("\n" + "="*80)
    print("🔍 ANÁLISE DE ÍNDICES")
    print("="*80)
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT
                tablename,
                indexname,
                indexdef
            FROM pg_indexes
            WHERE schemaname = 'public'
            ORDER BY tablename, indexname;
        """)
        indexes = cur.fetchall()
        
        print(f"\n✅ Total de índices: {len(indexes)}\n")
        
        current_table = None
        for idx in indexes:
            if idx['tablename'] != current_table:
                current_table = idx['tablename']
                print(f"\n📋 Tabela: {current_table}")
                print("-" * 80)
            print(f"  - {idx['indexname']}")
            print(f"    {idx['indexdef']}")
        
        return indexes


def analyze_rls(conn):
    """Analisa políticas RLS"""
    print("\n" + "="*80)
    print("🔒 ANÁLISE DE ROW LEVEL SECURITY (RLS)")
    print("="*80)
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        # Verificar RLS habilitado
        cur.execute("""
            SELECT 
                schemaname,
                tablename, 
                rowsecurity
            FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY tablename;
        """)
        rls_status = cur.fetchall()
        
        print("\n📊 Status RLS por tabela:\n")
        for table in rls_status:
            status = "✅ HABILITADO" if table['rowsecurity'] else "❌ DESABILITADO"
            print(f"  {table['tablename']}: {status}")
        
        # Listar políticas
        cur.execute("""
            SELECT 
                schemaname,
                tablename,
                policyname,
                permissive,
                roles,
                cmd,
                qual
            FROM pg_policies
            WHERE schemaname = 'public'
            ORDER BY tablename, policyname;
        """)
        policies = cur.fetchall()
        
        print(f"\n✅ Total de políticas RLS: {len(policies)}\n")
        
        current_table = None
        for policy in policies:
            if policy['tablename'] != current_table:
                current_table = policy['tablename']
                print(f"\n📋 Tabela: {current_table}")
                print("-" * 80)
            print(f"  - {policy['policyname']}")
            print(f"    Comando: {policy['cmd']}")
            print(f"    Roles: {policy['roles']}")
        
        return {'status': rls_status, 'policies': policies}


def analyze_triggers(conn):
    """Analisa triggers existentes"""
    print("\n" + "="*80)
    print("⚡ ANÁLISE DE TRIGGERS")
    print("="*80)
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT 
                trigger_name,
                event_object_table,
                event_manipulation,
                action_statement,
                action_timing
            FROM information_schema.triggers
            WHERE trigger_schema = 'public'
            ORDER BY event_object_table, trigger_name;
        """)
        triggers = cur.fetchall()
        
        print(f"\n✅ Total de triggers: {len(triggers)}\n")
        
        current_table = None
        for trigger in triggers:
            if trigger['event_object_table'] != current_table:
                current_table = trigger['event_object_table']
                print(f"\n📋 Tabela: {current_table}")
                print("-" * 80)
            print(f"  - {trigger['trigger_name']}")
            print(f"    Timing: {trigger['action_timing']} {trigger['event_manipulation']}")
            print(f"    Action: {trigger['action_statement'][:100]}...")
        
        return triggers


def analyze_functions(conn):
    """Analisa functions/procedures"""
    print("\n" + "="*80)
    print("🔧 ANÁLISE DE FUNCTIONS")
    print("="*80)
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT 
                routine_name,
                routine_type,
                data_type
            FROM information_schema.routines
            WHERE routine_schema = 'public'
            ORDER BY routine_name;
        """)
        functions = cur.fetchall()
        
        print(f"\n✅ Total de functions: {len(functions)}\n")
        
        for func in functions:
            print(f"  - {func['routine_name']} ({func['routine_type']})")
            if func['data_type']:
                print(f"    Returns: {func['data_type']}")
        
        return functions


def analyze_relationships(conn):
    """Analisa relacionamentos entre tabelas"""
    print("\n" + "="*80)
    print("🔗 ANÁLISE DE RELACIONAMENTOS (FOREIGN KEYS)")
    print("="*80)
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT
                tc.table_name, 
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name,
                tc.constraint_name
            FROM information_schema.table_constraints AS tc 
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
                AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY' 
                AND tc.table_schema = 'public'
            ORDER BY tc.table_name, kcu.column_name;
        """)
        relationships = cur.fetchall()
        
        print(f"\n✅ Total de foreign keys: {len(relationships)}\n")
        
        current_table = None
        for rel in relationships:
            if rel['table_name'] != current_table:
                current_table = rel['table_name']
                print(f"\n📋 Tabela: {current_table}")
                print("-" * 80)
            print(f"  - {rel['column_name']} → {rel['foreign_table_name']}.{rel['foreign_column_name']}")
        
        return relationships


def analyze_vector_support(conn):
    """Verifica suporte a vector embeddings"""
    print("\n" + "="*80)
    print("🧠 ANÁLISE DE SUPORTE A VECTOR EMBEDDINGS")
    print("="*80)
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        # Verificar extensão pgvector
        cur.execute("""
            SELECT * FROM pg_extension WHERE extname = 'vector';
        """)
        vector_ext = cur.fetchone()
        
        if vector_ext:
            print("\n✅ Extensão pgvector INSTALADA")
            print(f"   Versão: {vector_ext.get('extversion', 'N/A')}")
        else:
            print("\n❌ Extensão pgvector NÃO INSTALADA")
            print("   Necessário instalar para suporte a embeddings")
        
        # Verificar tabelas com colunas vector
        cur.execute("""
            SELECT 
                table_name,
                column_name,
                data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'
                AND data_type = 'USER-DEFINED'
            ORDER BY table_name, column_name;
        """)
        vector_columns = cur.fetchall()
        
        if vector_columns:
            print(f"\n✅ Colunas vector encontradas: {len(vector_columns)}\n")
            for col in vector_columns:
                print(f"  - {col['table_name']}.{col['column_name']}")
        else:
            print("\n⚠️  Nenhuma coluna vector encontrada")
        
        return {'extension': vector_ext, 'columns': vector_columns}


def analyze_storage_usage(conn):
    """Analisa uso de armazenamento"""
    print("\n" + "="*80)
    print("💾 ANÁLISE DE ARMAZENAMENTO")
    print("="*80)
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT
                schemaname,
                tablename,
                pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
                pg_total_relation_size(schemaname||'.'||tablename) AS size_bytes
            FROM pg_tables
            WHERE schemaname = 'public'
            ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
        """)
        sizes = cur.fetchall()
        
        print("\n📊 Tamanho das tabelas:\n")
        total_bytes = 0
        for table in sizes:
            print(f"  {table['tablename']}: {table['size']}")
            total_bytes += table['size_bytes']
        
        print(f"\n✅ Total: {total_bytes / (1024*1024):.2f} MB")
        
        return sizes


def generate_sicc_recommendations(analysis_data):
    """Gera recomendações para implementação do SICC"""
    print("\n" + "="*80)
    print("💡 RECOMENDAÇÕES PARA IMPLEMENTAÇÃO DO SICC")
    print("="*80)
    
    recommendations = []
    
    # 1. Vector Database
    if not analysis_data['vector']['extension']:
        recommendations.append({
            'priority': 'CRÍTICO',
            'category': 'Vector Database',
            'issue': 'Extensão pgvector não instalada',
            'action': 'Instalar pgvector para suporte a embeddings',
            'sql': 'CREATE EXTENSION IF NOT EXISTS vector;'
        })
    
    # 2. Tabelas necessárias
    required_tables = [
        'agent_memory_chunks',
        'agent_behavior_patterns', 
        'agent_learning_logs',
        'agent_knowledge_snapshots',
        'agent_performance_metrics'
    ]
    
    existing_tables = [t for t in analysis_data['tables'].keys()]
    missing_tables = [t for t in required_tables if t not in existing_tables]
    
    if missing_tables:
        recommendations.append({
            'priority': 'ALTO',
            'category': 'Schema',
            'issue': f'{len(missing_tables)} tabelas do SICC não existem',
            'action': f'Criar tabelas: {", ".join(missing_tables)}',
            'tables': missing_tables
        })
    
    # 3. Índices para performance
    recommendations.append({
        'priority': 'ALTO',
        'category': 'Performance',
        'issue': 'Índices específicos para queries de aprendizado',
        'action': 'Criar índices em colunas de timestamp, agent_id, e similarity search'
    })
    
    # 4. RLS para segurança
    recommendations.append({
        'priority': 'MÉDIO',
        'category': 'Segurança',
        'issue': 'Políticas RLS para novas tabelas do SICC',
        'action': 'Implementar RLS garantindo isolamento entre clientes'
    })
    
    print("\n")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. [{rec['priority']}] {rec['category']}")
        print(f"   Problema: {rec['issue']}")
        print(f"   Ação: {rec['action']}")
        if 'sql' in rec:
            print(f"   SQL: {rec['sql']}")
        print()
    
    return recommendations


def main():
    """Executa análise completa"""
    print("\n" + "="*80)
    print("🔍 ANÁLISE COMPLETA DO BANCO DE DADOS RENUM")
    print("Sistema de Inteligência Corporativa Contínua (SICC)")
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    try:
        # Conectar
        print("\n🔌 Conectando ao Supabase...")
        conn = connect_db()
        print("✅ Conexão estabelecida com sucesso!")
        
        # Executar análises
        analysis_data = {}
        
        analysis_data['tables'] = analyze_tables(conn)
        analysis_data['indexes'] = analyze_indexes(conn)
        analysis_data['rls'] = analyze_rls(conn)
        analysis_data['triggers'] = analyze_triggers(conn)
        analysis_data['functions'] = analyze_functions(conn)
        analysis_data['relationships'] = analyze_relationships(conn)
        analysis_data['vector'] = analyze_vector_support(conn)
        analysis_data['storage'] = analyze_storage_usage(conn)
        
        # Gerar recomendações
        recommendations = generate_sicc_recommendations(analysis_data)
        
        # Salvar relatório
        report = {
            'timestamp': datetime.now().isoformat(),
            'analysis': {
                'total_tables': len(analysis_data['tables']),
                'total_indexes': len(analysis_data['indexes']),
                'total_policies': len(analysis_data['rls']['policies']),
                'total_triggers': len(analysis_data['triggers']),
                'total_functions': len(analysis_data['functions']),
                'total_relationships': len(analysis_data['relationships']),
                'vector_support': bool(analysis_data['vector']['extension'])
            },
            'recommendations': recommendations
        }
        
        with open('SICC_DATABASE_ANALYSIS.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        print("\n" + "="*80)
        print("✅ ANÁLISE CONCLUÍDA")
        print("="*80)
        print("\n📄 Relatório salvo em: SICC_DATABASE_ANALYSIS.json")
        
        conn.close()
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
