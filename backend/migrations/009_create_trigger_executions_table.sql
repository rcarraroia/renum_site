-- Migration 009: Create trigger_executions table
-- Sprint 07A - Integrações Core
-- Created: 2025-12-04

-- Create trigger_executions table for audit log of trigger executions
CREATE TABLE IF NOT EXISTS trigger_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trigger_id UUID NOT NULL REFERENCES triggers(id) ON DELETE CASCADE,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    condition_met BOOLEAN NOT NULL,
    action_executed BOOLEAN NOT NULL,
    
    result JSONB DEFAULT '{}'::jsonb,
    error_message TEXT,
    execution_time_ms INTEGER,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Enable Row Level Security
ALTER TABLE trigger_executions ENABLE ROW LEVEL SECURITY;

-- RLS Policy: Admins have full access
CREATE POLICY "Admins have full access to trigger executions"
    ON trigger_executions
    FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );

-- RLS Policy: Clients can view their own trigger executions
CREATE POLICY "Clients can view own trigger executions"
    ON trigger_executions
    FOR SELECT
    TO authenticated
    USING (
        client_id = auth.uid()::uuid
    );

-- Create indexes for performance
CREATE INDEX idx_trigger_executions_trigger_id ON trigger_executions(trigger_id);
CREATE INDEX idx_trigger_executions_client_id ON trigger_executions(client_id);
CREATE INDEX idx_trigger_executions_executed_at ON trigger_executions(executed_at DESC);
CREATE INDEX idx_trigger_executions_condition_met ON trigger_executions(condition_met);

-- Add comment
COMMENT ON TABLE trigger_executions IS 'Audit log of trigger executions for monitoring and debugging';
