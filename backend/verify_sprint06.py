#!/usr/bin/env python3
"""
Script de verificação para Sprint 06 - Wizard de Criação de Agentes
Verifica estado atual do banco de dados e estrutura do projeto
"""

import psycopg2
import json
from pathlib import Path

def verify_database():
    """Verifica estado do banco de dados Supabase"""
    print("=" * 60)
    print("VERIFICAÇÃO DO BANCO DE DADOS (SUPABASE)")
    print("=" * 60)
    
    try:
        # Conectar ao Supabase
        conn = psycopg2.connect(
            host='db.vhixvzaxswphwoymdhgg.supabase.co',
            port=5432,
            database='postgres',
            user='postgres',
            password='BD5yEMQ9iDMOkeGW'
        )
        
        cur = conn.cursor()
        
        # 1. Listar todas as tabelas
        print("\n1. TABELAS EXISTENTES:")
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = [row[0] for row in cur.fetchall()]
        for table in tables:
            print(f"   ✅ {table}")
        
        # 2. Verificar sub_agents
        print("\n2. ESTRUTURA DA TABELA sub_agents:")
        if 'sub_agents' in tables:
            cur.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'sub_agents'
                ORDER BY ordinal_position;
            """)
            columns = cur.fetchall()
            for col in columns:
                nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                default = f"DEFAULT {col[3]}" if col[3] else ""
                print(f"   - {col[0]:<20} {col[1]:<20} {nullable:<10} {default}")
            
            # Verificar se config é JSONB
            cur.execute("""
                SELECT data_type 
                FROM information_schema.columns 
                WHERE table_name = 'sub_agents' AND column_name = 'config';
            """)
            config_type = cur.fetchone()
            if config_type:
                print(f"\n   📋 Campo 'config': {config_type[0]}")
                if config_type[0] == 'jsonb':
                    print("   ✅ JSONB suporta estruturas complexas")
                else:
                    print(f"   ⚠️ Tipo atual: {config_type[0]} (esperado: jsonb)")
        else:
            print("   ❌ Tabela sub_agents NÃO EXISTE")
        
        # 3. Verificar integrations
        print("\n3. ESTRUTURA DA TABELA integrations:")
        if 'integrations' in tables:
            cur.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'integrations'
                ORDER BY ordinal_position;
            """)
            int_columns = cur.fetchall()
            for col in int_columns:
                nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                print(f"   - {col[0]:<20} {col[1]:<20} {nullable}")
        else:
            print("   ❌ Tabela integrations NÃO EXISTE")
        
        # 4. Verificar RLS
        print("\n4. ROW LEVEL SECURITY (RLS):")
        cur.execute("""
            SELECT tablename, rowsecurity 
            FROM pg_tables 
            WHERE tablename IN ('sub_agents', 'integrations')
            AND schemaname = 'public';
        """)
        rls_status = cur.fetchall()
        for table, enabled in rls_status:
            status = "✅ Habilitado" if enabled else "❌ Desabilitado"
            print(f"   {table}: {status}")
        
        # 5. Verificar dados existentes
        print("\n5. DADOS EXISTENTES:")
        if 'sub_agents' in tables:
            cur.execute("SELECT COUNT(*) FROM sub_agents;")
            count = cur.fetchone()[0]
            print(f"   sub_agents: {count} registros")
            
            if count > 0:
                cur.execute("""
                    SELECT id, name, type, status, 
                           CASE WHEN config IS NOT NULL THEN 'Sim' ELSE 'Não' END as has_config
                    FROM sub_agents 
                    LIMIT 5;
                """)
                agents = cur.fetchall()
                print("\n   Exemplos:")
                for agent in agents:
                    print(f"   - {agent[1]} (type: {agent[2]}, status: {agent[3]}, config: {agent[4]})")
        
        if 'integrations' in tables:
            cur.execute("SELECT COUNT(*) FROM integrations;")
            count = cur.fetchone()[0]
            print(f"   integrations: {count} registros")
        
        # 6. Verificar índices
        print("\n6. ÍNDICES:")
        cur.execute("""
            SELECT indexname, indexdef 
            FROM pg_indexes 
            WHERE tablename IN ('sub_agents', 'integrations')
            AND schemaname = 'public'
            ORDER BY tablename, indexname;
        """)
        indexes = cur.fetchall()
        if indexes:
            for idx_name, idx_def in indexes:
                print(f"   - {idx_name}")
        else:
            print("   ⚠️ Nenhum índice encontrado")
        
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO ao conectar ao Supabase: {e}")
        return False

def verify_backend_structure():
    """Verifica estrutura do backend"""
    print("\n" + "=" * 60)
    print("VERIFICAÇÃO DA ESTRUTURA DO BACKEND")
    print("=" * 60)
    
    backend_path = Path(__file__).parent
    
    # Verificar agentes
    print("\n1. AGENTES (Sprint 04):")
    agents_path = backend_path / "src" / "agents"
    if agents_path.exists():
        agent_files = list(agents_path.glob("*.py"))
        for agent_file in agent_files:
            if agent_file.name != "__init__.py":
                print(f"   ✅ {agent_file.name}")
    else:
        print("   ❌ Diretório src/agents não existe")
    
    # Verificar integrações
    print("\n2. INTEGRAÇÕES (Sprint 07A):")
    integrations_path = backend_path / "src" / "integrations"
    if integrations_path.exists():
        integration_files = list(integrations_path.glob("*_client.py"))
        for int_file in integration_files:
            print(f"   ✅ {int_file.name}")
    else:
        print("   ❌ Diretório src/integrations não existe")
    
    # Verificar tools
    print("\n3. TOOLS (Sprint 07A):")
    tools_path = backend_path / "src" / "tools"
    if tools_path.exists():
        tool_files = list(tools_path.glob("*_tool.py"))
        for tool_file in tool_files:
            print(f"   ✅ {tool_file.name}")
    else:
        print("   ❌ Diretório src/tools não existe")
    
    # Verificar rotas existentes
    print("\n4. ROTAS API:")
    routes_path = backend_path / "src" / "api" / "routes"
    if routes_path.exists():
        route_files = list(routes_path.glob("*.py"))
        for route_file in route_files:
            if route_file.name != "__init__.py":
                print(f"   ✅ {route_file.name}")
    else:
        print("   ❌ Diretório src/api/routes não existe")

def verify_frontend_structure():
    """Verifica estrutura do frontend"""
    print("\n" + "=" * 60)
    print("VERIFICAÇÃO DA ESTRUTURA DO FRONTEND")
    print("=" * 60)
    
    frontend_path = Path(__file__).parent.parent / "frontend"
    
    if not frontend_path.exists():
        print("\n❌ Diretório frontend não encontrado")
        return
    
    # Verificar páginas
    print("\n1. PÁGINAS:")
    pages_path = frontend_path / "src" / "pages"
    if pages_path.exists():
        # Listar subdiretórios
        for subdir in pages_path.iterdir():
            if subdir.is_dir():
                print(f"   📁 {subdir.name}/")
                # Listar arquivos .tsx
                for file in subdir.glob("*.tsx"):
                    print(f"      - {file.name}")
    else:
        print("   ⚠️ Diretório src/pages não encontrado")
    
    # Verificar services
    print("\n2. SERVICES:")
    services_path = frontend_path / "src" / "services"
    if services_path.exists():
        service_files = list(services_path.glob("*.ts"))
        for service_file in service_files:
            print(f"   ✅ {service_file.name}")
    else:
        print("   ⚠️ Diretório src/services não encontrado")
    
    # Verificar componentes de integração
    print("\n3. COMPONENTES DE INTEGRAÇÃO:")
    components_path = frontend_path / "src" / "components"
    if components_path.exists():
        integrations_comp = components_path / "integrations"
        if integrations_comp.exists():
            for file in integrations_comp.glob("*.tsx"):
                print(f"   ✅ {file.name}")
        else:
            print("   ⚠️ Diretório components/integrations não encontrado")
    else:
        print("   ⚠️ Diretório src/components não encontrado")

def main():
    """Executa todas as verificações"""
    print("\n" + "=" * 60)
    print("VERIFICAÇÃO PRÉ-SPRINT 06")
    print("Wizard de Criação de Agentes")
    print("=" * 60)
    
    # Verificar banco de dados
    db_ok = verify_database()
    
    # Verificar backend
    verify_backend_structure()
    
    # Verificar frontend
    verify_frontend_structure()
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO DA VERIFICAÇÃO")
    print("=" * 60)
    
    if db_ok:
        print("\n✅ Conexão com Supabase: OK")
    else:
        print("\n❌ Conexão com Supabase: FALHOU")
    
    print("\n📋 Próximos passos:")
    print("   1. Revisar resultados acima")
    print("   2. Documentar divergências encontradas")
    print("   3. Criar especificações (requirements.md, design.md, tasks.md)")
    print("   4. Apresentar para aprovação")

if __name__ == "__main__":
    main()
