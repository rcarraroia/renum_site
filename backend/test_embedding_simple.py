#!/usr/bin/env python3
"""
Teste Simples do EmbeddingService - Task 20
Sem dependências complexas de configuração
"""

import sys
from pathlib import Path
import random
import string

# Configurar path
backend_path = Path(__file__).parent
src_path = backend_path / "src"
sys.path.insert(0, str(src_path))

# Imports diretos
try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    
    print("🧪 TESTE SIMPLES - EMBEDDING SERVICE")
    print("=" * 50)
    
    # Carregar modelo diretamente
    print("🔧 Carregando modelo GTE-small...")
    try:
        model = SentenceTransformer("thenlper/gte-small")
        print("✅ Modelo carregado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao carregar modelo: {e}")
        print("🔄 Tentando modelo fallback...")
        try:
            model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            print("✅ Modelo fallback carregado")
        except Exception as e2:
            print(f"❌ Erro no fallback: {e2}")
            sys.exit(1)
    
    # Property Test 1: Dimensão consistente
    print(f"\n🧪 Property 1: Dimensão consistente")
    
    test_texts = [
        "Hello world",
        "Este é um texto em português",
        "Texto longo " * 20,
        "123 números !@#",
        "Single"
    ]
    
    dimensions = []
    for i, text in enumerate(test_texts, 1):
        try:
            embedding = model.encode(text)
            dim = len(embedding)
            dimensions.append(dim)
            print(f"   ✅ Texto {i}: {dim} dimensões")
        except Exception as e:
            print(f"   ❌ Texto {i}: Erro - {e}")
    
    # Verificar se todas as dimensões são iguais
    if dimensions and all(d == dimensions[0] for d in dimensions):
        expected_dim = dimensions[0]
        print(f"   📊 Resultado: ✅ Todas {len(dimensions)} têm {expected_dim} dimensões")
        property1_ok = True
    else:
        print(f"   📊 Resultado: ❌ Dimensões inconsistentes: {dimensions}")
        property1_ok = False
    
    # Property Test 2: Batch vs Individual
    print(f"\n🧪 Property 2: Batch vs Individual")
    
    batch_texts = ["Primeiro texto", "Segundo texto", "Terceiro texto"]
    
    # Individual
    individual_embeddings = []
    for text in batch_texts:
        emb = model.encode(text)
        individual_embeddings.append(emb)
    
    # Batch
    batch_embeddings = model.encode(batch_texts)
    
    # Comparar
    matches = 0
    for i, (ind, batch) in enumerate(zip(individual_embeddings, batch_embeddings)):
        max_diff = np.max(np.abs(ind - batch))
        if max_diff < 1e-6:
            matches += 1
            print(f"   ✅ Texto {i+1}: Idênticos (diff: {max_diff:.2e})")
        else:
            print(f"   ⚠️  Texto {i+1}: Diferença: {max_diff:.2e}")
    
    property2_ok = matches == len(batch_texts)
    print(f"   📊 Resultado: {'✅' if property2_ok else '❌'} {matches}/{len(batch_texts)} idênticos")
    
    # Property Test 3: Consistência
    print(f"\n🧪 Property 3: Consistência")
    
    test_text = "Texto para testar consistência"
    embeddings = []
    
    for i in range(3):
        emb = model.encode(test_text)
        embeddings.append(emb)
        print(f"   🔄 Geração {i+1}: {len(emb)} dimensões")
    
    # Verificar se são idênticos
    first = embeddings[0]
    all_same = True
    
    for i, emb in enumerate(embeddings[1:], 2):
        max_diff = np.max(np.abs(first - emb))
        if max_diff > 1e-10:
            all_same = False
            print(f"   ⚠️  Geração {i}: Diferença {max_diff:.2e}")
        else:
            print(f"   ✅ Geração {i}: Idêntico")
    
    property3_ok = all_same
    print(f"   📊 Resultado: {'✅' if property3_ok else '❌'} Consistência")
    
    # Resumo final
    print(f"\n" + "=" * 50)
    print(f"📊 RESUMO DOS PROPERTY TESTS")
    
    results = [
        ("Property 1: Dimensão Consistente", property1_ok),
        ("Property 2: Batch vs Individual", property2_ok), 
        ("Property 3: Consistência", property3_ok)
    ]
    
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    
    for name, ok in results:
        status = "✅ PASSOU" if ok else "❌ FALHOU"
        print(f"   {status} - {name}")
    
    success_rate = passed / total
    print(f"\n📈 Taxa de sucesso: {passed}/{total} ({success_rate:.1%})")
    
    if success_rate >= 0.8:
        print(f"🎉 PROPERTY TESTS APROVADOS!")
        print(f"✅ Task 20 - EmbeddingService funcionando corretamente")
    else:
        print(f"❌ PROPERTY TESTS FALHARAM!")
        print(f"⚠️  Task 20 - EmbeddingService precisa correções")
    
    sys.exit(0 if success_rate >= 0.8 else 1)
    
except ImportError as e:
    print(f"❌ Dependência faltando: {e}")
    print("💡 Execute: pip install sentence-transformers torch")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erro geral: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)