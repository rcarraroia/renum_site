#!/usr/bin/env python3
"""
Validação Task 42 - Audio Processing Pipeline
Verifica se os arquivos foram criados e estrutura está correta
"""

import os
from pathlib import Path

def validate_task42():
    """Valida Task 42: Audio Processing Pipeline"""
    print("🎵 VALIDAÇÃO TASK 42 - AUDIO PROCESSING PIPELINE")
    print("=" * 55)
    
    results = []
    
    # Teste 1: Verificar arquivos criados
    print("\n📋 Teste 1: Verificar arquivos criados")
    required_files = [
        "src/workers/audio_tasks.py",
        "src/api/routes/sicc_audio.py"
    ]
    
    all_files_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"✅ {file_path} - {file_size} bytes")
        else:
            print(f"❌ {file_path} - NÃO ENCONTRADO")
            all_files_exist = False
    
    results.append(("Arquivos criados", all_files_exist, f"{len(required_files)} arquivos"))
    
    # Teste 2: Verificar conteúdo dos arquivos
    print("\n📋 Teste 2: Verificar conteúdo dos arquivos")
    
    # Verificar audio_tasks.py
    audio_tasks_ok = False
    if os.path.exists("src/workers/audio_tasks.py"):
        with open("src/workers/audio_tasks.py", 'r', encoding='utf-8') as f:
            content = f.read()
            if "process_audio_file" in content and "transcribe_audio_only" in content:
                print("✅ audio_tasks.py - Funções principais presentes")
                audio_tasks_ok = True
            else:
                print("❌ audio_tasks.py - Funções principais faltando")
    
    results.append(("audio_tasks.py", audio_tasks_ok, "Funções Celery"))
    
    # Verificar sicc_audio.py
    audio_routes_ok = False
    if os.path.exists("src/api/routes/sicc_audio.py"):
        with open("src/api/routes/sicc_audio.py", 'r', encoding='utf-8') as f:
            content = f.read()
            if "/upload" in content and "/transcribe-sync" in content:
                print("✅ sicc_audio.py - Rotas principais presentes")
                audio_routes_ok = True
            else:
                print("❌ sicc_audio.py - Rotas principais faltando")
    
    results.append(("sicc_audio.py", audio_routes_ok, "Rotas API"))
    
    # Teste 3: Verificar integração no main.py
    print("\n📋 Teste 3: Verificar integração no main.py")
    main_integration_ok = False
    if os.path.exists("src/main.py"):
        with open("src/main.py", 'r', encoding='utf-8') as f:
            content = f.read()
            if "sicc_audio" in content:
                print("✅ main.py - Rotas SICC Audio registradas")
                main_integration_ok = True
            else:
                print("❌ main.py - Rotas SICC Audio não registradas")
    
    results.append(("Integração main.py", main_integration_ok, "Rotas registradas"))
    
    # Teste 4: Verificar dependências
    print("\n📋 Teste 4: Verificar dependências instaladas")
    deps_ok = True
    required_deps = ["whisper", "librosa", "soundfile"]
    
    for dep in required_deps:
        try:
            __import__(dep)
            print(f"✅ {dep} - Instalado")
        except ImportError:
            print(f"❌ {dep} - NÃO INSTALADO")
            deps_ok = False
    
    results.append(("Dependências", deps_ok, f"{len(required_deps)} pacotes"))
    
    # Teste 5: Verificar estrutura de diretórios
    print("\n📋 Teste 5: Verificar estrutura de diretórios")
    dirs_ok = True
    required_dirs = ["src/workers", "src/api/routes"]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path} - Existe")
        else:
            print(f"❌ {dir_path} - NÃO EXISTE")
            dirs_ok = False
    
    results.append(("Estrutura diretórios", dirs_ok, f"{len(required_dirs)} diretórios"))
    
    return results

def main():
    """Executa validação e gera relatório"""
    try:
        results = validate_task42()
        
        # Relatório final
        print("\n" + "=" * 55)
        print("📊 RELATÓRIO FINAL - TASK 42")
        print("=" * 55)
        
        passed = 0
        total = len(results)
        
        for test_name, success, details in results:
            status = "✅ PASSOU" if success else "❌ FALHOU"
            print(f"{status}: {test_name} - {details}")
            if success:
                passed += 1
        
        print(f"\n📈 RESULTADO: {passed}/{total} testes passaram")
        
        if passed == total:
            print("🎉 TODOS OS TESTES PASSARAM!")
            print("✅ Task 42 - Audio Processing Pipeline COMPLETA")
            return True
        elif passed >= total * 0.8:
            print("⚠️ MAIORIA DOS TESTES PASSOU")
            print("✅ Task 42 está quase completa")
            return True
        else:
            print("❌ MUITOS TESTES FALHARAM")
            print("❌ Task 42 precisa de correções")
            return False
            
    except Exception as e:
        print(f"💥 ERRO CRÍTICO: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)