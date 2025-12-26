#!/usr/bin/env python3
"""
AUDITORIA COMPLETA: Sistema de Configuração de Agentes
Conecta ao Supabase REAL para analisar estrutura e dados atuais
"""

import os
import sys
import json
import psycopg2
from datetime import datetime
from typing import Dict, List, Any, Optional

# Adicionar path do backend para imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend', 'src'))

class SupabaseAuditor:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.audit_results = {
            'timestamp': datetime.now().isoformat(),
            'database_info': {},
            'tables_analysis': {},
            'agents_analysis': {},
            'config_structure': {},
            'relationships': {},
            'data_samples': {},
            'issues_found': []
        }
    
    def connect_to_supabase(self):
        """Conecta ao Supabase usando credenciais do arquivo de configuração"""
        try:
            # Tentar ler credenciais do arquivo de documentação
            credentials_file = os.path.join(os.path.dirname(__file__), '..', 'docs', 'SUPABASE_CREDENTIALS.md')
            
            if os.path.exists(credentials_file):
                with open(credentials_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Extrair informações das credenciais
                lines = content.split('\n')
                db_password = None
                db_host = None
                
                for line in lines:
                    if 'BD5yEMQ9iDMOkeGW' in line:
                        db_password = 'BD5yEMQ9iDMOkeGW'
                    if 'db.vhixvzaxswphwoymdhgg.supabase.co' in line:
                        db_host = 'db.vhixvzaxswphwoymdhgg.supabase.co'
                
                if db_password and db_host:
                    connection_string = f"postgresql://postgres:{db_password}@{db_host}:5432/postgres"
                    print(f"🔌 Conectando ao Supabase: {db_host}")
                    
                    self.connection = psycopg2.connect(connection_string)
                    self.cursor = self.connection.cursor()
                    
                    # Testar conexão
                    self.cursor.execute("SELECT version();")
                    version = self.cursor.fetchone()[0]
                    print(f"✅ Conectado com sucesso! PostgreSQL: {version}")
                    
                    return True
                else:
                    print("❌ Credenciais não encontradas no arquivo")
                    return False
            else:
                print("❌ Arquivo de credenciais não encontrado")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            return False
    
    def get_database_info(self):
        """Coleta informações gerais do banco de dados"""
        print("\n📊 Coletando informações do banco de dados...")
        
        try:
            # Versão do PostgreSQL
            self.cursor.execute("SELECT version();")
            version = self.cursor.fetchone()[0]
            
            # Tamanho do banco
            self.cursor.execute("SELECT pg_size_pretty(pg_database_size(current_database()));")
            db_size = self.cursor.fetchone()[0]
            
            # Número de conexões ativas
            self.cursor.execute("SELECT count(*) FROM pg_stat_activity WHERE state = 'active';")
            active_connections = self.cursor.fetchone()[0]
            
            self.audit_results['database_info'] = {
                'version': version,
                'size': db_size,
                'active_connections': active_connections,
                'current_database': 'postgres',
                'current_schema': 'public'
            }
            
            print(f"   📋 Versão: {version}")
            print(f"   💾 Tamanho: {db_size}")
            print(f"   🔗 Conexões ativas: {active_connections}")
            
        except Exception as e:
            print(f"❌ Erro ao coletar info do banco: {e}")
            self.audit_results['issues_found'].append(f"Erro ao coletar info do banco: {e}")
    
    def analyze_tables_structure(self):
        """Analisa estrutura de todas as tabelas relacionadas a agentes"""
        print("\n🗂️ Analisando estrutura das tabelas...")
        
        # Tabelas relacionadas ao sistema de agentes
        agent_tables = [
            'agents', 'sub_agents', 'tools', 'integrations', 
            'memory_chunks', 'learning_logs', 'behavior_patterns',
            'sicc_settings', 'agent_metrics', 'agent_snapshots',
            'triggers', 'renus_config', 'profiles', 'clients'
        ]
        
        for table_name in agent_tables:
            try:
                print(f"   🔍 Analisando tabela: {table_name}")
                
                # Verificar se tabela existe
                self.cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = %s
                    );
                """, (table_name,))
                
                table_exists = self.cursor.fetchone()[0]
                
                if not table_exists:
                    print(f"      ⚠️ Tabela {table_name} NÃO EXISTE")
                    self.audit_results['tables_analysis'][table_name] = {
                        'exists': False,
                        'reason': 'Tabela não encontrada no banco'
                    }
                    continue
                
                # Estrutura da tabela
                self.cursor.execute("""
                    SELECT 
                        column_name, 
                        data_type, 
                        is_nullable,
                        column_default,
                        character_maximum_length
                    FROM information_schema.columns 
                    WHERE table_name = %s 
                    ORDER BY ordinal_position;
                """, (table_name,))
                
                columns = self.cursor.fetchall()
                
                # Contar registros
                self.cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                record_count = self.cursor.fetchone()[0]
                
                # Verificar índices
                self.cursor.execute("""
                    SELECT indexname, indexdef 
                    FROM pg_indexes 
                    WHERE tablename = %s;
                """, (table_name,))
                
                indexes = self.cursor.fetchall()
                
                # Verificar RLS
                self.cursor.execute("""
                    SELECT rowsecurity 
                    FROM pg_tables 
                    WHERE tablename = %s;
                """, (table_name,))
                
                rls_result = self.cursor.fetchone()
                rls_enabled = rls_result[0] if rls_result else False
                
                # Verificar políticas RLS
                self.cursor.execute("""
                    SELECT policyname, cmd, qual 
                    FROM pg_policies 
                    WHERE tablename = %s;
                """, (table_name,))
                
                policies = self.cursor.fetchall()
                
                self.audit_results['tables_analysis'][table_name] = {
                    'exists': True,
                    'columns': [
                        {
                            'name': col[0],
                            'type': col[1],
                            'nullable': col[2],
                            'default': col[3],
                            'max_length': col[4]
                        } for col in columns
                    ],
                    'record_count': record_count,
                    'indexes': [{'name': idx[0], 'definition': idx[1]} for idx in indexes],
                    'rls_enabled': rls_enabled,
                    'policies': [{'name': pol[0], 'command': pol[1], 'condition': pol[2]} for pol in policies]
                }
                
                print(f"      ✅ {len(columns)} colunas, {record_count} registros, RLS: {rls_enabled}")
                
            except Exception as e:
                print(f"      ❌ Erro ao analisar {table_name}: {e}")
                self.audit_results['issues_found'].append(f"Erro ao analisar tabela {table_name}: {e}")
    
    def analyze_agents_data(self):
        """Analisa dados específicos dos agentes"""
        print("\n🤖 Analisando dados dos agentes...")
        
        try:
            # Verificar se tabela agents existe
            if 'agents' not in self.audit_results['tables_analysis'] or not self.audit_results['tables_analysis']['agents']['exists']:
                print("   ⚠️ Tabela 'agents' não existe - pulando análise")
                return
            
            # Listar todos os agentes
            self.cursor.execute("""
                SELECT id, name, slug, role, status, created_at, config
                FROM agents 
                ORDER BY created_at;
            """)
            
            agents = self.cursor.fetchall()
            
            agents_analysis = []
            
            for agent in agents:
                agent_id, name, slug, role, status, created_at, config = agent
                
                print(f"   🔍 Agente: {name} ({slug})")
                
                # Analisar estrutura do config
                config_structure = {}
                if config:
                    try:
                        if isinstance(config, str):
                            config_data = json.loads(config)
                        else:
                            config_data = config
                        
                        config_structure = self.analyze_config_structure(config_data)
                    except Exception as e:
                        config_structure = {'error': f'Erro ao parsear config: {e}'}
                
                # Contar sub-agentes (se tabela existir)
                sub_agents_count = 0
                if 'sub_agents' in self.audit_results['tables_analysis'] and self.audit_results['tables_analysis']['sub_agents']['exists']:
                    self.cursor.execute("SELECT COUNT(*) FROM sub_agents WHERE parent_agent_id = %s;", (agent_id,))
                    sub_agents_count = self.cursor.fetchone()[0]
                
                agent_analysis = {
                    'id': agent_id,
                    'name': name,
                    'slug': slug,
                    'role': role,
                    'status': status,
                    'created_at': created_at.isoformat() if created_at else None,
                    'config_structure': config_structure,
                    'sub_agents_count': sub_agents_count
                }
                
                agents_analysis.append(agent_analysis)
                
                print(f"      📊 Role: {role}, Status: {status}, Sub-agentes: {sub_agents_count}")
            
            self.audit_results['agents_analysis'] = {
                'total_agents': len(agents),
                'agents': agents_analysis
            }
            
            print(f"   📈 Total de agentes encontrados: {len(agents)}")
            
        except Exception as e:
            print(f"❌ Erro ao analisar dados dos agentes: {e}")
            self.audit_results['issues_found'].append(f"Erro ao analisar dados dos agentes: {e}")
    
    def analyze_config_structure(self, config_data: Dict) -> Dict:
        """Analisa a estrutura do campo config dos agentes"""
        structure = {
            'has_identity': 'identity' in config_data,
            'has_sicc': 'sicc' in config_data,
            'has_tools': 'tools' in config_data,
            'has_integrations': 'integrations' in config_data,
            'has_guardrails': 'guardrails' in config_data,
            'has_triggers': 'triggers' in config_data,
            'top_level_keys': list(config_data.keys())
        }
        
        # Analisar seções específicas
        if 'identity' in config_data:
            identity = config_data['identity']
            structure['identity_keys'] = list(identity.keys()) if isinstance(identity, dict) else []
        
        if 'sicc' in config_data:
            sicc = config_data['sicc']
            structure['sicc_keys'] = list(sicc.keys()) if isinstance(sicc, dict) else []
        
        if 'tools' in config_data:
            tools = config_data['tools']
            structure['tools_count'] = len(tools) if isinstance(tools, list) else 0
            structure['tools_type'] = type(tools).__name__
        
        return structure
    
    def analyze_relationships(self):
        """Analisa relacionamentos entre tabelas"""
        print("\n🔗 Analisando relacionamentos entre tabelas...")
        
        try:
            # Buscar foreign keys
            self.cursor.execute("""
                SELECT
                    tc.table_name,
                    kcu.column_name,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                    AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                    AND ccu.table_schema = tc.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY'
                    AND tc.table_schema = 'public'
                ORDER BY tc.table_name, kcu.column_name;
            """)
            
            foreign_keys = self.cursor.fetchall()
            
            relationships = []
            for fk in foreign_keys:
                table, column, ref_table, ref_column = fk
                relationships.append({
                    'from_table': table,
                    'from_column': column,
                    'to_table': ref_table,
                    'to_column': ref_column
                })
                print(f"   🔗 {table}.{column} → {ref_table}.{ref_column}")
            
            self.audit_results['relationships'] = {
                'foreign_keys': relationships,
                'total_relationships': len(relationships)
            }
            
        except Exception as e:
            print(f"❌ Erro ao analisar relacionamentos: {e}")
            self.audit_results['issues_found'].append(f"Erro ao analisar relacionamentos: {e}")
    
    def collect_data_samples(self):
        """Coleta amostras de dados para análise"""
        print("\n📋 Coletando amostras de dados...")
        
        sample_queries = {
            'agents_sample': "SELECT id, name, slug, role, status FROM agents LIMIT 5;",
            'config_samples': "SELECT name, config FROM agents WHERE config IS NOT NULL LIMIT 3;",
        }
        
        # Adicionar queries condicionais baseadas em tabelas existentes
        if 'sub_agents' in self.audit_results['tables_analysis'] and self.audit_results['tables_analysis']['sub_agents']['exists']:
            sample_queries['sub_agents_sample'] = "SELECT id, name, parent_agent_id FROM sub_agents LIMIT 5;"
        
        if 'tools' in self.audit_results['tables_analysis'] and self.audit_results['tables_analysis']['tools']['exists']:
            sample_queries['tools_sample'] = "SELECT id, name, function_name FROM tools LIMIT 5;"
        
        for query_name, query in sample_queries.items():
            try:
                self.cursor.execute(query)
                results = self.cursor.fetchall()
                
                # Converter para formato serializável
                serializable_results = []
                for row in results:
                    serializable_row = []
                    for item in row:
                        if isinstance(item, datetime):
                            serializable_row.append(item.isoformat())
                        else:
                            serializable_row.append(item)
                    serializable_results.append(serializable_row)
                
                self.audit_results['data_samples'][query_name] = serializable_results
                print(f"   📊 {query_name}: {len(results)} registros")
                
            except Exception as e:
                print(f"   ❌ Erro em {query_name}: {e}")
                self.audit_results['issues_found'].append(f"Erro em query {query_name}: {e}")
    
    def generate_report(self):
        """Gera relatório completo da auditoria"""
        print("\n📄 Gerando relatório da auditoria...")
        
        # Salvar resultados em JSON
        json_file = f"docs/auditorias/AUDITORIA_BANCO_CONFIG_AGENTES_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.audit_results, f, indent=2, ensure_ascii=False, default=str)
        
        # Gerar relatório em Markdown
        md_file = f"docs/auditorias/AUDITORIA_COMPLETA_CONFIG_AGENTES.md"
        
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(self.generate_markdown_report())
        
        print(f"✅ Relatórios salvos:")
        print(f"   📊 JSON: {json_file}")
        print(f"   📝 Markdown: {md_file}")
        
        return md_file, json_file
    
    def generate_markdown_report(self) -> str:
        """Gera relatório em formato Markdown"""
        report = f"""# AUDITORIA COMPLETA: Sistema de Configuração de Agentes

**Data da Auditoria:** {self.audit_results['timestamp']}  
**Banco de Dados:** Supabase PostgreSQL  
**Método:** Conexão direta ao banco real  

---

## 📊 RESUMO EXECUTIVO

### Estado do Banco de Dados
- **Versão:** {self.audit_results['database_info'].get('version', 'N/A')}
- **Tamanho:** {self.audit_results['database_info'].get('size', 'N/A')}
- **Conexões Ativas:** {self.audit_results['database_info'].get('active_connections', 'N/A')}

### Tabelas Analisadas
"""
        
        # Estatísticas das tabelas
        total_tables = len(self.audit_results['tables_analysis'])
        existing_tables = sum(1 for t in self.audit_results['tables_analysis'].values() if t.get('exists', False))
        missing_tables = total_tables - existing_tables
        
        report += f"""
- **Total de tabelas verificadas:** {total_tables}
- **Tabelas existentes:** {existing_tables}
- **Tabelas ausentes:** {missing_tables}

### Agentes Encontrados
- **Total de agentes:** {self.audit_results['agents_analysis'].get('total_agents', 0)}

---

## 🗂️ ANÁLISE DETALHADA DAS TABELAS

"""
        
        for table_name, table_info in self.audit_results['tables_analysis'].items():
            if table_info.get('exists', False):
                report += f"""
### Tabela: `{table_name}`
- **Status:** ✅ Existe
- **Registros:** {table_info.get('record_count', 0)}
- **Colunas:** {len(table_info.get('columns', []))}
- **RLS Habilitado:** {'✅ Sim' if table_info.get('rls_enabled') else '❌ Não'}
- **Políticas RLS:** {len(table_info.get('policies', []))}
- **Índices:** {len(table_info.get('indexes', []))}

#### Estrutura das Colunas
| Nome | Tipo | Nullable | Default |
|------|------|----------|---------|
"""
                for col in table_info.get('columns', []):
                    nullable = '✅' if col['nullable'] == 'YES' else '❌'
                    default = col['default'] or '-'
                    report += f"| {col['name']} | {col['type']} | {nullable} | {default} |\n"
                
                if table_info.get('policies'):
                    report += f"\n#### Políticas RLS\n"
                    for policy in table_info['policies']:
                        report += f"- **{policy['name']}:** {policy['command']}\n"
            else:
                report += f"""
### Tabela: `{table_name}`
- **Status:** ❌ NÃO EXISTE
- **Motivo:** {table_info.get('reason', 'Tabela não encontrada')}
"""
        
        # Análise dos agentes
        report += f"""
---

## 🤖 ANÁLISE DOS AGENTES

"""
        
        if self.audit_results['agents_analysis'].get('agents'):
            for agent in self.audit_results['agents_analysis']['agents']:
                report += f"""
### Agente: {agent['name']} (`{agent['slug']}`)
- **ID:** {agent['id']}
- **Role:** {agent['role']}
- **Status:** {agent['status']}
- **Criado em:** {agent['created_at']}
- **Sub-agentes:** {agent['sub_agents_count']}

#### Estrutura do Config
"""
                config = agent.get('config_structure', {})
                for key, value in config.items():
                    if isinstance(value, bool):
                        status = '✅' if value else '❌'
                        report += f"- **{key}:** {status}\n"
                    elif isinstance(value, list):
                        report += f"- **{key}:** {value}\n"
                    else:
                        report += f"- **{key}:** {value}\n"
        else:
            report += "❌ Nenhum agente encontrado ou erro ao acessar dados.\n"
        
        # Relacionamentos
        report += f"""
---

## 🔗 RELACIONAMENTOS ENTRE TABELAS

"""
        
        if self.audit_results['relationships'].get('foreign_keys'):
            report += "| Tabela Origem | Coluna | Tabela Destino | Coluna Destino |\n"
            report += "|---------------|--------|----------------|----------------|\n"
            
            for rel in self.audit_results['relationships']['foreign_keys']:
                report += f"| {rel['from_table']} | {rel['from_column']} | {rel['to_table']} | {rel['to_column']} |\n"
        else:
            report += "❌ Nenhum relacionamento encontrado ou erro ao analisar.\n"
        
        # Problemas encontrados
        if self.audit_results['issues_found']:
            report += f"""
---

## ⚠️ PROBLEMAS IDENTIFICADOS

"""
            for i, issue in enumerate(self.audit_results['issues_found'], 1):
                report += f"{i}. {issue}\n"
        
        # Amostras de dados
        report += f"""
---

## 📋 AMOSTRAS DE DADOS

"""
        
        for sample_name, sample_data in self.audit_results['data_samples'].items():
            report += f"""
### {sample_name}
```
{sample_data}
```
"""
        
        report += f"""
---

## 🎯 CONCLUSÕES E RECOMENDAÇÕES

### Estado Geral
- Banco de dados {'✅ acessível' if self.connection else '❌ inacessível'}
- Estrutura {'✅ parcialmente implementada' if existing_tables > 0 else '❌ não implementada'}

### Próximos Passos
1. Corrigir tabelas ausentes identificadas
2. Implementar políticas RLS faltantes
3. Verificar integridade dos dados de configuração
4. Validar relacionamentos entre agentes e sub-agentes

---

**Auditoria realizada em:** {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}  
**Ferramenta:** Script Python com conexão direta ao Supabase  
"""
        
        return report
    
    def close_connection(self):
        """Fecha conexão com o banco"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("🔌 Conexão fechada")

def main():
    """Função principal"""
    print("🔍 AUDITORIA COMPLETA: Sistema de Configuração de Agentes")
    print("=" * 60)
    
    auditor = SupabaseAuditor()
    
    try:
        # Conectar ao banco
        if not auditor.connect_to_supabase():
            print("❌ Falha na conexão. Abortando auditoria.")
            return
        
        # Executar análises
        auditor.get_database_info()
        auditor.analyze_tables_structure()
        auditor.analyze_agents_data()
        auditor.analyze_relationships()
        auditor.collect_data_samples()
        
        # Gerar relatórios
        md_file, json_file = auditor.generate_report()
        
        print("\n" + "=" * 60)
        print("✅ AUDITORIA CONCLUÍDA COM SUCESSO!")
        print(f"📝 Relatório principal: {md_file}")
        print(f"📊 Dados completos: {json_file}")
        
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO na auditoria: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        auditor.close_connection()

if __name__ == "__main__":
    main()