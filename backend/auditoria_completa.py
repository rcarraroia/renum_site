"""
🔍 AUDITORIA COMPLETA DO SISTEMA RENUM
Auditoria direta no Supabase + Verificação de código
"""
import json
from datetime import datetime
from supabase import create_client, Client

# Configurações
SUPABASE_URL = "https://vhixvzaxswphwoymdhgg.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"

# Cores
GREEN = "✅"
YELLOW = "⚠️"
RED = "❌"
CLOCK = "⏳"

class SystemAuditor:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "database": {},
            "backend": {"status": "NOT_RUNNING", "reason": "Cryptography dependency conflict"},
            "summary": {}
        }
        self.supabase: Client = None

    def log(self, message: str, status: str = ""):
        """Log com timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {status} {message}")

    def test_database_connection(self):
        """Testa conexão com Supabase"""
        self.log("\n" + "="*70)
        self.log("🗄️ PARTE 1: TESTANDO BANCO DE DADOS SUPABASE")
        self.log("="*70)

        try:
            self.supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
            self.log("Conexão com Supabase estabelecida", GREEN)
            self.results["database"]["connection"] = "SUCCESS"
            return True
        except Exception as e:
            self.log(f"ERRO ao conectar com Supabase: {str(e)}", RED)
            self.results["database"]["connection"] = f"FAILED: {str(e)}"
            return False

    def check_table_structure(self):
        """Verifica estrutura das tabelas"""
        self.log("\n📋 Verificando estrutura das tabelas...")

        tables = [
            "profiles", "clients", "leads", "projects",
            "conversations", "messages", "interviews", "interview_messages",
            "renus_config", "tools", "sub_agents", "isa_commands"
        ]

        table_status = {}

        for table in tables:
            try:
                # Tenta fazer uma query simples para verificar se a tabela existe
                result = self.supabase.table(table).select("count", count="exact").limit(0).execute()
                count = result.count if hasattr(result, 'count') else 0
                self.log(f"  Tabela '{table}': {count} registros", GREEN)
                table_status[table] = {"exists": True, "count": count}
            except Exception as e:
                self.log(f"  Tabela '{table}': ERRO - {str(e)[:50]}", RED)
                table_status[table] = {"exists": False, "error": str(e)[:100]}

        self.results["database"]["tables"] = table_status

    def check_auth_data(self):
        """Verifica dados de autenticação"""
        self.log("\n🔐 Verificando dados de autenticação...")

        try:
            # Buscar profiles (usuários)
            result = self.supabase.table("profiles").select("*").limit(5).execute()
            users = result.data if result.data else []

            self.log(f"  Total de usuários (profiles): {len(users)}", GREEN if len(users) > 0 else YELLOW)

            if len(users) > 0:
                self.log(f"  Exemplo de usuário: {users[0].get('email', 'N/A')}", GREEN)

            self.results["database"]["auth"] = {
                "total_users": len(users),
                "has_users": len(users) > 0,
                "sample_emails": [u.get("email") for u in users[:3]]
            }

        except Exception as e:
            self.log(f"  ERRO ao verificar profiles: {str(e)}", RED)
            self.results["database"]["auth"] = {"error": str(e)[:100]}

    def check_clients_data(self):
        """Verifica dados de clientes"""
        self.log("\n👥 Verificando dados de clientes...")

        try:
            result = self.supabase.table("clients").select("*").limit(10).execute()
            clients = result.data if result.data else []

            self.log(f"  Total de clientes: {len(clients)}", GREEN if len(clients) > 0 else YELLOW)

            if len(clients) > 0:
                self.log(f"  Exemplo: {clients[0].get('company_name', 'N/A')}", GREEN)

            self.results["database"]["clients"] = {
                "total": len(clients),
                "has_data": len(clients) > 0
            }

        except Exception as e:
            self.log(f"  ERRO ao verificar clients: {str(e)}", RED)
            self.results["database"]["clients"] = {"error": str(e)[:100]}

    def check_leads_data(self):
        """Verifica dados de leads"""
        self.log("\n📞 Verificando dados de leads...")

        try:
            result = self.supabase.table("leads").select("*").limit(10).execute()
            leads = result.data if result.data else []

            self.log(f"  Total de leads: {len(leads)}", GREEN if len(leads) > 0 else YELLOW)

            self.results["database"]["leads"] = {
                "total": len(leads),
                "has_data": len(leads) > 0
            }

        except Exception as e:
            self.log(f"  ERRO ao verificar leads: {str(e)}", RED)
            self.results["database"]["leads"] = {"error": str(e)[:100]}

    def check_projects_data(self):
        """Verifica dados de projetos"""
        self.log("\n📁 Verificando dados de projetos...")

        try:
            result = self.supabase.table("projects").select("*").limit(10).execute()
            projects = result.data if result.data else []

            self.log(f"  Total de projetos: {len(projects)}", GREEN if len(projects) > 0 else YELLOW)

            self.results["database"]["projects"] = {
                "total": len(projects),
                "has_data": len(projects) > 0
            }

        except Exception as e:
            self.log(f"  ERRO ao verificar projects: {str(e)}", RED)
            self.results["database"]["projects"] = {"error": str(e)[:100]}

    def check_conversations_data(self):
        """Verifica dados de conversas"""
        self.log("\n💬 Verificando dados de conversas...")

        try:
            result = self.supabase.table("conversations").select("*").limit(10).execute()
            conversations = result.data if result.data else []

            self.log(f"  Total de conversas: {len(conversations)}", GREEN if len(conversations) > 0 else YELLOW)

            self.results["database"]["conversations"] = {
                "total": len(conversations),
                "has_data": len(conversations) > 0
            }

        except Exception as e:
            self.log(f"  ERRO ao verificar conversations: {str(e)}", RED)
            self.results["database"]["conversations"] = {"error": str(e)[:100]}

    def check_interviews_data(self):
        """Verifica dados de entrevistas"""
        self.log("\n📋 Verificando dados de entrevistas...")

        try:
            result = self.supabase.table("interviews").select("*").limit(10).execute()
            interviews = result.data if result.data else []

            self.log(f"  Total de entrevistas: {len(interviews)}", GREEN if len(interviews) > 0 else YELLOW)

            self.results["database"]["interviews"] = {
                "total": len(interviews),
                "has_data": len(interviews) > 0
            }

        except Exception as e:
            self.log(f"  ERRO ao verificar interviews: {str(e)}", RED)
            self.results["database"]["interviews"] = {"error": str(e)[:100]}

    def check_sub_agents_data(self):
        """Verifica dados de sub-agentes"""
        self.log("\n🤖 Verificando dados de sub-agentes...")

        try:
            result = self.supabase.table("sub_agents").select("*").limit(10).execute()
            sub_agents = result.data if result.data else []

            self.log(f"  Total de sub-agentes: {len(sub_agents)}", GREEN if len(sub_agents) > 0 else YELLOW)

            if len(sub_agents) > 0:
                for agent in sub_agents[:3]:
                    self.log(f"    - {agent.get('name', 'N/A')} ({agent.get('type', 'N/A')})", GREEN)

            self.results["database"]["sub_agents"] = {
                "total": len(sub_agents),
                "has_data": len(sub_agents) > 0,
                "agents": [{"name": a.get("name"), "type": a.get("type")} for a in sub_agents[:5]]
            }

        except Exception as e:
            self.log(f"  ERRO ao verificar sub_agents: {str(e)}", RED)
            self.results["database"]["sub_agents"] = {"error": str(e)[:100]}

    def generate_summary(self):
        """Gera resumo da auditoria"""
        self.log("\n" + "="*70)
        self.log("📊 RESUMO DA AUDITORIA - PARTE 1 (BANCO DE DADOS)")
        self.log("="*70)

        # Contar tabelas com dados
        db_data = self.results["database"]
        tables_with_data = 0
        tables_checked = 0

        for key, value in db_data.items():
            if isinstance(value, dict) and "has_data" in value:
                tables_checked += 1
                if value["has_data"]:
                    tables_with_data += 1

        self.log(f"\n✅ Conexão com Supabase: {db_data.get('connection', 'N/A')}")
        self.log(f"📊 Tabelas com dados: {tables_with_data}/{tables_checked}")

        if "auth" in db_data and isinstance(db_data["auth"], dict):
            total_users = db_data["auth"].get("total_users", 0)
            self.log(f"👥 Usuários cadastrados: {total_users}")

        # Status geral do banco
        if db_data.get("connection") == "SUCCESS" and tables_with_data >= 3:
            status = f"{GREEN} Banco de dados FUNCIONAL"
        elif db_data.get("connection") == "SUCCESS":
            status = f"{YELLOW} Banco conectado mas com POUCOS dados"
        else:
            status = f"{RED} Banco de dados COM PROBLEMAS"

        self.log(f"\n🎯 Status Geral do Banco: {status}")

        self.results["summary"]["database_status"] = status
        self.results["summary"]["tables_with_data"] = f"{tables_with_data}/{tables_checked}"

    def run_database_audit(self):
        """Executa auditoria completa do banco de dados"""
        if not self.test_database_connection():
            return

        self.check_table_structure()
        self.check_auth_data()
        self.check_clients_data()
        self.check_leads_data()
        self.check_projects_data()
        self.check_conversations_data()
        self.check_interviews_data()
        self.check_sub_agents_data()
        self.generate_summary()

    def save_results(self):
        """Salva resultados em JSON"""
        with open("AUDITORIA_BANCO_DADOS.json", "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        self.log(f"\n{GREEN} Resultados salvos em: AUDITORIA_BANCO_DADOS.json")


def main():
    print("\n" + "="*70)
    print("🔍 AUDITORIA COMPLETA DO SISTEMA RENUM - FASE 1")
    print("="*70)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

    auditor = SystemAuditor()
    auditor.run_database_audit()
    auditor.save_results()

    print("\n" + "="*70)
    print("✅ AUDITORIA DA PARTE 1 (BANCO DE DADOS) CONCLUÍDA")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
