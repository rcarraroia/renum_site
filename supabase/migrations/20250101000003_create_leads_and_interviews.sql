-- 6. Tabela leads (Depende de sub_agents)
CREATE TABLE public.leads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  phone TEXT NOT NULL,
  email TEXT,
  source TEXT NOT NULL,
  status TEXT NOT NULL,
  subagent_id UUID REFERENCES sub_agents(id) ON DELETE SET NULL,
  first_contact_at TIMESTAMPTZ DEFAULT NOW(),
  last_interaction_at TIMESTAMPTZ DEFAULT NOW(),
  notes TEXT,
  score INTEGER, -- 0-100
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para leads
CREATE INDEX idx_lead_status ON leads(status);
CREATE INDEX idx_lead_source ON leads(source);
CREATE INDEX idx_lead_score ON leads(score);

-- Trigger para leads
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON public.leads
FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();

-- 7. Tabela interviews (Depende de leads e sub_agents)
CREATE TABLE public.interviews (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
  subagent_id UUID REFERENCES sub_agents(id) ON DELETE SET NULL,
  contact_name TEXT,
  contact_phone TEXT,
  status TEXT NOT NULL,
  started_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  topics_covered TEXT[],
  ai_analysis JSONB, -- Novo campo para análise da IA
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para interviews
CREATE INDEX idx_interview_lead ON interviews(lead_id);
CREATE INDEX idx_interview_status ON interviews(status);

-- Trigger para interviews
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON public.interviews
FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();

-- 8. Tabela interview_messages (Depende de interviews)
CREATE TABLE public.interview_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  interview_id UUID NOT NULL REFERENCES interviews(id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
  content TEXT NOT NULL,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para interview_messages
CREATE INDEX idx_interview_messages_interview ON interview_messages(interview_id, timestamp DESC);
CREATE INDEX idx_interview_messages_search ON interview_messages USING gin(to_tsvector('portuguese', content));