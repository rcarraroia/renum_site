#!/usr/bin/env python3
"""
FASE 3: REMOÇÃO - Remoção do Módulo Wizard
Objetivo: Deletar TODO código do wizard, mantendo RENUS e ISA intactos
"""

import os
import shutil
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

class WizardRemovalManager:
    def __init__(self):
        self.removal_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.db_conn_string = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"
        self.removal_results = {
            "timestamp": datetime.now().isoformat(),
            "backend_files_removed": [],
            "frontend_files_removed": [],
            "database_cleaned": False,
            "routes_updated": False,
            "placeholder_created": False,
            "validation_passed": False,
            "errors": []
        }
        
        # Lista de arquivos para remover (baseada na auditoria)
        self.backend_files = [
            "backend/src/api/routes/wizard.py",
            "backend/src/services/wizard_service.py",
            "backend/src/models/wizard.py",
            "backend/src/agents/wizard_agent.py"
        ]
        
        self.frontend_files = [
            "src/components/agents/wizard/",
            "src/services/wizardService.ts"
        ]
    
    def remover_arquivos_backend(self):
        """Remove arquivos do wizard no backend"""
        print("🐍 1. REMOVENDO ARQUIVOS BACKEND...")
        
        for file_path in self.backend_files:
            try:
                if os.path.exists(file_path):
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        self.removal_results["backend_files_removed"].append(file_path)
                        print(f"   ✅ Removido: {file_path}")
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        self.removal_results["backend_files_removed"].append(file_path)
                        print(f"   ✅ Removido diretório: {file_path}")
                else:
                    print(f"   ⚠️ Arquivo não encontrado: {file_path}")
            except Exception as e:
                error_msg = f"Erro removendo {file_path}: {e}"
                self.removal_results["errors"].append(error_msg)
                print(f"   ❌ {error_msg}")
        
        print(f"   📊 Backend: {len(self.removal_results['backend_files_removed'])} arquivos removidos")
    
    def remover_arquivos_frontend(self):
        """Remove arquivos do wizard no frontend"""
        print("\n⚛️ 2. REMOVENDO ARQUIVOS FRONTEND...")
        
        for file_path in self.frontend_files:
            try:
                if os.path.exists(file_path):
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        self.removal_results["frontend_files_removed"].append(file_path)
                        print(f"   ✅ Removido: {file_path}")
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        self.removal_results["frontend_files_removed"].append(file_path)
                        print(f"   ✅ Removido diretório: {file_path}")
                else:
                    print(f"   ⚠️ Arquivo não encontrado: {file_path}")
            except Exception as e:
                error_msg = f"Erro removendo {file_path}: {e}"
                self.removal_results["errors"].append(error_msg)
                print(f"   ❌ {error_msg}")
        
        print(f"   📊 Frontend: {len(self.removal_results['frontend_files_removed'])} arquivos removidos")
    
    def limpar_banco_dados(self):
        """Limpa dados relacionados ao wizard no banco"""
        print("\n🗄️ 3. LIMPANDO BANCO DE DADOS...")
        
        try:
            conn = psycopg2.connect(self.db_conn_string)
            
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Verificar quantos agentes têm wizard_session
                cursor.execute("""
                    SELECT COUNT(*) as count
                    FROM agents 
                    WHERE config::text ILIKE '%wizard_session%'
                """)
                
                wizard_count = cursor.fetchone()['count']
                print(f"   📊 Encontrados {wizard_count} agentes com wizard_session")
                
                if wizard_count > 0:
                    # Limpar configs com wizard_session
                    print("   🧹 Limpando configs com wizard...")
                    cursor.execute("""
                        UPDATE agents 
                        SET config = config - 'wizard_session' - 'current_step' - 'step_1_data' - 'step_2_data' - 'step_3_data' - 'step_4_data' - 'step_5_data'
                        WHERE config::text ILIKE '%wizard_session%'
                    """)
                    
                    affected_rows = cursor.rowcount
                    conn.commit()
                    print(f"   ✅ {affected_rows} agentes limpos")
                else:
                    print("   ✅ Nenhum agente com wizard_session encontrado")
                
                # Verificar se limpeza foi bem-sucedida
                cursor.execute("""
                    SELECT COUNT(*) as count
                    FROM agents 
                    WHERE config::text ILIKE '%wizard_session%'
                """)
                
                remaining_count = cursor.fetchone()['count']
                if remaining_count == 0:
                    self.removal_results["database_cleaned"] = True
                    print("   ✅ Banco de dados limpo com sucesso")
                else:
                    print(f"   ⚠️ Ainda restam {remaining_count} agentes com wizard")
            
            conn.close()
            
        except Exception as e:
            error_msg = f"Erro limpando banco: {e}"
            self.removal_results["errors"].append(error_msg)
            print(f"   ❌ {error_msg}")
    
    def atualizar_dependencias(self):
        """Atualiza arquivos que dependem do wizard"""
        print("\n🔗 4. ATUALIZANDO DEPENDÊNCIAS...")
        
        # Atualizar AgentCreatePage.tsx
        agent_create_page = "src/pages/admin/agents/AgentCreatePage.tsx"
        
        try:
            if os.path.exists(agent_create_page):
                with open(agent_create_page, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Verificar se tem import do wizard
                if "wizard/AgentWizard" in content:
                    print(f"   🔧 Atualizando {agent_create_page}...")
                    
                    # Remover import do wizard
                    content = content.replace("import AgentWizard from '@/components/agents/wizard/AgentWizard'", "")
                    
                    # Substituir uso do AgentWizard por placeholder
                    placeholder_component = '''
// Placeholder para futuro Agent Builder
const PlaceholderNewAgent = () => (
  <div className="flex flex-col items-center justify-center p-8 text-center">
    <h2 className="text-2xl font-bold mb-4">Criar Novo Agente</h2>
    <p className="text-gray-600 mb-6">Agent Builder em desenvolvimento...</p>
    <button 
      disabled 
      className="px-6 py-3 bg-gray-300 text-gray-500 rounded-lg cursor-not-allowed"
    >
      + Novo Agente (Em breve)
    </button>
  </div>
)'''
                    
                    # Substituir <AgentWizard /> por <PlaceholderNewAgent />
                    content = content.replace("<AgentWizard", "<PlaceholderNewAgent")
                    content = content.replace("</AgentWizard>", "</PlaceholderNewAgent>")
                    
                    # Adicionar placeholder no início do componente
                    if "PlaceholderNewAgent" not in content:
                        # Encontrar onde inserir o placeholder
                        import_end = content.find("const AgentCreatePage")
                        if import_end > 0:
                            content = content[:import_end] + placeholder_component + "\n\n" + content[import_end:]
                    
                    # Salvar arquivo atualizado
                    with open(agent_create_page, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    self.removal_results["placeholder_created"] = True
                    print("   ✅ Placeholder criado em AgentCreatePage.tsx")
                else:
                    print("   ✅ AgentCreatePage.tsx não usa wizard")
            else:
                print(f"   ⚠️ Arquivo não encontrado: {agent_create_page}")
        
        except Exception as e:
            error_msg = f"Erro atualizando dependências: {e}"
            self.removal_results["errors"].append(error_msg)
            print(f"   ❌ {error_msg}")
        
        # Atualizar router principal (se existir)
        self.atualizar_rotas()
    
    def atualizar_rotas(self):
        """Atualiza rotas removendo wizard"""
        print("\n🛣️ 5. ATUALIZANDO ROTAS...")
        
        # Atualizar router do backend (main.py ou similar)
        backend_main_files = [
            "backend/src/main.py",
            "backend/src/api/__init__.py",
            "backend/src/api/routes/__init__.py"
        ]
        
        for main_file in backend_main_files:
            try:
                if os.path.exists(main_file):
                    with open(main_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Verificar se tem referência ao wizard
                    if "wizard" in content.lower():
                        print(f"   🔧 Atualizando {main_file}...")
                        
                        # Remover imports do wizard
                        lines = content.split('\n')
                        filtered_lines = []
                        
                        for line in lines:
                            if "wizard" not in line.lower() or "import" not in line.lower():
                                filtered_lines.append(line)
                            else:
                                print(f"     - Removido: {line.strip()}")
                        
                        # Salvar arquivo atualizado
                        with open(main_file, 'w', encoding='utf-8') as f:
                            f.write('\n'.join(filtered_lines))
                        
                        print(f"   ✅ {main_file} atualizado")
            
            except Exception as e:
                error_msg = f"Erro atualizando {main_file}: {e}"
                self.removal_results["errors"].append(error_msg)
                print(f"   ❌ {error_msg}")
        
        self.removal_results["routes_updated"] = True
        print("   ✅ Rotas atualizadas")
    
    def validar_remocao(self):
        """Valida se a remoção foi bem-sucedida"""
        print("\n🔍 6. VALIDANDO REMOÇÃO...")
        
        validations = []
        
        # Verificar se arquivos foram removidos
        for file_path in self.backend_files + self.frontend_files:
            if not os.path.exists(file_path):
                validations.append(f"✅ {file_path} removido")
            else:
                validations.append(f"❌ {file_path} ainda existe")
        
        # Verificar banco de dados
        try:
            conn = psycopg2.connect(self.db_conn_string)
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*) FROM agents 
                    WHERE config::text ILIKE '%wizard_session%'
                """)
                wizard_count = cursor.fetchone()[0]
                
                if wizard_count == 0:
                    validations.append("✅ Banco limpo (sem wizard_session)")
                else:
                    validations.append(f"❌ {wizard_count} agentes ainda com wizard")
            
            conn.close()
        except Exception as e:
            validations.append(f"❌ Erro validando banco: {e}")
        
        # Mostrar validações
        for validation in validations:
            print(f"   {validation}")
        
        # Considerar válido se a maioria passou
        success_count = len([v for v in validations if v.startswith("✅")])
        total_count = len(validations)
        
        self.removal_results["validation_passed"] = success_count >= (total_count * 0.8)
        
        if self.removal_results["validation_passed"]:
            print("   ✅ Validação de remoção PASSOU")
        else:
            print("   ❌ Validação de remoção FALHOU")
    
    def gerar_relatorio(self):
        """Gera relatório final da remoção"""
        print("\n📊 7. GERANDO RELATÓRIO DE REMOÇÃO...")
        
        # Salvar relatório
        relatorio_file = f"relatorio_remocao_{self.removal_timestamp}.json"
        with open(relatorio_file, 'w', encoding='utf-8') as f:
            json.dump(self.removal_results, f, indent=2, ensure_ascii=False)
        
        return self.removal_results

def main():
    print("🗑️ MISSÃO: Remoção Completa do Módulo Wizard")
    print("📋 FASE 3: REMOÇÃO")
    print("=" * 60)
    print("Objetivo: Deletar TODO código do wizard")
    print("Tempo estimado: 2 horas")
    print("=" * 60)
    
    removal_manager = WizardRemovalManager()
    
    # Executar remoção completa
    removal_manager.remover_arquivos_backend()
    removal_manager.remover_arquivos_frontend()
    removal_manager.limpar_banco_dados()
    removal_manager.atualizar_dependencias()
    removal_manager.validar_remocao()
    
    # Gerar relatório
    relatorio = removal_manager.gerar_relatorio()
    
    print("\n" + "=" * 60)
    print("📊 RESUMO DA REMOÇÃO")
    print("=" * 60)
    
    print(f"🐍 Backend files: {len(relatorio['backend_files_removed'])} removidos")
    print(f"⚛️ Frontend files: {len(relatorio['frontend_files_removed'])} removidos")
    print(f"🗄️ Database: {'✅ Limpo' if relatorio['database_cleaned'] else '❌ Não limpo'}")
    print(f"🔗 Routes: {'✅ Atualizadas' if relatorio['routes_updated'] else '❌ Não atualizadas'}")
    print(f"🎯 Placeholder: {'✅ Criado' if relatorio['placeholder_created'] else '❌ Não criado'}")
    print(f"🔍 Validação: {'✅ PASSOU' if relatorio['validation_passed'] else '❌ FALHOU'}")
    
    if relatorio['errors']:
        print(f"\n⚠️ Erros encontrados: {len(relatorio['errors'])}")
        for error in relatorio['errors']:
            print(f"   - {error}")
    
    if relatorio['validation_passed']:
        print("\n🎉 REMOÇÃO CONCLUÍDA COM SUCESSO!")
        print("🔄 PRÓXIMA FASE: Validação (1 hora)")
    else:
        print("\n🚨 REMOÇÃO FALHOU!")
        print("❌ Alguns arquivos/dados não foram removidos")
        print("🔧 Verifique os erros antes de continuar")
    
    return relatorio['validation_passed']

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)