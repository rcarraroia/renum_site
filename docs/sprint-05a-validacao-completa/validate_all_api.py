"""
Script de validação completa da API Backend
Testa todos os grupos de endpoints de forma eficiente
"""
import requests
import json
from typing import Dict, List, Tuple

BASE_URL = "http://localhost:8000"

# Ler token
with open('test_token.txt', 'r') as f:
    TOKEN = f.read().strip()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

class APIValidator:
    def __init__(self):
        self.results = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "groups": {}
        }
    
    def test_endpoint(self, method: str, endpoint: str, data: dict = None, 
                     expected_status: int = 200, description: str = "") -> Tuple[bool, str]:
        """Testa um endpoint e retorna (sucesso, mensagem)"""
        self.results["total_tests"] += 1
        
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS)
            elif method == "POST":
                response = requests.post(f"{BASE_URL}{endpoint}", headers=HEADERS, json=data)
            elif method == "PUT":
                response = requests.put(f"{BASE_URL}{endpoint}", headers=HEADERS, json=data)
            elif method == "DELETE":
                response = requests.delete(f"{BASE_URL}{endpoint}", headers=HEADERS)
            
            if response.status_code == expected_status:
                self.results["passed"] += 1
                return True, f"✅ {description or endpoint}"
            else:
                self.results["failed"] += 1
                error_detail = response.text[:100] if response.text else "No detail"
                return False, f"❌ {description or endpoint} - Status {response.status_code}: {error_detail}"
                
        except Exception as e:
            self.results["failed"] += 1
            return False, f"❌ {description or endpoint} - Exception: {str(e)[:100]}"
    
    def validate_group(self, group_name: str, tests: List[Tuple]):
        """Valida um grupo de endpoints"""
        print(f"\n{'='*70}")
        print(f"🔍 VALIDANDO: {group_name}")
        print(f"{'='*70}\n")
        
        group_results = {
            "total": len(tests),
            "passed": 0,
            "failed": 0,
            "details": []
        }
        
        for test in tests:
            success, message = self.test_endpoint(*test)
            print(message)
            
            if success:
                group_results["passed"] += 1
            else:
                group_results["failed"] += 1
            
            group_results["details"].append({
                "success": success,
                "message": message
            })
        
        self.results["groups"][group_name] = group_results
        
        # Resumo do grupo
        status = "✅" if group_results["failed"] == 0 else "⚠️" if group_results["passed"] > 0 else "❌"
        print(f"\n{status} {group_name}: {group_results['passed']}/{group_results['total']} passaram")
    
    def print_summary(self):
        """Imprime resumo final"""
        print(f"\n\n{'='*70}")
        print(f"📊 RESUMO GERAL DA VALIDAÇÃO")
        print(f"{'='*70}\n")
        
        print(f"Total de testes: {self.results['total_tests']}")
        print(f"✅ Passaram: {self.results['passed']} ({self.results['passed']/self.results['total_tests']*100:.1f}%)")
        print(f"❌ Falharam: {self.results['failed']} ({self.results['failed']/self.results['total_tests']*100:.1f}%)")
        
        print(f"\n{'='*70}")
        print(f"RESUMO POR GRUPO")
        print(f"{'='*70}\n")
        
        for group_name, group_data in self.results["groups"].items():
            status = "✅" if group_data["failed"] == 0 else "⚠️" if group_data["passed"] > 0 else "❌"
            print(f"{status} {group_name}: {group_data['passed']}/{group_data['total']}")

def main():
    validator = APIValidator()
    
    # Grupo 5: Conversations (CRÍTICO - NÃO TESTADO)
    validator.validate_group("Conversations", [
        ("GET", "/api/conversations", None, 200, "Listar conversas"),
        ("POST", "/api/conversations", {
            "lead_id": "test-lead-id",
            "title": "Conversa Teste"
        }, 201, "Criar conversa"),
    ])
    
    # Grupo 6: Messages (CRÍTICO - NÃO TESTADO)
    validator.validate_group("Messages", [
        ("GET", "/api/messages", None, 200, "Listar mensagens"),
    ])
    
    # Grupo 7: Sub-Agents (CRÍTICO)
    validator.validate_group("Sub-Agents", [
        ("GET", "/api/sub-agents", None, 200, "Listar sub-agents"),
    ])
    
    # Grupo 8: Interviews (CRÍTICO)
    validator.validate_group("Interviews", [
        ("GET", "/api/interviews", None, 200, "Listar interviews"),
    ])
    
    # Grupo 9: Dashboard
    validator.validate_group("Dashboard", [
        ("GET", "/api/dashboard/stats", None, 200, "Dashboard stats"),
    ])
    
    # Grupo 10: ISA
    validator.validate_group("ISA", [
        ("POST", "/api/isa/chat", {"message": "Olá ISA"}, 200, "ISA chat"),
    ])
    
    # Grupo 11: RENUS Config
    validator.validate_group("RENUS Config", [
        ("GET", "/api/renus-config", None, 200, "Listar configs"),
    ])
    
    # Grupo 12: Tools
    validator.validate_group("Tools", [
        ("GET", "/api/tools", None, 200, "Listar tools"),
    ])
    
    validator.print_summary()

if __name__ == "__main__":
    main()
