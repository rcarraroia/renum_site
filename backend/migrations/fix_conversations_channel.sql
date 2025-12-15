-- Fix conversations channel constraint
-- Data: 2025-12-06
-- Problema: Constraint atual rejeita todos os valores

-- 1. Remover constraint problemático
ALTER TABLE conversations DROP CONSTRAINT IF EXISTS conversations_channel_check;

-- 2. Adicionar constraint correto
ALTER TABLE conversations ADD CONSTRAINT conversations_channel_check 
CHECK (channel IN ('whatsapp', 'email', 'web', 'sms', 'telegram', 'phone'));

-- 3. Verificar
SELECT conname, pg_get_constraintdef(oid) 
FROM pg_constraint 
WHERE conrelid = 'conversations'::regclass 
AND conname = 'conversations_channel_check';
