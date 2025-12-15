-- Migration 006: Add Wizard Fields to sub_agents
-- Sprint 06 - Wizard de Criação de Agentes
-- Date: 2025-12-04

-- ============================================================
-- STEP 1: Add new columns
-- ============================================================

-- Add client_id column (links agent to client for multi-tenant)
ALTER TABLE sub_agents
ADD COLUMN client_id UUID REFERENCES clients(id) ON DELETE CASCADE;

-- Add template_type column (identifies which template was used)
ALTER TABLE sub_agents
ADD COLUMN template_type VARCHAR(50) CHECK (template_type IN (
    'customer_service',
    'sales',
    'support',
    'recruitment',
    'custom'
));

-- Add status column (draft, active, paused, inactive)
ALTER TABLE sub_agents
ADD COLUMN status VARCHAR(20) DEFAULT 'draft' CHECK (status IN (
    'draft',
    'active',
    'paused',
    'inactive'
));

-- ============================================================
-- STEP 2: Create indexes for performance
-- ============================================================

CREATE INDEX idx_sub_agents_client_id ON sub_agents(client_id);
CREATE INDEX idx_sub_agents_status ON sub_agents(status);
CREATE INDEX idx_sub_agents_template_type ON sub_agents(template_type);
CREATE INDEX idx_sub_agents_slug ON sub_agents(slug);

-- Composite index for common queries
CREATE INDEX idx_sub_agents_client_status ON sub_agents(client_id, status);

-- ============================================================
-- STEP 3: Update existing data (if any)
-- ============================================================

-- Set default values for existing records
-- Note: client_id will need to be set manually or via script
-- since we don't know which client owns existing agents

UPDATE sub_agents
SET status = CASE
    WHEN is_active = true THEN 'active'
    ELSE 'inactive'
END
WHERE status IS NULL;

UPDATE sub_agents
SET template_type = 'custom'
WHERE template_type IS NULL;

-- ============================================================
-- STEP 4: Make client_id NOT NULL after data migration
-- ============================================================

-- Uncomment after setting client_id for all existing records
-- ALTER TABLE sub_agents
-- ALTER COLUMN client_id SET NOT NULL;

-- ============================================================
-- STEP 5: Update RLS policies
-- ============================================================

-- Drop old policies (if they exist)
DROP POLICY IF EXISTS "Admins have full access" ON sub_agents;
DROP POLICY IF EXISTS "Public agents are viewable" ON sub_agents;

-- Policy: Admins have full access
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
    );

-- Policy: Clients can view their own agents
CREATE POLICY "Clients can view own agents"
    ON sub_agents
    FOR SELECT
    TO authenticated
    USING (
        client_id IN (
            SELECT id FROM clients WHERE profile_id = auth.uid()
        )
    );

-- Policy: Clients can create their own agents
CREATE POLICY "Clients can create own agents"
    ON sub_agents
    FOR INSERT
    TO authenticated
    WITH CHECK (
        client_id IN (
            SELECT id FROM clients WHERE profile_id = auth.uid()
        )
    );

-- Policy: Clients can update their own agents
CREATE POLICY "Clients can update own agents"
    ON sub_agents
    FOR UPDATE
    TO authenticated
    USING (
        client_id IN (
            SELECT id FROM clients WHERE profile_id = auth.uid()
        )
    );

-- Policy: Clients can delete their own agents
CREATE POLICY "Clients can delete own agents"
    ON sub_agents
    FOR DELETE
    TO authenticated
    USING (
        client_id IN (
            SELECT id FROM clients WHERE profile_id = auth.uid()
        )
    );

-- Policy: Public agents are viewable by anyone (for public chat)
CREATE POLICY "Public agents are viewable"
    ON sub_agents
    FOR SELECT
    TO anon
    USING (
        is_public = true 
        AND status = 'active'
    );

-- ============================================================
-- STEP 6: Add helpful comments
-- ============================================================

COMMENT ON COLUMN sub_agents.client_id IS 'Client that owns this agent (multi-tenant)';
COMMENT ON COLUMN sub_agents.template_type IS 'Template used to create agent (customer_service, sales, support, recruitment, custom)';
COMMENT ON COLUMN sub_agents.status IS 'Agent status (draft, active, paused, inactive)';

-- ============================================================
-- ROLLBACK SCRIPT (if needed)
-- ============================================================

-- To rollback this migration, run:
/*
DROP POLICY IF EXISTS "Admins have full access to sub_agents" ON sub_agents;
DROP POLICY IF EXISTS "Clients can view own agents" ON sub_agents;
DROP POLICY IF EXISTS "Clients can create own agents" ON sub_agents;
DROP POLICY IF EXISTS "Clients can update own agents" ON sub_agents;
DROP POLICY IF EXISTS "Clients can delete own agents" ON sub_agents;
DROP POLICY IF EXISTS "Public agents are viewable" ON sub_agents;

DROP INDEX IF EXISTS idx_sub_agents_client_id;
DROP INDEX IF EXISTS idx_sub_agents_status;
DROP INDEX IF EXISTS idx_sub_agents_template_type;
DROP INDEX IF EXISTS idx_sub_agents_slug;
DROP INDEX IF EXISTS idx_sub_agents_client_status;

ALTER TABLE sub_agents DROP COLUMN IF EXISTS client_id;
ALTER TABLE sub_agents DROP COLUMN IF EXISTS template_type;
ALTER TABLE sub_agents DROP COLUMN IF EXISTS status;
*/

-- ============================================================
-- VERIFICATION QUERIES
-- ============================================================

-- Verify columns were added
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'sub_agents'
AND column_name IN ('client_id', 'template_type', 'status')
ORDER BY column_name;

-- Verify indexes were created
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'sub_agents'
AND indexname LIKE 'idx_sub_agents_%'
ORDER BY indexname;

-- Verify RLS policies
SELECT policyname, cmd, qual
FROM pg_policies
WHERE tablename = 'sub_agents'
ORDER BY policyname;

-- Count agents by status
SELECT status, COUNT(*) as count
FROM sub_agents
GROUP BY status
ORDER BY status;
