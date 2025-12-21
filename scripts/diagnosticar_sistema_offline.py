#!/usr/bin/env python3
"""
Script para diagnosticar por que backend e frontend estão offline
Identifica problemas de configuração, dependências e inicialização
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path

class SystemDiagnostic:
    def __init__(self):
        self.results = {
            "backend": {"status": "unknown", "issues": [], "suggestions": []},
            "frontend": {"status": "unknown", "issues": [], "suggestions": []},
            "environment": {"status": "unknown", "issues": [], "suggestions": []}
        }

    def check_backend_requirements(self):
        """Verifica se backend tem todos os requisitos"""
        print("🔍 DIAGNOSTICANDO BACKEND...")
        
        # Verificar se diretório backend existe
        if not os.path.exists("backend"):
            self.results["backend"]["issues"].append("Diretório 'backend' não existe")
            self.results["backend"]["suggestions"].append("Criar estrutura do backend")
            return False
        
        # Verificar arquivos críticos do backend
        critical_files = [
            "backend/src/main.py",
            "backend/requirements.txt",
            "backend/src/__init__.py"
        ]
        
        missing_files = []
        for file_path in critical_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            self.results["backend"]["issues"].append(f"Arquivos críticos faltando: {missing_files}")
            self.results["backend"]["suggestions"].append("Criar arquivos de entrada do backend")
        
        # Verificar se main.py tem conteúdo válido
        main_py_path = "backend/src/main.py"
        if os.path.exists(main_py_path):
            try:
                with open(main_py_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if len(content.strip()) < 50:
                    self.results["backend"]["issues"].append("main.py parece estar vazio ou incompleto")
                    self.results["backend"]["suggestions"].append("Implementar FastAPI app em main.py")
                elif "FastAPI" not in content and "app" not in content:
                    self.results["backend"]["issues"].append("main.py não parece ter FastAPI configurado")
                    self.results["backend"]["suggestions"].append("Configurar FastAPI app em main.py")
                else:
                    print("✅ main.py parece ter conteúdo FastAPI")
                    
            except Exception as e:
                self.results["backend"]["issues"].append(f"Erro lendo main.py: {e}")
        
        # Verificar requirements.txt
        req_path = "backend/requirements.txt"
        if os.path.exists(req_path):
            try:
                with open(req_path, 'r', encoding='utf-8') as f:
                    requirements = f.read()
                
                if "fastapi" not in requirements.lower():
                    self.results["backend"]["issues"].append("FastAPI não está em requirements.txt")
                    self.results["backend"]["suggestions"].append("Adicionar FastAPI às dependências")
                else:
                    print("✅ FastAPI encontrado em requirements.txt")
                    
            except Exception as e:
                self.results["backend"]["issues"].append(f"Erro lendo requirements.txt: {e}")
        
        # Verificar se Python virtual env existe
        venv_paths = ["backend/venv", "backend/.venv", "venv", ".venv"]
        venv_found = False
        for venv_path in venv_paths:
            if os.path.exists(venv_path):
                venv_found = True
                print(f"✅ Virtual environment encontrado: {venv_path}")
                break
        
        if not venv_found:
            self.results["backend"]["issues"].append("Virtual environment não encontrado")
            self.results["backend"]["suggestions"].append("Criar virtual environment: python -m venv venv")
        
        return len(self.results["backend"]["issues"]) == 0

    def check_frontend_requirements(self):
        """Verifica se frontend tem todos os requisitos"""
        print("\n🔍 DIAGNOSTICANDO FRONTEND...")
        
        # Verificar package.json
        if not os.path.exists("package.json"):
            self.results["frontend"]["issues"].append("package.json não existe")
            self.results["frontend"]["suggestions"].append("Inicializar projeto Node.js: npm init")
            return False
        
        # Verificar conteúdo do package.json
        try:
            with open("package.json", 'r', encoding='utf-8') as f:
                package_data = json.load(f)
            
            # Verificar scripts
            scripts = package_data.get("scripts", {})
            if "dev" not in scripts and "start" not in scripts:
                self.results["frontend"]["issues"].append("Script 'dev' ou 'start' não encontrado em package.json")
                self.results["frontend"]["suggestions"].append("Adicionar script dev: 'vite' ou 'react-scripts start'")
            else:
                print("✅ Scripts de desenvolvimento encontrados")
            
            # Verificar dependências críticas
            deps = package_data.get("dependencies", {})
            dev_deps = package_data.get("devDependencies", {})
            all_deps = {**deps, **dev_deps}
            
            critical_deps = ["react", "vite"]
            missing_deps = []
            for dep in critical_deps:
                if not any(dep in key for key in all_deps.keys()):
                    missing_deps.append(dep)
            
            if missing_deps:
                self.results["frontend"]["issues"].append(f"Dependências críticas faltando: {missing_deps}")
                self.results["frontend"]["suggestions"].append(f"Instalar dependências: npm install {' '.join(missing_deps)}")
            else:
                print("✅ Dependências críticas encontradas")
                
        except Exception as e:
            self.results["frontend"]["issues"].append(f"Erro lendo package.json: {e}")
        
        # Verificar node_modules
        if not os.path.exists("node_modules"):
            self.results["frontend"]["issues"].append("node_modules não existe")
            self.results["frontend"]["suggestions"].append("Instalar dependências: npm install")
        else:
            print("✅ node_modules encontrado")
        
        # Verificar arquivos críticos do frontend
        critical_files = [
            "src/main.tsx",
            "src/App.tsx",
            "index.html"
        ]
        
        missing_files = []
        for file_path in critical_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            self.results["frontend"]["issues"].append(f"Arquivos críticos faltando: {missing_files}")
            self.results["frontend"]["suggestions"].append("Criar estrutura básica do React")
        else:
            print("✅ Arquivos críticos do React encontrados")
        
        return len(self.results["frontend"]["issues"]) == 0

    def check_environment(self):
        """Verifica ambiente geral"""
        print("\n🔍 DIAGNOSTICANDO AMBIENTE...")
        
        # Verificar Python
        try:
            result = subprocess.run(["python", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                python_version = result.stdout.strip()
                print(f"✅ Python encontrado: {python_version}")
            else:
                self.results["environment"]["issues"].append("Python não encontrado")
                self.results["environment"]["suggestions"].append("Instalar Python 3.11+")
        except Exception as e:
            self.results["environment"]["issues"].append(f"Erro verificando Python: {e}")
        
        # Verificar Node.js
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                node_version = result.stdout.strip()
                print(f"✅ Node.js encontrado: {node_version}")
            else:
                self.results["environment"]["issues"].append("Node.js não encontrado")
                self.results["environment"]["suggestions"].append("Instalar Node.js 18+")
        except Exception as e:
            self.results["environment"]["issues"].append(f"Erro verificando Node.js: {e}")
        
        # Verificar npm
        try:
            result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                npm_version = result.stdout.strip()
                print(f"✅ npm encontrado: {npm_version}")
            else:
                self.results["environment"]["issues"].append("npm não encontrado")
                self.results["environment"]["suggestions"].append("Instalar npm (vem com Node.js)")
        except Exception as e:
            self.results["environment"]["issues"].append(f"Erro verificando npm: {e}")
        
        # Verificar portas em uso
        try:
            # Verificar porta 8000 (backend)
            result = subprocess.run(["netstat", "-an"], capture_output=True, text=True)
            if ":8000" in result.stdout:
                print("⚠️ Porta 8000 pode estar em uso")
                self.results["environment"]["issues"].append("Porta 8000 pode estar ocupada")
                self.results["environment"]["suggestions"].append("Verificar processos na porta 8000: netstat -ano | findstr :8000")
            
            # Verificar porta 5173 (frontend)
            if ":5173" in result.stdout:
                print("⚠️ Porta 5173 pode estar em uso")
                self.results["environment"]["issues"].append("Porta 5173 pode estar ocupada")
                self.results["environment"]["suggestions"].append("Verificar processos na porta 5173: netstat -ano | findstr :5173")
                
        except Exception as e:
            print(f"Não foi possível verificar portas: {e}")
        
        return len(self.results["environment"]["issues"]) == 0

    def try_start_backend(self):
        """Tenta iniciar backend e captura erros"""
        print("\n🚀 TENTANDO INICIAR BACKEND...")
        
        if not os.path.exists("backend/src/main.py"):
            print("❌ main.py não existe, não é possível iniciar")
            return False
        
        try:
            # Tentar iniciar backend
            os.chdir("backend")
            result = subprocess.run(
                ["python", "-m", "src.main"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode != 0:
                error_output = result.stderr or result.stdout
                print(f"❌ Backend falhou ao iniciar:")
                print(f"Erro: {error_output}")
                
                # Analisar erros comuns
                if "ModuleNotFoundError" in error_output:
                    self.results["backend"]["issues"].append("Dependências não instaladas")
                    self.results["backend"]["suggestions"].append("Instalar dependências: pip install -r requirements.txt")
                
                if "ImportError" in error_output:
                    self.results["backend"]["issues"].append("Erro de importação de módulos")
                    self.results["backend"]["suggestions"].append("Verificar estrutura de imports")
                
                if "SyntaxError" in error_output:
                    self.results["backend"]["issues"].append("Erro de sintaxe no código")
                    self.results["backend"]["suggestions"].append("Corrigir erros de sintaxe")
                
                if "Address already in use" in error_output:
                    self.results["backend"]["issues"].append("Porta 8000 já está em uso")
                    self.results["backend"]["suggestions"].append("Matar processo na porta 8000 ou usar porta diferente")
                
                return False
            else:
                print("✅ Backend iniciou com sucesso (processo terminado)")
                return True
                
        except subprocess.TimeoutExpired:
            print("⚠️ Backend iniciou mas não terminou em 10s (pode estar rodando)")
            return True
        except Exception as e:
            print(f"❌ Erro tentando iniciar backend: {e}")
            self.results["backend"]["issues"].append(f"Erro de execução: {e}")
            return False
        finally:
            os.chdir("..")

    def try_start_frontend(self):
        """Tenta iniciar frontend e captura erros"""
        print("\n🚀 TENTANDO INICIAR FRONTEND...")
        
        if not os.path.exists("package.json"):
            print("❌ package.json não existe, não é possível iniciar")
            return False
        
        try:
            # Tentar npm run dev
            result = subprocess.run(
                ["npm", "run", "dev"], 
                capture_output=True, 
                text=True, 
                timeout=15
            )
            
            if result.returncode != 0:
                error_output = result.stderr or result.stdout
                print(f"❌ Frontend falhou ao iniciar:")
                print(f"Erro: {error_output}")
                
                # Analisar erros comuns
                if "command not found" in error_output or "not recognized" in error_output:
                    self.results["frontend"]["issues"].append("npm não encontrado")
                    self.results["frontend"]["suggestions"].append("Instalar Node.js e npm")
                
                if "Missing script" in error_output:
                    self.results["frontend"]["issues"].append("Script 'dev' não existe")
                    self.results["frontend"]["suggestions"].append("Adicionar script dev ao package.json")
                
                if "Cannot resolve dependency" in error_output:
                    self.results["frontend"]["issues"].append("Dependências não instaladas")
                    self.results["frontend"]["suggestions"].append("Executar: npm install")
                
                if "EADDRINUSE" in error_output:
                    self.results["frontend"]["issues"].append("Porta já está em uso")
                    self.results["frontend"]["suggestions"].append("Matar processo na porta ou usar porta diferente")
                
                return False
            else:
                print("✅ Frontend iniciou com sucesso")
                return True
                
        except subprocess.TimeoutExpired:
            print("⚠️ Frontend iniciou mas não terminou em 15s (pode estar rodando)")
            return True
        except Exception as e:
            print(f"❌ Erro tentando iniciar frontend: {e}")
            self.results["frontend"]["issues"].append(f"Erro de execução: {e}")
            return False

    def generate_fix_script(self):
        """Gera script com comandos para corrigir problemas"""
        fix_commands = []
        
        # Comandos para backend
        if self.results["backend"]["issues"]:
            fix_commands.append("# === CORREÇÕES BACKEND ===")
            for suggestion in self.results["backend"]["suggestions"]:
                if "virtual environment" in suggestion:
                    fix_commands.append("python -m venv backend/venv")
                    fix_commands.append("backend/venv/Scripts/activate")  # Windows
                elif "requirements.txt" in suggestion:
                    fix_commands.append("cd backend && pip install -r requirements.txt")
                elif "FastAPI" in suggestion:
                    fix_commands.append("cd backend && pip install fastapi uvicorn")
        
        # Comandos para frontend
        if self.results["frontend"]["issues"]:
            fix_commands.append("\n# === CORREÇÕES FRONTEND ===")
            for suggestion in self.results["frontend"]["suggestions"]:
                if "npm install" in suggestion and "dependencies" not in suggestion:
                    fix_commands.append("npm install")
                elif "react" in suggestion or "vite" in suggestion:
                    fix_commands.append("npm install react react-dom vite @vitejs/plugin-react")
        
        # Comandos para ambiente
        if self.results["environment"]["issues"]:
            fix_commands.append("\n# === CORREÇÕES AMBIENTE ===")
            for suggestion in self.results["environment"]["suggestions"]:
                if "Python" in suggestion:
                    fix_commands.append("# Instalar Python 3.11+ de https://python.org")
                elif "Node.js" in suggestion:
                    fix_commands.append("# Instalar Node.js 18+ de https://nodejs.org")
        
        return fix_commands

    def run_full_diagnostic(self):
        """Executa diagnóstico completo"""
        print("🔍 DIAGNÓSTICO COMPLETO DO SISTEMA OFFLINE")
        print("=" * 60)
        
        # Verificar requisitos
        env_ok = self.check_environment()
        backend_ok = self.check_backend_requirements()
        frontend_ok = self.check_frontend_requirements()
        
        # Tentar iniciar serviços
        if backend_ok:
            backend_starts = self.try_start_backend()
        else:
            backend_starts = False
            
        if frontend_ok:
            frontend_starts = self.try_start_frontend()
        else:
            frontend_starts = False
        
        # Atualizar status final
        self.results["environment"]["status"] = "ok" if env_ok else "issues"
        self.results["backend"]["status"] = "ok" if backend_ok and backend_starts else "issues"
        self.results["frontend"]["status"] = "ok" if frontend_ok and frontend_starts else "issues"
        
        return self.results

def main():
    """Função principal"""
    diagnostic = SystemDiagnostic()
    results = diagnostic.run_full_diagnostic()
    
    # Gerar relatório
    print("\n" + "=" * 60)
    print("📋 RELATÓRIO DE DIAGNÓSTICO")
    print("=" * 60)
    
    for component, data in results.items():
        status_icon = "✅" if data["status"] == "ok" else "❌"
        print(f"\n{status_icon} {component.upper()}: {data['status'].upper()}")
        
        if data["issues"]:
            print("  Problemas encontrados:")
            for issue in data["issues"]:
                print(f"    - {issue}")
        
        if data["suggestions"]:
            print("  Sugestões de correção:")
            for suggestion in data["suggestions"]:
                print(f"    → {suggestion}")
    
    # Gerar script de correção
    fix_commands = diagnostic.generate_fix_script()
    if fix_commands:
        print("\n" + "=" * 60)
        print("🔧 SCRIPT DE CORREÇÃO AUTOMÁTICA")
        print("=" * 60)
        
        script_content = "\n".join(fix_commands)
        
        # Salvar script
        with open("fix_system.bat", "w") as f:
            f.write("@echo off\n")
            f.write("echo Corrigindo problemas do sistema...\n")
            f.write(script_content.replace("#", "REM"))
        
        print("Script salvo em: fix_system.bat")
        print("\nComandos para executar:")
        for cmd in fix_commands:
            if not cmd.startswith("#"):
                print(f"  {cmd}")
    
    # Salvar relatório JSON
    report_path = "docs/validacoes/DIAGNOSTICO_SISTEMA_OFFLINE.json"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 Relatório completo salvo em: {report_path}")
    
    # Resumo final
    total_issues = sum(len(data["issues"]) for data in results.values())
    if total_issues == 0:
        print("\n🎉 SISTEMA PRONTO! Nenhum problema encontrado.")
    else:
        print(f"\n⚠️ {total_issues} PROBLEMAS ENCONTRADOS. Executar correções necessárias.")
    
    return results

if __name__ == "__main__":
    main()