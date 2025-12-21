#!/usr/bin/env python3
"""
Script para verificar o estado REAL do sistema RENUM
Conecta ao banco de dados real e verifica implementação atual
"""

import psycopg2
import json
from datetime import datetime
import sys
import os

# Credenciais do banco (do arquivo de credenciais)
DB_CONFIG = {
    'host': 'db.vhixvzaxswphwoymdhgg.supabase.co',
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres',
    'password': 'BD5yEMQ9iDMOkeGW'
}

def conectar_banco():
    """Conecta ao banco de dados real"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        return None

def verificar_tabelas(conn):
    """Verifica quais tabelas existem no banco real"""
    cursor = conn.cursor()
    
    # Listar todas as tabelas públicas
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    
    tabelas = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    return tabelas

def verificar_estrutura_agents(conn):
    """Verifica a estrutura da tabela agents"""
    cursor = conn.cursor()
    
    try:
        # Verificar se tabela agents existe
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'agents' AND table_schema = 'public'
            ORDER BY ordinal_position;
        """)
        
        colunas = cursor.fetchall()
        
        if not colunas:
            return {"existe": False}
        
        # Contar registros
        cursor.execute("SELECT COUNT(*) FROM agents;")
        total_registros = cursor.fetchone()[0]
        
        # Verificar RLS
        cursor.execute("""
            SELECT tablename, rowsecurity 
            FROM pg_tables 
            WHERE tablename = 'agents' AND schemaname = 'public';
        """)
        rls_info = cursor.fetchone()
        
        # Verificar políticas RLS
        cursor.execute("""
            SELECT policyname, cmd, roles, qual
            FROM pg_policies 
            WHERE tablename = 'agents' AND schemaname = 'public';
        """)
        politicas = cursor.fetchall()
        
        # Verificar índices
        cursor.execute("""
            SELECT indexname, indexdef
            FROM pg_indexes 
            WHERE tablename = 'agents' AND schemaname = 'public';
        """)
        indices = cursor.fetchall()
        
        cursor.close()
        
        return {
            "existe": True,
            "colunas": colunas,
            "total_registros": total_registros,
            "rls_habilitado": rls_info[1] if rls_info else False,
            "politicas": politicas,
            "indices": indices
        }
        
    except Exception as e:
        cursor.close()
        return {"existe": False, "erro": str(e)}

def verificar_estrutura_sub_agents(conn):
    """Verifica a estrutura da tabela sub_agents"""
    cursor = conn.cursor()
    
    try:
        # Verificar se tabela sub_agents existe
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'sub_agents' AND table_schema = 'public'
            ORDER BY ordinal_position;
        """)
        
        colunas = cursor.fetchall()
        
        if not colunas:
            return {"existe": False}
        
        # Contar registros
        cursor.execute("SELECT COUNT(*) FROM sub_agents;")
        total_registros = cursor.fetchone()[0]
        
        # Verificar se tem agent_id (nova estrutura)
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'sub_agents' 
            AND column_name = 'agent_id'
            AND table_schema = 'public';
        """)
        tem_agent_id = cursor.fetchone() is not None
        
        # Verificar se ainda tem client_id (estrutura antiga)
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'sub_agents' 
            AND column_name = 'client_id'
            AND table_schema = 'public';
        """)
        tem_client_id = cursor.fetchone() is not None
        
        cursor.close()
        
        return {
            "existe": True,
            "colunas": colunas,
            "total_registros": total_registros,
            "tem_agent_id": tem_agent_id,
            "tem_client_id": tem_client_id
        }
        
    except Exception as e:
        cursor.close()
        return {"existe": False, "erro": str(e)}

def verificar_outras_tabelas(conn):
    """Verifica outras tabelas importantes"""
    cursor = conn.cursor()
    
    tabelas_importantes = [
        'clients', 'leads', 'projects', 'conversations', 'messages',
        'interviews', 'interview_messages', 'integrations', 'tools',
        'triggers', 'renus_config', 'profiles'
    ]
    
    resultado = {}
    
    for tabela in tabelas_importantes:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {tabela};")
            count = cursor.fetchone()[0]
            resultado[tabela] = {"existe": True, "registros": count}
        except Exception as e:
            resultado[tabela] = {"existe": False, "erro": str(e)}
    
    cursor.close()
    return resultado

def verificar_backend_rodando():
    """Verifica se o backend está rodando"""
    import requests
    
    try:
        # Tentar acessar endpoint de health check
        response = requests.get("http://localhost:8000/health", timeout=5)
        return {
            "rodando": True,
            "status_code": response.status_code,
            "response": response.text[:200]
        }
    except Exception as e:
        return {
            "rodando": False,
            "erro": str(e)
        }

def verificar_arquivos_frontend():
    """Verifica se arquivos do frontend existem"""
    arquivos_importantes = [
        "src/components/agents/wizard/AgentWizard.tsx",
        "src/components/agents/config/InstructionsTab.tsx",
        "src/components/agents/config/IntegrationsTab.tsx",
        "src/components/agents/config/ToolsTab.tsx",
        "src/components/agents/config/KnowledgeTab.tsx",
        "src/components/agents/config/TriggersTab.tsx",
        "src/components/agents/config/GuardrailsTab.tsx",
        "src/components/agents/config/SubAgentsTab.tsx",
        "src/components/agents/config/AdvancedTab.tsx",
        "src/components/agents/config/SiccTab.tsx",
        "src/pages/agents/AgentsPage.tsx",
        "src/services/agentService.ts",
        "src/services/wizardService.ts"
    ]
    
    resultado = {}
    
    for arquivo in arquivos_importantes:
        resultado[arquivo] = os.path.exists(arquivo)
    
    return resultado

def verificar_arquivos_backend():
    """Verifica se arquivos do backend existem"""
    arquivos_importantes = [
        "backend/src/services/agent_service.py",
        "backend/src/services/wizard_service.py",
        "backend/src/services/integration_service.py",
        "backend/src/services/sub_agent_inheritance_service.py",
        "backend/src/api/routes/agents.py",
        "backend/src/models/agent.py",
        "backend/src/models/wizard.py"
    ]
    
    resultado = {}
    
    for arquivo in arquivos_importantes:
        resultado[arquivo] = os.path.exists(arquivo)
    
    return resultado

def main():
    """Função principal"""
    print("🔍 VERIFICAÇÃO DO ESTADO REAL DO SISTEMA RENUM")
    print("=" * 60)
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    # Conectar ao banco
    print("📊 CONECTANDO AO BANCO DE DADOS REAL...")
    conn = conectar_banco()
    
    if not conn:
        print("❌ Não foi possível conectar ao banco. Abortando verificação.")
        return
    
    print("✅ Conectado ao banco com sucesso!")
    print()
    
    # Verificar tabelas
    print("📋 VERIFICANDO TABELAS...")
    tabelas = verificar_tabelas(conn)
    print(f"✅ Encontradas {len(tabelas)} tabelas: {', '.join(tabelas)}")
    print()
    
    # Verificar estrutura agents
    print("🤖 VERIFICANDO TABELA AGENTS...")
    agents_info = verificar_estrutura_agents(conn)
    
    if agents_info["existe"]:
        print(f"✅ Tabela agents existe com {agents_info['total_registros']} registros")
        print(f"✅ RLS habilitado: {agents_info['rls_habilitado']}")
        print(f"✅ Políticas RLS: {len(agents_info['politicas'])}")
        print(f"✅ Índices: {len(agents_info['indices'])}")
        print(f"✅ Colunas: {len(agents_info['colunas'])}")
    else:
        print("❌ Tabela agents não existe!")
    print()
    
    # Verificar estrutura sub_agents
    print("🔧 VERIFICANDO TABELA SUB_AGENTS...")
    sub_agents_info = verificar_estrutura_sub_agents(conn)
    
    if sub_agents_info["existe"]:
        print(f"✅ Tabela sub_agents existe com {sub_agents_info['total_registros']} registros")
        print(f"✅ Tem agent_id: {sub_agents_info['tem_agent_id']}")
        print(f"⚠️ Ainda tem client_id: {sub_agents_info['tem_client_id']}")
    else:
        print("❌ Tabela sub_agents não existe!")
    print()
    
    # Verificar outras tabelas
    print("📊 VERIFICANDO OUTRAS TABELAS...")
    outras_tabelas = verificar_outras_tabelas(conn)
    
    for tabela, info in outras_tabelas.items():
        if info["existe"]:
            print(f"✅ {tabela}: {info['registros']} registros")
        else:
            print(f"❌ {tabela}: não existe")
    print()
    
    # Fechar conexão
    conn.close()
    
    # Verificar backend
    print("🖥️ VERIFICANDO BACKEND...")
    backend_info = verificar_backend_rodando()
    
    if backend_info["rodando"]:
        print(f"✅ Backend rodando (status: {backend_info['status_code']})")
    else:
        print(f"❌ Backend não está rodando: {backend_info['erro']}")
    print()
    
    # Verificar arquivos frontend
    print("🎨 VERIFICANDO ARQUIVOS FRONTEND...")
    frontend_files = verificar_arquivos_frontend()
    
    existem = sum(1 for exists in frontend_files.values() if exists)
    total = len(frontend_files)
    print(f"📁 Arquivos frontend: {existem}/{total} existem")
    
    for arquivo, existe in frontend_files.items():
        status = "✅" if existe else "❌"
        print(f"  {status} {arquivo}")
    print()
    
    # Verificar arquivos backend
    print("⚙️ VERIFICANDO ARQUIVOS BACKEND...")
    backend_files = verificar_arquivos_backend()
    
    existem = sum(1 for exists in backend_files.values() if exists)
    total = len(backend_files)
    print(f"📁 Arquivos backend: {existem}/{total} existem")
    
    for arquivo, existe in backend_files.items():
        status = "✅" if existe else "❌"
        print(f"  {status} {arquivo}")
    print()
    
    print("🎯 VERIFICAÇÃO CONCLUÍDA!")
    print("=" * 60)

if __name__ == "__main__":
    main()