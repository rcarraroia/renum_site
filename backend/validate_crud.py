"""
VALIDAÇÃO CRUD COMPLETO - SPRINT 05A
Testa CRUD de todas as entidades principais
IMPORTANTE: Usa prefixo TEST_ em todos os dados criados
"""

import requests
import json
import time
import sys
from datetime import datetime
from typing import Dict, List, Any

print("Initializing validation script...", flush=True)

# Configuração
BASE_URL = "http://localhost:8000"
TOKEN_FILE = "test_token.txt"

# Ler token
try:
    with open(TOKEN_FILE, "r") as f:
        TOKEN = f.read().strip()
    print(f"Token loaded successfully", flush=True)
except Exception as e:
    print(f"ERROR loading token: {e}", flush=True)
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Timestamp para dados únicos
TIMESTAMP = int(time.time())

# Armazenar IDs criados para cleanup
created_ids = {
    "clients": [],
    "leads": [],
    "projects": [],
    "conversations": [],
    "interviews": []
}

# Resultados
results = {
    "clients": {"total": 0, "success": 0, "errors": []},
    "leads": {"total": 0, "success": 0, "errors": []},
    "projects": {"total": 0, "success": 0, "errors": []},
    "conversations": {"total": 0, "success": 0, "errors": []},
    "interviews": {"total": 0, "success": 0, "errors": []}
}


def log(message: str):
    """Log com timestamp"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")


def test_endpoint(entity: str, method: str, endpoint: str, data: Dict = None, expected_status: int = 200) -> Dict:
    """Testa um endpoint e registra resultado"""
    results[entity]["total"] += 1
    
    try:
        url = f"{BASE_URL}{endpoint}"
        log(f"Testing {method} {endpoint}")
        
        if method == "GET":
            response = requests.get(url, headers=HEADERS, timeout=5)
        elif method == "POST":
            response = requests.post(url, headers=HEADERS, json=data, timeout=5)
        elif method == "PUT":
            response = requests.put(url, headers=HEADERS, json=data, timeout=5)
        elif method == "DELETE":
            response = requests.delete(url, headers=HEADERS, timeout=5)
        
        if response.status_code == expected_status:
            results[entity]["success"] += 1
            log(f"✅ SUCCESS: {method} {endpoint} - Status {response.status_code}")
            return {"success": True, "data": response.json() if response.text else None}
        else:
            error_msg = f"{method} {endpoint} - Expected {expected_status}, got {response.status_code}"
            results[entity]["errors"].append(error_msg)
            log(f"❌ FAIL: {error_msg}")
            log(f"   Response: {response.text[:200]}")
            return {"success": False, "error": error_msg, "response": response.text}
    
    except Exception as e:
        error_msg = f"{method} {endpoint} - Exception: {str(e)}"
        results[entity]["errors"].append(error_msg)
        log(f"❌ ERROR: {error_msg}")
        return {"success": False, "error": str(e)}


def validate_clients():
    """Valida CRUD de Clients"""
    log("\n" + "="*60)
    log("VALIDANDO CLIENTS")
    log("="*60)
    
    # 1. CREATE (POST)
    client_data = {
        "company_name": f"TEST_Cliente_{TIMESTAMP}",
        "cnpj": "12345678000199",
        "plan": "basic",
        "status": "active"
    }
    result = test_endpoint("clients", "POST", "/api/clients", client_data, 201)
    
    if result["success"]:
        client_id = result["data"]["id"]
        created_ids["clients"].append(client_id)
        log(f"   Created client ID: {client_id}")
        
        # 2. READ (GET by ID)
        test_endpoint("clients", "GET", f"/api/clients/{client_id}", expected_status=200)
        
        # 3. UPDATE (PUT)
        update_data = {
            "company_name": f"TEST_Cliente_Updated_{TIMESTAMP}",
            "cnpj": "12345678000199",
            "plan": "pro",
            "status": "active"
        }
        test_endpoint("clients", "PUT", f"/api/clients/{client_id}", update_data, 200)
        
        # 4. DELETE
        test_endpoint("clients", "DELETE", f"/api/clients/{client_id}", expected_status=204)
        created_ids["clients"].remove(client_id)  # Removido da lista


def validate_leads():
    """Valida CRUD de Leads"""
    log("\n" + "="*60)
    log("VALIDANDO LEADS")
    log("="*60)
    
    # Precisamos de um client_id válido
    # Criar cliente temporário
    client_data = {
        "company_name": f"TEST_Cliente_For_Leads_{TIMESTAMP}",
        "cnpj": "98765432000188",
        "plan": "basic",
        "status": "active"
    }
    client_result = test_endpoint("clients", "POST", "/api/clients", client_data, 201)
    
    if not client_result["success"]:
        log("❌ Não foi possível criar cliente para testar leads")
        return
    
    client_id = client_result["data"]["id"]
    created_ids["clients"].append(client_id)
    
    # 1. CREATE (POST)
    lead_data = {
        "client_id": client_id,
        "name": f"TEST_Lead_{TIMESTAMP}",
        "phone": "+5511999999999",
        "email": f"test_lead_{TIMESTAMP}@example.com",
        "status": "active"
    }
    result = test_endpoint("leads", "POST", "/api/leads", lead_data, 201)
    
    if result["success"]:
        lead_id = result["data"]["id"]
        created_ids["leads"].append(lead_id)
        log(f"   Created lead ID: {lead_id}")
        
        # 2. READ (GET by ID)
        test_endpoint("leads", "GET", f"/api/leads/{lead_id}", expected_status=200)
        
        # 3. UPDATE (PUT)
        update_data = {
            "client_id": client_id,
            "name": f"TEST_Lead_Updated_{TIMESTAMP}",
            "phone": "+5511988888888",
            "email": f"test_lead_updated_{TIMESTAMP}@example.com",
            "status": "active"
        }
        test_endpoint("leads", "PUT", f"/api/leads/{lead_id}", update_data, 200)
        
        # 4. DELETE
        test_endpoint("leads", "DELETE", f"/api/leads/{lead_id}", expected_status=204)
        created_ids["leads"].remove(lead_id)
    
    # Cleanup: deletar cliente temporário
    test_endpoint("clients", "DELETE", f"/api/clients/{client_id}", expected_status=204)
    created_ids["clients"].remove(client_id)


def validate_projects():
    """Valida CRUD de Projects"""
    log("\n" + "="*60)
    log("VALIDANDO PROJECTS")
    log("="*60)
    
    # Precisamos de um client_id válido
    client_data = {
        "company_name": f"TEST_Cliente_For_Projects_{TIMESTAMP}",
        "cnpj": "11122233000144",
        "plan": "basic",
        "status": "active"
    }
    client_result = test_endpoint("clients", "POST", "/api/clients", client_data, 201)
    
    if not client_result["success"]:
        log("❌ Não foi possível criar cliente para testar projetos")
        return
    
    client_id = client_result["data"]["id"]
    created_ids["clients"].append(client_id)
    
    # 1. CREATE (POST)
    project_data = {
        "client_id": client_id,
        "name": f"TEST_Project_{TIMESTAMP}",
        "description": "Projeto de teste para validação CRUD",
        "type": "survey",
        "status": "active"
    }
    result = test_endpoint("projects", "POST", "/api/projects", project_data, 201)
    
    if result["success"]:
        project_id = result["data"]["id"]
        created_ids["projects"].append(project_id)
        log(f"   Created project ID: {project_id}")
        
        # 2. READ (GET by ID)
        test_endpoint("projects", "GET", f"/api/projects/{project_id}", expected_status=200)
        
        # 3. UPDATE (PUT)
        update_data = {
            "client_id": client_id,
            "name": f"TEST_Project_Updated_{TIMESTAMP}",
            "description": "Projeto atualizado",
            "type": "campaign",
            "status": "paused"
        }
        test_endpoint("projects", "PUT", f"/api/projects/{project_id}", update_data, 200)
        
        # 4. DELETE
        test_endpoint("projects", "DELETE", f"/api/projects/{project_id}", expected_status=204)
        created_ids["projects"].remove(project_id)
    
    # Cleanup: deletar cliente temporário
    test_endpoint("clients", "DELETE", f"/api/clients/{client_id}", expected_status=204)
    created_ids["clients"].remove(client_id)


def validate_conversations():
    """Valida CRUD de Conversations"""
    log("\n" + "="*60)
    log("VALIDANDO CONVERSATIONS")
    log("="*60)
    
    # Precisamos de client_id e lead_id válidos
    client_data = {
        "company_name": f"TEST_Cliente_For_Conversations_{TIMESTAMP}",
        "cnpj": "55566677000133",
        "plan": "basic",
        "status": "active"
    }
    client_result = test_endpoint("clients", "POST", "/api/clients", client_data, 201)
    
    if not client_result["success"]:
        log("❌ Não foi possível criar cliente para testar conversas")
        return
    
    client_id = client_result["data"]["id"]
    created_ids["clients"].append(client_id)
    
    # Criar lead
    lead_data = {
        "client_id": client_id,
        "name": f"TEST_Lead_For_Conversations_{TIMESTAMP}",
        "phone": "+5511977777777",
        "email": f"test_conv_{TIMESTAMP}@example.com",
        "status": "active"
    }
    lead_result = test_endpoint("leads", "POST", "/api/leads", lead_data, 201)
    
    if not lead_result["success"]:
        log("❌ Não foi possível criar lead para testar conversas")
        test_endpoint("clients", "DELETE", f"/api/clients/{client_id}", expected_status=204)
        created_ids["clients"].remove(client_id)
        return
    
    lead_id = lead_result["data"]["id"]
    created_ids["leads"].append(lead_id)
    
    # 1. CREATE (POST)
    conversation_data = {
        "lead_id": lead_id,
        "client_id": client_id,
        "status": "open"
    }
    result = test_endpoint("conversations", "POST", "/api/conversations", conversation_data, 201)
    
    if result["success"]:
        conversation_id = result["data"]["id"]
        created_ids["conversations"].append(conversation_id)
        log(f"   Created conversation ID: {conversation_id}")
        
        # 2. READ (GET by ID)
        test_endpoint("conversations", "GET", f"/api/conversations/{conversation_id}", expected_status=200)
        
        # 3. POST MESSAGE
        message_data = {
            "content": f"TEST_Message_{TIMESTAMP}",
            "role": "user"
        }
        test_endpoint("conversations", "POST", f"/api/conversations/{conversation_id}/messages", message_data, 201)
        
        # 4. GET MESSAGES
        test_endpoint("conversations", "GET", f"/api/conversations/{conversation_id}/messages", expected_status=200)
    
    # Cleanup
    if conversation_id in created_ids["conversations"]:
        created_ids["conversations"].remove(conversation_id)
    test_endpoint("leads", "DELETE", f"/api/leads/{lead_id}", expected_status=204)
    created_ids["leads"].remove(lead_id)
    test_endpoint("clients", "DELETE", f"/api/clients/{client_id}", expected_status=204)
    created_ids["clients"].remove(client_id)


def validate_interviews():
    """Valida CRUD de Interviews"""
    log("\n" + "="*60)
    log("VALIDANDO INTERVIEWS")
    log("="*60)
    
    # Precisamos de client_id, lead_id e project_id válidos
    client_data = {
        "company_name": f"TEST_Cliente_For_Interviews_{TIMESTAMP}",
        "cnpj": "99988877000166",
        "plan": "basic",
        "status": "active"
    }
    client_result = test_endpoint("clients", "POST", "/api/clients", client_data, 201)
    
    if not client_result["success"]:
        log("❌ Não foi possível criar cliente para testar entrevistas")
        return
    
    client_id = client_result["data"]["id"]
    created_ids["clients"].append(client_id)
    
    # Criar lead
    lead_data = {
        "client_id": client_id,
        "name": f"TEST_Lead_For_Interviews_{TIMESTAMP}",
        "phone": "+5511966666666",
        "email": f"test_interview_{TIMESTAMP}@example.com",
        "status": "active"
    }
    lead_result = test_endpoint("leads", "POST", "/api/leads", lead_data, 201)
    
    if not lead_result["success"]:
        log("❌ Não foi possível criar lead para testar entrevistas")
        test_endpoint("clients", "DELETE", f"/api/clients/{client_id}", expected_status=204)
        created_ids["clients"].remove(client_id)
        return
    
    lead_id = lead_result["data"]["id"]
    created_ids["leads"].append(lead_id)
    
    # Criar project
    project_data = {
        "client_id": client_id,
        "name": f"TEST_Project_For_Interviews_{TIMESTAMP}",
        "description": "Projeto para teste de entrevistas",
        "type": "survey",
        "status": "active"
    }
    project_result = test_endpoint("projects", "POST", "/api/projects", project_data, 201)
    
    if not project_result["success"]:
        log("❌ Não foi possível criar projeto para testar entrevistas")
        test_endpoint("leads", "DELETE", f"/api/leads/{lead_id}", expected_status=204)
        created_ids["leads"].remove(lead_id)
        test_endpoint("clients", "DELETE", f"/api/clients/{client_id}", expected_status=204)
        created_ids["clients"].remove(client_id)
        return
    
    project_id = project_result["data"]["id"]
    created_ids["projects"].append(project_id)
    
    # 1. START INTERVIEW (POST)
    interview_data = {
        "lead_id": lead_id,
        "project_id": project_id
    }
    result = test_endpoint("interviews", "POST", "/api/interviews/start", interview_data, 201)
    
    if result["success"]:
        interview_id = result["data"]["id"]
        created_ids["interviews"].append(interview_id)
        log(f"   Created interview ID: {interview_id}")
        
        # 2. READ (GET by ID)
        test_endpoint("interviews", "GET", f"/api/interviews/{interview_id}", expected_status=200)
    
    # Cleanup
    if interview_id in created_ids["interviews"]:
        created_ids["interviews"].remove(interview_id)
    test_endpoint("projects", "DELETE", f"/api/projects/{project_id}", expected_status=204)
    created_ids["projects"].remove(project_id)
    test_endpoint("leads", "DELETE", f"/api/leads/{lead_id}", expected_status=204)
    created_ids["leads"].remove(lead_id)
    test_endpoint("clients", "DELETE", f"/api/clients/{client_id}", expected_status=204)
    created_ids["clients"].remove(client_id)


def print_summary():
    """Imprime resumo dos resultados"""
    log("\n" + "="*60)
    log("RESUMO DA VALIDAÇÃO CRUD")
    log("="*60)
    
    total_tests = 0
    total_success = 0
    
    for entity, data in results.items():
        total_tests += data["total"]
        total_success += data["success"]
        
        if data["total"] > 0:
            percentage = (data["success"] / data["total"]) * 100
            status = "✅" if percentage == 100 else "⚠️" if percentage >= 50 else "❌"
            
            log(f"\n{entity.upper()}:")
            log(f"  {status} {data['success']}/{data['total']} testes passaram ({percentage:.1f}%)")
            
            if data["errors"]:
                log(f"  Erros encontrados:")
                for error in data["errors"]:
                    log(f"    - {error}")
    
    # Total geral
    if total_tests > 0:
        overall_percentage = (total_success / total_tests) * 100
        log(f"\n{'='*60}")
        log(f"TOTAL GERAL: {total_success}/{total_tests} ({overall_percentage:.1f}%)")
        log(f"{'='*60}")
        
        if overall_percentage >= 90:
            log("✅ CRUD VALIDADO - Sistema funcionando bem")
        elif overall_percentage >= 70:
            log("⚠️ CRUD PARCIALMENTE FUNCIONAL - Alguns problemas encontrados")
        else:
            log("❌ CRUD COM PROBLEMAS - Muitos erros encontrados")
    
    # IDs que sobraram (não foram deletados)
    log(f"\n{'='*60}")
    log("DADOS DE TESTE RESTANTES:")
    log(f"{'='*60}")
    for entity, ids in created_ids.items():
        if ids:
            log(f"{entity}: {len(ids)} registros não deletados")
            for id in ids:
                log(f"  - {id}")
        else:
            log(f"{entity}: ✅ Nenhum registro restante")


if __name__ == "__main__":
    log("="*60)
    log("INICIANDO VALIDAÇÃO CRUD COMPLETA")
    log("="*60)
    log(f"Base URL: {BASE_URL}")
    log(f"Timestamp: {TIMESTAMP}")
    log(f"Token: {TOKEN[:20]}...")
    
    try:
        # Executar validações
        validate_clients()
        validate_leads()
        validate_projects()
        validate_conversations()
        validate_interviews()
        
        # Imprimir resumo
        print_summary()
        
    except KeyboardInterrupt:
        log("\n\n⚠️ Validação interrompida pelo usuário")
        print_summary()
    except Exception as e:
        log(f"\n\n❌ ERRO FATAL: {str(e)}")
        import traceback
        traceback.print_exc()
        print_summary()
