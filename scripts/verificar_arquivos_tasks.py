#!/usr/bin/env python3
"""
Script para verificar quais arquivos mencionados nas tasks realmente existem
"""

from pathlib import Path

def verificar_arquivo_existe(caminho):
    """Verifica se um arquivo existe"""
    return Path(caminho).exists()

def verificar_arquivos_tasks():
    """Verifica todos os arquivos mencionados nas tasks"""
    
    print("🔍 VERIFICAÇÃO DE ARQUIVOS DAS TASKS")
    print("=" * 50)
    
    # Lista de todos os arquivos mencionados nas tasks
    arquivos_tasks = [
        # Phase 1: Database
        ("Task 1", "backend/migrations/009_create_agents_table.sql"),
        ("Task 1.1", "src/tests/property/unified-storage.test.ts"),
        ("Task 1.2", "src/tests/property/sub-agent-relationships.test.ts"),
        ("Task 2", "backend/migrations/010_migrate_subagents_to_agents.sql"),
        
        # Phase 2: Backend API
        ("Task 3", "backend/src/services/agent_service.py"),
        ("Task 3.1", "src/tests/property/config-integrity.test.ts"),
        ("Task 3.2", "src/tests/property/query-filtering.test.ts"),
        ("Task 4", "backend/src/services/wizard_service.py"),
        ("Task 4.1", "src/tests/property/wizard-type-validation.test.ts"),
        ("Task 5", "backend/src/api/routes/agents.py"),
        
        # Phase 3: Sub-agent System
        ("Task 6", "backend/src/services/sub_agent_inheritance_service.py"),
        ("Task 6.1", "src/tests/property/inheritance-consistency.test.ts"),
        ("Task 6.2", "src/tests/property/inheritance-independence.test.ts"),
        
        # Phase 4: Integration System
        ("Task 8", "backend/src/services/integration_service.py"),
        
        # Phase 5: Frontend Wizard
        ("Task 10.1", "src/components/agents/wizard/steps/WizardStep1TypeSelection.tsx"),
        ("Task 10.2", "src/components/agents/wizard/steps/WizardStep2BasicInfo.tsx"),
        ("Task 10.3", "src/components/agents/wizard/steps/WizardStep3Personality.tsx"),
        ("Task 10.4", "src/components/agents/wizard/steps/WizardStep4DataCollection.tsx"),
        ("Task 10.5", "src/components/agents/wizard/steps/WizardStep5Integrations.tsx"),
        ("Task 10.6", "src/components/agents/wizard/steps/WizardStep6TestPublish.tsx"),
        ("Task 11", "src/components/agents/wizard/AgentWizard.tsx"),
        
        # Phase 6: Configuration Tabs
        ("Task 13", "src/components/agents/config/InstructionsTab.tsx"),
        ("Task 14", "src/components/agents/config/SiccTab.tsx"),
        ("Task 15", "src/components/agents/config/ToolsTab.tsx"),
        ("Task 16", "src/components/agents/config/IntegrationsTab.tsx"),
        ("Task 17", "src/components/agents/config/KnowledgeTab.tsx"),
        ("Task 18", "src/components/agents/config/TriggersTab.tsx"),
        ("Task 19", "src/components/agents/config/GuardrailsTab.tsx"),
        ("Task 20", "src/components/agents/config/SubAgentsTab.tsx"),
        ("Task 21", "src/components/agents/config/AdvancedTab.tsx"),
        
        # Phase 7: Contextual Interfaces
        ("Task 22", "src/pages/agents/contextual/RenusInterface.tsx"),
        ("Task 23", "src/pages/agents/contextual/PesquisasInterface.tsx"),
        ("Task 24", "src/pages/agents/contextual/IsaInterface.tsx"),
        
        # Phase 8: Marketplace
        ("Task 25.1", "src/pages/marketplace/TemplateMarketplace.tsx"),
        ("Task 25.2", "src/pages/marketplace/TemplatePreview.tsx"),
        
        # Phase 9: Navigation
        ("Task 27", "src/components/dashboard/Sidebar.tsx"),
        ("Task 30", "src/pages/intelligence/IntelligenceDashboard.tsx"),
        ("Task 31", "src/pages/integrations/IntegrationsRadar.tsx"),
        
        # Phase 10: Cross-Component
        ("Task 32", "src/components/navigation/CrossComponentNav.tsx"),
        
        # Phase 11: Testing
        ("Task 33.1", "e2e/wizard-flow.spec.ts"),
        ("Task 34", "backend/tests/performance/load_test.py"),
        ("Task 35", "backend/tests/security/test_security_compliance.py"),
    ]
    
    existem = 0
    nao_existem = 0
    
    for task, arquivo in arquivos_tasks:
        existe = verificar_arquivo_existe(arquivo)
        status = "✅" if existe else "❌"
        print(f"{status} {task}: {arquivo}")
        
        if existe:
            existem += 1
        else:
            nao_existem += 1
    
    print()
    print("📊 RESUMO")
    print("=" * 50)
    total = len(arquivos_tasks)
    print(f"Total de arquivos verificados: {total}")
    print(f"✅ Existem: {existem} ({existem/total*100:.1f}%)")
    print(f"❌ Não existem: {nao_existem} ({nao_existem/total*100:.1f}%)")
    
    return existem, nao_existem, total

if __name__ == "__main__":
    verificar_arquivos_tasks()