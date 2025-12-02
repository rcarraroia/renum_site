# 🗄️ Guia de Acesso ao Supabase

## Informações Gerais

**Projeto:** RENUM Backend  
**Banco de Dados:** PostgreSQL 15+  
**Plataforma:** Supabase  

---

## 📋 Credenciais

⚠️ **IMPORTANTE:** As credenciais reais estão em `SUPABASE_CREDENTIALS.md` (arquivo não versionado)

### Variáveis de Ambiente Necessárias

```bash
# .env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Diferença entre as chaves:**
- **ANON_KEY:** Chave pública, pode ser exposta no frontend, respeita RLS
- **SERVICE_KEY:** Chave privada, NUNCA expor, bypassa RLS, apenas backend

---

## 🔐 Acesso ao Dashboard

1. Acesse: https://supabase.com/dashboard
2. Faça login com a conta do projeto
3. Selecione o projeto RENUM

### Seções Importantes

**Table Editor:**
- Visualizar e editar dados das tabelas
- Criar/modificar estrutura de tabelas
- Gerenciar relacionamentos

**SQL Editor:**
- Executar queries SQL customizadas
- Criar migrations
- Testar queries antes de implementar

**Authentication:**
- Gerenciar usuários
- Configurar provedores de autenticação
- Políticas de senha

**Database:**
- Visualizar schema
- Gerenciar triggers e functions
- Configurar backups

**API:**
- Documentação automática da API
- Testar endpoints
- Gerar código de exemplo

---

## 🛠️ Configuração Inicial

### 1. Habilitar RLS em Todas as Tabelas

```sql
-- Executar para cada tabela
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE interviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE interview_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE renus_config ENABLE ROW LEVEL SECURITY;
ALTER TABLE tools ENABLE ROW LEVEL SECURITY;
ALTER TABLE sub_agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE isa_commands ENABLE ROW LEVEL SECURITY;
```

### 2. Criar Função para updated_at

```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### 3. Aplicar Trigger em Todas as Tabelas

```sql
-- Exemplo para uma tabela
CREATE TRIGGER update_profiles_updated_at
    BEFORE UPDATE ON profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Repetir para: clients, leads, interviews, projects, conversations, 
-- renus_config, tools, sub_agents
```

---

## 📊 Estrutura do Banco

### Tabelas Principais (12)

1. **profiles** - Usuários do sistema (admins, clientes)
2. **clients** - Empresas que compram agentes
3. **leads** - Contatos dos clientes
4. **interviews** - Metadados de pesquisas
5. **interview_messages** - Mensagens das entrevistas (1:N)
6. **projects** - Projetos/campanhas
7. **conversations** - Conversas gerais
8. **messages** - Mensagens de conversas gerais
9. **renus_config** - Configurações dos agentes
10. **tools** - Ferramentas disponíveis
11. **sub_agents** - Sub-agentes especializados
12. **isa_commands** - Comandos administrativos

### Relacionamentos Principais

```
profiles (1:N) → clients
clients (1:N) → leads
clients (1:N) → projects
leads (1:N) → interviews
interviews (1:N) → interview_messages
leads (1:N) → conversations
conversations (1:N) → messages
clients (1:N) → renus_config
```

---

## 🔍 Queries Úteis

### Verificar RLS Habilitado

```sql
SELECT schemaname, tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;
```

### Listar Políticas RLS

```sql
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
FROM pg_policies
WHERE schemaname = 'public'
ORDER BY tablename, policyname;
```

### Verificar Índices

```sql
SELECT
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;
```

### Estatísticas de Uso

```sql
-- Tamanho das tabelas
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Contagem de registros
SELECT
    'profiles' as table_name,
    COUNT(*) as count
FROM profiles
UNION ALL
SELECT 'clients', COUNT(*) FROM clients
UNION ALL
SELECT 'leads', COUNT(*) FROM leads
UNION ALL
SELECT 'interviews', COUNT(*) FROM interviews
UNION ALL
SELECT 'interview_messages', COUNT(*) FROM interview_messages;
```

---

## 🔒 Políticas RLS Padrão

### Para Admins (Acesso Total)

```sql
CREATE POLICY "Admins have full access"
    ON <table_name>
    FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );
```

### Para Clientes (Apenas Seus Dados)

```sql
-- Exemplo para tabela clients
CREATE POLICY "Clients can view own data"
    ON clients
    FOR SELECT
    TO authenticated
    USING (profile_id = auth.uid());

-- Exemplo para tabela leads
CREATE POLICY "Clients can view own leads"
    ON leads
    FOR SELECT
    TO authenticated
    USING (
        client_id IN (
            SELECT id FROM clients
            WHERE profile_id = auth.uid()
        )
    );
```

---

## 🚨 Troubleshooting

### Erro: "new row violates row-level security policy"

**Causa:** Tentando inserir/atualizar dados sem permissão RLS

**Solução:**
1. Verificar se política existe para a operação
2. Verificar se usuário tem role correto
3. Usar SERVICE_KEY se for operação administrativa

### Erro: "permission denied for table"

**Causa:** Usuário não tem permissão na tabela

**Solução:**
```sql
GRANT ALL ON <table_name> TO authenticated;
GRANT ALL ON <table_name> TO service_role;
```

### Performance Lenta em Queries

**Causa:** Falta de índices

**Solução:**
```sql
-- Criar índices em colunas frequentemente consultadas
CREATE INDEX idx_leads_client_id ON leads(client_id);
CREATE INDEX idx_interviews_lead_id ON interviews(lead_id);
CREATE INDEX idx_interview_messages_interview_id ON interview_messages(interview_id);
```

---

## 📦 Backup e Restore

### Backup Manual

1. Acesse Dashboard → Database → Backups
2. Clique em "Create backup"
3. Aguarde conclusão
4. Download do backup (se necessário)

### Backup Automático

Supabase faz backups automáticos diários. Configurar retenção:
- **Free tier:** 7 dias
- **Pro tier:** 30 dias
- **Enterprise:** Customizável

### Restore

1. Acesse Dashboard → Database → Backups
2. Selecione backup desejado
3. Clique em "Restore"
4. Confirme operação

⚠️ **ATENÇÃO:** Restore sobrescreve dados atuais!

---

## 🔗 Links Úteis

- **Dashboard:** https://supabase.com/dashboard
- **Documentação:** https://supabase.com/docs
- **API Reference:** https://supabase.com/docs/reference/javascript
- **SQL Reference:** https://www.postgresql.org/docs/15/

---

## 📞 Suporte

**Problemas de Acesso:**
- Verificar credenciais em `SUPABASE_CREDENTIALS.md`
- Resetar senha no dashboard
- Contatar admin do projeto

**Problemas Técnicos:**
- Suporte Supabase: https://supabase.com/support
- Discord Supabase: https://discord.supabase.com
- GitHub Issues: https://github.com/supabase/supabase/issues

---

**Última atualização:** 2025-11-25  
**Versão:** 1.0  
**Responsável:** Equipe RENUM
