#!/usr/bin/env python3
"""
Script de Validação das Funcionalidades de Preview de Conversa
Verifica onde o PreviewChat está sendo usado e se está funcionando
"""
import os
import re
from datetime import datetime

def print_header(title):
    print("\n" + "="*60)
    print(f"🔍 {title}")
    print("="*60)

def print_result(test_name, status, details=""):
    icons = {"✅": "✅", "❌": "❌", "⚠️": "⚠️", "🔄": "🔄", "📍": "📍"}
    icon = icons.get(status, "❓")
    print(f"{icon} {test_name}")
    if details:
        print(f"   {details}")

def find_preview_chat_usage():
    """Encontra todos os locais onde PreviewChat é usado"""
    print_header("LOCALIZANDO USOS DO PREVIEWCHAT")
    
    locations = []
    
    # Procurar em todos os arquivos .tsx
    for root, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith(".tsx"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Verificar se usa PreviewChat
                    if "PreviewChat" in content:
                        # Verificar se é import ou uso
                        has_import = "import PreviewChat" in content or "import { PreviewChat }" in content
                        has_usage = "<PreviewChat" in content
                        
                        if has_import or has_usage:
                            locations.append({
                                "file": file_path,
                                "has_import": has_import,
                                "has_usage": has_usage,
                                "content": content
                            })
                except Exception as e:
                    continue
    
    return locations

def analyze_preview_chat_locations():
    """Analisa cada local onde PreviewChat é usado"""
    print_header("ANÁLISE DOS LOCAIS DE USO DO PREVIEWCHAT")
    
    locations = find_preview_chat_usage()
    
    for i, location in enumerate(locations, 1):
        file_path = location["file"]
        print(f"\n📍 LOCAL {i}: {file_path}")
        
        # Determinar o contexto
        if "AgentsListPage" in file_path:
            context = "Página de Lista de Agentes (sidebar direita)"
        elif "AgentDetailsPage" in file_path:
            context = "Página de Detalhes do Agente (nova aba)"
        elif "Step4ConfigRenus" in file_path:
            context = "Wizard - Passo 4 (Configuração)"
        elif "Step5Review" in file_path:
            context = "Wizard - Passo 5 (Review)"
        elif "InstructionsTab" in file_path:
            context = "Aba de Instruções (dentro de Configuração)"
        else:
            context = "Local não identificado"
        
        print_result("📍", f"Contexto: {context}")
        
        # Verificar se tem import
        if location["has_import"]:
            print_result("✅", "Import presente")
        else:
            print_result("❌", "Import ausente")
        
        # Verificar se tem uso
        if location["has_usage"]:
            print_result("✅", "Componente usado")
            
            # Verificar se passa props
            content = location["content"]
            if "agentName=" in content:
                print_result("✅", "Prop agentName configurada")
            else:
                print_result("⚠️", "Prop agentName não configurada")
            
            if "systemPrompt=" in content:
                print_result("✅", "Prop systemPrompt configurada")
            else:
                print_result("⚠️", "Prop systemPrompt não configurada")
                
            if "onTest=" in content:
                print_result("✅", "Prop onTest configurada")
            else:
                print_result("⚠️", "Prop onTest não configurada")
        else:
            print_result("❌", "Componente não usado (apenas import)")

def check_preview_chat_component():
    """Verifica o componente PreviewChat em si"""
    print_header("ANÁLISE DO COMPONENTE PREVIEWCHAT")
    
    try:
        with open("src/components/agents/PreviewChat.tsx", 'r', encoding='utf-8') as f:
            content = f.read()
        
        print_result("✅", "Arquivo PreviewChat.tsx existe")
        
        # Verificar funcionalidades
        if "useState" in content:
            print_result("✅", "Usa state (componente interativo)")
        
        if "handleSend" in content:
            print_result("✅", "Função handleSend implementada")
        
        if "setTimeout" in content:
            print_result("✅", "Simulação de resposta implementada")
        
        if "MessageBubble" in content:
            print_result("✅", "Componente MessageBubble implementado")
        
        if "TypingIndicator" in content:
            print_result("✅", "Indicador de digitação implementado")
        
        # Verificar se há problemas potenciais
        if "mock" in content.lower() or "Mock" in content:
            print_result("🔄", "Usa dados mock (normal para simulação)")
        
        # Verificar props aceitas
        if "agentName?" in content:
            print_result("✅", "Prop agentName opcional implementada")
        
        if "systemPrompt?" in content:
            print_result("✅", "Prop systemPrompt opcional implementada")
        
        if "onTest?" in content:
            print_result("✅", "Prop onTest opcional implementada")
            
    except FileNotFoundError:
        print_result("❌", "Arquivo PreviewChat.tsx não encontrado")
    except Exception as e:
        print_result("❌", "Erro ao analisar PreviewChat.tsx", f"Erro: {e}")

def check_agent_details_page_tabs():
    """Verifica especificamente as abas do AgentDetailsPage"""
    print_header("VERIFICAÇÃO DAS ABAS DO AGENTDETAILSPAGE")
    
    try:
        with open("src/pages/admin/agents/AgentDetailsPage.tsx", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Procurar pela definição das mainTabs
        tabs_match = re.search(r'const mainTabs = \[(.*?)\];', content, re.DOTALL)
        if tabs_match:
            tabs_content = tabs_match.group(1)
            
            # Verificar cada aba
            tabs = [
                ("overview", "Visão Geral"),
                ("config", "Configuração"),
                ("chat", "Chat de Teste"),
                ("users", "Usuários/Instâncias"),
                ("metrics", "Métricas"),
                ("logs", "Logs")
            ]
            
            for tab_value, tab_label in tabs:
                if f"'{tab_value}'" in tabs_content and tab_label in tabs_content:
                    print_result("✅", f"Aba {tab_label} configurada")
                else:
                    print_result("❌", f"Aba {tab_label} não encontrada")
            
            # Verificar se Chat de Teste usa PreviewChat
            if "component: PreviewChat" in tabs_content:
                print_result("✅", "Aba Chat de Teste usa PreviewChat")
            else:
                print_result("❌", "Aba Chat de Teste não usa PreviewChat")
        else:
            print_result("❌", "Definição de mainTabs não encontrada")
            
    except Exception as e:
        print_result("❌", "Erro ao verificar AgentDetailsPage", f"Erro: {e}")

def identify_potential_issues():
    """Identifica possíveis problemas com o chat de teste"""
    print_header("IDENTIFICAÇÃO DE PROBLEMAS POTENCIAIS")
    
    issues = []
    
    # Verificar se há conflitos de import
    try:
        with open("src/pages/admin/agents/AgentDetailsPage.tsx", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Contar imports de PreviewChat
        import_count = content.count("import PreviewChat")
        if import_count > 1:
            issues.append("Múltiplos imports de PreviewChat")
        elif import_count == 0:
            issues.append("Import de PreviewChat ausente")
        
        # Verificar se há erros de sintaxe óbvios
        if "component: PreviewChat" in content and "import PreviewChat" not in content:
            issues.append("PreviewChat usado sem import")
        
        # Verificar se há props sendo passadas incorretamente
        if "<PreviewChat" in content:
            # Extrair uso do componente
            usage_match = re.search(r'<PreviewChat[^>]*>', content)
            if usage_match:
                usage = usage_match.group(0)
                if "agentName={" not in usage and "agentName=" not in usage:
                    issues.append("PreviewChat sem prop agentName")
    except Exception as e:
        issues.append(f"Erro ao analisar AgentDetailsPage: {e}")
    
    if issues:
        for issue in issues:
            print_result("❌", f"Problema identificado: {issue}")
    else:
        print_result("✅", "Nenhum problema óbvio identificado")

def generate_summary():
    """Gera resumo da análise"""
    print_header("RESUMO DA ANÁLISE")
    
    print("📊 LOCAIS ONDE PREVIEWCHAT DEVERIA ESTAR:")
    print("1. 📍 Página de Lista de Agentes (sidebar) - Para preview geral")
    print("2. 📍 Wizard Passo 4 (Configuração) - Para testar durante criação")
    print("3. 📍 Wizard Passo 5 (Review) - Para validação final")
    print("4. 📍 Aba de Instruções - Para testar prompts")
    print("5. 📍 Nova Aba 'Chat de Teste' - Para testar agente pronto")
    
    print("\n🎯 PROBLEMAS MAIS PROVÁVEIS:")
    print("- Props não configuradas corretamente")
    print("- Import duplicado ou ausente")
    print("- Componente não renderizando por erro de sintaxe")
    print("- Dados do agente não sendo passados")
    
    print(f"\n📝 ANÁLISE CONCLUÍDA EM: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

def main():
    """Executa análise completa dos Preview Chats"""
    print("🚀 ANÁLISE COMPLETA DOS PREVIEW CHATS")
    print(f"⏰ Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Encontrar todos os usos
    analyze_preview_chat_locations()
    
    # Verificar o componente
    check_preview_chat_component()
    
    # Verificar abas específicas
    check_agent_details_page_tabs()
    
    # Identificar problemas
    identify_potential_issues()
    
    # Gerar resumo
    generate_summary()

if __name__ == "__main__":
    main()