#!/usr/bin/env python3
"""
Script para iniciar o frontend
"""

import subprocess
import time
import requests
import sys

def check_frontend():
    """Verifica se frontend está rodando"""
    try:
        response = requests.get("http://localhost:8081", timeout=2)
        return response.status_code == 200
    except:
        return False

def main():
    print("🚀 INICIANDO FRONTEND")
    print("=" * 50)
    
    # Verificar se já está rodando
    if check_frontend():
        print("✅ Frontend já está rodando na porta 8081")
        return
    
    print("🔧 Frontend não está rodando, iniciando...")
    print("\n📋 INSTRUÇÕES:")
    print("1. Abra um novo terminal")
    print("2. Execute: npm run dev")
    print("3. Aguarde o frontend iniciar")
    print("4. Acesse: http://localhost:8081")
    print("\nOu execute manualmente:")
    print("  cd E:\\PROJETOS SITE\\Projeto Renum\\Projeto Site Renum\\renum_site")
    print("  npm run dev")

if __name__ == "__main__":
    main()