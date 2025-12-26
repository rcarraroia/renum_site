#!/usr/bin/env python3
"""
Teste de conexão com Redis da VPS N8N
"""
import redis
import sys
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv("backend/.env")

def test_redis_connection():
    """Testa conexão com Redis"""
    redis_url = os.getenv("REDIS_URL")
    
    if not redis_url:
        print("❌ REDIS_URL não encontrada no .env")
        return False
    
    print(f"🔍 Testando conexão: {redis_url}")
    
    try:
        # Conectar ao Redis
        r = redis.from_url(redis_url)
        
        # Testar ping
        response = r.ping()
        if response:
            print("✅ Redis conectado com sucesso!")
            
            # Testar operações básicas
            r.set("test_key", "test_value")
            value = r.get("test_key")
            
            if value and value.decode() == "test_value":
                print("✅ Operações Redis funcionando!")
                r.delete("test_key")
                return True
            else:
                print("❌ Erro nas operações Redis")
                return False
        else:
            print("❌ Redis não respondeu ao ping")
            return False
            
    except redis.ConnectionError as e:
        print(f"❌ Erro de conexão: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    success = test_redis_connection()
    sys.exit(0 if success else 1)