#!/usr/bin/env python3
"""
Teste de conexão Redis via SSH tunnel
"""
import subprocess
import time
import redis
import sys
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv("backend/.env")

def test_redis_via_ssh():
    """Testa Redis conectando via SSH na VPS"""
    
    print("🔍 Testando Redis via SSH na VPS...")
    
    # Comando SSH para testar Redis internamente
    ssh_command = [
        "ssh", 
        "root@72.60.151.78",
        "redis-cli -h localhost -p 6379 -a 'M$151173c@' ping"
    ]
    
    try:
        print("📡 Conectando via SSH...")
        result = subprocess.run(
            ssh_command, 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ Redis respondeu via SSH!")
            print(f"📋 Resposta: {result.stdout.strip()}")
            return True
        else:
            print("❌ Redis não respondeu via SSH")
            print(f"📋 Erro: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout na conexão SSH")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_redis_tunnel():
    """Testa criando tunnel SSH para Redis"""
    
    print("\n🔍 Testando com SSH Tunnel...")
    
    # Criar tunnel SSH (porta local 6380 -> VPS:6379)
    tunnel_command = [
        "ssh", 
        "-L", "6380:localhost:6379",
        "-N", "-f",
        "root@72.60.151.78"
    ]
    
    try:
        print("🚇 Criando SSH tunnel...")
        subprocess.run(tunnel_command, timeout=5)
        
        # Aguardar tunnel estabelecer
        time.sleep(2)
        
        # Testar Redis via tunnel
        r = redis.Redis(
            host='localhost', 
            port=6380, 
            password='M$151173c@',
            decode_responses=True
        )
        
        response = r.ping()
        if response:
            print("✅ Redis conectado via tunnel!")
            
            # Testar operação
            r.set("test_tunnel", "success")
            value = r.get("test_tunnel")
            
            if value == "success":
                print("✅ Operações Redis funcionando via tunnel!")
                r.delete("test_tunnel")
                return True
            
        return False
        
    except Exception as e:
        print(f"❌ Erro no tunnel: {e}")
        return False
    finally:
        # Limpar tunnel
        try:
            subprocess.run(["pkill", "-f", "ssh.*6380:localhost:6379"], timeout=2)
        except:
            pass

if __name__ == "__main__":
    print("🧪 Teste de Conectividade Redis VPS")
    print("=" * 50)
    
    # Teste 1: Via SSH direto
    ssh_success = test_redis_via_ssh()
    
    # Teste 2: Via SSH tunnel
    tunnel_success = test_redis_tunnel()
    
    print("\n📊 Resultados:")
    print(f"SSH Direto: {'✅' if ssh_success else '❌'}")
    print(f"SSH Tunnel: {'✅' if tunnel_success else '❌'}")
    
    if ssh_success or tunnel_success:
        print("\n💡 Solução: Redis funciona na VPS!")
        if tunnel_success:
            print("🔧 Usar SSH tunnel para desenvolvimento local")
        sys.exit(0)
    else:
        print("\n❌ Redis não acessível. Verificar configuração na VPS.")
        sys.exit(1)