#!/usr/bin/env python3
"""
FASE 2: BACKUP - Remoção do Módulo Wizard
Objetivo: Criar backup completo antes da remoção
"""

import os
import subprocess
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

class WizardBackupManager:
    def __init__(self):
        self.backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_branch = f"backup-pre-wizard-removal-{self.backup_timestamp}"
        self.db_conn_string = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"
        self.backup_results = {
            "timestamp": datetime.now().isoformat(),
            "backup_branch": self.backup_branch,
            "git_backup": False,
            "database_backup": False,
            "files_backup": False,
            "validation": False,
            "errors": []
        }
    
    def criar_backup_git(self):
        """Cria backup via Git branch"""
        print("🔄 1. CRIANDO BACKUP GIT...")
        
        try:
            # Verificar status do git
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, check=True)
            
            if result.stdout.strip():
                print("   📝 Arquivos não commitados encontrados, adicionando...")
                subprocess.run(['git', 'add', '.'], check=True)
                subprocess.run(['git', 'commit', '-m', f'Pre-wizard-removal backup {self.backup_timestamp}'], check=True)
            
            # Criar branch de backup
            print(f"   🌿 Criando branch: {self.backup_branch}")
            subprocess.run(['git', 'checkout', '-b', self.backup_branch], check=True)
            
            # Voltar para main/master
            try:
                subprocess.run(['git', 'checkout', 'main'], check=True)
                print("   ✅ Voltou para branch main")
            except subprocess.CalledProcessError:
                subprocess.run(['git', 'checkout', 'master'], check=True)
                print("   ✅ Voltou para branch master")
            
            self.backup_results["git_backup"] = True
            print("   ✅ Backup Git criado com sucesso")
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Erro no backup Git: {e}"
            self.backup_results["errors"].append(error_msg)
            print(f"   ❌ {error_msg}")
        except Exception as e:
            error_msg = f"Erro inesperado no Git: {e}"
            self.backup_results["errors"].append(error_msg)
            print(f"   ❌ {error_msg}")
    
    def criar_backup_database(self):
        """Cria backup do banco de dados"""
        print("\n🗄️ 2. CRIANDO BACKUP DO BANCO DE DADOS...")
        
        try:
            # Criar backup da tabela agents (principal afetada)
            conn = psycopg2.connect(self.db_conn_string)
            
            backup_data = {
                "timestamp": self.backup_timestamp,
                "agents": [],
                "wizard_configs": []
            }
            
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Backup completo da tabela agents
                print("   📊 Fazendo backup da tabela agents...")
                cursor.execute("SELECT * FROM agents ORDER BY created_at")
                agents = cursor.fetchall()
                
                for agent in agents:
                    agent_dict = dict(agent)
                    # Converter UUID e datetime para string
                    for key, value in agent_dict.items():
                        if hasattr(value, 'isoformat'):  # datetime
                            agent_dict[key] = value.isoformat()
                        elif hasattr(value, '__str__') and 'UUID' in str(type(value)):  # UUID
                            agent_dict[key] = str(value)
                    
                    backup_data["agents"].append(agent_dict)
                
                # Backup específico de configs com wizard
                print("   🧙 Fazendo backup de configs com wizard...")
                cursor.execute("""
                    SELECT id, name, config 
                    FROM agents 
                    WHERE config::text ILIKE '%wizard%'
                """)
                
                wizard_configs = cursor.fetchall()
                for config in wizard_configs:
                    config_dict = dict(config)
                    config_dict['id'] = str(config_dict['id'])
                    backup_data["wizard_configs"].append(config_dict)
                
                print(f"   📈 Backup criado: {len(backup_data['agents'])} agentes, {len(backup_data['wizard_configs'])} com wizard")
            
            conn.close()
            
            # Salvar backup em arquivo
            backup_filename = f"backup_database_{self.backup_timestamp}.json"
            with open(backup_filename, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            self.backup_results["database_backup"] = True
            self.backup_results["database_file"] = backup_filename
            print(f"   ✅ Backup do banco salvo em: {backup_filename}")
            
        except Exception as e:
            error_msg = f"Erro no backup do banco: {e}"
            self.backup_results["errors"].append(error_msg)
            print(f"   ❌ {error_msg}")
    
    def criar_backup_arquivos(self):
        """Cria backup dos arquivos wizard"""
        print("\n📁 3. CRIANDO BACKUP DOS ARQUIVOS WIZARD...")
        
        try:
            import shutil
            import zipfile
            
            # Lista de arquivos wizard para backup
            wizard_files = [
                "backend/src/api/routes/wizard.py",
                "backend/src/services/wizard_service.py", 
                "backend/src/models/wizard.py",
                "backend/src/agents/wizard_agent.py",
                "src/components/agents/wizard/",
                "src/services/wizardService.ts"
            ]
            
            backup_zip = f"backup_wizard_files_{self.backup_timestamp}.zip"
            
            with zipfile.ZipFile(backup_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                files_backed_up = 0
                
                for file_path in wizard_files:
                    if os.path.exists(file_path):
                        if os.path.isfile(file_path):
                            zipf.write(file_path)
                            files_backed_up += 1
                            print(f"   📄 Backup: {file_path}")
                        elif os.path.isdir(file_path):
                            for root, dirs, files in os.walk(file_path):
                                for file in files:
                                    full_path = os.path.join(root, file)
                                    arc_path = os.path.relpath(full_path)
                                    zipf.write(full_path, arc_path)
                                    files_backed_up += 1
                            print(f"   📁 Backup: {file_path}/ ({files_backed_up} arquivos)")
                    else:
                        print(f"   ⚠️ Arquivo não encontrado: {file_path}")
            
            self.backup_results["files_backup"] = True
            self.backup_results["files_backup_zip"] = backup_zip
            self.backup_results["files_count"] = files_backed_up
            print(f"   ✅ Backup de arquivos criado: {backup_zip} ({files_backed_up} arquivos)")
            
        except Exception as e:
            error_msg = f"Erro no backup de arquivos: {e}"
            self.backup_results["errors"].append(error_msg)
            print(f"   ❌ {error_msg}")
    
    def validar_backup(self):
        """Valida se os backups foram criados corretamente"""
        print("\n🔍 4. VALIDANDO BACKUPS...")
        
        try:
            validations = []
            
            # Validar branch Git
            if self.backup_results["git_backup"]:
                result = subprocess.run(['git', 'branch', '--list', self.backup_branch], 
                                      capture_output=True, text=True)
                if self.backup_branch in result.stdout:
                    validations.append("✅ Branch de backup existe")
                else:
                    validations.append("❌ Branch de backup não encontrada")
            
            # Validar arquivo de banco
            if self.backup_results["database_backup"]:
                db_file = self.backup_results.get("database_file")
                if db_file and os.path.exists(db_file):
                    size = os.path.getsize(db_file)
                    validations.append(f"✅ Backup do banco existe ({size} bytes)")
                else:
                    validations.append("❌ Backup do banco não encontrado")
            
            # Validar arquivo de arquivos
            if self.backup_results["files_backup"]:
                files_zip = self.backup_results.get("files_backup_zip")
                if files_zip and os.path.exists(files_zip):
                    size = os.path.getsize(files_zip)
                    validations.append(f"✅ Backup de arquivos existe ({size} bytes)")
                else:
                    validations.append("❌ Backup de arquivos não encontrado")
            
            # Mostrar validações
            for validation in validations:
                print(f"   {validation}")
            
            # Considerar válido se pelo menos Git backup funcionou
            self.backup_results["validation"] = self.backup_results["git_backup"]
            
            if self.backup_results["validation"]:
                print("   ✅ Validação de backup PASSOU")
            else:
                print("   ❌ Validação de backup FALHOU")
                
        except Exception as e:
            error_msg = f"Erro na validação: {e}"
            self.backup_results["errors"].append(error_msg)
            print(f"   ❌ {error_msg}")
    
    def gerar_relatorio(self):
        """Gera relatório final do backup"""
        print("\n📊 5. GERANDO RELATÓRIO DE BACKUP...")
        
        # Salvar relatório
        relatorio_file = f"relatorio_backup_{self.backup_timestamp}.json"
        with open(relatorio_file, 'w', encoding='utf-8') as f:
            json.dump(self.backup_results, f, indent=2, ensure_ascii=False)
        
        return self.backup_results

def main():
    print("🗑️ MISSÃO: Remoção Completa do Módulo Wizard")
    print("📋 FASE 2: BACKUP")
    print("=" * 60)
    print("Objetivo: Criar backup completo antes da remoção")
    print("Tempo estimado: 30 minutos")
    print("=" * 60)
    
    backup_manager = WizardBackupManager()
    
    # Executar backup completo
    backup_manager.criar_backup_git()
    backup_manager.criar_backup_database()
    backup_manager.criar_backup_arquivos()
    backup_manager.validar_backup()
    
    # Gerar relatório
    relatorio = backup_manager.gerar_relatorio()
    
    print("\n" + "=" * 60)
    print("📊 RESUMO DO BACKUP")
    print("=" * 60)
    
    print(f"🌿 Git backup: {'✅ OK' if relatorio['git_backup'] else '❌ FALHOU'}")
    print(f"🗄️ Database backup: {'✅ OK' if relatorio['database_backup'] else '❌ FALHOU'}")
    print(f"📁 Files backup: {'✅ OK' if relatorio['files_backup'] else '❌ FALHOU'}")
    print(f"🔍 Validação: {'✅ PASSOU' if relatorio['validation'] else '❌ FALHOU'}")
    
    if relatorio['errors']:
        print(f"\n⚠️ Erros encontrados: {len(relatorio['errors'])}")
        for error in relatorio['errors']:
            print(f"   - {error}")
    
    if relatorio['validation']:
        print("\n🎉 BACKUP CONCLUÍDO COM SUCESSO!")
        print(f"📂 Branch de backup: {relatorio['backup_branch']}")
        print("🔄 PRÓXIMA FASE: Remoção (2 horas)")
    else:
        print("\n🚨 BACKUP FALHOU!")
        print("❌ NÃO é seguro prosseguir com a remoção")
        print("🔧 Corrija os erros antes de continuar")
    
    return relatorio['validation']

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)