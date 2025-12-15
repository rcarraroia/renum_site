"""
Script de Auditoria Remota do Banco de Dados PostgreSQL (Via Conector Python)
VERSÃO: TENTATIVA DE CONEXAO DIRETA (Porta 5432)
"""
import psycopg2
import sys
import json
import urllib.parse
from datetime import datetime

# Credenciais
DB_PASSWORD = "[REDACTED]"
PROJECT_REF = "[REDACTED]"

def audit_database():
    print("=== INICIANDO AUDITORIA DO BANCO DE DADOS (CONEXAO DIRETA) ===")
    results = {"timestamp": datetime.now().isoformat(), "tables": {}}
    
    try:
        # Tentar conexao DIRETA (bypass pooler)
        # Formato: postgresql://postgres:[password]@db.[ref].supabase.co:5432/postgres
        password = urllib.parse.quote_plus(DB_PASSWORD)
        dsn = f"postgresql://postgres:{password}@db.{PROJECT_REF}.supabase.co:5432/postgres"
        
        print(f"\n[TENTATIVA] Conectando a db.{PROJECT_REF}.supabase.co:5432...")
        
        conn = psycopg2.connect(dsn, connect_timeout=10)
        cur = conn.cursor()
        print("\n[OK] [SUCESSO] Conexao Direta Estabelecida!")
        
        # 1. Listar Tabelas
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = [row[0] for row in cur.fetchall()]
        print(f"\n- Tabelas Encontradas: {len(tables)}")
        print(f"   Lista: {', '.join(tables)}")
        
        # 2. Contar Registros (Amostra de tabelas criticas)
        critical_tables = [
            'clients', 'leads', 'projects', 'agents', 'sub_agents',
            'conversations', 'messages', 'users', 'profiles'
        ]
        
        print("\n- Contagem de Registros:")
        for table in tables:
            # Contar todas para ter certeza
            try:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                count = cur.fetchone()[0]
                marker = "[VAZIO]" if count == 0 else "[OK]"
                print(f"   {marker} {table}: {count}")
                results["tables"][table] = count
            except Exception as e:
                print(f"   [X] Erro em {table}: {e}")
                
        # 3. Verificar RLS
        print("\n- Status RLS:")
        cur.execute("""
            SELECT tablename, rowsecurity 
            FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY tablename;
        """)
        for row in cur.fetchall():
            status = "[ATIVADO]" if row[1] else "[DESATIVADO]"
            print(f"   - {row[0]}: {status}")
            
        cur.close()
        conn.close()
        
        with open("audit_db_final.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        print("\n=== AUDITORIA DE DB CONCLUIDA ===")
            
    except Exception as e:
        print(f"\n[X] ERRO FATAL: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    audit_database()
