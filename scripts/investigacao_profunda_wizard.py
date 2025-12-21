#!/usr/bin/env python3
"""
Investigação profunda e completa do módulo wizard
Objetivo: Encontrar TODOS os bugs, erros e inconsistências
APENAS REPORTAR - NÃO CORRIGIR
"""

import os
import json
import requests
import psycopg2
from psycopg2.extras import RealDictCursor
import ast
import re
from datetime import datetime

class WizardInvestigator:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.db_conn_string = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"
        self.bugs_encontrados = []
        self.inconsistencias = []
        self.warnings = []
        
    def log_bug(self, categoria, titulo, descricao, severidade="MÉDIO", arquivo=None, linha=None):
        """Registra um bug encontrado"""
        bug = {
            "categoria": categoria,
            "titulo": titulo,
            "descricao": descricao,
            "severidade": severidade,
            "arquivo": arquivo,
            "linha": linha,
            "timestamp": datetime.now().isoformat()
        }
        self.bugs_encontrados.append(bug)
        
    def log_inconsistencia(self, titulo, descricao, arquivos_envolvidos=None):
        """Registra uma inconsistência encontrada"""
        inconsistencia = {
            "titulo": titulo,
            "descricao": descricao,
            "arquivos_envolvidos": arquivos_envolvidos or [],
            "timestamp": datetime.now().isoformat()
        }
        self.inconsistencias.append(inconsistencia)
        
    def log_warning(self, titulo, descricao):
        """Registra um warning/alerta"""
        warning = {
            "titulo": titulo,
            "descricao": descricao,
            "timestamp": datetime.now().isoformat()
        }
        self.warnings.append(warning)

    def investigar_estrutura_banco(self):
        """Investiga estrutura do banco relacionada ao wizard"""
        print("🔍 1. INVESTIGANDO ESTRUTURA DO BANCO DE DADOS...")
        
        try:
            conn = psycopg2.connect(self.db_conn_string)
            
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # 1.1 Verificar estrutura da tabela agents
                print("   1.1 Analisando tabela 'agents'...")
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable, column_default, character_maximum_length
                    FROM information_schema.columns 
                    WHERE table_name = 'agents'
                    ORDER BY ordinal_position
                """)
                
                columns = cursor.fetchall()
                print(f"       Total de colunas: {len(columns)}")
                
                # Verificar colunas obrigatórias para wizard
                required_columns = ['id', 'name', 'status', 'config', 'client_id', 'slug', 'system_prompt']
                missing_columns = []
                
                existing_columns = [col['column_name'] for col in columns]
                for req_col in required_columns:
                    if req_col not in existing_columns:
                        missing_columns.append(req_col)
                
                if missing_columns:
                    self.log_bug(
                        "BANCO_DADOS", 
                        "Colunas obrigatórias faltando",
                        f"Colunas necessárias para wizard não encontradas: {missing_columns}",
                        "CRÍTICO"
                    )
                
                # 1.2 Verificar tipos de dados problemáticos
                for col in columns:
                    col_name = col['column_name']
                    data_type = col['data_type']
                    is_nullable = col['is_nullable']
                    
                    # Verificar se config é JSONB
                    if col_name == 'config' and data_type != 'jsonb':
                        self.log_bug(
                            "BANCO_DADOS",
                            "Tipo incorreto para coluna config",
                            f"Coluna 'config' deveria ser JSONB mas é {data_type}",
                            "ALTO"
                        )
                    
                    # Verificar se campos de texto têm limite adequado
                    if col_name in ['name', 'slug'] and col['character_maximum_length'] and col['character_maximum_length'] < 100:
                        self.log_warning(
                            f"Limite baixo para {col_name}",
                            f"Coluna '{col_name}' tem limite de {col['character_maximum_length']} caracteres"
                        )
                
                # 1.3 Verificar índices
                print("   1.2 Verificando índices...")
                cursor.execute("""
                    SELECT indexname, indexdef 
                    FROM pg_indexes 
                    WHERE tablename = 'agents'
                """)
                
                indexes = cursor.fetchall()
                index_columns = []
                for idx in indexes:
                    # Extrair colunas do índice
                    if 'client_id' in idx['indexdef']:
                        index_columns.append('client_id')
                    if 'slug' in idx['indexdef']:
                        index_columns.append('slug')
                
                # Verificar índices importantes
                if 'client_id' not in index_columns:
                    self.log_warning(
                        "Índice faltando",
                        "Índice em 'client_id' recomendado para performance"
                    )
                
                if 'slug' not in index_columns:
                    self.log_warning(
                        "Índice faltando",
                        "Índice em 'slug' recomendado para URLs únicas"
                    )
                
                # 1.4 Verificar constraints
                print("   1.3 Verificando constraints...")
                cursor.execute("""
                    SELECT constraint_name, constraint_type 
                    FROM information_schema.table_constraints 
                    WHERE table_name = 'agents'
                """)
                
                constraints = cursor.fetchall()
                constraint_types = [c['constraint_type'] for c in constraints]
                
                if 'UNIQUE' not in constraint_types:
                    self.log_warning(
                        "Constraint UNIQUE faltando",
                        "Nenhuma constraint UNIQUE encontrada - slug deveria ser único"
                    )
                
                # 1.5 Verificar dados existentes
                print("   1.4 Analisando dados existentes...")
                cursor.execute("SELECT COUNT(*) as total FROM agents")
                total_agents = cursor.fetchone()['total']
                
                cursor.execute("SELECT COUNT(*) as total FROM agents WHERE config IS NULL")
                null_configs = cursor.fetchone()['total']
                
                cursor.execute("SELECT COUNT(*) as total FROM agents WHERE status IS NULL")
                null_status = cursor.fetchone()['total']
                
                if null_configs > 0:
                    self.log_bug(
                        "DADOS",
                        "Agentes com config NULL",
                        f"{null_configs} de {total_agents} agentes têm config NULL",
                        "MÉDIO"
                    )
                
                if null_status > 0:
                    self.log_bug(
                        "DADOS",
                        "Agentes com status NULL",
                        f"{null_status} de {total_agents} agentes têm status NULL",
                        "ALTO"
                    )
                
                # 1.6 Verificar estrutura do config JSONB
                print("   1.5 Analisando estrutura do config JSONB...")
                cursor.execute("""
                    SELECT id, name, config 
                    FROM agents 
                    WHERE config IS NOT NULL 
                    LIMIT 10
                """)
                
                agents_with_config = cursor.fetchall()
                config_structures = {}
                
                for agent in agents_with_config:
                    config = agent['config']
                    if config:
                        # Analisar estrutura do config
                        keys = list(config.keys()) if isinstance(config, dict) else []
                        config_structures[agent['id']] = keys
                
                # Verificar consistência das estruturas
                if config_structures:
                    all_keys = set()
                    for keys in config_structures.values():
                        all_keys.update(keys)
                    
                    # Verificar se todos os agentes têm as mesmas chaves
                    inconsistent_configs = []
                    for agent_id, keys in config_structures.items():
                        missing_keys = all_keys - set(keys)
                        if missing_keys:
                            inconsistent_configs.append((agent_id, missing_keys))
                    
                    if inconsistent_configs:
                        self.log_inconsistencia(
                            "Estruturas de config inconsistentes",
                            f"Agentes com estruturas diferentes no config: {inconsistent_configs}"
                        )
            
            conn.close()
            print("   ✅ Investigação do banco concluída")
            
        except Exception as e:
            self.log_bug(
                "BANCO_DADOS",
                "Erro conectando ao banco",
                f"Não foi possível conectar ao banco: {e}",
                "CRÍTICO"
            )

    def investigar_backend_wizard(self):
        """Investiga código do backend relacionado ao wizard"""
        print("\n🔍 2. INVESTIGANDO BACKEND WIZARD...")
        
        # 2.1 Verificar arquivos do wizard
        wizard_files = [
            "backend/src/api/routes/wizard.py",
            "backend/src/services/wizard_service.py",
            "backend/src/models/wizard.py"
        ]
        
        for file_path in wizard_files:
            if os.path.exists(file_path):
                print(f"   2.1 Analisando {file_path}...")
                self.analisar_arquivo_python(file_path)
            else:
                self.log_bug(
                    "ARQUIVO_FALTANDO",
                    f"Arquivo wizard não encontrado",
                    f"Arquivo esperado não existe: {file_path}",
                    "CRÍTICO"
                )

    def analisar_arquivo_python(self, file_path):
        """Analisa um arquivo Python em busca de bugs"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar sintaxe Python
            try:
                ast.parse(content)
            except SyntaxError as e:
                self.log_bug(
                    "SINTAXE",
                    "Erro de sintaxe Python",
                    f"Erro de sintaxe em {file_path}: {e}",
                    "CRÍTICO",
                    file_path,
                    e.lineno
                )
                return
            
            lines = content.split('\n')
            
            # Verificar problemas comuns
            for i, line in enumerate(lines, 1):
                line_stripped = line.strip()
                
                # 1. Verificar imports problemáticos
                if line_stripped.startswith('from') or line_stripped.startswith('import'):
                    if 'datetime' in line and 'timezone' not in line:
                        self.log_warning(
                            "Import de datetime sem timezone",
                            f"Linha {i} em {file_path}: {line_stripped}"
                        )
                
                # 2. Verificar uso de datetime sem timezone
                if 'datetime.now()' in line and 'timezone' not in line:
                    self.log_bug(
                        "DATETIME",
                        "datetime.now() sem timezone",
                        f"Uso de datetime.now() sem timezone pode causar problemas de ISO format",
                        "ALTO",
                        file_path,
                        i
                    )
                
                # 3. Verificar variáveis não definidas
                if re.search(r'\b(step_\d+_data)\b', line) and 'def ' not in line and '=' not in line:
                    if not re.search(r'(step_\d+_data)\s*=', content[:content.find(line)]):
                        self.log_bug(
                            "VARIAVEL_NAO_DEFINIDA",
                            "Variável possivelmente não definida",
                            f"Variável step_X_data usada mas pode não estar definida",
                            "ALTO",
                            file_path,
                            i
                        )
                
                # 4. Verificar SQL injection potencial
                if 'cursor.execute(' in line and '%s' not in line and '?' not in line:
                    if any(var in line for var in ['f"', "f'", '.format(', '%']):
                        self.log_bug(
                            "SEGURANCA",
                            "Possível SQL injection",
                            f"Query SQL com interpolação de string não segura",
                            "CRÍTICO",
                            file_path,
                            i
                        )
                
                # 5. Verificar exception handling
                if 'except:' in line and 'pass' in lines[i] if i < len(lines) else False:
                    self.log_bug(
                        "EXCEPTION_HANDLING",
                        "Exception silenciosa",
                        f"Exception capturada mas ignorada com pass",
                        "MÉDIO",
                        file_path,
                        i
                    )
                
                # 6. Verificar async/await inconsistente
                if 'def ' in line and 'async' not in line:
                    # Verificar se função usa await
                    func_content = self.extrair_funcao(content, i)
                    if 'await ' in func_content:
                        self.log_bug(
                            "ASYNC_AWAIT",
                            "Função não-async usando await",
                            f"Função não marcada como async mas usa await",
                            "CRÍTICO",
                            file_path,
                            i
                        )
                
                # 7. Verificar return types inconsistentes
                if 'return ' in line:
                    # Verificar se função tem type hints
                    func_line = self.encontrar_linha_funcao(lines, i)
                    if func_line and '->' not in func_line:
                        self.log_warning(
                            "Type hints faltando",
                            f"Função sem type hint de retorno em linha {i}"
                        )
            
            # Verificar estrutura geral do arquivo
            self.verificar_estrutura_arquivo(file_path, content)
            
        except Exception as e:
            self.log_bug(
                "ANALISE_ARQUIVO",
                "Erro analisando arquivo",
                f"Erro ao analisar {file_path}: {e}",
                "MÉDIO"
            )

    def extrair_funcao(self, content, line_num):
        """Extrai conteúdo de uma função a partir da linha"""
        lines = content.split('\n')
        func_lines = []
        indent_level = None
        
        for i in range(line_num - 1, len(lines)):
            line = lines[i]
            if indent_level is None and line.strip():
                indent_level = len(line) - len(line.lstrip())
            
            if line.strip() and len(line) - len(line.lstrip()) <= indent_level and i > line_num - 1:
                break
                
            func_lines.append(line)
        
        return '\n'.join(func_lines)

    def encontrar_linha_funcao(self, lines, current_line):
        """Encontra a linha de definição da função atual"""
        for i in range(current_line - 1, -1, -1):
            if lines[i].strip().startswith('def ') or lines[i].strip().startswith('async def '):
                return lines[i]
        return None

    def verificar_estrutura_arquivo(self, file_path, content):
        """Verifica estrutura geral do arquivo"""
        # Verificar se tem docstring
        if '"""' not in content and "'''" not in content:
            self.log_warning(
                "Docstring faltando",
                f"Arquivo {file_path} não tem docstring"
            )
        
        # Verificar imports organizados
        lines = content.split('\n')
        import_section = []
        for line in lines:
            if line.startswith('import ') or line.startswith('from '):
                import_section.append(line)
            elif line.strip() and not line.startswith('#'):
                break
        
        # Verificar se imports estão ordenados
        if len(import_section) > 1:
            sorted_imports = sorted(import_section)
            if import_section != sorted_imports:
                self.log_warning(
                    "Imports não ordenados",
                    f"Imports em {file_path} não estão ordenados alfabeticamente"
                )

    def investigar_endpoints_wizard(self):
        """Investiga endpoints do wizard via API"""
        print("\n🔍 3. INVESTIGANDO ENDPOINTS DO WIZARD...")
        
        endpoints = [
            ("POST", "/api/agents/wizard/start", {"client_id": None, "category": "b2c"}),
            ("GET", "/api/agents/wizard/templates", None),
            ("PUT", "/api/agents/wizard/test-id/step/1", {"test": "data"}),
            ("POST", "/api/agents/wizard/test-id/publish", None),
            ("GET", "/api/agents/wizard/test-id", None),
            ("DELETE", "/api/agents/wizard/test-id", None)
        ]
        
        for method, endpoint, data in endpoints:
            print(f"   3.1 Testando {method} {endpoint}...")
            self.testar_endpoint(method, endpoint, data)

    def testar_endpoint(self, method, endpoint, data):
        """Testa um endpoint específico"""
        try:
            url = f"{self.backend_url}{endpoint}"
            
            if method == "GET":
                response = requests.get(url, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=10)
            elif method == "PUT":
                response = requests.put(url, json=data, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, timeout=10)
            else:
                self.log_bug(
                    "ENDPOINT",
                    "Método HTTP não suportado",
                    f"Método {method} não implementado no teste",
                    "BAIXO"
                )
                return
            
            # Analisar resposta
            status_code = response.status_code
            
            if status_code >= 500:
                self.log_bug(
                    "ENDPOINT",
                    f"Erro 5xx em {endpoint}",
                    f"{method} {endpoint} retornou {status_code}: {response.text}",
                    "CRÍTICO"
                )
            elif status_code >= 400:
                # Verificar se é erro esperado ou bug
                if endpoint.endswith("/test-id") or endpoint.endswith("/test-id/step/1"):
                    # Erro esperado para ID inexistente
                    pass
                else:
                    self.log_bug(
                        "ENDPOINT",
                        f"Erro 4xx em {endpoint}",
                        f"{method} {endpoint} retornou {status_code}: {response.text}",
                        "ALTO"
                    )
            
            # Verificar headers de resposta
            content_type = response.headers.get('content-type', '')
            if status_code == 200 and 'application/json' not in content_type:
                self.log_warning(
                    "Content-Type incorreto",
                    f"{endpoint} não retorna JSON: {content_type}"
                )
            
            # Verificar estrutura da resposta JSON
            if status_code == 200:
                try:
                    json_data = response.json()
                    self.validar_estrutura_resposta(endpoint, json_data)
                except json.JSONDecodeError:
                    self.log_bug(
                        "ENDPOINT",
                        "Resposta não é JSON válido",
                        f"{endpoint} retorna conteúdo que não é JSON válido",
                        "ALTO"
                    )
            
        except requests.exceptions.ConnectionError:
            self.log_bug(
                "ENDPOINT",
                "Backend não acessível",
                f"Não foi possível conectar ao backend em {self.backend_url}",
                "CRÍTICO"
            )
        except requests.exceptions.Timeout:
            self.log_bug(
                "ENDPOINT",
                "Timeout no endpoint",
                f"{method} {endpoint} demorou mais que 10 segundos",
                "ALTO"
            )
        except Exception as e:
            self.log_bug(
                "ENDPOINT",
                "Erro testando endpoint",
                f"Erro inesperado testando {method} {endpoint}: {e}",
                "MÉDIO"
            )

    def validar_estrutura_resposta(self, endpoint, json_data):
        """Valida estrutura da resposta JSON"""
        if "/wizard/start" in endpoint:
            required_fields = ['id', 'current_step', 'created_at']
            for field in required_fields:
                if field not in json_data:
                    self.log_bug(
                        "RESPOSTA_API",
                        f"Campo obrigatório faltando em {endpoint}",
                        f"Campo '{field}' não encontrado na resposta",
                        "ALTO"
                    )
            
            # Verificar formato do ID
            if 'id' in json_data:
                import uuid
                try:
                    uuid.UUID(json_data['id'])
                except ValueError:
                    self.log_bug(
                        "RESPOSTA_API",
                        "ID não é UUID válido",
                        f"Campo 'id' não é um UUID válido: {json_data['id']}",
                        "MÉDIO"
                    )

    def investigar_frontend_wizard(self):
        """Investiga componentes do frontend relacionados ao wizard"""
        print("\n🔍 4. INVESTIGANDO FRONTEND WIZARD...")
        
        # Verificar arquivos do wizard
        frontend_files = [
            "src/components/agents/wizard/AgentWizard.tsx",
            "src/components/agents/wizard/WizardContext.tsx",
            "src/components/agents/wizard/steps/WizardStep1TypeSelection.tsx",
            "src/components/agents/wizard/steps/WizardStep2BasicInfo.tsx",
            "src/components/agents/wizard/steps/WizardStep3Personality.tsx",
            "src/components/agents/wizard/steps/WizardStep4DataCollection.tsx",
            "src/components/agents/wizard/steps/WizardStep5Integrations.tsx",
            "src/components/agents/wizard/steps/WizardStep6TestPublish.tsx",
            "src/services/wizardService.ts"
        ]
        
        for file_path in frontend_files:
            if os.path.exists(file_path):
                print(f"   4.1 Analisando {file_path}...")
                self.analisar_arquivo_frontend(file_path)
            else:
                self.log_bug(
                    "ARQUIVO_FALTANDO",
                    f"Arquivo frontend não encontrado",
                    f"Arquivo esperado não existe: {file_path}",
                    "ALTO"
                )

    def analisar_arquivo_frontend(self, file_path):
        """Analisa arquivo do frontend (TypeScript/React)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                line_stripped = line.strip()
                
                # 1. Verificar console.log em produção
                if 'console.log(' in line and 'development' not in line:
                    self.log_warning(
                        "Console.log em produção",
                        f"Console.log encontrado em {file_path}:{i}"
                    )
                
                # 2. Verificar useState sem tipo
                if 'useState(' in line and not re.search(r'useState<.*>\(', line):
                    self.log_warning(
                        "useState sem tipo TypeScript",
                        f"useState sem tipo explícito em {file_path}:{i}"
                    )
                
                # 3. Verificar any types
                if ': any' in line or 'any[]' in line:
                    self.log_warning(
                        "Uso de tipo 'any'",
                        f"Tipo 'any' usado em {file_path}:{i}"
                    )
                
                # 4. Verificar props sem interface
                if 'props:' in line and 'any' in line:
                    self.log_bug(
                        "TYPESCRIPT",
                        "Props sem interface definida",
                        f"Props usando 'any' em vez de interface",
                        "MÉDIO",
                        file_path,
                        i
                    )
                
                # 5. Verificar useEffect sem dependências
                if 'useEffect(' in line:
                    # Verificar se próximas linhas têm array de dependências
                    effect_content = self.extrair_useeffect(lines, i)
                    if '], [])' not in effect_content and '], [' not in effect_content:
                        self.log_warning(
                            "useEffect sem dependências",
                            f"useEffect sem array de dependências em {file_path}:{i}"
                        )
                
                # 6. Verificar fetch sem error handling
                if 'fetch(' in line or 'axios.' in line:
                    func_content = self.extrair_funcao_js(lines, i)
                    if 'catch' not in func_content and 'try' not in func_content:
                        self.log_bug(
                            "ERROR_HANDLING",
                            "Request sem tratamento de erro",
                            f"Request HTTP sem tratamento de erro",
                            "ALTO",
                            file_path,
                            i
                        )
                
                # 7. Verificar controlled vs uncontrolled components
                if 'value={' in line and 'onChange=' not in content:
                    self.log_bug(
                        "REACT",
                        "Componente controlled sem onChange",
                        f"Input com value mas sem onChange",
                        "ALTO",
                        file_path,
                        i
                    )
                
                # 8. Verificar key prop em listas
                if '.map(' in line and 'key=' not in line:
                    # Verificar se próxima linha tem key
                    next_lines = lines[i:i+3] if i < len(lines) - 3 else lines[i:]
                    if not any('key=' in l for l in next_lines):
                        self.log_warning(
                            "Key prop faltando",
                            f"Map sem key prop em {file_path}:{i}"
                        )
            
            # Verificar imports
            self.verificar_imports_frontend(file_path, content)
            
        except Exception as e:
            self.log_bug(
                "ANALISE_ARQUIVO",
                "Erro analisando arquivo frontend",
                f"Erro ao analisar {file_path}: {e}",
                "MÉDIO"
            )

    def extrair_useeffect(self, lines, start_line):
        """Extrai conteúdo do useEffect"""
        effect_lines = []
        paren_count = 0
        started = False
        
        for i in range(start_line - 1, len(lines)):
            line = lines[i]
            if 'useEffect(' in line:
                started = True
            
            if started:
                effect_lines.append(line)
                paren_count += line.count('(') - line.count(')')
                
                if paren_count <= 0 and started and i > start_line - 1:
                    break
        
        return '\n'.join(effect_lines)

    def extrair_funcao_js(self, lines, start_line):
        """Extrai conteúdo de função JavaScript/TypeScript"""
        func_lines = []
        brace_count = 0
        started = False
        
        # Procurar início da função
        for i in range(start_line - 1, -1, -1):
            line = lines[i]
            if any(keyword in line for keyword in ['function ', 'const ', 'let ', '=>', 'async ']):
                start_line = i
                break
        
        for i in range(start_line, len(lines)):
            line = lines[i]
            func_lines.append(line)
            
            brace_count += line.count('{') - line.count('}')
            
            if brace_count <= 0 and i > start_line:
                break
        
        return '\n'.join(func_lines)

    def verificar_imports_frontend(self, file_path, content):
        """Verifica imports do frontend"""
        lines = content.split('\n')
        imports = []
        
        for line in lines:
            if line.startswith('import '):
                imports.append(line)
        
        # Verificar imports não utilizados
        for imp in imports:
            # Extrair nome do import
            if ' from ' in imp:
                import_part = imp.split(' from ')[0]
                if '{' in import_part:
                    # Named imports
                    names = re.findall(r'\b\w+\b', import_part.split('{')[1].split('}')[0])
                    for name in names:
                        if name not in content.replace(imp, ''):
                            self.log_warning(
                                "Import não utilizado",
                                f"Import '{name}' não utilizado em {file_path}"
                            )

    def investigar_consistencia_dados(self):
        """Investiga consistência entre frontend, backend e banco"""
        print("\n🔍 5. INVESTIGANDO CONSISTÊNCIA DE DADOS...")
        
        # 5.1 Verificar modelos Pydantic vs estrutura do banco
        self.verificar_modelos_vs_banco()
        
        # 5.2 Verificar tipos TypeScript vs API
        self.verificar_tipos_frontend_vs_api()
        
        # 5.3 Verificar fluxo de dados
        self.verificar_fluxo_dados()

    def verificar_modelos_vs_banco(self):
        """Verifica se modelos Pydantic batem com estrutura do banco"""
        print("   5.1 Verificando modelos Pydantic vs banco...")
        
        # Ler modelo wizard.py se existir
        wizard_model_path = "backend/src/models/wizard.py"
        if os.path.exists(wizard_model_path):
            try:
                with open(wizard_model_path, 'r') as f:
                    model_content = f.read()
                
                # Extrair campos dos modelos
                model_fields = re.findall(r'(\w+):\s*([^=\n]+)', model_content)
                
                # Comparar com estrutura do banco
                try:
                    conn = psycopg2.connect(self.db_conn_string)
                    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                        cursor.execute("""
                            SELECT column_name, data_type 
                            FROM information_schema.columns 
                            WHERE table_name = 'agents'
                        """)
                        db_columns = {row['column_name']: row['data_type'] for row in cursor.fetchall()}
                    
                    conn.close()
                    
                    # Verificar inconsistências
                    for field_name, field_type in model_fields:
                        if field_name in db_columns:
                            db_type = db_columns[field_name]
                            # Verificar compatibilidade de tipos
                            if not self.tipos_compativeis(field_type, db_type):
                                self.log_inconsistencia(
                                    f"Tipo incompatível: {field_name}",
                                    f"Modelo Pydantic: {field_type}, Banco: {db_type}",
                                    [wizard_model_path, "banco de dados"]
                                )
                        else:
                            self.log_inconsistencia(
                                f"Campo no modelo mas não no banco: {field_name}",
                                f"Campo '{field_name}' existe no modelo mas não na tabela agents",
                                [wizard_model_path, "banco de dados"]
                            )
                
                except Exception as e:
                    self.log_bug(
                        "CONSISTENCIA",
                        "Erro verificando consistência modelo-banco",
                        f"Erro: {e}",
                        "MÉDIO"
                    )
                    
            except Exception as e:
                self.log_bug(
                    "ANALISE_ARQUIVO",
                    "Erro lendo modelo wizard",
                    f"Erro lendo {wizard_model_path}: {e}",
                    "MÉDIO"
                )

    def tipos_compativeis(self, pydantic_type, db_type):
        """Verifica se tipos Pydantic e PostgreSQL são compatíveis"""
        # Mapeamento básico de tipos
        type_mapping = {
            'str': ['text', 'varchar', 'character varying'],
            'int': ['integer', 'bigint', 'smallint'],
            'float': ['real', 'double precision', 'numeric'],
            'bool': ['boolean'],
            'datetime': ['timestamp with time zone', 'timestamp without time zone'],
            'UUID': ['uuid'],
            'dict': ['jsonb', 'json'],
            'list': ['jsonb', 'json']
        }
        
        pydantic_clean = pydantic_type.strip().split('[')[0]  # Remove generics
        
        for py_type, db_types in type_mapping.items():
            if py_type in pydantic_clean and db_type.lower() in db_types:
                return True
        
        return False

    def verificar_tipos_frontend_vs_api(self):
        """Verifica se tipos TypeScript batem com API"""
        print("   5.2 Verificando tipos TypeScript vs API...")
        
        # Verificar se existe arquivo de tipos
        types_files = [
            "src/types/wizard.ts",
            "src/types/agent.ts",
            "src/services/wizardService.ts"
        ]
        
        for file_path in types_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    # Extrair interfaces TypeScript
                    interfaces = re.findall(r'interface\s+(\w+)\s*{([^}]+)}', content, re.DOTALL)
                    
                    for interface_name, interface_body in interfaces:
                        # Analisar campos da interface
                        fields = re.findall(r'(\w+)[?]?:\s*([^;\n]+)', interface_body)
                        
                        # Verificar se interface corresponde à resposta da API
                        # (Isso seria mais complexo na prática, aqui só verificamos estrutura básica)
                        if not fields:
                            self.log_warning(
                                f"Interface vazia: {interface_name}",
                                f"Interface {interface_name} em {file_path} está vazia"
                            )
                
                except Exception as e:
                    self.log_bug(
                        "ANALISE_ARQUIVO",
                        "Erro analisando tipos TypeScript",
                        f"Erro lendo {file_path}: {e}",
                        "MÉDIO"
                    )

    def verificar_fluxo_dados(self):
        """Verifica fluxo de dados entre componentes"""
        print("   5.3 Verificando fluxo de dados...")
        
        # Verificar se WizardContext está sendo usado corretamente
        context_file = "src/components/agents/wizard/WizardContext.tsx"
        if os.path.exists(context_file):
            try:
                with open(context_file, 'r') as f:
                    context_content = f.read()
                
                # Verificar se context tem todos os métodos necessários
                required_methods = ['updateStep', 'goToStep', 'submitWizard']
                for method in required_methods:
                    if method not in context_content:
                        self.log_warning(
                            f"Método faltando no context: {method}",
                            f"WizardContext pode estar incompleto"
                        )
                
            except Exception as e:
                self.log_bug(
                    "ANALISE_ARQUIVO",
                    "Erro analisando WizardContext",
                    f"Erro: {e}",
                    "MÉDIO"
                )

    def gerar_relatorio(self):
        """Gera relatório final da investigação"""
        print("\n📊 GERANDO RELATÓRIO FINAL...")
        
        total_bugs = len(self.bugs_encontrados)
        total_inconsistencias = len(self.inconsistencias)
        total_warnings = len(self.warnings)
        
        # Contar por severidade
        bugs_criticos = len([b for b in self.bugs_encontrados if b['severidade'] == 'CRÍTICO'])
        bugs_altos = len([b for b in self.bugs_encontrados if b['severidade'] == 'ALTO'])
        bugs_medios = len([b for b in self.bugs_encontrados if b['severidade'] == 'MÉDIO'])
        bugs_baixos = len([b for b in self.bugs_encontrados if b['severidade'] == 'BAIXO'])
        
        # Contar por categoria
        categorias = {}
        for bug in self.bugs_encontrados:
            cat = bug['categoria']
            categorias[cat] = categorias.get(cat, 0) + 1
        
        relatorio = {
            "timestamp": datetime.now().isoformat(),
            "resumo": {
                "total_bugs": total_bugs,
                "total_inconsistencias": total_inconsistencias,
                "total_warnings": total_warnings,
                "bugs_por_severidade": {
                    "CRÍTICO": bugs_criticos,
                    "ALTO": bugs_altos,
                    "MÉDIO": bugs_medios,
                    "BAIXO": bugs_baixos
                },
                "bugs_por_categoria": categorias
            },
            "bugs_encontrados": self.bugs_encontrados,
            "inconsistencias": self.inconsistencias,
            "warnings": self.warnings
        }
        
        return relatorio

def main():
    print("🔍 INVESTIGAÇÃO PROFUNDA E COMPLETA DO MÓDULO WIZARD")
    print("=" * 70)
    print("Objetivo: Encontrar TODOS os bugs, erros e inconsistências")
    print("Método: Análise estática + testes dinâmicos + verificação de consistência")
    print("APENAS REPORTAR - NÃO CORRIGIR")
    print("=" * 70)
    
    investigator = WizardInvestigator()
    
    # Executar todas as investigações
    investigator.investigar_estrutura_banco()
    investigator.investigar_backend_wizard()
    investigator.investigar_endpoints_wizard()
    investigator.investigar_frontend_wizard()
    investigator.investigar_consistencia_dados()
    
    # Gerar relatório
    relatorio = investigator.gerar_relatorio()
    
    # Salvar relatório em arquivo
    with open('relatorio_investigacao_wizard.json', 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 INVESTIGAÇÃO CONCLUÍDA!")
    print(f"Total de problemas encontrados: {relatorio['resumo']['total_bugs'] + relatorio['resumo']['total_inconsistencias'] + relatorio['resumo']['total_warnings']}")
    print(f"Bugs críticos: {relatorio['resumo']['bugs_por_severidade']['CRÍTICO']}")
    print(f"Bugs altos: {relatorio['resumo']['bugs_por_severidade']['ALTO']}")
    print(f"Relatório salvo em: relatorio_investigacao_wizard.json")
    
    return relatorio

if __name__ == "__main__":
    relatorio = main()