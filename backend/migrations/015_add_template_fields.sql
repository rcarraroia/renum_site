-- Migration 015: Add Template Fields to Agents
-- Data: 2025-12-18
-- Objetivo: Adicionar campos para suporte a templates no marketplace

BEGIN;

-- Adicionar campos de template
ALTER TABLE agents ADD COLUMN IF NOT EXISTS is_template BOOLEAN DEFAULT FALSE;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS category TEXT CHECK (category IN ('b2b', 'b2c'));
ALTER TABLE agents ADD COLUMN IF NOT EXISTS niche TEXT;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS marketplace_visible BOOLEAN DEFAULT FALSE;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS available_tools JSONB DEFAULT '{}'::jsonb;
ALTER TABLE agents ADD COLUMN IF NOT EXISTS available_integrations JSONB DEFAULT '{}'::jsonb;

-- Criar índices para performance
CREATE INDEX IF NOT EXISTS idx_agents_is_template ON agents(is_template) WHERE is_template = TRUE;
CREATE INDEX IF NOT EXISTS idx_agents_marketplace ON agents(marketplace_visible) WHERE marketplace_visible = TRUE;
CREATE INDEX IF NOT EXISTS idx_agents_category ON agents(category);
CREATE INDEX IF NOT EXISTS idx_agents_niche ON agents(niche);

-- Índice composto para marketplace
CREATE INDEX IF NOT EXISTS idx_agents_marketplace_category 
ON agents(marketplace_visible, category) 
WHERE marketplace_visible = TRUE;

-- Comentários
COMMENT ON COLUMN agents.is_template IS 'Indica se o agente é um template do marketplace';
COMMENT ON COLUMN agents.category IS 'Categoria do template: b2b ou b2c';
COMMENT ON COLUMN agents.niche IS 'Nicho de atuação do agente (ex: Imobiliário, Vendas)';
COMMENT ON COLUMN agents.marketplace_visible IS 'Se o template está visível no marketplace';
COMMENT ON COLUMN agents.available_tools IS 'Ferramentas que o cliente pode ativar';
COMMENT ON COLUMN agents.available_integrations IS 'Integrações que o cliente pode ativar';

COMMIT;
