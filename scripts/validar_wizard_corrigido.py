#!/usr/bin/env python3
"""
Script para validar se as correções do wizard funcionaram
Testa funcionalidade real após correções aplicadas
"""

import requests
import json
import time
import psycopg2
from psycopg2.extras import RealDictCursor

class WizardValidator:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.results = {
            "database_check": {"status": "pending", "details": []},
            "wizard_api_test": {"status": "pending", "details": []},
            "frontend_test": {"status": "pending", "details": []},
            "overall_status": "pending"
        }
        
        # Credenciais Supabase
        self.db_config = {
            'host': 'db.vhixvzaxswphwoymdhgg.supabase.co',
            'port': 5432,
            'database': 'postgres',
            'user': 'postgres',
            'password': 'BD5yEMQ9iDMOkeGW'
        }

    def test_database_corrections(self):
        """Testa se as correções no banco foram aplicadas corretamente"""
        print("🔍 TESTANDO CORREÇÕES NO BANCO DE DADOS...")
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # 1. Verificar se colunas foram adicionadas
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'agents' 
                AND column_name IN ('template_type', 'type', 'agent_role')
                ORDER BY column_name
            """)
            
            added_columns = [row['column_name'] for row in cursor.fetchall()]
            expected_columns = ['agent_role', 'template_type', 'type']
            
            if set(added_columns) == set(expected_columns):
                self.results["database_check"]["details"].append("✅ Todas as colunas necessárias foram adicionadas")
                self.results["database_check"]["status"] = "passed"
            else:
                missing = set(expected_columns) - set(added_columns)
                self.results["database_check"]["details"].append(f"❌ Colunas faltando: {missing}")
                self.results["database_check"]["status"] = "failed"
            
            # 2. Verificar se dados foram atualizados
            cursor.execute("""
                SELECT id, name, type, template_type, agent_role 
                FROM agents 
                WHERE type IS NOT NULL AND template_type IS NOT NULL
            """)
            
            updated_agents = cursor.fetchall()
            if updated_agents:
                self.results["database_check"]["details"].append(f"✅ {len(updated_agents)} agentes com dados atualizados")
                for agent in updated_agents:
                    self.results["database_check"]["details"].append(
                        f"   - {agent['name']}: type={agent['type']}, template_type={agent['template_type']}"
                    )
            else:
                self.results["database_check"]["details"].append("⚠️ Nenhum agente com dados atualizados encontrado")
            
            conn.close()
            
        except Exception as e:
            self.results["database_check"]["status"] = "failed"
            self.results["database_check"]["details"].append(f"❌ Erro: {e}")

    def test_wizard_api(self):
        """Testa se a API do wizard está funcionando"""
        print("🔍 TESTANDO API DO WIZARD...")
        
        try:
            # 1. Testar endpoint de início do wizard
            wizard_data = {
                "client_id": None,
                "category": "b2c"
            }
            
            response = requests.post(
                f"{self.backend_url}/api/agents/wizard/start",
                json=wizard_data,
                timeout=10
            )
            
            if response.status_code == 200:
                self.results["wizard_api_test"]["details"].append("✅ Wizard start endpoint funcionando")
                
                # Tentar parsear resposta
                try:
                    data = response.json()
                    if 'id' in data:
                        self.results["wizard_api_test"]["details"].append(f"✅ Wizard ID gerado: {data['id']}")
                        self.results["wizard_api_test"]["status"] = "passed"
                    else:
                        self.results["wizard_api_test"]["details"].append("⚠️ Resposta sem ID do wizard")
                        self.results["wizard_api_test"]["status"] = "partial"
                except json.JSONDecodeError:
                    self.results["wizard_api_test"]["details"].append("⚠️ Resposta não é JSON válido")
                    self.results["wizard_api_test"]["status"] = "partial"
                    
            elif response.status_code == 500:
                # Verificar se ainda é o erro de coluna faltante
                try:
                    error_data = response.json()
                    error_msg = str(error_data)
                    
                    if "template_type" in error_msg and "schema cache" in error_msg:
                        self.results["wizard_api_test"]["details"].append("❌ ERRO AINDA PERSISTE: Coluna template_type não encontrada")
                        self.results["wizard_api_test"]["status"] = "failed"
                    else:
                        self.results["wizard_api_test"]["details"].append(f"❌ Erro 500 diferente: {error_msg}")
                        self.results["wizard_api_test"]["status"] = "failed"
                except:
                    self.results["wizard_api_test"]["details"].append(f"❌ Erro 500: {response.text}")
                    self.results["wizard_api_test"]["status"] = "failed"
            else:
                self.results["wizard_api_test"]["details"].append(f"❌ Status inesperado: {response.status_code}")
                self.results["wizard_api_test"]["status"] = "failed"
                
        except requests.exceptions.ConnectionError:
            self.results["wizard_api_test"]["details"].append("❌ Backend não está rodando")
            self.results["wizard_api_test"]["status"] = "failed"
        except Exception as e:
            self.results["wizard_api_test"]["details"].append(f"❌ Erro: {e}")
            self.results["wizard_api_test"]["status"] = "failed"

    def test_frontend_accessibility(self):
        """Testa se o frontend está acessível"""
        print("🔍 TESTANDO ACESSIBILIDADE DO FRONTEND...")
        
        try:
            response = requests.get("http://localhost:5173", timeout=5)
            if response.status_code == 200:
                self.results["frontend_test"]["details"].append("✅ Frontend está rodando")
                self.results["frontend_test"]["status"] = "passed"
            else:
                self.results["frontend_test"]["details"].append(f"⚠️ Frontend retornou status {response.status_code}")
                self.results["frontend_test"]["status"] = "partial"
        except requests.exceptions.ConnectionError:
            self.results["frontend_test"]["details"].append("❌ Frontend não está rodando")
            self.results["frontend_test"]["status"] = "failed"
        except Exception as e:
            self.results["frontend_test"]["details"].append(f"❌ Erro: {e}")
            self.results["frontend_test"]["status"] = "failed"

    def run_validation(self):
        """Executa todas as validações"""
        print("🚀 INICIANDO VALIDAÇÃO DO WIZARD CORRIGIDO")
        print("=" * 60)
        
        # Executar testes
        self.test_database_corrections()
        self.test_wizard_api()
        self.test_frontend_accessibility()
        
        # Determinar status geral
        test_results = {k: v for k, v in self.results.items() if k != "overall_status"}
        statuses = [test["status"] for test in test_results.values() if test["status"] != "pending"]
        
        if all(status == "passed" for status in statuses):
            self.results["overall_status"] = "passed"
        elif any(status == "failed" for status in statuses):
            self.results["overall_status"] = "failed"
        else:
            self.results["overall_status"] = "partial"
        
        return self.results

    def print_results(self):
        """Imprime resultados formatados"""
        print("\n" + "=" * 60)
        print("📋 RESULTADOS DA VALIDAÇÃO")
        print("=" * 60)
        
        for test_name, test_data in self.results.items():
            if test_name == "overall_status":
                continue
                
            status_icon = {
                "passed": "✅",
                "failed": "❌",
                "partial": "⚠️",
                "pending": "⏳"
            }.get(test_data["status"], "❓")
            
            print(f"\n{status_icon} {test_name.upper().replace('_', ' ')}: {test_data['status'].upper()}")
            
            for detail in test_data["details"]:
                print(f"   {detail}")
        
        # Status geral
        overall_icon = {
            "passed": "🎉",
            "failed": "🚨",
            "partial": "⚠️"
        }.get(self.results["overall_status"], "❓")
        
        print(f"\n{overall_icon} STATUS GERAL: {self.results['overall_status'].upper()}")
        
        if self.results["overall_status"] == "passed":
            print("🎯 WIZARD CORRIGIDO COM SUCESSO! Todas as validações passaram.")
        elif self.results["overall_status"] == "failed":
            print("🔧 CORREÇÕES ADICIONAIS NECESSÁRIAS. Alguns testes falharam.")
        else:
            print("🔍 CORREÇÕES PARCIAIS APLICADAS. Alguns testes precisam de atenção.")

def main():
    validator = WizardValidator()
    results = validator.run_validation()
    validator.print_results()
    
    # Salvar relatório
    report_path = "docs/validacoes/VALIDACAO_WIZARD_CORRIGIDO.json"
    import os
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 Relatório salvo em: {report_path}")
    
    return results

if __name__ == "__main__":
    main()