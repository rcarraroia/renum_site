#!/usr/bin/env python3
"""
Script para corrigir roles inválidos dos agentes
Problema: Agentes com role='assistant' causando erro 500 na API
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

def main():
    print("🔧 CORREÇÃO: Roles Inválidos dos Agentes")
    print("=" * 50)
    
    conn_string = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"
    
    try:
        conn = psycopg2.connect(conn_string)
        
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # 1. Verificar agentes atuais
            print("📊 1. VERIFICANDO AGENTES ATUAIS...")
            cursor.execute("SELECT id, name, role FROM agents ORDER BY name")
            agents = cursor.fetchall()
            
            print(f"Total de agentes: {len(agents)}")
            print("\nAgentes encontrados:")
            
            roles_invalidos = []
            for agent in agents:
                print(f"  - {agent['name']}: role='{agent['role']}'")
                if agent['role'] not in ['system_orchestrator', 'system_supervisor', 'client_agent']:
                    roles_invalidos.append(agent)
            
            if not roles_invalidos:
                print("\n✅ Todos os agentes têm roles válidos!")
                return
            
            print(f"\n⚠️ Encontrados {len(roles_invalidos)} agentes com roles inválidos:")
            for agent in roles_invalidos:
                print(f"  - {agent['name']}: '{agent['role']}'")
            
            # 2. Mapear correções
            print("\n🔄 2. MAPEANDO CORREÇÕES...")
            
            correcoes = []
            for agent in roles_invalidos:
                role_atual = agent['role']
                
                # Mapear role baseado no nome e contexto
                if agent['name'] in ['RENUS', 'ISA']:
                    novo_role = 'system_orchestrator'
                elif 'system' in agent['name'].lower() or 'admin' in agent['name'].lower():
                    novo_role = 'system_supervisor'
                else:
                    novo_role = 'client_agent'
                
                correcoes.append({
                    'id': agent['id'],
                    'name': agent['name'],
                    'role_atual': role_atual,
                    'novo_role': novo_role
                })
                
                print(f"  - {agent['name']}: '{role_atual}' → '{novo_role}'")
            
            # 3. Confirmar correções
            print(f"\n❓ Deseja aplicar estas {len(correcoes)} correções? (s/N): ", end="")
            resposta = input().strip().lower()
            
            if resposta != 's':
                print("❌ Operação cancelada pelo usuário")
                return
            
            # 4. Aplicar correções
            print("\n🔧 3. APLICANDO CORREÇÕES...")
            
            for correcao in correcoes:
                cursor.execute("""
                    UPDATE agents 
                    SET role = %s, updated_at = NOW()
                    WHERE id = %s
                """, (correcao['novo_role'], correcao['id']))
                
                print(f"  ✅ {correcao['name']}: {correcao['role_atual']} → {correcao['novo_role']}")
            
            conn.commit()
            
            # 5. Verificar resultado
            print("\n📊 4. VERIFICANDO RESULTADO...")
            cursor.execute("SELECT id, name, role FROM agents ORDER BY name")
            agents_atualizados = cursor.fetchall()
            
            roles_ainda_invalidos = []
            for agent in agents_atualizados:
                if agent['role'] not in ['system_orchestrator', 'system_supervisor', 'client_agent']:
                    roles_ainda_invalidos.append(agent)
            
            if roles_ainda_invalidos:
                print(f"❌ Ainda há {len(roles_ainda_invalidos)} agentes com roles inválidos:")
                for agent in roles_ainda_invalidos:
                    print(f"  - {agent['name']}: '{agent['role']}'")
            else:
                print("✅ Todos os agentes agora têm roles válidos!")
            
            print(f"\n🎉 CORREÇÃO CONCLUÍDA!")
            print(f"✅ {len(correcoes)} agentes corrigidos")
            print("✅ API /api/agents/ deve funcionar agora")
            
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)