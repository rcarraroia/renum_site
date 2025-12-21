#!/usr/bin/env python3
"""
Script CORRIGIDO para validar checkpoints - testa múltiplas portas
Baseado na correção do usuário: sistema roda na porta 8081, não 5173
"""

import os
import sys
import json
import requests
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Any, Tuple
import psycopg2
from psycopg2.extras import RealDictCursor

class CheckpointValidatorCorrigido:
    def __init__(self):
        self.results = {
            "checkpoint_38": {"status": "pending", "tests": [], "errors": []},
            "checkpoint_39": {"status": "pending", "tests": [], "errors": []},
            "checkpoint_40": {"status": "pending", "tests": [], "errors": []},
            "checkpoint_41": {"status": "pending", "tests": [], "errors": []},
            "checkpoint_42": {"status": "pending", "tests": [], "errors": []}
        }
        
        # CORREÇÃO: Testar múltiplas portas possíveis
        self.possible_backend_ports = [8000, 8080, 3000, 5000, 8081]
        self.possible_frontend_ports = [5173, 3000, 8080, 8081, 4173, 5174]
        
        self.backend_url = None
        self.frontend_url = None
        
        # Credenciais Supabase
        self.db_config = {
            'host': 'db.vhixvzaxswphwoymdhgg.supabase.co',
            'port': 5432,
            'database': 'postgres',
            'user': 'postgres',
            'password': 'BD5yEMQ9iDMOkeGW'
        }

    def discover_running_services(self):
        """Descobre automaticamente em quais portas os serviços estão rodando"""
        print("🔍 DESCOBRINDO SERVIÇOS ATIVOS...")
        
        # Descobrir backend
        for port in self.possible_backend_ports:
            try:
                test_url = f"http://localhost:{port}"
                response = requests.get(f"{test_url}/health", timeout=3)
                if response.status_code == 200:
                    self.backend_url = test_url
                    print(f"✅ Backend encontrado na porta {port}")
                    break
            except:
                continue
        
        if not self.backend_url:
            # Tentar endpoints alternativos
            for port in self.possible_backend_ports:
                try:
                    test_url = f"http://localhost:{port}"
                    response = requests.get(f"{test_url}/api/agents", timeout=3)
                    if response.status_code in [200, 401, 403]:  # Qualquer resposta válida
                        self.backend_url = test_url
                        print(f"✅ Backend encontrado na porta {port} (via /api/agents)")
                        break
                except:
                    continue
        
        # Descobrir frontend
        for port in self.possible_frontend_ports:
            try:
                test_url = f"http://localhost:{port}"
                response = requests.get(test_url, timeout=3)
                if response.status_code == 200:
                    # Verificar se é realmente frontend (contém HTML)
                    if "html" in response.text.lower() or "react" in response.text.lower():
                        self.frontend_url = test_url
                        print(f"✅ Frontend encontrado na porta {port}")
                        break
            except:
                continue
        
        print(f"Backend URL: {self.backend_url or 'NÃO ENCONTRADO'}")
        print(f"Frontend URL: {self.frontend_url or 'NÃO ENCONTRADO'}")

    def log_test(self, checkpoint: str, test_name: str, status: str, details: str = ""):
        """Log resultado de um teste específico"""
        self.results[checkpoint]["tests"].append({
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        print(f"[{checkpoint}] {test_name}: {status}")
        if details:
            print(f"    Details: {details}")

    def log_error(self, checkpoint: str, error: str):
        """Log erro encontrado"""
        self.results[checkpoint]["errors"].append({
            "error": error,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        print(f"[{checkpoint}] ERROR: {error}")

    def test_database_connection(self) -> bool:
        """Testa conexão com banco de dados"""
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT 1")
            conn.close()
            return True
        except Exception as e:
            print(f"Erro conexão DB: {e}")
            return False

    def test_backend_health(self) -> bool:
        """Testa se backend está rodando"""
        if not self.backend_url:
            return False
        
        try:
            # Tentar /health primeiro
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            if response.status_code == 200:
                return True
        except:
            pass
        
        try:
            # Tentar /api/agents como alternativa
            response = requests.get(f"{self.backend_url}/api/agents", timeout=5)
            if response.status_code in [200, 401, 403]:  # Qualquer resposta válida
                return True
        except:
            pass
        
        return False

    def test_frontend_health(self) -> bool:
        """Testa se frontend está rodando"""
        if not self.frontend_url:
            return False
        
        try:
            response = requests.get(self.frontend_url, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"Frontend não acessível: {e}")
            return False

    def test_frontend_functionality(self) -> Dict[str, Any]:
        """Testa funcionalidades específicas do frontend"""
        if not self.frontend_url:
            return {"accessible": False, "dashboard": False, "data_loading": False}
        
        results = {"accessible": False, "dashboard": False, "data_loading": False}
        
        try:
            # Testar página principal
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                results["accessible"] = True
                
                # Verificar se contém elementos do dashboard
                content = response.text.lower()
                if "dashboard" in content or "admin" in content:
                    results["dashboard"] = True
                
                # Verificar se há indicações de carregamento de dados
                if "clientes" in content or "projetos" in content or "conversas" in content:
                    results["data_loading"] = True
            
        except Exception as e:
            print(f"Erro testando frontend: {e}")
        
        return results

    def test_backend_endpoints(self) -> Dict[str, Any]:
        """Testa endpoints específicos do backend"""
        if not self.backend_url:
            return {}
        
        endpoints_to_test = [
            "/api/agents",
            "/api/clients", 
            "/api/leads",
            "/api/projects",
            "/api/agents/wizard/templates"
        ]
        
        results = {}
        
        for endpoint in endpoints_to_test:
            try:
                response = requests.get(f"{self.backend_url}{endpoint}", timeout=5)
                results[endpoint] = {
                    "status_code": response.status_code,
                    "accessible": response.status_code in [200, 401, 403, 422],
                    "response_size": len(response.text)
                }
            except Exception as e:
                results[endpoint] = {
                    "status_code": None,
                    "accessible": False,
                    "error": str(e)
                }
        
        return results

    def checkpoint_38_phase1_complete_corrigido(self):
        """Checkpoint 38 corrigido com descoberta automática de serviços"""
        checkpoint = "checkpoint_38"
        print(f"\n=== EXECUTANDO {checkpoint.upper()} - PHASE 1 COMPLETE (CORRIGIDO) ===")
        
        # Test 1: Database connection
        if self.test_database_connection():
            self.log_test(checkpoint, "Database Connection", "✅ PASS", "Conectou ao Supabase")
        else:
            self.log_test(checkpoint, "Database Connection", "❌ FAIL", "Não conseguiu conectar")
            self.results[checkpoint]["status"] = "failed"
            return

        # Test 2: Verificar tabelas críticas (mesmo código anterior)
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Verificar tabela agents
            cursor.execute("SELECT COUNT(*) as count FROM information_schema.tables WHERE table_name = 'agents'")
            agents_exists = cursor.fetchone()['count'] > 0
            
            if agents_exists:
                self.log_test(checkpoint, "Agents Table Exists", "✅ PASS", "Tabela agents existe")
                
                # Verificar dados na tabela
                cursor.execute("SELECT COUNT(*) as count FROM agents")
                agent_count = cursor.fetchone()['count']
                self.log_test(checkpoint, "Agents Table Data", "✅ PASS" if agent_count > 0 else "⚠️ EMPTY", f"{agent_count} registros")
                
            else:
                self.log_test(checkpoint, "Agents Table Exists", "❌ FAIL", "Tabela agents não existe")
            
            conn.close()
            
        except Exception as e:
            self.log_error(checkpoint, f"Erro verificando tabelas: {e}")
            self.log_test(checkpoint, "Database Tables Check", "❌ FAIL", str(e))

        # Test 3: Backend API Health (CORRIGIDO)
        if self.test_backend_health():
            self.log_test(checkpoint, "Backend API Health", "✅ PASS", f"Backend respondendo em {self.backend_url}")
            
            # Test 4: Testar endpoints específicos (CORRIGIDO)
            endpoint_results = self.test_backend_endpoints()
            
            working_endpoints = 0
            total_endpoints = len(endpoint_results)
            
            for endpoint, result in endpoint_results.items():
                if result.get("accessible", False):
                    working_endpoints += 1
                    self.log_test(checkpoint, f"Endpoint {endpoint}", "✅ PASS", f"Status {result['status_code']}")
                else:
                    self.log_test(checkpoint, f"Endpoint {endpoint}", "❌ FAIL", f"Status {result.get('status_code', 'N/A')}")
            
            if working_endpoints > 0:
                self.log_test(checkpoint, "API Endpoints Overall", "✅ PASS", f"{working_endpoints}/{total_endpoints} endpoints acessíveis")
            else:
                self.log_test(checkpoint, "API Endpoints Overall", "❌ FAIL", "Nenhum endpoint acessível")
                
        else:
            self.log_test(checkpoint, "Backend API Health", "❌ FAIL", "Backend não encontrado em nenhuma porta")

        # Determinar status final do checkpoint
        failed_tests = [t for t in self.results[checkpoint]["tests"] if t["status"] == "❌ FAIL"]
        if failed_tests:
            self.results[checkpoint]["status"] = "failed"
        else:
            self.results[checkpoint]["status"] = "passed"

    def checkpoint_39_phase5_complete_corrigido(self):
        """Checkpoint 39 corrigido - Wizard Implementation"""
        checkpoint = "checkpoint_39"
        print(f"\n=== EXECUTANDO {checkpoint.upper()} - PHASE 5 COMPLETE (CORRIGIDO) ===")
        
        # Test 1: Verificar arquivos do wizard (mesmo código)
        wizard_files = [
            "src/components/agents/wizard/steps/WizardStep1TypeSelection.tsx",
            "src/components/agents/wizard/steps/WizardStep2BasicInfo.tsx",
            "src/components/agents/wizard/steps/WizardStep3Personality.tsx",
            "src/components/agents/wizard/steps/WizardStep4DataCollection.tsx",
            "src/components/agents/wizard/steps/WizardStep5Integrations.tsx",
            "src/components/agents/wizard/steps/WizardStep6TestPublish.tsx",
            "src/components/agents/wizard/AgentWizard.tsx"
        ]
        
        missing_files = []
        for file_path in wizard_files:
            if os.path.exists(file_path):
                self.log_test(checkpoint, f"Wizard File: {os.path.basename(file_path)}", "✅ PASS", "Arquivo existe")
            else:
                missing_files.append(file_path)
                self.log_test(checkpoint, f"Wizard File: {os.path.basename(file_path)}", "❌ FAIL", "Arquivo não existe")
        
        if not missing_files:
            self.log_test(checkpoint, "All Wizard Files Present", "✅ PASS", "Todos os 7 arquivos do wizard existem")
        else:
            self.log_test(checkpoint, "All Wizard Files Present", "❌ FAIL", f"{len(missing_files)} arquivos faltando")

        # Test 2: Frontend Health (CORRIGIDO)
        if self.test_frontend_health():
            self.log_test(checkpoint, "Frontend Health", "✅ PASS", f"Frontend rodando em {self.frontend_url}")
            
            # Test 3: Testar funcionalidades do frontend (NOVO)
            frontend_results = self.test_frontend_functionality()
            
            if frontend_results["accessible"]:
                self.log_test(checkpoint, "Frontend Accessible", "✅ PASS", "Frontend acessível")
            else:
                self.log_test(checkpoint, "Frontend Accessible", "❌ FAIL", "Frontend não acessível")
            
            if frontend_results["dashboard"]:
                self.log_test(checkpoint, "Dashboard Elements", "✅ PASS", "Elementos de dashboard encontrados")
            else:
                self.log_test(checkpoint, "Dashboard Elements", "⚠️ PARTIAL", "Dashboard não identificado claramente")
            
            if frontend_results["data_loading"]:
                self.log_test(checkpoint, "Data Loading Evidence", "✅ PASS", "Evidências de carregamento de dados")
            else:
                self.log_test(checkpoint, "Data Loading Evidence", "⚠️ PARTIAL", "Carregamento de dados não identificado")
                
        else:
            self.log_test(checkpoint, "Frontend Health", "❌ FAIL", "Frontend não encontrado em nenhuma porta")

        # Test 4: Backend wizard endpoints (se backend disponível)
        if self.backend_url:
            wizard_endpoints = [
                "/api/agents/wizard/start",
                "/api/agents/wizard/templates",
                "/api/agents/wizard/step/1"
            ]
            
            for endpoint in wizard_endpoints:
                try:
                    response = requests.post(f"{self.backend_url}{endpoint}", json={}, timeout=5)
                    if response.status_code in [200, 201, 400, 422]:  # 400/422 são aceitáveis (validação)
                        self.log_test(checkpoint, f"Wizard Endpoint: {endpoint}", "✅ PASS", f"Status {response.status_code}")
                    elif response.status_code == 404:
                        self.log_test(checkpoint, f"Wizard Endpoint: {endpoint}", "❌ NOT_IMPLEMENTED", f"Status {response.status_code}")
                    else:
                        self.log_test(checkpoint, f"Wizard Endpoint: {endpoint}", "❌ FAIL", f"Status {response.status_code}")
                except Exception as e:
                    self.log_test(checkpoint, f"Wizard Endpoint: {endpoint}", "❌ FAIL", str(e))

        # Determinar status final
        failed_tests = [t for t in self.results[checkpoint]["tests"] if t["status"] == "❌ FAIL"]
        not_implemented = [t for t in self.results[checkpoint]["tests"] if "NOT_IMPLEMENTED" in t["status"]]
        
        if failed_tests:
            self.results[checkpoint]["status"] = "failed"
        elif not_implemented:
            self.results[checkpoint]["status"] = "partial"
        else:
            self.results[checkpoint]["status"] = "passed"

    def run_all_checkpoints_corrigido(self):
        """Executa todos os checkpoints com descoberta automática"""
        print("🚀 INICIANDO EXECUÇÃO DE CHECKPOINTS CORRIGIDOS")
        print("=" * 60)
        
        # PRIMEIRO: Descobrir serviços ativos
        self.discover_running_services()
        
        # Executar checkpoints corrigidos
        self.checkpoint_38_phase1_complete_corrigido()
        self.checkpoint_39_phase5_complete_corrigido()
        
        # Para os outros checkpoints, usar a mesma lógica de descoberta
        # (implementar conforme necessário)
        
        return self.results

    def generate_report_corrigido(self):
        """Gera relatório corrigido"""
        report = {
            "execution_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "discovered_services": {
                "backend_url": self.backend_url,
                "frontend_url": self.frontend_url,
                "backend_ports_tested": self.possible_backend_ports,
                "frontend_ports_tested": self.possible_frontend_ports
            },
            "summary": {
                "total_checkpoints": len(self.results),
                "passed": 0,
                "failed": 0,
                "partial": 0
            },
            "checkpoints": self.results
        }
        
        # Calcular resumo
        for checkpoint_data in self.results.values():
            status = checkpoint_data["status"]
            if status == "passed":
                report["summary"]["passed"] += 1
            elif status == "failed":
                report["summary"]["failed"] += 1
            elif status == "partial":
                report["summary"]["partial"] += 1
        
        return report

def main():
    """Função principal corrigida"""
    print("🔍 EXECUTANDO CHECKPOINTS CORRIGIDOS - DESCOBERTA AUTOMÁTICA")
    print("=" * 60)
    
    validator = CheckpointValidatorCorrigido()
    results = validator.run_all_checkpoints_corrigido()
    report = validator.generate_report_corrigido()
    
    # Salvar relatório corrigido
    report_path = "docs/validacoes/RELATORIO_CHECKPOINTS_CORRIGIDO.json"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 RELATÓRIO CORRIGIDO SALVO EM: {report_path}")
    
    # Resumo final corrigido
    print("\n" + "=" * 60)
    print("📋 RESUMO FINAL DOS CHECKPOINTS CORRIGIDOS")
    print("=" * 60)
    
    print(f"🔍 SERVIÇOS DESCOBERTOS:")
    print(f"   Backend: {validator.backend_url or 'NÃO ENCONTRADO'}")
    print(f"   Frontend: {validator.frontend_url or 'NÃO ENCONTRADO'}")
    print()
    
    for checkpoint_id, data in results.items():
        status_icon = {
            "passed": "✅",
            "failed": "❌", 
            "partial": "⚠️",
            "pending": "⏳"
        }.get(data["status"], "❓")
        
        print(f"{status_icon} {checkpoint_id.upper()}: {data['status'].upper()}")
        print(f"   Testes executados: {len(data['tests'])}")
        print(f"   Erros encontrados: {len(data['errors'])}")
        print()
    
    # Status geral
    summary = report["summary"]
    print(f"🎯 RESULTADO GERAL CORRIGIDO:")
    print(f"   ✅ Passou: {summary['passed']}/{summary['total_checkpoints']} checkpoints")
    print(f"   ❌ Falhou: {summary['failed']}/{summary['total_checkpoints']} checkpoints") 
    print(f"   ⚠️ Parcial: {summary['partial']}/{summary['total_checkpoints']} checkpoints")
    
    return report

if __name__ == "__main__":
    main()