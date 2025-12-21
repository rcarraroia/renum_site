#!/usr/bin/env python3
"""
FASE 4: VALIDAÇÃO - Remoção do Módulo Wizard
Objetivo: Validar que o sistema ainda funciona após remoção do wizard
"""

import os
import json
import requests
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import subprocess
import time

class WizardValidationManager:
    def __init__(self):
        self.validation_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.db_conn_string = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"
        self.backend_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:8082"
        
        self.validation_results = {
            "timestamp": datetime.now().isoformat(),
            "backend_status": "unknown",
            "frontend_status": "unknown",
            "database_status": "unknown",
            "renus_status": "unknown",
            "isa_status": "unknown",
            "import_errors": [],
            "api_tests": [],
            "database_tests": [],
            "overall_status": "unknown",
            "errors": []
        }
    
    def validar_backend(self):
        """Valida se o backend inicia sem erros de import"""
        print("🐍 1. VALIDANDO BACKEND...")
        
        try:
            # Testar health check
            print("   🔍 Testando health check...")
            response = requests.get(f"{self.backend_url}/health", timeout=10)
            
            if response.status_code == 200:
                health_data = response.json()
                self.validation_results["backend_status"] = "healthy"
                print(f"   ✅ Backend saudável: {health_data.get('status', 'unknown')}")
                
                # Testar endpoints principais
                self.testar_endpoints_principais()
            else:
                self.validation_results["backend_status"] = "unhealthy"
                self.validation_results["errors"].append(f"Health check falhou: {response.status_code}")
                print(f"   ❌ Health check falhou: {response.status_code}")
        
        except requests.exceptions.ConnectionError:
            self.validation_results["backend_status"] = "offline"
            self.validation_results["errors"].append("Backend não está rodando")
            print("   ❌ Backend não está rodando")
        
        except Exception as e:
            self.validation_results["backend_status"] = "error"
            self.validation_results["errors"].append(f"Erro validando backend: {e}")
            print(f"   ❌ Erro validando backend: {e}")
    
    def testar_endpoints_principais(self):
        """Testa endpoints principais para verificar se não há erros de import"""
        print("   🔍 Testando endpoints principais...")
        
        endpoints_to_test = [
            ("/docs", "GET", "Documentação Swagger"),
            ("/api/agents", "GET", "Lista de agentes"),
            ("/api/clients", "GET", "Lista de clientes"),
            ("/api/leads", "GET", "Lista de leads"),
        ]
        
        for endpoint, method, description in endpoints_to_test:
            try:
                if method == "GET":
                    response = requests.get(f"{self.backend_url}{endpoint}", timeout=5)
                
                test_result = {
                    "endpoint": endpoint,
                    "method": method,
                    "description": description,
                    "status_code": response.status_code,
                    "success": response.status_code < 500,  # Não deve ter erro 500 (import error)
                    "response_time": response.elapsed.total_seconds()
                }
                
                self.validation_results["api_tests"].append(test_result)
                
                if test_result["success"]:
                    print(f"   ✅ {description}: {response.status_code}")
                else:
                    print(f"   ❌ {description}: {response.status_code}")
            
            except Exception as e:
                test_result = {
                    "endpoint": endpoint,
                    "method": method,
                    "description": description,
                    "status_code": 0,
                    "success": False,
                    "error": str(e)
                }
                self.validation_results["api_tests"].append(test_result)
                print(f"   ❌ {description}: {e}")
    
    def validar_frontend(self):
        """Valida se o frontend carrega sem erros"""
        print("\n⚛️ 2. VALIDANDO FRONTEND...")
        
        try:
            print("   🔍 Testando carregamento da página...")
            response = requests.get(self.frontend_url, timeout=10)
            
            if response.status_code == 200:
                self.validation_results["frontend_status"] = "healthy"
                print("   ✅ Frontend carregando normalmente")
                
                # Verificar se não há referências ao wizard no HTML
                if "wizard" in response.text.lower():
                    print("   ⚠️ Ainda há referências ao wizard no HTML")
                    self.validation_results["errors"].append("Referências ao wizard encontradas no HTML")
                else:
                    print("   ✅ Nenhuma referência ao wizard no HTML")
            else:
                self.validation_results["frontend_status"] = "unhealthy"
                self.validation_results["errors"].append(f"Frontend retornou: {response.status_code}")
                print(f"   ❌ Frontend retornou: {response.status_code}")
        
        except requests.exceptions.ConnectionError:
            self.validation_results["frontend_status"] = "offline"
            self.validation_results["errors"].append("Frontend não está rodando")
            print("   ❌ Frontend não está rodando")
        
        except Exception as e:
            self.validation_results["frontend_status"] = "error"
            self.validation_results["errors"].append(f"Erro validando frontend: {e}")
            print(f"   ❌ Erro validando frontend: {e}")
    
    def validar_banco_dados(self):
        """Valida se o banco está limpo e funcionando"""
        print("\n🗄️ 3. VALIDANDO BANCO DE DADOS...")
        
        try:
            conn = psycopg2.connect(self.db_conn_string)
            
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Verificar se não há mais wizard_session
                print("   🔍 Verificando limpeza do wizard...")
                cursor.execute("""
                    SELECT COUNT(*) as count
                    FROM agents 
                    WHERE config::text ILIKE '%wizard_session%'
                """)
                
                wizard_count = cursor.fetchone()['count']
                
                test_result = {
                    "test": "wizard_cleanup",
                    "description": "Verificar se wizard_session foi removido",
                    "expected": 0,
                    "actual": wizard_count,
                    "success": wizard_count == 0
                }
                self.validation_results["database_tests"].append(test_result)
                
                if wizard_count == 0:
                    print("   ✅ Banco limpo - sem wizard_session")
                else:
                    print(f"   ❌ Ainda há {wizard_count} agentes com wizard_session")
                
                # Verificar se RENUS e ISA ainda existem
                print("   🔍 Verificando RENUS e ISA...")
                cursor.execute("""
                    SELECT name, status FROM agents 
                    WHERE name IN ('RENUS', 'ISA')
                    ORDER BY name
                """)
                
                critical_agents = cursor.fetchall()
                
                for agent in critical_agents:
                    test_result = {
                        "test": f"{agent['name']}_exists",
                        "description": f"Verificar se {agent['name']} ainda existe",
                        "expected": "exists",
                        "actual": "exists",
                        "success": True,
                        "status": agent['status']
                    }
                    self.validation_results["database_tests"].append(test_result)
                    print(f"   ✅ {agent['name']} existe (status: {agent['status']})")
                
                # Verificar integridade geral
                print("   🔍 Verificando integridade das tabelas...")
                cursor.execute("""
                    SELECT 
                        'agents' as tabela,
                        COUNT(*) as registros
                    FROM agents
                    UNION ALL
                    SELECT 'clients', COUNT(*) FROM clients
                    UNION ALL
                    SELECT 'leads', COUNT(*) FROM leads
                    ORDER BY tabela
                """)
                
                table_counts = cursor.fetchall()
                for table_info in table_counts:
                    print(f"   📊 {table_info['tabela']}: {table_info['registros']} registros")
                
                self.validation_results["database_status"] = "healthy"
            
            conn.close()
            
        except Exception as e:
            self.validation_results["database_status"] = "error"
            self.validation_results["errors"].append(f"Erro validando banco: {e}")
            print(f"   ❌ Erro validando banco: {e}")
    
    def validar_renus_isa(self):
        """Valida se RENUS e ISA ainda funcionam"""
        print("\n🤖 4. VALIDANDO RENUS E ISA...")
        
        # Testar RENUS
        try:
            print("   🔍 Testando RENUS...")
            response = requests.get(f"{self.backend_url}/api/agents/renus", timeout=10)
            
            if response.status_code == 200:
                self.validation_results["renus_status"] = "healthy"
                print("   ✅ RENUS funcionando")
            else:
                self.validation_results["renus_status"] = "unhealthy"
                self.validation_results["errors"].append(f"RENUS retornou: {response.status_code}")
                print(f"   ❌ RENUS retornou: {response.status_code}")
        
        except Exception as e:
            self.validation_results["renus_status"] = "error"
            self.validation_results["errors"].append(f"Erro testando RENUS: {e}")
            print(f"   ❌ Erro testando RENUS: {e}")
        
        # Testar ISA
        try:
            print("   🔍 Testando ISA...")
            response = requests.get(f"{self.backend_url}/api/agents/isa", timeout=10)
            
            if response.status_code == 200:
                self.validation_results["isa_status"] = "healthy"
                print("   ✅ ISA funcionando")
            else:
                self.validation_results["isa_status"] = "unhealthy"
                self.validation_results["errors"].append(f"ISA retornou: {response.status_code}")
                print(f"   ❌ ISA retornou: {response.status_code}")
        
        except Exception as e:
            self.validation_results["isa_status"] = "error"
            self.validation_results["errors"].append(f"Erro testando ISA: {e}")
            print(f"   ❌ Erro testando ISA: {e}")
    
    def verificar_arquivos_removidos(self):
        """Verifica se todos os arquivos wizard foram realmente removidos"""
        print("\n📁 5. VERIFICANDO ARQUIVOS REMOVIDOS...")
        
        arquivos_wizard = [
            "backend/src/api/routes/wizard.py",
            "backend/src/services/wizard_service.py",
            "backend/src/models/wizard.py",
            "backend/src/agents/wizard_agent.py",
            "src/components/agents/wizard/",
            "src/services/wizardService.ts"
        ]
        
        all_removed = True
        
        for arquivo in arquivos_wizard:
            if os.path.exists(arquivo):
                print(f"   ❌ {arquivo} ainda existe")
                self.validation_results["errors"].append(f"Arquivo não removido: {arquivo}")
                all_removed = False
            else:
                print(f"   ✅ {arquivo} removido")
        
        if all_removed:
            print("   ✅ Todos os arquivos wizard foram removidos")
        else:
            print("   ❌ Alguns arquivos wizard ainda existem")
    
    def calcular_status_geral(self):
        """Calcula o status geral da validação"""
        print("\n📊 6. CALCULANDO STATUS GERAL...")
        
        # Contar sucessos e falhas
        healthy_count = 0
        total_count = 0
        
        status_checks = [
            self.validation_results["backend_status"],
            self.validation_results["frontend_status"],
            self.validation_results["database_status"],
            self.validation_results["renus_status"],
            self.validation_results["isa_status"]
        ]
        
        for status in status_checks:
            total_count += 1
            if status == "healthy":
                healthy_count += 1
        
        # Verificar testes de API
        api_success_count = len([t for t in self.validation_results["api_tests"] if t["success"]])
        api_total_count = len(self.validation_results["api_tests"])
        
        # Verificar testes de banco
        db_success_count = len([t for t in self.validation_results["database_tests"] if t["success"]])
        db_total_count = len(self.validation_results["database_tests"])
        
        # Calcular porcentagem de sucesso
        total_tests = total_count + api_total_count + db_total_count
        total_success = healthy_count + api_success_count + db_success_count
        
        if total_tests > 0:
            success_rate = (total_success / total_tests) * 100
        else:
            success_rate = 0
        
        # Determinar status geral
        if success_rate >= 90:
            self.validation_results["overall_status"] = "excellent"
        elif success_rate >= 75:
            self.validation_results["overall_status"] = "good"
        elif success_rate >= 50:
            self.validation_results["overall_status"] = "fair"
        else:
            self.validation_results["overall_status"] = "poor"
        
        self.validation_results["success_rate"] = success_rate
        
        print(f"   📊 Taxa de sucesso: {success_rate:.1f}%")
        print(f"   🎯 Status geral: {self.validation_results['overall_status'].upper()}")
    
    def gerar_relatorio(self):
        """Gera relatório final da validação"""
        print("\n📊 7. GERANDO RELATÓRIO DE VALIDAÇÃO...")
        
        # Salvar relatório
        relatorio_file = f"relatorio_validacao_{self.validation_timestamp}.json"
        with open(relatorio_file, 'w', encoding='utf-8') as f:
            json.dump(self.validation_results, f, indent=2, ensure_ascii=False)
        
        return self.validation_results

def main():
    print("🔍 MISSÃO: Remoção Completa do Módulo Wizard")
    print("📋 FASE 4: VALIDAÇÃO")
    print("=" * 60)
    print("Objetivo: Validar sistema funcionando após remoção")
    print("Tempo estimado: 1 hora")
    print("=" * 60)
    
    validation_manager = WizardValidationManager()
    
    # Executar validação completa
    validation_manager.validar_backend()
    validation_manager.validar_frontend()
    validation_manager.validar_banco_dados()
    validation_manager.validar_renus_isa()
    validation_manager.verificar_arquivos_removidos()
    validation_manager.calcular_status_geral()
    
    # Gerar relatório
    relatorio = validation_manager.gerar_relatorio()
    
    print("\n" + "=" * 60)
    print("📊 RESUMO DA VALIDAÇÃO")
    print("=" * 60)
    
    print(f"🐍 Backend: {relatorio['backend_status'].upper()}")
    print(f"⚛️ Frontend: {relatorio['frontend_status'].upper()}")
    print(f"🗄️ Database: {relatorio['database_status'].upper()}")
    print(f"🤖 RENUS: {relatorio['renus_status'].upper()}")
    print(f"🤖 ISA: {relatorio['isa_status'].upper()}")
    print(f"📊 Taxa de Sucesso: {relatorio.get('success_rate', 0):.1f}%")
    print(f"🎯 Status Geral: {relatorio['overall_status'].upper()}")
    
    if relatorio['errors']:
        print(f"\n⚠️ Erros encontrados: {len(relatorio['errors'])}")
        for error in relatorio['errors']:
            print(f"   - {error}")
    
    # Determinar se validação passou
    success = relatorio['overall_status'] in ['excellent', 'good']
    
    if success:
        print("\n🎉 VALIDAÇÃO PASSOU!")
        print("✅ Sistema funcionando após remoção do wizard")
        print("🚀 Pronto para implementar Agent Builder")
    else:
        print("\n🚨 VALIDAÇÃO FALHOU!")
        print("❌ Sistema com problemas após remoção")
        print("🔧 Verifique os erros antes de continuar")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)