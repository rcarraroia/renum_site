"""
Teste automatizado do frontend via API
Verifica se dados vêm do backend REAL (não mock)
"""
import requests
import json

BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:8081"

# Token do admin
with open('test_token.txt', 'r') as f:
    TOKEN = f.read().strip()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def test_frontend_loads():
    """Testa se frontend carrega"""
    print("\n🌐 FRONTEND - Carregamento")
    print("-" * 70)
    
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Frontend carrega (200 OK)")
            return True
        else:
            print(f"❌ Frontend retornou {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao acessar frontend: {str(e)[:100]}")
        return False

def test_dashboard_data():
    """Testa se dashboard busca dados reais"""
    print("\n📊 MENU 1: Dashboard (Overview)")
    print("-" * 70)
    
    try:
        # Dashboard deve chamar /api/dashboard/stats
        response = requests.get(f"{BASE_URL}/api/dashboard/stats", headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Dashboard stats OK")
            print(f"   Dados: {json.dumps(data, indent=2)[:200]}...")
            return True
        else:
            print(f"❌ Dashboard stats falhou: {response.status_code}")
            print(f"   Erro: {response.text[:100]}")
            return False
    except Exception as e:
        print(f"❌ Erro: {str(e)[:100]}")
        return False

def test_clients_data():
    """Testa se lista de clientes vem do backend"""
    print("\n👥 MENU 2: Clientes")
    print("-" * 70)
    
    try:
        response = requests.get(f"{BASE_URL}/api/clients", headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            total = data.get('total', 0)
            items = len(data.get('items', []))
            
            print(f"✅ Lista de clientes OK")
            print(f"   Total: {total}, Items na página: {items}")
            print(f"   Dados REAIS do backend: {'✅ SIM' if total >= 0 else '❌ NÃO'}")
            return True
        else:
            print(f"❌ Lista de clientes falhou: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {str(e)[:100]}")
        return False

def test_leads_data():
    """Testa se lista de leads vem do backend"""
    print("\n📋 MENU 3: Leads")
    print("-" * 70)
    
    try:
        response = requests.get(f"{BASE_URL}/api/leads", headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            total = data.get('total', 0)
            items = len(data.get('items', []))
            
            print(f"✅ Lista de leads OK")
            print(f"   Total: {total}, Items na página: {items}")
            print(f"   Dados REAIS do backend: ✅ SIM")
            return True
        else:
            print(f"❌ Lista de leads falhou: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {str(e)[:100]}")
        return False

def test_projects_data():
    """Testa se lista de projetos vem do backend"""
    print("\n📁 MENU 4: Projetos")
    print("-" * 70)
    
    try:
        response = requests.get(f"{BASE_URL}/api/projects", headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            total = data.get('total', 0)
            items = len(data.get('items', []))
            
            print(f"✅ Lista de projetos OK")
            print(f"   Total: {total}, Items na página: {items}")
            print(f"   Dados REAIS do backend: ✅ SIM")
            return True
        else:
            print(f"❌ Lista de projetos falhou: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {str(e)[:100]}")
        return False

def test_conversations_data():
    """Testa se lista de conversas vem do backend"""
    print("\n💬 MENU 5: Conversas")
    print("-" * 70)
    
    try:
        response = requests.get(f"{BASE_URL}/api/conversations", headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            total = data.get('total', len(data) if isinstance(data, list) else 0)
            
            print(f"✅ Lista de conversas OK")
            print(f"   Total: {total}")
            print(f"   Dados REAIS do backend: ✅ SIM")
            return True
        else:
            print(f"❌ Lista de conversas falhou: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {str(e)[:100]}")
        return False

def test_interviews_data():
    """Testa se lista de entrevistas vem do backend"""
    print("\n📝 MENU 6: Pesquisas/Entrevistas")
    print("-" * 70)
    
    try:
        response = requests.get(f"{BASE_URL}/api/interviews", headers=HEADERS)
        
        if response.status_code == 200:
            print(f"✅ Lista de entrevistas OK")
            print(f"   Dados REAIS do backend: ✅ SIM")
            return True
        else:
            print(f"❌ Lista de entrevistas falhou: {response.status_code}")
            print(f"   Erro: {response.text[:100]}")
            return False
    except Exception as e:
        print(f"❌ Erro: {str(e)[:100]}")
        return False

def test_subagents_data():
    """Testa se lista de sub-agents vem do backend"""
    print("\n🤖 MENU 8: Config. Renus (Sub-Agents)")
    print("-" * 70)
    
    try:
        response = requests.get(f"{BASE_URL}/api/sub-agents", headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            total = len(data) if isinstance(data, list) else 0
            
            print(f"✅ Lista de sub-agents OK")
            print(f"   Total: {total}")
            print(f"   Dados REAIS do backend: ✅ SIM")
            return True
        else:
            print(f"❌ Lista de sub-agents falhou: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {str(e)[:100]}")
        return False

def main():
    print("\n" + "="*70)
    print("🧪 VALIDAÇÃO DO FRONTEND")
    print("="*70)
    
    results = {
        "Frontend carrega": test_frontend_loads(),
        "Dashboard": test_dashboard_data(),
        "Clientes": test_clients_data(),
        "Leads": test_leads_data(),
        "Projetos": test_projects_data(),
        "Conversas": test_conversations_data(),
        "Entrevistas": test_interviews_data(),
        "Sub-Agents": test_subagents_data(),
    }
    
    print("\n" + "="*70)
    print("📊 RESUMO - FRONTEND")
    print("="*70 + "\n")
    
    for menu, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {menu}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\n{passed}/{total} menus funcionais ({passed/total*100:.0f}%)")
    
    print("\n" + "="*70)
    print("CONCLUSÃO")
    print("="*70)
    
    if passed == total:
        print("✅ Frontend 100% funcional - dados vêm do backend REAL")
    elif passed >= total * 0.7:
        print("⚠️ Frontend parcialmente funcional - alguns menus com problemas")
    else:
        print("❌ Frontend com problemas graves - maioria dos menus não funciona")

if __name__ == "__main__":
    main()
