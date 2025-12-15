#!/usr/bin/env python3
"""
Script de Validação da Funcionalidade de Chat
Verifica o estado real dos Preview Chats em todos os locais
"""
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

def validate_preview_chat_locations():
    """Valida cada local onde PreviewChat deveria estar"""
    print_header("VALIDAÇÃO DOS LOCAIS DE PREVIEW CHAT")
    
    locations = [
        {
            "name": "Página de Lista de Agentes (Sidebar)",
            "file": "src/pages/admin/agents/AgentsListPage.tsx",
            "expected": "Sidebar direita com PreviewChat para preview geral",
            "status": "unknown"
        },
        {
            "name": "Aba Chat de Teste (AgentDetailsPage)",
            "file": "src/pages/admin/agents/AgentDetailsPage.tsx", 
            "expected": "Aba dedicada com PreviewChat configurado",
            "status": "unknown"
        },
        {
            "name": "Wizard Passo 4 (Configuração)",
            "file": "src/components/agents/wizard/Step4ConfigRenus.tsx",
            "expected": "Coluna direita com PreviewChat durante configuração",
            "status": "unknown"
        },
        {
            "name": "Wizard Passo 5 (Review)",
            "file": "src/components/agents/wizard/Step5Review.tsx",
            "expected": "PreviewChat para validação final",
            "status": "unknown"
        },
        {
            "name": "Aba de Instruções (dentro de Configuração)",
            "file": "src/components/agents/config/InstructionsTab.tsx",
            "expected": "Preview de conversa para testar prompts",
            "status": "unknown"
        }
    ]
    
    for location in locations:
        print(f"\n📍 {location['name']}")
        
        try:
            with open(location['file'], 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar se PreviewChat está presente
            has_import = "import PreviewChat" in content
            has_usage = "<PreviewChat" in content
            
            if has_import and has_usage:
                print_result("✅", "PreviewChat implementado")
                
                # Verificar configuração
                if "agentName=" in content:
                    print_result("✅", "Prop agentName configurada")
                else:
                    print_result("⚠️", "Prop agentName não configurada")
                
                if "systemPrompt=" in content:
                    print_result("✅", "Prop systemPrompt configurada")
                else:
                    print_result("⚠️", "Prop systemPrompt não configurada")
                    
            elif has_import and not has_usage:
                print_result("⚠️", "PreviewChat importado mas não usado")
            elif not has_import and has_usage:
                print_result("❌", "PreviewChat usado sem import")
            else:
                print_result("❌", "PreviewChat não implementado")
                
        except FileNotFoundError:
            print_result("❌", f"Arquivo não encontrado: {location['file']}")
        except Exception as e:
            print_result("❌", f"Erro ao analisar: {e}")

def check_preview_chat_component_issues():
    """Verifica possíveis problemas no componente PreviewChat"""
    print_header("ANÁLISE DE PROBLEMAS NO COMPONENTE PREVIEWCHAT")
    
    try:
        with open("src/components/agents/PreviewChat.tsx", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar estrutura básica
        if "const PreviewChat: React.FC" in content:
            print_result("✅", "Componente definido corretamente")
        else:
            print_result("❌", "Definição do componente incorreta")
        
        # Verificar props interface
        if "interface PreviewChatProps" in content:
            print_result("✅", "Interface de props definida")
        else:
            print_result("❌", "Interface de props não encontrada")
        
        # Verificar estado
        if "useState<Message[]>" in content:
            print_result("✅", "Estado de mensagens implementado")
        else:
            print_result("❌", "Estado de mensagens não encontrado")
        
        # Verificar função de envio
        if "const handleSend" in content:
            print_result("✅", "Função handleSend implementada")
        else:
            print_result("❌", "Função handleSend não encontrada")
        
        # Verificar simulação de resposta
        if "setTimeout" in content and "setIsAgentTyping" in content:
            print_result("✅", "Simulação de resposta implementada")
        else:
            print_result("❌", "Simulação de resposta não encontrada")
        
        # Verificar export
        if "export default PreviewChat" in content:
            print_result("✅", "Export default correto")
        else:
            print_result("❌", "Export default incorreto")
            
    except FileNotFoundError:
        print_result("❌", "Arquivo PreviewChat.tsx não encontrado")
    except Exception as e:
        print_result("❌", f"Erro ao analisar PreviewChat: {e}")

def check_agent_details_page_implementation():
    """Verifica especificamente a implementação na página de detalhes"""
    print_header("VERIFICAÇÃO ESPECÍFICA DO AGENTDETAILSPAGE")
    
    try:
        with open("src/pages/admin/agents/AgentDetailsPage.tsx", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar import
        if "import PreviewChat from" in content:
            print_result("✅", "PreviewChat importado")
        else:
            print_result("❌", "PreviewChat não importado")
        
        # Verificar definição na mainTabs
        if "'chat', label: 'Chat de Teste'" in content:
            print_result("✅", "Aba Chat de Teste definida")
        else:
            print_result("❌", "Aba Chat de Teste não definida")
        
        # Verificar componente na mainTabs
        if "component: PreviewChat" in content:
            print_result("✅", "PreviewChat definido como componente da aba")
        else:
            print_result("❌", "PreviewChat não definido como componente")
        
        # Verificar TabsContent
        if 'value="chat"' in content and "TabsContent" in content:
            print_result("✅", "TabsContent para chat implementado")
        else:
            print_result("❌", "TabsContent para chat não encontrado")
        
        # Verificar se PreviewChat está sendo renderizado
        if "<PreviewChat" in content:
            print_result("✅", "PreviewChat sendo renderizado")
            
            # Verificar props
            if "agentName={" in content:
                print_result("✅", "Prop agentName passada")
            else:
                print_result("⚠️", "Prop agentName não passada")
        else:
            print_result("❌", "PreviewChat não sendo renderizado")
            
    except Exception as e:
        print_result("❌", f"Erro ao verificar AgentDetailsPage: {e}")

def identify_why_chat_not_working():
    """Identifica por que o chat pode não estar funcionando"""
    print_header("DIAGNÓSTICO: POR QUE O CHAT NÃO FUNCIONA")
    
    possible_issues = []
    
    # Verificar AgentDetailsPage
    try:
        with open("src/pages/admin/agents/AgentDetailsPage.tsx", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Issue 1: TabsContent ausente
        if "'chat'" in content and "component: PreviewChat" in content:
            if 'TabsContent value="chat"' not in content:
                possible_issues.append("TabsContent para aba 'chat' não implementado")
        
        # Issue 2: Grid columns incorreto
        if "grid-cols-5" in content and content.count("{ value:") == 6:
            possible_issues.append("Grid tem 5 colunas mas 6 abas definidas")
        elif "grid-cols-6" not in content and content.count("{ value:") == 6:
            possible_issues.append("Grid precisa ser atualizado para 6 colunas")
        
        # Issue 3: Props não passadas
        if "<PreviewChat" in content:
            if "agentName=" not in content:
                possible_issues.append("Prop agentName não passada para PreviewChat")
    
    except Exception as e:
        possible_issues.append(f"Erro ao analisar AgentDetailsPage: {e}")
    
    # Verificar PreviewChat
    try:
        with open("src/components/agents/PreviewChat.tsx", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Issue 4: Problemas no componente
        if "useState" not in content:
            possible_issues.append("PreviewChat não usa useState")
        
        if "handleSend" not in content:
            possible_issues.append("PreviewChat não tem função handleSend")
            
    except Exception as e:
        possible_issues.append(f"Erro ao analisar PreviewChat: {e}")
    
    if possible_issues:
        print("🚨 PROBLEMAS IDENTIFICADOS:")
        for i, issue in enumerate(possible_issues, 1):
            print_result("❌", f"Problema {i}: {issue}")
    else:
        print_result("✅", "Nenhum problema óbvio identificado")
    
    return possible_issues

def generate_fix_recommendations(issues):
    """Gera recomendações de correção"""
    print_header("RECOMENDAÇÕES DE CORREÇÃO")
    
    if not issues:
        print_result("✅", "Sistema parece estar correto")
        return
    
    print("🔧 CORREÇÕES NECESSÁRIAS:")
    
    for issue in issues:
        if "TabsContent" in issue:
            print_result("🔧", "Adicionar TabsContent para aba chat")
            print("   Código necessário:")
            print("   <TabsContent value=\"chat\">")
            print("     <PreviewChat agentName={agent.name} />")
            print("   </TabsContent>")
        
        elif "grid-cols" in issue:
            print_result("🔧", "Atualizar grid para 6 colunas")
            print("   Alterar: grid-cols-5 → grid-cols-6")
        
        elif "agentName" in issue:
            print_result("🔧", "Passar prop agentName")
            print("   <PreviewChat agentName={agent.name} />")

def main():
    """Executa validação completa da funcionalidade de chat"""
    print("🚀 VALIDAÇÃO DA FUNCIONALIDADE DE CHAT")
    print(f"⏰ Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Validar locais
    validate_preview_chat_locations()
    
    # Verificar componente
    check_preview_chat_component_issues()
    
    # Verificar implementação específica
    check_agent_details_page_implementation()
    
    # Diagnosticar problemas
    issues = identify_why_chat_not_working()
    
    # Gerar recomendações
    generate_fix_recommendations(issues)
    
    print(f"\n📝 DIAGNÓSTICO CONCLUÍDO EM: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

if __name__ == "__main__":
    main()