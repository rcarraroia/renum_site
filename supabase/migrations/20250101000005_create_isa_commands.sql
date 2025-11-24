-- 12. Tabela isa_commands (Depende de profiles)
CREATE TABLE public.isa_commands (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  admin_id UUID REFERENCES profiles(id) ON DELETE SET NULL,
  user_message TEXT NOT NULL,
  assistant_response TEXT NOT NULL,
  command_executed BOOLEAN DEFAULT FALSE,
  executed_at TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para isa_commands
CREATE INDEX idx_isa_admin ON isa_commands(admin_id);