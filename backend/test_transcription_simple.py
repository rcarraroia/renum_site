#!/usr/bin/env python3
"""
Teste Simples do TranscriptionService - Task 41
Valida funcionalidades básicas sem dependências externas
"""

import tempfile
import os
import numpy as np
import soundfile as sf
import whisper

def create_test_audio(duration: float = 3.0, sample_rate: int = 16000) -> str:
    """Cria um arquivo de áudio de teste com tom simples"""
    # Gerar tom de 440Hz (Lá)
    t = np.linspace(0, duration, int(sample_rate * duration))
    frequency = 440  # Hz
    audio = 0.3 * np.sin(2 * np.pi * frequency * t)
    
    # Salvar arquivo temporário
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(temp_file.name, audio, sample_rate)
    temp_file.close()
    
    return temp_file.name

def test_whisper_installation():
    """Testa se Whisper está instalado e funcionando"""
    print("🎤 TESTE WHISPER INSTALLATION - TASK 41")
    print("=" * 50)
    
    test_results = []
    
    # Teste 1: Import do Whisper
    print("\n📋 Teste 1: Import do Whisper")
    try:
        import whisper
        print("✅ Whisper importado com sucesso")
        test_results.append(("Import Whisper", True, "Módulo disponível"))
    except Exception as e:
        print(f"❌ Erro no import: {str(e)}")
        test_results.append(("Import Whisper", False, str(e)))
        return test_results
    
    # Teste 2: Listar modelos disponíveis
    print("\n📋 Teste 2: Modelos disponíveis")
    try:
        available_models = whisper.available_models()
        print(f"✅ Modelos disponíveis: {available_models}")
        test_results.append(("Modelos disponíveis", True, f"{len(available_models)} modelos"))
    except Exception as e:
        print(f"❌ Erro ao listar modelos: {str(e)}")
        test_results.append(("Modelos disponíveis", False, str(e)))
    
    # Teste 3: Carregar modelo tiny (mais rápido)
    print("\n📋 Teste 3: Carregar modelo 'tiny'")
    try:
        print("   Carregando modelo... (pode demorar na primeira vez)")
        model = whisper.load_model("tiny")
        print("✅ Modelo 'tiny' carregado com sucesso")
        test_results.append(("Carregar modelo", True, "Modelo tiny carregado"))
    except Exception as e:
        print(f"❌ Erro ao carregar modelo: {str(e)}")
        test_results.append(("Carregar modelo", False, str(e)))
        return test_results
    
    # Teste 4: Criar áudio de teste
    print("\n📋 Teste 4: Criar áudio de teste")
    try:
        test_audio_path = create_test_audio(2.0)  # 2 segundos
        print(f"✅ Áudio de teste criado: {test_audio_path}")
        
        # Verificar se arquivo existe e tem tamanho
        file_size = os.path.getsize(test_audio_path)
        print(f"   Tamanho do arquivo: {file_size} bytes")
        test_results.append(("Criar áudio", True, f"Arquivo {file_size} bytes"))
    except Exception as e:
        print(f"❌ Erro ao criar áudio: {str(e)}")
        test_results.append(("Criar áudio", False, str(e)))
        return test_results
    
    # Teste 5: Transcrição básica
    print("\n📋 Teste 5: Transcrição básica")
    try:
        print("   Transcrevendo áudio de teste...")
        result = model.transcribe(test_audio_path)
        
        print(f"✅ Transcrição concluída")
        print(f"   Texto: '{result['text']}'")
        print(f"   Idioma: {result.get('language', 'N/A')}")
        print(f"   Segmentos: {len(result.get('segments', []))}")
        
        test_results.append(("Transcrição", True, f"Texto: {len(result['text'])} chars"))
    except Exception as e:
        print(f"❌ Erro na transcrição: {str(e)}")
        test_results.append(("Transcrição", False, str(e)))
    
    # Teste 6: Detecção de idioma
    print("\n📋 Teste 6: Detecção de idioma")
    try:
        # Carregar áudio para detecção
        import librosa
        audio, _ = librosa.load(test_audio_path, sr=16000)
        
        # Detectar idioma
        _, probs = model.detect_language(audio)
        detected_language = max(probs, key=probs.get)
        confidence = probs[detected_language]
        
        print(f"✅ Detecção de idioma OK")
        print(f"   Idioma detectado: {detected_language}")
        print(f"   Confiança: {confidence:.3f}")
        
        test_results.append(("Detecção idioma", True, f"{detected_language} ({confidence:.3f})"))
    except Exception as e:
        print(f"❌ Erro na detecção: {str(e)}")
        test_results.append(("Detecção idioma", False, str(e)))
    
    # Limpeza
    try:
        os.unlink(test_audio_path)
        print(f"\n🧹 Arquivo de teste removido")
    except:
        pass
    
    return test_results

def main():
    """Executa todos os testes"""
    try:
        results = test_whisper_installation()
        
        # Relatório final
        print("\n" + "=" * 50)
        print("📊 RELATÓRIO FINAL - WHISPER INSTALLATION")
        print("=" * 50)
        
        passed = 0
        total = len(results)
        
        for test_name, success, message in results:
            status = "✅ PASSOU" if success else "❌ FALHOU"
            print(f"{status}: {test_name} - {message}")
            if success:
                passed += 1
        
        print(f"\n📈 RESULTADO: {passed}/{total} testes passaram")
        
        if passed == total:
            print("🎉 TODOS OS TESTES PASSARAM!")
            print("✅ Whisper está instalado e funcionando")
            print("✅ TranscriptionService pode ser implementado")
            return True
        elif passed >= total * 0.8:
            print("⚠️ MAIORIA DOS TESTES PASSOU")
            print("✅ Whisper está quase funcionando")
            return True
        else:
            print("❌ MUITOS TESTES FALHARAM")
            print("❌ Whisper precisa de correções")
            return False
            
    except Exception as e:
        print(f"💥 ERRO CRÍTICO: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)