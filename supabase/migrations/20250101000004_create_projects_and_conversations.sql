-- 9. Tabela projects (Depende de clients e profiles)
CREATE TABLE public.projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
  status TEXT NOT NULL,
  type TEXT NOT NULL,
  start_date DATE,
  due_date DATE,
  progress INTEGER DEFAULT 0,
  responsible_id UUID REFERENCES profiles(id),
  budget NUMERIC(10, 2),
  description TEXT,
  scope TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para projects
CREATE INDEX idx_project_client ON projects(client_id);
CREATE INDEX idx_project_status ON projects(status);
CREATE INDEX idx_project_responsible ON projects(responsible_id);

-- Trigger para projects
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON public.projects
FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();

-- 10. Tabela conversations (Depende de clients e profiles)
CREATE TABLE public.conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
  status TEXT NOT NULL,
  channel TEXT NOT NULL,
  assigned_agent_id UUID REFERENCES profiles(id),
  unread_count INTEGER DEFAULT 0,
  priority TEXT DEFAULT 'Low',
  start_date TIMESTAMPTZ DEFAULT NOW(),
  last_update TIMESTAMPTZ DEFAULT NOW(),
  summary TEXT,
  tags TEXT[],
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para conversations
CREATE INDEX idx_conv_client ON conversations(client_id);
CREATE INDEX idx_conv_status ON conversations(status);
CREATE INDEX idx_conv_priority ON conversations(priority);

-- Trigger para conversations
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON public.conversations
FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();

-- 11. Tabela messages (Depende de conversations)
CREATE TABLE public.messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
  sender TEXT NOT NULL,
  type TEXT NOT NULL,
  content TEXT NOT NULL,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  is_read BOOLEAN DEFAULT FALSE,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para messages
CREATE INDEX idx_msg_conv ON messages(conversation_id);
CREATE INDEX idx_msg_sender ON messages(sender);