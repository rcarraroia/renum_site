-- 4. Tabela tools (Depende de renus_config)
CREATE TABLE public.tools (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  config_id INTEGER REFERENCES renus_config(id) ON DELETE CASCADE,
  name TEXT NOT NULL UNIQUE,
  description TEXT,
  is_enabled BOOLEAN DEFAULT TRUE,
  parameters JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trigger para tools
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON public.tools
FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();

-- 5. Tabela sub_agents (Depende de renus_config)
CREATE TABLE public.sub_agents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  config_id INTEGER REFERENCES renus_config(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  channel TEXT NOT NULL CHECK (channel IN ('site', 'whatsapp')),
  system_prompt TEXT NOT NULL,
  topics TEXT[],
  is_active BOOLEAN DEFAULT TRUE,
  model TEXT,
  fine_tuning_config JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trigger para sub_agents
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON public.sub_agents
FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();