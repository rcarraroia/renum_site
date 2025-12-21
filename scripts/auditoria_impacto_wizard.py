#!/usr/bin/env python3
"""
FASE 1: AUDITORIA DE IMPACTO - Remoção do Módulo Wizard
Objetivo: Mapear TODAS as dependências antes da remoção
"""

import os
import re
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

class WizardImpactAuditor:
    def __init__(self):
        self.db_conn_string = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"
        self.impactos = {
            "arquivos_wizard": [],
            "dependencias_backend": [],
            "dependencias_frontend": [],
            "tabelas_colunas_wizard": [],
            "rotas_afetadas": [],
            "componentes_dependentes": [],
            "funcionalidades_criticas": [],
            "renus_isa_safe": True,
            "warnings": []
        }
    
    def auditar_backend(self):
        """Audita dependências do wizard no backend"""
        print("🔍 1. AUDITANDO BACKEND...")
        
        backend_dirs = [
            "backend/src/api/routes",
            "backend/src/services", 
            "backend/src/models",
            "backend/src/agents",
            "backend/src/utils"
        ]
        
        wizard_patterns = [
            r'wizard',
            r'WizardService',
            r'wizard_id',
            r'wizard_session',
            r'WizardStep',
            r'from.*wizard',
            r'import.*wizard'
        ]
        
        for directory in backend_dirs:
            if os.path.exists(directory):
                print(f"   Analisando {directory}...")
                self.buscar_referencias(directory, wizard_patterns, "backend")
    
    def auditar_frontend(self):
        """Audita dependências do wizard no frontend"""
        print("\n🔍 2. AUDITANDO FRONTEND...")
        
        frontend_dirs = [
            "src/components",
            "src/pages", 
            "src/services",
            "src/types",
            "src/hooks"
        ]
        
        wizard_patterns = [
            r'wizard',
            r'Wizard',
            r'wizardService',
            r'WizardContext',
            r'WizardStep',
            r'from.*wizard',
            r'import.*wizard',
            r'/wizard',
            r'wizard/'
        ]
        
        for directory in frontend_dirs:
            if os.path.exists(directory):
                print(f"   Analisando {directory}...")
                self.buscar_referencias(directory, wizard_patterns, "frontend")
    
    def buscar_referencias(self, directory, patterns, tipo):
        """Busca referências aos padrões em arquivos"""
        for root, dirs, files in os.walk(directory):
            # Ignorar node_modules, __pycache__, etc
            dirs[:] = [d for d in dirs if d not in ['node_modules', '__pycache__', '.git', 'dist']]
            
            for file in files:
                if file.endswith(('.py', '.ts', '.tsx', '.js', '.jsx')):
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Verificar se é arquivo wizard
                        if 'wizard' in file.lower():
                            self.impactos["arquivos_wizard"].append({
                                "arquivo": file_path,
                                "tipo": "arquivo_wizard",
                                "descricao": "Arquivo do módulo wizard (para deletar)"
                            })
                        
                        # Buscar referências
                        for pattern in patterns:
                            matches = re.finditer(pattern, content, re.IGNORECASE)
                            for match in matches:
                                line_num = content[:match.start()].count('\n') + 1
                                line_content = content.split('\n')[line_num - 1].strip()
                                
                                dependencia = {
                                    "arquivo": file_path,
                                    "linha": line_num,
                                    "conteudo": line_content,
                                    "pattern": pattern,
                                    "match": match.group()
                                }
                                
                                if tipo == "backend":
                                    self.impactos["dependencias_backend"].append(dependencia)
                                else:
                                    self.impactos["dependencias_frontend"].append(dependencia)
                                
                                # Verificar se afeta RENUS ou ISA
                                if any(agent in file_path.lower() for agent in ['renus', 'isa']):
                                    self.impactos["funcionalidades_criticas"].append({
                                        "arquivo": file_path,
                                        "linha": line_num,
                                        "agente": "RENUS/ISA",
                                        "dependencia": line_content,
                                        "risco": "ALTO - Pode quebrar agente crítico"
                                    })
                                    self.impactos["renus_isa_safe"] = False
                    
                    except Exception as e:
                        self.impactos["warnings"].append(f"Erro lendo {file_path}: {e}")
    
    def auditar_banco(self):
        """Audita colunas e tabelas relacionadas ao wizard no banco"""
        print("\n🔍 3. AUDITANDO BANCO DE DADOS...")
        
        try:
            conn = psycopg2.connect(self.db_conn_string)
            
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Buscar colunas com 'wizard' no nome
                print("   3.1 Buscando colunas com 'wizard'...")
                cursor.execute("""
                    SELECT table_name, column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE column_name ILIKE '%wizard%'
                    ORDER BY table_name, column_name
                """)
                
                wizard_columns = cursor.fetchall()
                for col in wizard_columns:
                    self.impactos["tabelas_colunas_wizard"].append({
                        "tabela": col['table_name'],
                        "coluna": col['column_name'],
                        "tipo": col['data_type'],
                        "nullable": col['is_nullable'],
                        "default": col['column_default'],
                        "acao": "REMOVER coluna"
                    })
                
                # Verificar dados com wizard_session no config
                print("   3.2 Buscando dados com wizard_session...")
                cursor.execute("""
                    SELECT id, name, config
                    FROM agents 
                    WHERE config::text ILIKE '%wizard%'
                    LIMIT 10
                """)
                
                wizard_data = cursor.fetchall()
                for agent in wizard_data:
                    config = agent['config'] if agent['config'] else {}
                    if isinstance(config, dict) and config.get('wizard_session'):
                        self.impactos["tabelas_colunas_wizard"].append({
                            "tabela": "agents",
                            "registro_id": agent['id'],
                            "nome": agent['name'],
                            "problema": "Config contém wizard_session",
                            "acao": "LIMPAR config ou DELETAR registro"
                        })
                
                # Verificar se RENUS/ISA dependem de wizard
                print("   3.3 Verificando RENUS/ISA...")
                cursor.execute("""
                    SELECT id, name, config, system_prompt
                    FROM agents 
                    WHERE name ILIKE '%renus%' OR name ILIKE '%isa%'
                """)
                
                critical_agents = cursor.fetchall()
                for agent in critical_agents:
                    config_str = str(agent['config']) if agent['config'] else ""
                    prompt_str = str(agent['system_prompt']) if agent['system_prompt'] else ""
                    
                    if 'wizard' in config_str.lower() or 'wizard' in prompt_str.lower():
                        self.impactos["funcionalidades_criticas"].append({
                            "agente": agent['name'],
                            "id": agent['id'],
                            "problema": "Referência a wizard no config ou prompt",
                            "risco": "CRÍTICO - Pode quebrar RENUS/ISA",
                            "acao": "REVISAR e LIMPAR referências"
                        })
                        self.impactos["renus_isa_safe"] = False
            
            conn.close()
            print("   ✅ Auditoria do banco concluída")
            
        except Exception as e:
            self.impactos["warnings"].append(f"Erro auditando banco: {e}")
            print(f"   ❌ Erro auditando banco: {e}")
    
    def auditar_rotas(self):
        """Audita rotas que serão afetadas"""
        print("\n🔍 4. AUDITANDO ROTAS...")
        
        # Backend routes
        routes_file = "backend/src/api/routes/wizard.py"
        if os.path.exists(routes_file):
            try:
                with open(routes_file, 'r') as f:
                    content = f.read()
                
                # Extrair rotas definidas
                route_patterns = [
                    r'@router\.(get|post|put|delete)\("([^"]+)"',
                    r'@app\.(get|post|put|delete)\("([^"]+)"'
                ]
                
                for pattern in route_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        self.impactos["rotas_afetadas"].append({
                            "arquivo": routes_file,
                            "metodo": match.group(1).upper(),
                            "rota": match.group(2),
                            "acao": "REMOVER rota"
                        })
            
            except Exception as e:
                self.impactos["warnings"].append(f"Erro lendo rotas: {e}")
        
        # Frontend routes
        frontend_routes = [
            "src/App.tsx",
            "src/router.tsx", 
            "src/routes.tsx"
        ]
        
        for route_file in frontend_routes:
            if os.path.exists(route_file):
                try:
                    with open(route_file, 'r') as f:
                        content = f.read()
                    
                    # Buscar rotas com wizard
                    wizard_routes = re.finditer(r'path[=:]\s*["\']([^"\']*wizard[^"\']*)["\']', content, re.IGNORECASE)
                    for match in wizard_routes:
                        self.impactos["rotas_afetadas"].append({
                            "arquivo": route_file,
                            "rota": match.group(1),
                            "acao": "REMOVER rota do frontend"
                        })
                
                except Exception as e:
                    self.impactos["warnings"].append(f"Erro lendo {route_file}: {e}")
    
    def auditar_componentes_dependentes(self):
        """Audita componentes que podem depender do wizard"""
        print("\n🔍 5. AUDITANDO COMPONENTES DEPENDENTES...")
        
        # Buscar componentes que importam ou usam wizard
        frontend_files = []
        for root, dirs, files in os.walk("src"):
            dirs[:] = [d for d in dirs if d not in ['node_modules', 'dist']]
            for file in files:
                if file.endswith(('.tsx', '.ts', '.jsx', '.js')):
                    frontend_files.append(os.path.join(root, file))
        
        for file_path in frontend_files:
            if 'wizard' not in file_path.lower():  # Não é arquivo wizard
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    # Buscar imports de wizard
                    wizard_imports = re.finditer(r'import.*from.*["\'].*wizard.*["\']', content, re.IGNORECASE)
                    for match in wizard_imports:
                        self.impactos["componentes_dependentes"].append({
                            "arquivo": file_path,
                            "import": match.group(),
                            "acao": "REMOVER import e código dependente"
                        })
                    
                    # Buscar uso de componentes wizard
                    wizard_usage = re.finditer(r'<Wizard[A-Za-z]*', content)
                    for match in wizard_usage:
                        self.impactos["componentes_dependentes"].append({
                            "arquivo": file_path,
                            "uso": match.group(),
                            "acao": "SUBSTITUIR por placeholder ou remover"
                        })
                
                except Exception as e:
                    self.impactos["warnings"].append(f"Erro analisando {file_path}: {e}")
    
    def gerar_relatorio(self):
        """Gera relatório final da auditoria"""
        print("\n📊 GERANDO RELATÓRIO DE IMPACTO...")
        
        relatorio = {
            "timestamp": datetime.now().isoformat(),
            "missao": "Remoção Completa do Módulo Wizard",
            "fase": "1 - Auditoria de Impacto",
            "resumo": {
                "arquivos_wizard_encontrados": len(self.impactos["arquivos_wizard"]),
                "dependencias_backend": len(self.impactos["dependencias_backend"]),
                "dependencias_frontend": len(self.impactos["dependencias_frontend"]),
                "tabelas_colunas_afetadas": len(self.impactos["tabelas_colunas_wizard"]),
                "rotas_afetadas": len(self.impactos["rotas_afetadas"]),
                "componentes_dependentes": len(self.impactos["componentes_dependentes"]),
                "funcionalidades_criticas": len(self.impactos["funcionalidades_criticas"]),
                "renus_isa_safe": self.impactos["renus_isa_safe"],
                "warnings": len(self.impactos["warnings"])
            },
            "detalhes": self.impactos
        }
        
        # Salvar relatório
        with open('auditoria_impacto_wizard.json', 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
        
        return relatorio

def main():
    print("🗑️ MISSÃO: Remoção Completa do Módulo Wizard")
    print("📋 FASE 1: AUDITORIA DE IMPACTO")
    print("=" * 60)
    print("Objetivo: Mapear TODAS as dependências antes da remoção")
    print("Tempo estimado: 2 horas")
    print("=" * 60)
    
    auditor = WizardImpactAuditor()
    
    # Executar auditoria completa
    auditor.auditar_backend()
    auditor.auditar_frontend()
    auditor.auditar_banco()
    auditor.auditar_rotas()
    auditor.auditar_componentes_dependentes()
    
    # Gerar relatório
    relatorio = auditor.gerar_relatorio()
    
    print("\n" + "=" * 60)
    print("📊 RESUMO DA AUDITORIA")
    print("=" * 60)
    
    resumo = relatorio["resumo"]
    print(f"📁 Arquivos wizard encontrados: {resumo['arquivos_wizard_encontrados']}")
    print(f"🐍 Dependências backend: {resumo['dependencias_backend']}")
    print(f"⚛️ Dependências frontend: {resumo['dependencias_frontend']}")
    print(f"🗄️ Tabelas/colunas afetadas: {resumo['tabelas_colunas_afetadas']}")
    print(f"🛣️ Rotas afetadas: {resumo['rotas_afetadas']}")
    print(f"🧩 Componentes dependentes: {resumo['componentes_dependentes']}")
    print(f"⚠️ Funcionalidades críticas: {resumo['funcionalidades_criticas']}")
    print(f"🛡️ RENUS/ISA seguros: {'✅ SIM' if resumo['renus_isa_safe'] else '❌ NÃO'}")
    print(f"⚠️ Warnings: {resumo['warnings']}")
    
    print(f"\n📄 Relatório detalhado salvo em: auditoria_impacto_wizard.json")
    
    if not resumo['renus_isa_safe']:
        print("\n🚨 ATENÇÃO: RENUS/ISA podem ser afetados!")
        print("   Revisar funcionalidades críticas antes de prosseguir")
    
    if resumo['funcionalidades_criticas'] > 0:
        print(f"\n⚠️ CUIDADO: {resumo['funcionalidades_criticas']} funcionalidades críticas encontradas")
        print("   Verificar impacto antes da remoção")
    
    print("\n🔄 PRÓXIMA FASE: Backup (30 min)")
    print("   Criar branch de backup antes da remoção")
    
    return relatorio

if __name__ == "__main__":
    relatorio = main()