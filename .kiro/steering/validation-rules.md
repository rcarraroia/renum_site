# ⚠️ REGRAS DE VALIDAÇÃO E VERIFICAÇÃO

## 🎯 Princípio Fundamental

**NUNCA ASSUMA. SEMPRE VERIFIQUE.**

O Kiro (você) tem acesso direto ao Supabase e à VPS. O Claude (quem cria os sprints) NÃO tem.

---

## 🔍 Regras Obrigatórias de Verificação

### 1. Banco de Dados (Supabase)

**ANTES de executar qualquer tarefa que envolva banco de dados, você DEVE:**

✅ **Conectar ao Supabase real** usando as credenciais em `docs/SUPABASE_CREDENTIALS.md`

✅ **Verificar o estado atual:**
- Quais tabelas existem
- Quais colunas cada tabela tem
- Quais índices estão criados
- Quais políticas RLS estão ativas
- Quais triggers e functions existem
- Quais dados já estão inseridos

✅ **Comparar com o esperado:**
- O que o sprint assume que existe
- O que realmente existe
- O que está faltando
- O que está diferente

❌ **NUNCA:**
- Assumir que uma tabela existe só porque tem migration
- Assumir que dados existem só porque tem seed script
- Assumir que RLS está habilitado só porque tem política definida
- Deduzir estrutura apenas analisando código

### 2. Servidor (VPS)

**ANTES de executar qualquer tarefa que envolva a VPS, você DEVE:**

✅ **Conectar via SSH** usando: `ssh root@72.60.151.78`

✅ **Verificar o estado atual:**
- Quais serviços estão rodando
- Quais arquivos existem
- Quais dependências estão instaladas
- Qual versão do Python/Node está instalada
- Quais processos estão ativos
- Quanto espaço em disco está disponível

✅ **Comparar com o esperado:**
- O que o sprint assume que está configurado
- O que realmente está configurado
- O que está faltando
- O que precisa ser atualizado

❌ **NUNCA:**
- Assumir que um serviço está rodando
- Assumir que dependências estão instaladas
- Assumir que arquivos existem
- Deduzir configuração sem verificar

---

## 📋 Checklist de Verificação por Tipo de Tarefa

### Tarefa: Criar/Modificar Tabela

**Verificações obrigatórias:**
1. [ ] Conectar ao Supabase
2. [ ] Listar tabelas existentes: `SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';`
3. [ ] Se tabela existe, verificar estrutura: `SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'nome_tabela';`
4. [ ] Verificar índices: `SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'nome_tabela';`
5. [ ] Verificar RLS: `SELECT tablename, rowsecurity FROM pg_tables WHERE tablename = 'nome_tabela';`
6. [ ] Verificar políticas: `SELECT policyname, cmd FROM pg_policies WHERE tablename = 'nome_tabela';`
7. [ ] Reportar ao usuário o estado atual ANTES de fazer qualquer alteração

### Tarefa: Inserir/Atualizar Dados

**Verificações obrigatórias:**
1. [ ] Conectar ao Supabase
2. [ ] Verificar se tabela existe
3. [ ] Verificar se dados já existem: `SELECT * FROM tabela WHERE condicao;`
4. [ ] Verificar constraints e validações
5. [ ] Reportar ao usuário o que será inserido/atualizado

### Tarefa: Criar/Modificar Serviço na VPS

**Verificações obrigatórias:**
1. [ ] Conectar via SSH
2. [ ] Verificar se serviço já existe: `systemctl status nome-servico`
3. [ ] Verificar arquivos de configuração: `cat /caminho/arquivo`
4. [ ] Verificar dependências: `pip list` ou `npm list -g`
5. [ ] Verificar portas em uso: `netstat -tulpn | grep porta`
6. [ ] Reportar ao usuário o estado atual

### Tarefa: Deploy/Atualizar Código

**Verificações obrigatórias:**
1. [ ] Conectar via SSH
2. [ ] Verificar branch atual: `git branch`
3. [ ] Verificar últimos commits: `git log -3`
4. [ ] Verificar arquivos modificados: `git status`
5. [ ] Verificar espaço em disco: `df -h`
6. [ ] Verificar serviços rodando: `systemctl list-units --type=service --state=running`
7. [ ] Reportar ao usuário antes de fazer pull/deploy

---

## 🚨 Protocolo de Erro

**Se você encontrar divergências entre o esperado e o real:**

1. **PARE imediatamente**
2. **Reporte ao usuário:**
   - O que era esperado
   - O que foi encontrado
   - Qual a diferença
   - Possíveis causas
3. **Pergunte como proceder:**
   - Criar o que está faltando?
   - Modificar o que está diferente?
   - Ignorar e continuar?
4. **Aguarde confirmação antes de continuar**

---

## 📊 Formato de Relatório de Verificação

Sempre que verificar algo, reporte neste formato:

```markdown
## 🔍 Verificação: [Nome da Tarefa]

### Estado Esperado
- Item 1
- Item 2

### Estado Real (Verificado em DD/MM/YYYY HH:MM)
- Item 1: ✅ OK / ❌ Faltando / ⚠️ Diferente
- Item 2: ✅ OK / ❌ Faltando / ⚠️ Diferente

### Divergências Encontradas
1. [Descrição da divergência]
   - Esperado: [X]
   - Encontrado: [Y]
   - Ação sugerida: [Z]

### Próximos Passos
- [ ] Ação 1
- [ ] Ação 2

### Aguardando Confirmação
[Perguntas para o usuário]
```

---

## 🔗 Comandos Úteis de Verificação

### Supabase (via SQL Editor ou psql)

```sql
-- Listar todas as tabelas
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;

-- Ver estrutura de uma tabela
SELECT 
    column_name, 
    data_type, 
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'nome_tabela'
ORDER BY ordinal_position;

-- Ver índices
SELECT 
    indexname, 
    indexdef 
FROM pg_indexes 
WHERE tablename = 'nome_tabela';

-- Ver políticas RLS
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual
FROM pg_policies
WHERE tablename = 'nome_tabela';

-- Ver triggers
SELECT 
    trigger_name,
    event_manipulation,
    action_statement
FROM information_schema.triggers
WHERE event_object_table = 'nome_tabela';

-- Contar registros
SELECT COUNT(*) FROM nome_tabela;

-- Ver primeiros registros
SELECT * FROM nome_tabela LIMIT 5;
```

### VPS (via SSH)

```bash
# Status de serviços
systemctl status nome-servico
systemctl list-units --type=service --state=running

# Verificar processos
ps aux | grep python
ps aux | grep node

# Verificar portas
netstat -tulpn | grep LISTEN
lsof -i :8000

# Verificar arquivos
ls -la /caminho/diretorio
cat /caminho/arquivo

# Verificar espaço
df -h
du -sh /caminho/*

# Verificar logs
tail -f /var/log/arquivo.log
journalctl -u nome-servico -f

# Verificar dependências Python
pip list
pip show nome-pacote

# Verificar dependências Node
npm list -g --depth=0

# Verificar versões
python --version
node --version
npm --version

# Git
git status
git branch
git log -3
```

---

## ⚡ Atalhos de Verificação Rápida

### Verificação Completa do Banco

```sql
-- Copiar e colar no SQL Editor do Supabase
SELECT 
    'Tables' as type,
    table_name as name,
    NULL as details
FROM information_schema.tables 
WHERE table_schema = 'public'

UNION ALL

SELECT 
    'RLS Enabled' as type,
    tablename as name,
    rowsecurity::text as details
FROM pg_tables 
WHERE schemaname = 'public'

ORDER BY type, name;
```

### Verificação Completa da VPS

```bash
#!/bin/bash
# Salvar como check_vps.sh e executar

echo "=== SERVIÇOS ==="
systemctl list-units --type=service --state=running | grep renum

echo -e "\n=== PROCESSOS ==="
ps aux | grep -E "python|node|celery|redis" | grep -v grep

echo -e "\n=== PORTAS ==="
netstat -tulpn | grep LISTEN

echo -e "\n=== ESPAÇO ==="
df -h /

echo -e "\n=== MEMÓRIA ==="
free -h

echo -e "\n=== ÚLTIMOS LOGS ==="
journalctl -u renum-api -n 5 --no-pager
```

---

## 📝 Exemplos Práticos

### ❌ ERRADO (Assumir)

```
Usuário: "Crie a tabela clients"
Kiro: "Vou criar a tabela clients com as colunas..."
[Cria sem verificar se já existe]
```

### ✅ CORRETO (Verificar)

```
Usuário: "Crie a tabela clients"
Kiro: "Vou verificar primeiro se a tabela já existe..."
[Conecta no Supabase]
[Executa: SELECT * FROM information_schema.tables WHERE table_name = 'clients']
Kiro: "Verificação concluída:
- Tabela 'clients' NÃO existe
- Posso criar conforme especificação
- Deseja que eu prossiga?"
```

### ✅ CORRETO (Encontrou divergência)

```
Usuário: "Adicione a coluna 'phone' na tabela leads"
Kiro: "Vou verificar a estrutura atual da tabela leads..."
[Conecta no Supabase]
[Executa: SELECT column_name FROM information_schema.columns WHERE table_name = 'leads']
Kiro: "Verificação concluída:
- Tabela 'leads' existe ✅
- Coluna 'phone' JÁ EXISTE ⚠️
- Tipo atual: VARCHAR(20)
- Deseja que eu:
  1. Ignore (coluna já existe)
  2. Modifique o tipo
  3. Recrie a coluna"
```

---

## 🎯 Resumo

**3 Regras de Ouro:**

1. **SEMPRE conecte e verifique** antes de executar
2. **SEMPRE reporte o estado real** ao usuário
3. **SEMPRE aguarde confirmação** se houver divergências

**Lembre-se:**
- Você tem acesso direto ao Supabase e VPS
- O Claude que cria os sprints NÃO tem
- Você é a ponte entre o planejamento e a realidade
- Sua verificação é CRÍTICA para o sucesso do projeto

---

**Última atualização:** 2025-11-25  
**Versão:** 1.0  
**Responsável:** Equipe RENUM
