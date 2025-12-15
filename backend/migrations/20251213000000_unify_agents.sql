BEGIN;

-- 1. Criar Tipo Enum
DO $$ BEGIN
    CREATE TYPE agent_role AS ENUM ('system_orchestrator', 'system_supervisor', 'client_agent');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 2. Criar Tabela Agents
DROP TABLE IF EXISTS agents CASCADE;
CREATE TABLE agents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
  parent_id UUID REFERENCES agents(id) ON DELETE SET NULL,
  role agent_role NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  config JSONB NOT NULL DEFAULT '{}'::jsonb,
  sicc_enabled BOOLEAN DEFAULT TRUE,
  fine_tuning_config JSONB DEFAULT '{}'::jsonb,
  is_active BOOLEAN DEFAULT TRUE,
  slug TEXT UNIQUE,
  is_public BOOLEAN DEFAULT FALSE,
  public_url TEXT,
  access_count INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Criar RENUS (System Orchestrator) - Explicito (renus_config vazio)
INSERT INTO agents (id, role, name, description, config, sicc_enabled)
VALUES (
  '00000000-0000-0000-0000-000000000001'::uuid,
  'system_orchestrator',
  'RENUS',
  'Orquestrador Global do Sistema RENUM',
  jsonb_build_object(
    'model', 'gpt-4o',
    'system_prompt', 'Você é o RENUS, agente orquestrador principal da plataforma RENUM. Sua função é conduzir entrevistas de requisitos, qualificar leads e rotear conversas para agentes especializados.',
    'temperature', 0.7,
    'max_tokens', 2000,
    'provider', 'openai',
    'tools', jsonb_build_array('supabase_query', 'whatsapp', 'email')
  ),
  true
)
ON CONFLICT (id) DO NOTHING;

-- 4. Migrar Client Agents (Antigos Sub-Agents) - REMOVIDO PARA LIMPEZA
-- A tabela sub_agents foi dropada. Estamos começando do zero.


-- 5. Criar ISA (System Supervisor)
INSERT INTO agents (id, role, name, description, config, sicc_enabled)
VALUES (
  '00000000-0000-0000-0000-000000000002'::uuid,
  'system_supervisor',
  'ISA',
  'Assistente Supervisora do Sistema e SICC',
  jsonb_build_object(
    'model', 'gpt-4o',
    'system_prompt', 'Você é a ISA, assistente administrativa e supervisora de aprendizado...',
    'tools', jsonb_build_array('supabase_query', 'send_email')
  ),
  true
)
ON CONFLICT (id) DO NOTHING;

COMMIT;
