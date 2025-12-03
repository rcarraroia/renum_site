"""
Teste direto no banco via PostgreSQL
"""
import psycopg2
from datetime import datetime

# Connection string
DATABASE_URL = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"

GREEN = "✅"
RED = "❌"
YELLOW = "⚠️"

def test_connection():
    """Testa conexão PostgreSQL"""
    print("\n" + "="*70)
    print("🗄️ TESTANDO CONEXÃO DIRETA COM POSTGRESQL")
    print("="*70)

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        print(f"{GREEN} Conexão PostgreSQL estabelecida!")

        return conn, cur
    except Exception as e:
        print(f"{RED} ERRO ao conectar: {str(e)}")
        return None, None

def check_tables(cur):
    """Lista todas as tabelas públicas"""
    print("\n📋 Verificando tabelas existentes...")

    try:
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)

        tables = cur.fetchall()
        print(f"\n{GREEN} Encontradas {len(tables)} tabelas:")

        for table in tables:
            print(f"  - {table[0]}")

        return [t[0] for t in tables]

    except Exception as e:
        print(f"{RED} ERRO ao listar tabelas: {str(e)}")
        return []

def count_records(cur, tables):
    """Conta registros em cada tabela"""
    print("\n📊 Contando registros em cada tabela...")

    counts = {}

    for table in tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {table};")
            count = cur.fetchone()[0]

            status = GREEN if count > 0 else YELLOW
            print(f"{status} {table}: {count} registros")

            counts[table] = count

        except Exception as e:
            print(f"{RED} {table}: ERRO - {str(e)[:50]}")
            counts[table] = -1

    return counts

def check_sample_data(cur):
    """Verifica dados de exemplo"""
    print("\n🔍 Verificando dados de exemplo...")

    # Tentar buscar usuários
    try:
        cur.execute("SELECT id, email, raw_user_meta_data->>'role' as role FROM auth.users LIMIT 5;")
        users = cur.fetchall()

        print(f"\n👥 Usuários cadastrados: {len(users)}")
        for user in users:
            print(f"  - {user[1]} (role: {user[2]})")

    except Exception as e:
        print(f"{RED} ERRO ao buscar usuários: {str(e)[:100]}")

    # Tentar buscar sub-agentes
    try:
        cur.execute("SELECT name, type, is_active FROM sub_agents LIMIT 5;")
        agents = cur.fetchall()

        print(f"\n🤖 Sub-agentes cadastrados: {len(agents)}")
        for agent in agents:
            print(f"  - {agent[0]} (type: {agent[1]}, active: {agent[2]})")

    except Exception as e:
        print(f"{RED} ERRO ao buscar sub-agentes: {str(e)[:100]}")

def main():
    print("\n" + "="*70)
    print("🔍 AUDITORIA DIRETA NO BANCO DE DADOS (PostgreSQL)")
    print("="*70)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

    conn, cur = test_connection()

    if not conn:
        print(f"\n{RED} Não foi possível conectar ao banco. Encerrando.")
        return

    tables = check_tables(cur)
    counts = count_records(cur, tables)
    check_sample_data(cur)

    # Resumo
    print("\n" + "="*70)
    print("📊 RESUMO")
    print("="*70)

    total_tables = len(tables)
    tables_with_data = sum(1 for c in counts.values() if c > 0)
    total_records = sum(c for c in counts.values() if c > 0)

    print(f"\n✅ Total de tabelas: {total_tables}")
    print(f"📊 Tabelas com dados: {tables_with_data}/{total_tables}")
    print(f"📝 Total de registros: {total_records}")

    if tables_with_data >= 5:
        print(f"\n{GREEN} Banco de dados FUNCIONAL e com DADOS")
    elif tables_with_data >= 2:
        print(f"\n{YELLOW} Banco de dados FUNCIONAL mas com POUCOS DADOS")
    else:
        print(f"\n{RED} Banco de dados VAZIO ou com PROBLEMAS")

    cur.close()
    conn.close()

    print("\n" + "="*70)
    print("✅ AUDITORIA CONCLUÍDA")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
