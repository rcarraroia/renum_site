-- 1. Tabela profiles (Depende de auth.users)
CREATE TABLE public.profiles (
  id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  first_name TEXT,
  last_name TEXT,
  role TEXT NOT NULL DEFAULT 'guest', -- 'admin', 'client', 'guest'
  avatar_url TEXT,
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (id)
);

-- Trigger para profiles
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON public.profiles
FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();

-- 2. Tabela clients
CREATE TABLE public.clients (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_name TEXT NOT NULL,
  document TEXT UNIQUE,
  website TEXT,
  segment TEXT NOT NULL,
  status TEXT NOT NULL,
  contact JSONB,
  address JSONB,
  last_interaction TIMESTAMPTZ,
  tags TEXT[],
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trigger para clients
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON public.clients
FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();

-- 3. Tabela renus_config (Singleton)
CREATE TABLE public.renus_config (
  id INTEGER PRIMARY KEY DEFAULT 1,
  system_prompt TEXT,
  persona TEXT,
  capabilities TEXT,
  limitations TEXT,
  security_level TEXT,
  is_guardrails_enabled BOOLEAN DEFAULT TRUE,
  provider TEXT DEFAULT 'openrouter',
  model TEXT DEFAULT 'anthropic/claude-sonnet-4',
  temperature NUMERIC(3, 2) DEFAULT 0.7,
  max_tokens INTEGER DEFAULT 4000,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trigger para renus_config
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON public.renus_config
FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();