-- Função auxiliar para verificar se o usuário é admin
CREATE OR REPLACE FUNCTION public.is_admin()
RETURNS boolean
LANGUAGE sql
SECURITY DEFINER
AS $$
  SELECT EXISTS (
    SELECT 1
    FROM public.profiles
    WHERE profiles.id = auth.uid() AND profiles.role = 'admin'
  );
$$;

-- Habilitar RLS em todas as tabelas
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.renus_config ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.tools ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sub_agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.interviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.interview_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.isa_commands ENABLE ROW LEVEL SECURITY;

-- Políticas de Acesso Total para Admin (Usando a função is_admin)

-- profiles
CREATE POLICY "Admins full access to profiles" ON public.profiles 
FOR ALL TO authenticated USING (public.is_admin()) WITH CHECK (public.is_admin());

-- clients
CREATE POLICY "Admins full access to clients" ON public.clients 
FOR ALL TO authenticated USING (public.is_admin()) WITH CHECK (public.is_admin());

-- renus_config
CREATE POLICY "Admins full access to renus_config" ON public.renus_config 
FOR ALL TO authenticated USING (public.is_admin()) WITH CHECK (public.is_admin());

-- tools
CREATE POLICY "Admins full access to tools" ON public.tools 
FOR ALL TO authenticated USING (public.is_admin()) WITH CHECK (public.is_admin());

-- sub_agents
CREATE POLICY "Admins full access to sub_agents" ON public.sub_agents 
FOR ALL TO authenticated USING (public.is_admin()) WITH CHECK (public.is_admin());

-- leads
CREATE POLICY "Admins full access to leads" ON public.leads 
FOR ALL TO authenticated USING (public.is_admin()) WITH CHECK (public.is_admin());

-- interviews
CREATE POLICY "Admins full access to interviews" ON public.interviews 
FOR ALL TO authenticated USING (public.is_admin()) WITH CHECK (public.is_admin());

-- interview_messages
CREATE POLICY "Admins full access to interview_messages" ON public.interview_messages 
FOR ALL TO authenticated USING (public.is_admin()) WITH CHECK (public.is_admin());

-- projects
CREATE POLICY "Admins full access to projects" ON public.projects 
FOR ALL TO authenticated USING (public.is_admin()) WITH CHECK (public.is_admin());

-- conversations
CREATE POLICY "Admins full access to conversations" ON public.conversations 
FOR ALL TO authenticated USING (public.is_admin()) WITH CHECK (public.is_admin());

-- messages
CREATE POLICY "Admins full access to messages" ON public.messages 
FOR ALL TO authenticated USING (public.is_admin()) WITH CHECK (public.is_admin());

-- isa_commands
CREATE POLICY "Admins full access to isa_commands" ON public.isa_commands 
FOR ALL TO authenticated USING (public.is_admin()) WITH CHECK (public.is_admin());