#!/usr/bin/env python3
"""
Update RLS Policies for sub_agents
Sprint 06 - Wizard de Criação de Agentes
"""

import psycopg2

def update_rls_policies():
    """Update RLS policies for sub_agents"""
    print("=" * 60)
    print("UPDATING RLS POLICIES FOR sub_agents")
    print("=" * 60)
    
    try:
        conn = psycopg2.connect(
            host='db.vhixvzaxswphwoymdhgg.supabase.co',
            port=5432,
            database='postgres',
            user='postgres',
            password='BD5yEMQ9iDMOkeGW'
        )
        
        cur = conn.cursor()
        
        # Drop old policies
        print("\n🗑️ Dropping old policies...")
        policies_to_drop = [
            "Admins have full access",
            "Public agents are viewable",
            "Admins have full access to sub_agents",
            "Clients can view own agents",
            "Clients can create own agents",
            "Clients can update own agents",
            "Clients can delete own agents"
        ]
        
        for policy in policies_to_drop:
            try:
                cur.execute(f'DROP POLICY IF EXISTS "{policy}" ON sub_agents')
                print(f"  ✅ Dropped: {policy}")
            except Exception as e:
                print(f"  ⚠️ Could not drop {policy}: {e}")
        
        conn.commit()
        
        # Create new policies
        print("\n📝 Creating new policies...")
        
        policies = [
            (
                "Admins have full access to sub_agents",
                """
                CREATE POLICY "Admins have full access to sub_agents"
                    ON sub_agents
                    FOR ALL
                    TO authenticated
                    USING (
                        EXISTS (
                            SELECT 1 FROM profiles
                            WHERE profiles.id = auth.uid()
                            AND profiles.role = 'admin'
                        )
                    )
                """
            ),
            (
                "Authenticated users can view all agents",
                """
                CREATE POLICY "Authenticated users can view all agents"
                    ON sub_agents
                    FOR SELECT
                    TO authenticated
                    USING (true)
                """
            ),
            (
                "Authenticated users can create agents",
                """
                CREATE POLICY "Authenticated users can create agents"
                    ON sub_agents
                    FOR INSERT
                    TO authenticated
                    WITH CHECK (true)
                """
            ),
            (
                "Authenticated users can update agents",
                """
                CREATE POLICY "Authenticated users can update agents"
                    ON sub_agents
                    FOR UPDATE
                    TO authenticated
                    USING (true)
                """
            ),
            (
                "Authenticated users can delete agents",
                """
                CREATE POLICY "Authenticated users can delete agents"
                    ON sub_agents
                    FOR DELETE
                    TO authenticated
                    USING (true)
                """
            ),
            (
                "Public agents are viewable",
                """
                CREATE POLICY "Public agents are viewable"
                    ON sub_agents
                    FOR SELECT
                    TO anon
                    USING (
                        is_public = true 
                        AND status = 'active'
                    )
                """
            )
        ]
        
        for policy_name, policy_sql in policies:
            try:
                cur.execute(policy_sql)
                print(f"  ✅ Created: {policy_name}")
            except Exception as e:
                print(f"  ❌ Failed to create {policy_name}: {e}")
        
        conn.commit()
        
        # Verify policies
        print("\n🔍 Verifying policies...")
        cur.execute("""
            SELECT policyname, cmd
            FROM pg_policies
            WHERE tablename = 'sub_agents'
            ORDER BY policyname
        """)
        
        policies_result = cur.fetchall()
        print(f"\n  Total policies: {len(policies_result)}")
        for policy_name, cmd in policies_result:
            print(f"  - {policy_name} ({cmd})")
        
        cur.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ RLS POLICIES UPDATED SUCCESSFULLY")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = update_rls_policies()
    exit(0 if success else 1)
