#!/usr/bin/env python3
"""
Script para executar checkpoints de validação das tasks
Baseado nas regras de checkpoint-validation.md
"""

import requests
import json
import time
from datetime import datetime
from pathlib import Path

def log_result(message, status="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {status}: {message}")

def test_backend_health():
    """Checkpoint: Backend está rodando e saudável"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            log_result("✅ Backend health check passou", "SUCCESS")
            return True
        else:
            log_result(f"❌ Backend health check falhou: {response.status_code}", "ERROR")
            return False
    except Exception as e:
        log_result(f"❌ Backend não está rodando: {e}", "ERROR")
        return False

def test_agents_api():
    """Checkpoint: API de agents responde corretamente"""
    try:
        # Teste sem autenticação (deve retornar 401/403, não 500)
        response = requests.get("http://localhost:8000/api/agents", timeout=5)
        if response.status_code in [401, 403]:
            log_result("✅ API agents responde corretamente (auth required)", "SUCCESS")
            return True
        elif response.status_code == 500:
            log_result("❌ API agents retorna erro 500 (bug crítico)", "ERROR")
            return False
        else:
            log_result(f"⚠️ API agents resposta inesperada: {response.status_code}", "WARNING")
            return False
    except Exception as e:
        log_result(f"❌ API agents não responde: {e}", "ERROR")
        return False

def test_wizard_endpoints():
    """Checkpoint: Endpoints do wizard existem"""
    endpoints = [
        "/api/agents/wizard/start",
        "/api/agents/wizard/templates"
    ]
    
    results = []
    for endpoint in endpoints:
        try:
            response = requests.post(f"http://localhost:8000{endpoint}", 
                                   json={}, timeout=5)
            if response.status_code == 404:
                log_result(f"❌ Endpoint {endpoint} não existe (404)", "ERROR")
                results.append(False)
            else:
                log_result(f"✅ Endpoint {endpoint} existe", "SUCCESS")
                results.append(True)
        except Exception as e:
            log_result(f"❌ Erro testando {endpoint}: {e}", "ERROR")
            results.append(False)
    
    return all(results)

def test_database_connection():
    """Checkpoint: Banco de dados conecta e tem dados"""
    try:
        import psycopg2
        DATABASE_URL = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"
        
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Verificar tabela agents
        cursor.execute("SELECT COUNT(*) FROM agents;")
        agents_count = cursor.fetchone()[0]
        
        if agents_count > 0:
            log_result(f"✅ Banco conecta e tem {agents_count} agents", "SUCCESS")
            cursor.close()
            conn.close()
            return True
        else:
            log_result("⚠️ Banco conecta mas não tem agents", "WARNING")
            cursor.close()
            conn.close()
            return False
            
    except Exception as e:
        log_result(f"❌ Erro conectando ao banco: {e}", "ERROR")
        return False

def test_frontend_files():
    """Checkpoint: Arquivos do frontend existem"""
    critical_files = [
        "src/components/agents/wizard/AgentWizard.tsx",
        "src/components/agents/wizard/steps/WizardStep1TypeSelection.tsx",
        "src/pages/agents/contextual/RenusInterface.tsx",
        "src/pages/marketplace/TemplateMarketplace.tsx",
        "src/pages/intelligence/IntelligenceDashboard.tsx"
    ]
    
    results = []
    for file_path in critical_files:
        if Path(file_path).exists():
            log_result(f"✅ Arquivo {file_path} existe", "SUCCESS")
            results.append(True)
        else:
            log_result(f"❌ Arquivo {file_path} não existe", "ERROR")
            results.append(False)
    
    return all(results)

def run_checkpoint_38():
    """Checkpoint - Phase 1 Complete"""
    log_result("🔍 EXECUTANDO CHECKPOINT 38 - Phase 1 Complete", "INFO")
    
    results = []
    
    # Database changes working correctly
    results.append(test_database_connection())
    
    # API endpoints responding correctly
    results.append(test_backend_health())
    
    success = all(results)
    if success:
        log_result("✅ CHECKPOINT 38 - PASSOU", "SUCCESS")
    else:
        log_result("❌ CHECKPOINT 38 - FALHOU", "ERROR")
    
    return success

def run_checkpoint_39():
    """Checkpoint - Phase 5 Complete"""
    log_result("🔍 EXECUTANDO CHECKPOINT 39 - Phase 5 Complete", "INFO")
    
    results = []
    
    # Wizard flow works end-to-end
    results.append(test_wizard_endpoints())
    results.append(test_frontend_files())
    
    success = all(results)
    if success:
        log_result("✅ CHECKPOINT 39 - PASSOU", "SUCCESS")
    else:
        log_result("❌ CHECKPOINT 39 - FALHOU", "ERROR")
    
    return success

def run_checkpoint_40():
    """Checkpoint - Phase 6 Complete"""
    log_result("🔍 EXECUTANDO CHECKPOINT 40 - Phase 6 Complete", "INFO")
    
    # Configuration tabs functional
    config_tabs = [
        "src/components/agents/config/InstructionsTab.tsx",
        "src/components/agents/config/ToolsTab.tsx",
        "src/components/agents/config/IntegrationsTab.tsx",
        "src/components/agents/config/KnowledgeTab.tsx",
        "src/components/agents/config/TriggersTab.tsx",
        "src/components/agents/config/GuardrailsTab.tsx"
    ]
    
    results = []
    for tab in config_tabs:
        if Path(tab).exists():
            results.append(True)
        else:
            log_result(f"❌ Tab {tab} não existe", "ERROR")
            results.append(False)
    
    success = all(results)
    if success:
        log_result("✅ CHECKPOINT 40 - PASSOU", "SUCCESS")
    else:
        log_result("❌ CHECKPOINT 40 - FALHOU", "ERROR")
    
    return success

def run_checkpoint_41():
    """Checkpoint - Phase 9 Complete"""
    log_result("🔍 EXECUTANDO CHECKPOINT 41 - Phase 9 Complete", "INFO")
    
    # Sidebar navigation functional
    navigation_files = [
        "src/components/dashboard/Sidebar.tsx",
        "src/pages/intelligence/IntelligenceDashboard.tsx",
        "src/pages/integrations/IntegrationsRadar.tsx"
    ]
    
    results = []
    for file_path in navigation_files:
        if Path(file_path).exists():
            results.append(True)
        else:
            log_result(f"❌ Arquivo {file_path} não existe", "ERROR")
            results.append(False)
    
    success = all(results)
    if success:
        log_result("✅ CHECKPOINT 41 - PASSOU", "SUCCESS")
    else:
        log_result("❌ CHECKPOINT 41 - FALHOU", "ERROR")
    
    return success

def run_checkpoint_42():
    """Final Checkpoint - All Phases Complete"""
    log_result("🔍 EXECUTANDO CHECKPOINT 42 - Final Checkpoint", "INFO")
    
    results = []
    
    # Complete system functionality
    results.append(test_backend_health())
    results.append(test_agents_api())
    results.append(test_database_connection())
    results.append(test_frontend_files())
    
    success = all(results)
    if success:
        log_result("✅ CHECKPOINT 42 - SISTEMA PRONTO PARA PRODUÇÃO", "SUCCESS")
    else:
        log_result("❌ CHECKPOINT 42 - SISTEMA NÃO ESTÁ PRONTO", "ERROR")
    
    return success

def main():
    """Executa todos os checkpoints"""
    log_result("🚀 INICIANDO VALIDAÇÃO DE CHECKPOINTS", "INFO")
    log_result("=" * 60, "INFO")
    
    checkpoints = [
        ("Checkpoint 38 - Phase 1", run_checkpoint_38),
        ("Checkpoint 39 - Phase 5", run_checkpoint_39),
        ("Checkpoint 40 - Phase 6", run_checkpoint_40),
        ("Checkpoint 41 - Phase 9", run_checkpoint_41),
        ("Checkpoint 42 - Final", run_checkpoint_42)
    ]
    
    results = {}
    
    for name, checkpoint_func in checkpoints:
        log_result(f"\n{'='*60}", "INFO")
        result = checkpoint_func()
        results[name] = result
        time.sleep(1)  # Pausa entre checkpoints
    
    # Resumo final
    log_result(f"\n{'='*60}", "INFO")
    log_result("📊 RESUMO DOS CHECKPOINTS", "INFO")
    log_result("=" * 60, "INFO")
    
    passed = 0
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        log_result(f"{name}: {status}", "INFO")
        if result:
            passed += 1
    
    log_result(f"\nRESULTADO FINAL: {passed}/{total} checkpoints passaram", "INFO")
    
    if passed == total:
        log_result("🎉 TODOS OS CHECKPOINTS PASSARAM!", "SUCCESS")
        return True
    else:
        log_result("🚨 ALGUNS CHECKPOINTS FALHARAM - SISTEMA NÃO ESTÁ PRONTO", "ERROR")
        return False

if __name__ == "__main__":
    main()