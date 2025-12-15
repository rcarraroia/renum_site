-- Migration 008: Create triggers table
-- Sprint 07A - Integrações Core
-- Created: 2025-12-04

-- Create triggers table for automation rules (WHEN → IF → THEN)
CREATE TABLE IF NOT EXISTS triggers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    active BOOLEAN DEFAULT true NOT NULL,
    
    -- WHEN (Trigger Event)
    trigger_type VARCHAR(50) NOT NULL CHECK (trigger_type IN ('time_based', 'event_based', 'condition_based')),
    trigger_config JSONB NOT NULL DEFAULT '{}'::jsonb,
    
    -- IF (Condition)
    condition_type VARCHAR(50) CHECK (condition_type IN ('field_equals', 'field_contains', 'time_elapsed', 'always', 'field_greater_than', 'field_less_than')),
    condition_config JSONB DEFAULT '{}'::jsonb,
    
    -- THEN (Action)
    action_type VARCHAR(50) NOT NULL CHECK (action_type IN ('send_message', 'send_email', 'call_tool', 'change_status', 'notify_team')),
    action_config JSONB NOT NULL DEFAULT '{}'::jsonb,
    
    -- Execution tracking
    last_executed_at TIMESTAMP WITH TIME ZONE,
    execution_count INTEGER DEFAULT 0 NOT NULL,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Enable Row Level Security
ALTER TABLE triggers ENABLE ROW LEVEL SECURITY;

-- RLS Policy: Admins have full access
CREATE POLICY "Admins have full access to triggers"
    ON triggers
    FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );

-- RLS Policy: Clients can manage their own triggers
CREATE POLICY "Clients can manage own triggers"
    ON triggers
    FOR ALL
    TO authenticated
    USING (
        client_id = auth.uid()::uuid
    );

-- Create indexes for performance
CREATE INDEX idx_triggers_client_id ON triggers(client_id);
CREATE INDEX idx_triggers_active ON triggers(active) WHERE active = true;
CREATE INDEX idx_triggers_type ON triggers(trigger_type);
CREATE INDEX idx_triggers_last_executed ON triggers(last_executed_at DESC);

-- Create trigger for updated_at
CREATE TRIGGER update_triggers_updated_at
    BEFORE UPDATE ON triggers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Add comment
COMMENT ON TABLE triggers IS 'Stores automation triggers with WHEN → IF → THEN structure for event-based actions';
