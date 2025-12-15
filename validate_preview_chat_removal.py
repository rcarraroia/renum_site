#!/usr/bin/env python3
"""
Script para validar remoção do card Preview Chat da página de listagem
"""
import os

def validate_preview_chat_removal():
    """Valida que o card Preview Chat foi removido da página de listagem"""
    print("=== VALIDANDO REMOÇÃO DO PREVIEW CHAT ===")
    
    file_path = "src/pages/admin/agents/AgentsListPage.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ Arquivo não encontrado: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificações
    checks = [
        {
            "name": "Import PreviewChat removido",
            "check": "import PreviewChat" not in content,
            "error": "Import do PreviewChat ainda existe"
        },
        {
            "name": "Componente PreviewChat removido",
            "check": "<PreviewChat" not in content,
            "error": "Componente PreviewChat ainda está sendo usado"
        },
        {
            "name": "Grid de filtros/preview removido",
            "check": "grid lg:grid-cols-3 gap-6 mb-6" not in content,
            "error": "Grid específico de filtros/preview ainda existe"
        },
        {
            "name": "Comentário 'Filters and Preview' removido",
            "check": "Filters and Preview" not in content,
            "error": "Comentário antigo ainda existe"
        },
        {
            "name": "Novo comentário 'Filters' existe",
            "check": "{/* Filters */" in content,
            "error": "Novo comentário não foi adicionado"
        }
    ]
    
    all_passed = True
    
    for check in checks:
        if check["check"]:
            print(f"✅ {check['name']}")
        else:
            print(f"❌ {check['name']}: {check['error']}")
            all_passed = False
    
    return all_passed

def validate_frontend_structure():
    """Valida que a estrutura do frontend ainda está correta"""
    print("\n=== VALIDANDO ESTRUTURA DO FRONTEND ===")
    
    # Verificar se AgentFilters ainda existe
    filters_path = "src/components/agents/AgentFilters.tsx"
    if os.path.exists(filters_path):
        print("✅ AgentFilters.tsx existe")
    else:
        print("❌ AgentFilters.tsx não encontrado")
        return False
    
    # Verificar se PreviewChat ainda existe (deve existir para outras páginas)
    preview_path = "src/components/agents/PreviewChat.tsx"
    if os.path.exists(preview_path):
        print("✅ PreviewChat.tsx ainda existe (correto, usado em outras páginas)")
    else:
        print("⚠️ PreviewChat.tsx não encontrado (pode ser problema)")
    
    return True

def show_before_after():
    """Mostra o antes e depois da mudança"""
    print("\n=== ANTES E DEPOIS ===")
    
    print("❌ ANTES (INCORRETO):")
    print("- Card 'Preview Chat (Simulação)' solto na página de listagem")
    print("- Não estava vinculado a nenhum agente específico")
    print("- Grid de 3 colunas (2 para filtros + 1 para preview)")
    print("- Confuso para o usuário")
    
    print("\n✅ DEPOIS (CORRETO):")
    print("- Card Preview Chat removido da listagem")
    print("- Filtros ocupam toda a largura disponível")
    print("- Preview Chat só aparece em contextos específicos:")
    print("  - Aba 'Chat de Teste' de cada agente individual")
    print("  - Wizard de criação de agentes")
    print("- Experiência mais clara e focada")

if __name__ == "__main__":
    print("🔍 VALIDAÇÃO: REMOÇÃO DO PREVIEW CHAT DA LISTAGEM")
    print("=" * 60)
    
    # Validar remoção
    removal_ok = validate_preview_chat_removal()
    
    # Validar estrutura
    structure_ok = validate_frontend_structure()
    
    # Mostrar comparação
    show_before_after()
    
    # Resultado final
    print("\n" + "=" * 60)
    if removal_ok and structure_ok:
        print("🎉 VALIDAÇÃO COMPLETA: SUCESSO!")
        print("✅ Card Preview Chat removido da listagem")
        print("✅ Estrutura do frontend mantida")
        print("✅ Componente ainda disponível para outras páginas")
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Testar a página no navegador")
        print("2. Verificar se filtros funcionam corretamente")
        print("3. Confirmar que Preview Chat funciona nas páginas corretas")
    else:
        print("❌ VALIDAÇÃO FALHOU!")
        print("Verifique os erros acima e corrija antes de continuar.")