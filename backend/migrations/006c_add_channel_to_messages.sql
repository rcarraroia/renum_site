-- Migration 006c: Add channel column to messages table
-- Sprint 06 - Fix critical bug for sandbox messaging
-- Date: 2025-12-04

-- Add channel column to messages
ALTER TABLE messages
ADD COLUMN IF NOT EXISTS channel TEXT;

-- Add comment
COMMENT ON COLUMN messages.channel IS 'Communication channel (WhatsApp, Web, Email, API)';

-- Verify
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'messages'
AND column_name = 'channel';
