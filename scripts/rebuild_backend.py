#!/usr/bin/env python3
"""
Script para reconstruir o container do backend
Automatiza o processo de rebuild após correções
"""

import subprocess
import time
import requests
import sys

def run_command(command, description):
    """Executa comando e mostra resultado"""
    print(f"🔧 {description}...")
    print(f"Executando: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} - SUCESSO")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print(f"❌ {description} - ERRO")
            print(f"Error: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"❌ {description} - EXCEÇÃO: {e}")
        return False
    
    return True

def wait_for_backend(max_attempts=30):
    """Aguarda backend ficar disponível"""
    print("⏳ Aguardando backend ficar disponível...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                print(f"✅ Backend disponível após {attempt + 1} tentativas")
                return True
        except:
            pass
        
        print(f"   Tentativa {attempt + 1}/{max_attempts}...")
        time.sleep(2)
    
    print("❌ Backend não ficou disponível no tempo esperado")
    return False

def test_wizard_endpoint():
    """Testa se o wizard está funcionando"""
    print("🧪 Testando endpoint do wizard...")
    
    try:
        response = requests.post(
            "http://localhost:8000/api/agents/wizard/start",
            json={"client_id": None, "category": "b2c"},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Wizard funcionando corretamente!")
            data = response.json()
            print(f"   Wizard ID gerado: {data.get('id', 'N/A')}")
            return True
        else:
            print(f"❌ Wizard retornou erro {response.status_code}")
            try:
                error = response.json()
                print(f"   Erro: {error}")
            except:
                print(f"   Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro testando wizard: {e}")
        return False

def main():
    print("🚀 RECONSTRUINDO CONTAINER DO BACKEND")
    print("=" * 50)
    
    # 1. Parar containers
    if not run_command("docker-compose down", "Parando containers"):
        print("⚠️ Erro parando containers, continuando...")
    
    print()
    
    # 2. Reconstruir backend
    if not run_command("docker-compose build backend", "Reconstruindo backend"):
        print("❌ FALHA CRÍTICA: Não foi possível reconstruir o backend")
        sys.exit(1)
    
    print()
    
    # 3. Iniciar backend
    if not run_command("docker-compose up -d backend", "Iniciando backend"):
        print("❌ FALHA CRÍTICA: Não foi possível iniciar o backend")
        sys.exit(1)
    
    print()
    
    # 4. Aguardar backend ficar disponível
    if not wait_for_backend():
        print("❌ Backend não ficou disponível")
        print("\n🔍 DIAGNÓSTICO:")
        print("Execute manualmente:")
        print("  docker-compose logs backend")
        sys.exit(1)
    
    print()
    
    # 5. Testar wizard
    wizard_ok = test_wizard_endpoint()
    
    print("\n" + "=" * 50)
    print("📋 RESULTADO FINAL")
    print("=" * 50)
    
    if wizard_ok:
        print("🎉 REBUILD CONCLUÍDO COM SUCESSO!")
        print("✅ Backend reconstruído e funcionando")
        print("✅ Wizard endpoint funcionando")
        print("✅ Todas as correções aplicadas")
        print("\n🎯 PRÓXIMOS PASSOS:")
        print("1. Teste o wizard no navegador")
        print("2. Acesse: http://localhost:8081/dashboard/admin/agents/create")
        print("3. Verifique se não há mais erros no console")
    else:
        print("⚠️ REBUILD CONCLUÍDO MAS WIZARD COM PROBLEMAS")
        print("✅ Backend reconstruído")
        print("❌ Wizard ainda com erros")
        print("\n🔍 DIAGNÓSTICO NECESSÁRIO:")
        print("1. Verificar logs: docker-compose logs backend")
        print("2. Verificar se todas as correções foram aplicadas")
        print("3. Testar manualmente no navegador")

if __name__ == "__main__":
    main()