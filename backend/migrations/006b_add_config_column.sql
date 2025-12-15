-- Migration 006b: Add config JSONB column to sub_agents
-- Sprint 06 - Wizard de Criação de Agentes
-- Date: 2025-12-04
-- Purpose: Store wizard session data and agent configuration

-- Add config column for storing wizard data and agent settings
ALTER TABLE sub_agents
ADD COLUMN IF NOT EXISTS config JSONB DEFAULT '{}'::jsonb;

-- Create GIN index for JSONB queries
CREATE INDEX IF NOT EXISTS idx_sub_agents_config ON sub_agents USING GIN (config);

-- Add comment
COMMENT ON COLUMN sub_agents.config IS 'Agent configuration and wizard session data (JSONB)';

-- Verify
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'sub_agents'
AND column_name = 'config';
