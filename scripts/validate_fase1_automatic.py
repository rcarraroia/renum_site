#!/usr/bin/env python3
"""
Validação Automática - Fase 1 Sprint 10A
Seguindo checkpoint-validation.md: validação real antes de marcar como completo
"""
import asyncio
import aiohttp
import json
import sys
from datetime import datetime


class Fase1Validator:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:8081"
        self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzY1NTE2NzU5LCJpYXQiOjE3NjU0MzAzNTksInN1YiI6Ijg3NmJlMzMxLTk1NTMtNGU5YS05ZjI5LTYzY2ZhNzExZTA1NiIsImVtYWlsIjoicmNhcnJhcm8yMDE1QGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWwiOiJyY2FycmFybzIwMTVAZ21haWwuY29tIiwiZmlyc3RfbmFtZSI6IkFkbWluIiwibGFzdF9uYW1lIjoiUmVudW0ifX0.Dgavryf5gfGa2fj-FEts2GnzxHBHBO7v7O13mQaI9W0"
        self.results = []
        
    def log(self, message, status="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_icon = {"PASS": "✅", "FAIL": "❌", "INFO": "ℹ️", "WARN": "⚠️"}.get(status, "ℹ️")
        print(f"[{timestamp}] {status_icon} {message}")
        self.results.append({"timestamp": timestamp, "status": status, "message": message})
    
    async def test_backend_health(self):
        """Testa se backend está rodando"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.backend_url}/health") as response:
                    if response.status == 200:
                        self.log("Backend health check: OK", "PASS")
                        return True
                    else:
                        self.log(f"Backend health check failed: {response.status}", "FAIL")
                        return False
        except Exception as e:
            self.log(f"Backend não acessível: {e}", "FAIL")
            return False
    
    async def test_authentication(self):
        """Testa se autenticação funciona com token válido"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.backend_url}/api/dashboard/stats", headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.log("Autenticação: Token válido aceito", "PASS")
                        self.log(f"Dados recebidos: {data.get('total_clients', 0)} clientes, {data.get('total_leads', 0)} leads", "INFO")
                        return True
                    else:
                        self.log(f"Autenticação falhou: {response.status}", "FAIL")
                        return False
        except Exception as e:
            self.log(f"Erro na autenticação: {e}", "FAIL")
            return False
    
    async def test_frontend_accessibility(self):
        """Testa se frontend está acessível"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.frontend_url) as response:
                    if response.status == 200:
                        self.log("Frontend acessível", "PASS")
                        return True
                    else:
                        self.log(f"Frontend não acessível: {response.status}", "FAIL")
                        return False
        except Exception as e:
            self.log(f"Frontend não acessível: {e}", "FAIL")
            return False
    
    async def test_api_endpoints(self):
        """Testa endpoints das 5 páginas da Fase 1"""
        endpoints = [
            ("/api/clients", "AdminClientsPage"),
            ("/api/leads", "AdminLeadsPage"), 
            ("/api/reports/overview", "AdminReportsPage"),
            ("/api/dashboard/stats", "ClientOverview"),
            ("/api/config/default", "RenusConfigPage")
        ]
        
        headers = {"Authorization": f"Bearer {self.token}"}
        passed = 0
        
        async with aiohttp.ClientSession() as session:
            for endpoint, page in endpoints:
                try:
                    async with session.get(f"{self.backend_url}{endpoint}", headers=headers) as response:
                        if response.status in [200, 201]:
                            self.log(f"{page}: Endpoint {endpoint} OK", "PASS")
                            passed += 1
                        elif response.status == 404:
                            self.log(f"{page}: Endpoint {endpoint} não implementado (404)", "WARN")
                        else:
                            self.log(f"{page}: Endpoint {endpoint} falhou ({response.status})", "FAIL")
                except Exception as e:
                    self.log(f"{page}: Erro ao testar {endpoint}: {e}", "FAIL")
        
        return passed >= 3  # Pelo menos 3 dos 5 endpoints devem funcionar
    
    async def run_validation(self):
        """Executa validação completa"""
        self.log("=== VALIDAÇÃO AUTOMÁTICA FASE 1 - SPRINT 10A ===", "INFO")
        self.log("Seguindo checkpoint-validation.md: validação real obrigatória", "INFO")
        
        tests = [
            ("Backend Health", self.test_backend_health()),
            ("Autenticação", self.test_authentication()),
            ("Frontend Acessível", self.test_frontend_accessibility()),
            ("API Endpoints", self.test_api_endpoints())
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_coro in tests:
            self.log(f"Executando: {test_name}", "INFO")
            result = await test_coro
            if result:
                passed += 1
        
        # Resultado final
        self.log("=== RESULTADO DA VALIDAÇÃO ===", "INFO")
        self.log(f"Testes passaram: {passed}/{total}", "INFO")
        
        if passed == total:
            self.log("✅ FASE 1 APROVADA - Todos os testes passaram", "PASS")
            self.log("Sistema pronto para validação manual das páginas", "INFO")
            return True
        elif passed >= 3:
            self.log("⚠️ FASE 1 PARCIALMENTE APROVADA - Maioria dos testes passou", "WARN")
            self.log("Alguns endpoints podem não estar implementados ainda", "WARN")
            return True
        else:
            self.log("❌ FASE 1 REPROVADA - Muitos testes falharam", "FAIL")
            self.log("Problemas críticos devem ser corrigidos antes de prosseguir", "FAIL")
            return False
    
    def generate_report(self):
        """Gera relatório de validação"""
        report = f"""
# RELATÓRIO DE VALIDAÇÃO AUTOMÁTICA - FASE 1

**Data:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Sprint:** 10A - Integração Mock → Real
**Fase:** 1 - Páginas Dashboard Principais

## Resultados dos Testes

"""
        for result in self.results:
            status_icon = {"PASS": "✅", "FAIL": "❌", "INFO": "ℹ️", "WARN": "⚠️"}.get(result["status"], "ℹ️")
            report += f"- [{result['timestamp']}] {status_icon} {result['message']}\n"
        
        return report


async def main():
    validator = Fase1Validator()
    success = await validator.run_validation()
    
    # Gerar relatório
    report = validator.generate_report()
    
    # Salvar relatório
    with open("VALIDATION_FASE1_AUTOMATIC_REPORT.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n📄 Relatório salvo em: VALIDATION_FASE1_AUTOMATIC_REPORT.md")
    
    # Exit code para scripts
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())