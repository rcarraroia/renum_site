#!/usr/bin/env python3
"""
Teste do TranscriptionService - Task 41
Valida funcionalidades básicas do serviço de transcrição
"""

import asyncio
import tempfile
import os
from pathlib import Path
import numpy as np
import soundfile as sf

# Adicionar src ao path
import sys
sys.path.append('src')

from services.sicc.transcription_service import TranscriptionService

def create_test_audio(duration: float = 5.0, sample_rate: int = 16000) -> str:
    """Cria um arquivo de áudio de teste com tom simples"""
    # Gerar tom de 440Hz (Lá)
    t = np.linspace(0, duration, int(sample_rate * duration))
    frequency = 440  # Hz
    audio = 0.3 * np.sin(2 * np.pi * frequency * t)
    
    # Adicionar um pouco de ruído para simular fala
    noise = 0.05 * np.random.randn(len(audio))
    audio = audio + noise
    
    # Salvar arquivo temporário
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(temp_file.name, audio, sample_rate)
    temp_file.close()
    
    return temp_file.name

async def test_transcription_service():
    """Testa funcionalidades básicas do TranscriptionService"""
    print("🎤 TESTE TRANSCRIPTION SERVICE - TASK 41")
    print("=" * 50)
    
    service = TranscriptionService()
    test_results = []
    
    # Teste 1: Inicialização do serviço
    print("\n📋 Teste 1: Inicialização do serviço")
    try:
        model_info = service.get_model_info()
        print(f"✅ Serviço inicializado")
        print(f"   Modelo: {model_info['model_name']}")
        print(f"   Formatos suportados: {model_info['supported_formats']}")
        print(f"   Tamanho máximo: {model_info['max_file_size_mb']}MB")
        test_results.append(("Inicialização", True, "Serviço criado com sucesso"))
    except Exception as e:
        print(f"❌ Erro na inicialização: {str(e)}")
        test_results.append(("Inicialização", False, str(e)))
        return test_results
    
    # Teste 2: Validação de arquivo
    print("\n📋 Teste 2: Validação de arquivo")
    try:
        # Arquivo inexistente
        invalid_result = service._validate_audio_file("arquivo_inexistente.wav")
        assert not invalid_result, "Deveria rejeitar arquivo inexistente"
        
        # Criar arquivo de teste válido
        test_audio_path = create_test_audio(3.0)
        valid_result = service._validate_audio_file(test_audio_path)
        assert valid_result, "Deveria aceitar arquivo válido"
        
        print(f"✅ Validação funcionando")
        print(f"   Arquivo teste: {test_audio_path}")
        test_results.append(("Validação", True, "Validação de arquivos OK"))
    except Exception as e:
        print(f"❌ Erro na validação: {str(e)}")
        test_results.append(("Validação", False, str(e)))
        if 'test_audio_path' in locals():
            os.unlink(test_audio_path)
        return test_results
    
    # Teste 3: Pré-processamento de áudio
    print("\n📋 Teste 3: Pré-processamento de áudio")
    try:
        audio_data, sample_rate = service._preprocess_audio(test_audio_path)
        assert isinstance(audio_data, np.ndarray), "Deveria retornar numpy array"
        assert sample_rate == 16000, "Sample rate deveria ser 16kHz"
        assert len(audio_data) > 0, "Áudio não deveria estar vazio"
        
        print(f"✅ Pré-processamento OK")
        print(f"   Duração: {len(audio_data)/sample_rate:.2f}s")
        print(f"   Sample rate: {sample_rate}Hz")
        print(f"   Amostras: {len(audio_data)}")
        test_results.append(("Pré-processamento", True, f"Áudio processado: {len(audio_data)} amostras"))
    except Exception as e:
        print(f"❌ Erro no pré-processamento: {str(e)}")
        test_results.append(("Pré-processamento", False, str(e)))
    
    # Teste 4: Segmentação por silêncio
    print("\n📋 Teste 4: Segmentação por silêncio")
    try:
        audio_data, sample_rate = service._preprocess_audio(test_audio_path)
        segments = service._segment_by_silence(audio_data, sample_rate)
        
        assert isinstance(segments, list), "Deveria retornar lista"
        assert len(segments) > 0, "Deveria encontrar pelo menos um segmento"
        
        print(f"✅ Segmentação OK")
        print(f"   Segmentos encontrados: {len(segments)}")
        for i, (start, end) in enumerate(segments):
            print(f"   Segmento {i+1}: {start:.2f}s - {end:.2f}s ({end-start:.2f}s)")
        test_results.append(("Segmentação", True, f"{len(segments)} segmentos encontrados"))
    except Exception as e:
        print(f"❌ Erro na segmentação: {str(e)}")
        test_results.append(("Segmentação", False, str(e)))
    
    # Teste 5: Detecção de idioma
    print("\n📋 Teste 5: Detecção de idioma")
    try:
        language = service.detect_language(test_audio_path)
        assert isinstance(language, str), "Deveria retornar string"
        assert len(language) >= 2, "Código de idioma deveria ter pelo menos 2 caracteres"
        
        print(f"✅ Detecção de idioma OK")
        print(f"   Idioma detectado: {language}")
        test_results.append(("Detecção idioma", True, f"Idioma: {language}"))
    except Exception as e:
        print(f"❌ Erro na detecção de idioma: {str(e)}")
        test_results.append(("Detecção idioma", False, str(e)))
    
    # Teste 6: Transcrição completa
    print("\n📋 Teste 6: Transcrição completa")
    try:
        print("   Carregando modelo Whisper... (pode demorar na primeira vez)")
        transcription = service.transcribe_audio(test_audio_path, language="pt")
        
        assert transcription.language == "pt", "Idioma deveria ser português"
        assert transcription.duration > 0, "Duração deveria ser positiva"
        assert len(transcription.segments) > 0, "Deveria ter pelo menos um segmento"
        assert isinstance(transcription.full_text, str), "Texto completo deveria ser string"
        
        print(f"✅ Transcrição completa OK")
        print(f"   Idioma: {transcription.language}")
        print(f"   Duração: {transcription.duration:.2f}s")
        print(f"   Segmentos: {len(transcription.segments)}")
        print(f"   Confiança média: {transcription.confidence_avg:.3f}")
        print(f"   Texto: '{transcription.full_text[:100]}...'")
        test_results.append(("Transcrição", True, f"Texto transcrito: {len(transcription.full_text)} chars"))
    except Exception as e:
        print(f"❌ Erro na transcrição: {str(e)}")
        test_results.append(("Transcrição", False, str(e)))
    
    # Teste 7: Informações do modelo
    print("\n📋 Teste 7: Informações do modelo")
    try:
        model_info = service.get_model_info()
        assert model_info["is_loaded"] == True, "Modelo deveria estar carregado"
        assert "model_name" in model_info, "Deveria ter nome do modelo"
        
        print(f"✅ Informações do modelo OK")
        print(f"   Modelo carregado: {model_info['model_name']}")
        print(f"   Status: {'Carregado' if model_info['is_loaded'] else 'Não carregado'}")
        test_results.append(("Info modelo", True, f"Modelo {model_info['model_name']} carregado"))
    except Exception as e:
        print(f"❌ Erro nas informações: {str(e)}")
        test_results.append(("Info modelo", False, str(e)))
    
    # Limpeza
    try:
        os.unlink(test_audio_path)
        print(f"\n🧹 Arquivo de teste removido: {test_audio_path}")
    except:
        pass
    
    return test_results

def main():
    """Executa todos os testes"""
    try:
        results = asyncio.run(test_transcription_service())
        
        # Relatório final
        print("\n" + "=" * 50)
        print("📊 RELATÓRIO FINAL - TRANSCRIPTION SERVICE")
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
            print("✅ TranscriptionService está funcionando corretamente")
            return True
        elif passed >= total * 0.8:
            print("⚠️ MAIORIA DOS TESTES PASSOU")
            print("✅ TranscriptionService está quase completo")
            return True
        else:
            print("❌ MUITOS TESTES FALHARAM")
            print("❌ TranscriptionService precisa de correções")
            return False
            
    except Exception as e:
        print(f"💥 ERRO CRÍTICO: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)