#!/usr/bin/env python3
"""
Script de Auditoria do Banco de Dados RENUM
Conecta ao Supabase e mapeia toda a estrutura
"""

import psycopg2
import json
from datetime import datetime

# Credenciais do Supabase
DATABASE_URL = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"

def conectar_banco():
    """Conecta ao banco Supabase"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("✅ Conectado ao Supabase com sucesso!")
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return None

def listar_tabelas(conn):
    """Lista todas as tabelas do schema public"""
    cursor = conn.cursor()
    
    query = """
    SELECT table_name, table_type
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    ORDER BY table_name;
    """
    
    cursor.execute(query)
    tabelas = cursor.fetchall()
    
    print(f"\n📊 TOTAL DE TABELAS: {len(tabelas)}")
    print("=" * 50)
    
    for nome, tipo in tabelas:
        print(f"- {nome} ({tipo})")
    
    cursor.close()
    return [nome for nome, tipo in tabelas]

def analisar_tabela(conn, nome_tabela):
    """Analisa estrutura detalhada de uma tabela"""
    cursor = conn.cursor()
    
    # Estrutura da tabela
    query_estrutura = """
    SELECT 
        column_name, 
        data_type, 
        is_nullable,
        column_default,
        character_maximum_length
    FROM information_schema.columns 
    WHERE table_name = %s AND table_schema = 'public'
    ORDER BY ordinal_position;
    """
    
    cursor.execute(query_estrutura, (nome_tabela,))
    colunas = cursor.fetchall()
    
    # Contar registros
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {nome_tabela};")
        count = cursor.fetchone()[0]
    except:
        count = "ERRO"
    
    # Verificar RLS
    query_rls = """
    SELECT rowsecurity 
    FROM pg_tables 
    WHERE tablename = %s AND schemaname = 'public';
    """
    
    cursor.execute(query_rls, (nome_tabela,))
    rls_result = cursor.fetchone()
    rls_enabled = rls_result[0] if rls_result else False
    
    # Políticas RLS
    query_policies = """
    SELECT policyname, cmd, permissive, roles, qual
    FROM pg_policies 
    WHERE tablename = %s AND schemaname = 'public';
    """
    
    cursor.execute(query_policies, (nome_tabela,))
    policies = cursor.fetchall()
    
    cursor.close()
    
    return {
        'nome': nome_tabela,
        'colunas': colunas,
        'registros': count,
        'rls_enabled': rls_enabled,
        'policies': policies
    }

def identificar_tabelas_agentes(tabelas):
    """Identifica tabelas relacionadas a agentes"""
    keywords_agentes = [
        'agent', 'wizard', 'sub_agent', 'renus', 'discovery',
        'integration', 'tool', 'memory', 'learning', 'behavior',
        'sicc', 'isa', 'command'
    ]
    
    tabelas_agentes = []
    tabelas_sicc = []
    tabelas_integracao = []
    
    for tabela in tabelas:
        tabela_lower = tabela.lower()
        
        # Tabelas de agentes
        if any(keyword in tabela_lower for keyword in ['agent', 'wizard', 'renus', 'discovery']):
            tabelas_agentes.append(tabela)
        
        # Tabelas SICC
        if any(keyword in tabela_lower for keyword in ['memory', 'learning', 'behavior', 'sicc', 'isa']):
            tabelas_sicc.append(tabela)
        
        # Tabelas de integração
        if any(keyword in tabela_lower for keyword in ['integration', 'tool', 'webhook']):
            tabelas_integracao.append(tabela)
    
    return tabelas_agentes, tabelas_sicc, tabelas_integracao

def main():
    print("🔍 INICIANDO AUDITORIA DO BANCO DE DADOS RENUM")
    print(f"⏰ Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)
    
    # Conectar
    conn = conectar_banco()
    if not conn:
        return
    
    # Listar todas as tabelas
    tabelas = listar_tabelas(conn)
    
    # Categorizar tabelas
    tabelas_agentes, tabelas_sicc, tabelas_integracao = identificar_tabelas_agentes(tabelas)
    
    print(f"\n🤖 TABELAS DE AGENTES ({len(tabelas_agentes)}):")
    for tabela in tabelas_agentes:
        print(f"  - {tabela}")
    
    print(f"\n🧠 TABELAS SICC ({len(tabelas_sicc)}):")
    for tabela in tabelas_sicc:
        print(f"  - {tabela}")
    
    print(f"\n🔌 TABELAS DE INTEGRAÇÃO ({len(tabelas_integracao)}):")
    for tabela in tabelas_integracao:
        print(f"  - {tabela}")
    
    # Analisar tabelas críticas
    tabelas_criticas = tabelas_agentes + tabelas_sicc + tabelas_integracao
    
    print(f"\n📋 ANÁLISE DETALHADA DAS TABELAS CRÍTICAS:")
    print("=" * 60)
    
    analises = {}
    
    for tabela in tabelas_criticas:
        print(f"\n🔍 Analisando: {tabela}")
        try:
            analise = analisar_tabela(conn, tabela)
            analises[tabela] = analise
            
            print(f"  📊 Registros: {analise['registros']}")
            print(f"  🔒 RLS: {'✅' if analise['rls_enabled'] else '❌'}")
            print(f"  📝 Colunas: {len(analise['colunas'])}")
            print(f"  🛡️ Políticas: {len(analise['policies'])}")
            
            # Mostrar estrutura básica
            print("  📋 Estrutura:")
            for col_name, data_type, nullable, default, max_len in analise['colunas'][:5]:  # Primeiras 5 colunas
                nullable_str = "NULL" if nullable == "YES" else "NOT NULL"
                print(f"    - {col_name}: {data_type} {nullable_str}")
            
            if len(analise['colunas']) > 5:
                print(f"    ... e mais {len(analise['colunas']) - 5} colunas")
                
        except Exception as e:
            print(f"  ❌ Erro ao analisar: {e}")
    
    # Salvar resultado em JSON
    with open('scripts/auditoria_resultado.json', 'w', encoding='utf-8') as f:
        # Converter dados para formato serializável
        analises_json = {}
        for tabela, dados in analises.items():
            analises_json[tabela] = {
                'nome': dados['nome'],
                'registros': dados['registros'],
                'rls_enabled': dados['rls_enabled'],
                'total_colunas': len(dados['colunas']),
                'total_policies': len(dados['policies']),
                'colunas': [
                    {
                        'nome': col[0],
                        'tipo': col[1],
                        'nullable': col[2],
                        'default': col[3],
                        'max_length': col[4]
                    }
                    for col in dados['colunas']
                ]
            }
        
        resultado = {
            'timestamp': datetime.now().isoformat(),
            'total_tabelas': len(tabelas),
            'tabelas_agentes': tabelas_agentes,
            'tabelas_sicc': tabelas_sicc,
            'tabelas_integracao': tabelas_integracao,
            'analises': analises_json
        }
        
        json.dump(resultado, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultado salvo em: scripts/auditoria_resultado.json")
    
    conn.close()
    print("\n✅ Auditoria do banco concluída!")

if __name__ == "__main__":
    main()