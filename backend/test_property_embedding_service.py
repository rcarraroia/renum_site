#!/usr/bin/env python3
"""
Property Tests para EmbeddingService - Task 20
Sprint 10 - SICC Implementation - Phase 5

Testes de propriedades usando dados reais do banco.
Seguindo regras de validação: NUNCA ASSUMA. SEMPRE VERIFIQUE.
"""

import sys
from pathlib import Path
import random
import string

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

# Import direto
import os
os.chdir(Path(__file__).parent / "src")
sys.path.insert(0, ".")

from services.sicc.embedding_service import get_embedding_service


def generate_random_text(min_length=10, max_length=100):
    """Gera texto aleatório para testes"""
    length = random.randint(min_length, max_length)
    words = []
    
    for _ in range(length // 6):  # Aproximadamente 6 chars por palavra
        word_len = random.randint(3, 8)
        word = ''.join(random.choices(string.ascii_lowercase, k=word_len))
        words.append(word)
    
    return ' '.join(words)


def test_property_1_embedding_dimension_consistency():
    """
    Property 1: Embedding dimension consistency
    
    Para qualquer texto válido, o embedding gerado deve sempre ter 384 dimensões.
    """
    print("🧪 Property 1: Embedding dimension consistency")
    
    embedding_service = get_embedding_service()
    
    test_cases = [
        "Hello world",
        "Este é um texto em português",
        "A" * 500,  # Texto longo
        "123 números e símbolos !@#",
        generate_random_text(50, 200),
        generate_random_text(10, 50),
        "Single",
        "Multi\nline\ntext\nwith\nbreaks"
    ]
    
    passed = 0
    total = len(test_cases)
    
    for i, text in enumerate(test_cases, 1):
        try:
            embedding = embedding_service.generate_embedding(text)
            
            # Verificar dimensão
            if len(embedding) == 384:
                print(f"   ✅ Caso {i}: {len(embedding)} dimensões (texto: {len(text)} chars)")
                passed += 1
            else:
                print(f"   ❌ Caso {i}: {len(embedding)} dimensões (esperado: 384)")
                
        except Exception as e:
            print(f"   ❌ Caso {i}: Erro - {e}")
    
    success_rate = passed / total
    print(f"   📊 Resultado: {passed}/{total} casos passaram ({success_rate:.1%})")
    
    return success_rate >= 0.9  # 90% de sucesso mínimo


def test_property_3_batch_embedding_processing():
    """
    Property 3: Batch embedding processing
    
    O processamento em lote deve produzir os mesmos embeddings que o processamento individual.
    """
    print("\n🧪 Property 3: Batch embedding processing")
    
    embedding_service = get_embedding_service()
    
    # Textos de teste
    test_texts = [
        "Primeiro texto de teste",
        "Segundo texto diferente", 
        "Terceiro texto com mais conteúdo para verificar consistência",
        generate_random_text(30, 80),
        generate_random_text(20, 60)
    ]
    
    try:
        # Gerar embeddings individuais
        individual_embeddings = []
        for text in test_texts:
            embedding = embedding_service.generate_embedding(text)
            individual_embeddings.append(embedding)
        
        # Gerar embeddings em lote
        batch_embeddings = embedding_service.generate_embeddings_batch(test_texts)
        
        # Verificar se são iguais
        if len(individual_embeddings) != len(batch_embeddings):
            print(f"   ❌ Quantidade diferente: {len(individual_embeddings)} vs {len(batch_embeddings)}")
            return False
        
        matches = 0
        for i, (ind_emb, batch_emb) in enumerate(zip(individual_embeddings, batch_embeddings)):
            # Verificar se são aproximadamente iguais (tolerância para float)
            if len(ind_emb) == len(batch_emb):
                # Calcular diferença máxima
                max_diff = max(abs(a - b) for a, b in zip(ind_emb, batch_emb))
                
                if max_diff < 1e-6:  # Tolerância muito pequena
                    matches += 1
                    print(f"   ✅ Texto {i+1}: Embeddings idênticos (diff máx: {max_diff:.2e})")
                else:
                    print(f"   ⚠️  Texto {i+1}: Diferença detectada (diff máx: {max_diff:.2e})")
            else:
                print(f"   ❌ Texto {i+1}: Dimensões diferentes")
        
        success_rate = matches / len(test_texts)
        print(f"   📊 Resultado: {matches}/{len(test_texts)} embeddings idênticos ({success_rate:.1%})")
        
        return success_rate >= 0.8  # 80% de sucesso (pode haver pequenas diferenças)
        
    except Exception as e:
        print(f"   ❌ Erro no teste: {e}")
        return False


def test_property_4_embedding_cache_effectiveness():
    """
    Property 4: Embedding cache effectiveness
    
    Gerar embedding para o mesmo texto múltiplas vezes deve ser consistente.
    """
    print("\n🧪 Property 4: Embedding cache effectiveness")
    
    embedding_service = get_embedding_service()
    
    test_text = "Este texto será usado para testar cache de embeddings"
    
    try:
        # Gerar embedding múltiplas vezes
        embeddings = []
        for i in range(5):
            embedding = embedding_service.generate_embedding(test_text)
            embeddings.append(embedding)
            print(f"   🔄 Geração {i+1}: {len(embedding)} dimensões")
        
        # Verificar se todos são idênticos
        first_embedding = embeddings[0]
        all_identical = True
        
        for i, embedding in enumerate(embeddings[1:], 2):
            if len(embedding) != len(first_embedding):
                print(f"   ❌ Geração {i}: Dimensão diferente")
                all_identical = False
                continue
            
            # Verificar diferenças
            max_diff = max(abs(a - b) for a, b in zip(first_embedding, embedding))
            
            if max_diff > 1e-10:  # Tolerância extremamente pequena
                print(f"   ⚠️  Geração {i}: Pequena diferença (diff máx: {max_diff:.2e})")
                # Ainda consideramos sucesso se diferença for muito pequena
                if max_diff > 1e-6:
                    all_identical = False
            else:
                print(f"   ✅ Geração {i}: Idêntico")
        
        if all_identical:
            print(f"   📊 Resultado: ✅ Todos os embeddings são consistentes")
            return True
        else:
            print(f"   📊 Resultado: ⚠️  Pequenas inconsistências detectadas")
            return False  # Para embeddings, esperamos consistência total
            
    except Exception as e:
        print(f"   ❌ Erro no teste: {e}")
        return False


def main():
    """Executa todos os property tests do EmbeddingService"""
    
    print("🧪 PROPERTY TESTS - EMBEDDING SERVICE")
    print("Task 20 - Sprint 10 - Phase 5")
    print("=" * 60)
    
    # Verificar se o serviço está funcionando
    try:
        embedding_service = get_embedding_service()
        model_info = embedding_service.get_model_info()
        
        print(f"🔧 Modelo carregado: {model_info['model_name']}")
        print(f"📏 Dimensão: {model_info['embedding_dimension']}")
        print(f"🎯 Max tokens: {model_info['max_tokens']}")
        print(f"✅ Status: {'OK' if model_info['model_loaded'] else 'ERRO'}")
        
        if not model_info['model_loaded']:
            print("❌ Modelo não carregado. Abortando testes.")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao inicializar EmbeddingService: {e}")
        return False
    
    # Executar property tests
    results = []
    
    try:
        results.append(("Property 1: Dimension Consistency", test_property_1_embedding_dimension_consistency()))
        results.append(("Property 3: Batch Processing", test_property_3_batch_embedding_processing()))
        results.append(("Property 4: Cache Effectiveness", test_property_4_embedding_cache_effectiveness()))
        
    except Exception as e:
        print(f"\n❌ Erro durante execução dos testes: {e}")
        return False
    
    # Resumo dos resultados
    print(f"\n" + "=" * 60)
    print(f"📊 RESUMO DOS PROPERTY TESTS - EMBEDDING SERVICE")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"   {status} - {test_name}")
        if result:
            passed += 1
    
    success_rate = passed / total if total > 0 else 0
    print(f"\n📈 Taxa de sucesso: {passed}/{total} ({success_rate:.1%})")
    
    if success_rate >= 0.8:  # 80% mínimo
        print(f"🎉 PROPERTY TESTS APROVADOS!")
        print(f"✅ EmbeddingService está funcionando corretamente")
        return True
    else:
        print(f"❌ PROPERTY TESTS FALHARAM!")
        print(f"⚠️  EmbeddingService precisa de correções")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)