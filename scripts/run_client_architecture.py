"""
Script para executar a configuração da arquitetura de client_id
Executa diretamente no Supabase
"""

import os
import sys

# Adicionar path do backend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Carregar variáveis de ambiente do backend
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))

def main():
    from supabase import create_client
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not url or not key:
        print("❌ ERRO: Variáveis SUPABASE_URL e SUPABASE_SERVICE_KEY não configuradas")
        return False
    
    supabase = create_client(url, key)
    
    print("=" * 60)
    print("  CONFIGURAÇÃO DA ARQUITETURA DE CLIENT_ID")
    print("=" * 60)
    
    # PASSO 0: Verificar estrutura da tabela clients
    print("\n📌 PASSO 0: Verificando estrutura da tabela clients...")
    try:
        # Buscar um registro para ver as colunas
        sample = supabase.table("clients").select("*").limit(1).execute()
        if sample.data:
            print(f"   Colunas disponíveis: {list(sample.data[0].keys())}")
        else:
            print("   Tabela clients está vazia, tentando inserir...")
    except Exception as e:
        print(f"   ⚠️ Erro ao verificar estrutura: {e}")
    
    # PASSO 1: Criar/Atualizar Cliente RENUM (Interno)
    print("\n📌 PASSO 1: Criando cliente RENUM (Interno)...")
    try:
        # Verificar se já existe
        existing = supabase.table("clients").select("id").eq("id", "00000000-0000-0000-0000-000000000000").execute()
        
        if existing.data:
            print("   ✅ Cliente RENUM (Interno) já existe")
        else:
            # Inserir com campos obrigatórios (segment é NOT NULL)
            result = supabase.table("clients").insert({
                "id": "00000000-0000-0000-0000-000000000000",
                "company_name": "RENUM (Interno)",
                "segment": "technology",
                "status": "active"
            }).execute()
            print("   ✅ Cliente RENUM (Interno) criado com sucesso")
    except Exception as e:
        error_msg = str(e)
        if "duplicate key" in error_msg.lower() or "already exists" in error_msg.lower():
            print("   ✅ Cliente RENUM (Interno) já existe")
        else:
            print(f"   ⚠️ Erro ao criar cliente interno: {e}")
            # Tentar com estrutura alternativa
            try:
                result = supabase.table("clients").upsert({
                    "id": "00000000-0000-0000-0000-000000000000",
                    "company_name": "RENUM (Interno)",
                    "segment": "technology",
                    "status": "active"
                }).execute()
                print("   ✅ Cliente RENUM (Interno) criado via upsert")
            except Exception as e2:
                print(f"   ❌ Falha no upsert também: {e2}")
    
    # PASSO 2: Atualizar agentes sem client_id
    print("\n📌 PASSO 2: Atualizando agentes sem client_id...")
    try:
        # Buscar agentes sem client_id
        agents_without = supabase.table("agents").select("id, name").is_("client_id", "null").execute()
        
        if agents_without.data:
            for agent in agents_without.data:
                try:
                    supabase.table("agents").update({
                        "client_id": "00000000-0000-0000-0000-000000000000"
                    }).eq("id", agent["id"]).execute()
                    print(f"   ✅ Agente '{agent['name']}' atualizado com client_id interno")
                except Exception as e:
                    print(f"   ⚠️ Erro ao atualizar agente '{agent['name']}': {e}")
        else:
            print("   ✅ Todos os agentes já têm client_id")
    except Exception as e:
        print(f"   ⚠️ Erro ao atualizar agentes: {e}")
    
    # PASSO 3: Listar todos os agentes e seus client_id
    print("\n📌 PASSO 3: Validação - Listando agentes...")
    try:
        agents = supabase.table("agents").select("id, name, slug, client_id, status").execute()
        
        print("\n   | Nome | Slug | Client ID | Status |")
        print("   |------|------|-----------|--------|")
        
        for agent in agents.data or []:
            client_id = agent.get("client_id", "NULL")
            if client_id:
                client_id = client_id[:8] + "..."
            else:
                client_id = "❌ NULL"
            print(f"   | {agent.get('name', 'N/A')[:20]} | {agent.get('slug', 'N/A')[:15]} | {client_id} | {agent.get('status', 'N/A')} |")
    except Exception as e:
        print(f"   ⚠️ Erro ao listar agentes: {e}")
    
    # PASSO 4: Verificar agentes sem client_id
    print("\n📌 PASSO 4: Verificação final...")
    try:
        agents_without = supabase.table("agents").select("id", count="exact").is_("client_id", "null").execute()
        count = agents_without.count or 0
        
        if count == 0:
            print("   ✅ SUCESSO: Todos os agentes têm client_id!")
        else:
            print(f"   ❌ ERRO: {count} agente(s) ainda sem client_id")
    except Exception as e:
        print(f"   ⚠️ Erro na verificação: {e}")
    
    # PASSO 5: Listar clientes
    print("\n📌 PASSO 5: Listando clientes...")
    try:
        clients = supabase.table("clients").select("id, company_name, status").execute()
        
        print("\n   | ID | Empresa | Status |")
        print("   |----|---------|--------|")
        
        for client in clients.data or []:
            client_id = client.get("id", "")[:8] + "..."
            print(f"   | {client_id} | {client.get('company_name', 'N/A')[:25]} | {client.get('status', 'N/A')} |")
    except Exception as e:
        print(f"   ⚠️ Erro ao listar clientes: {e}")
    
    print("\n" + "=" * 60)
    print("  CONFIGURAÇÃO CONCLUÍDA")
    print("=" * 60)
    print("\n⚠️  IMPORTANTE: Reinicie o backend para aplicar as mudanças!")
    print("   docker-compose restart backend")
    print("   OU")
    print("   Ctrl+C e reinicie o uvicorn")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
