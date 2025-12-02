# 📋 TEMPLATE DE SPRINT - RENUM

## 🎯 INSTRUÇÕES DE USO (Claude)

Este template deve ser usado para criar TODOS os sprints do projeto RENUM.

**Como usar:**
1. Copie este template completo
2. Substitua todos os `[PREENCHER: ...]` com conteúdo específico do sprint
3. Mantenha TODA a estrutura e seções
4. Não remova nenhuma seção, mesmo que pareça vazia
5. Use os exemplos como referência

**Responsabilidades:**
- **Claude (você):** Preenche o template com planejamento detalhado
- **Kiro:** Verifica estado real do Supabase/VPS e executa
- **Usuário:** Aprova e decide em caso de divergências

---

# SPRINT [NÚMERO] - [NOME DO SPRINT]

> **Exemplo:** SPRINT 02 - CRUD CORE

---

## 🎯 OBJETIVO

[PREENCHER: 2-3 frases descrevendo o objetivo principal deste sprint]

**Exemplo:**
```
Implementar CRUD completo para as entidades principais do sistema (Clientes, Leads, Projetos).
Ao final deste sprint, o sistema terá endpoints funcionais para criar, ler, atualizar e deletar
estas entidades, com validações de negócio e políticas RLS aplicadas.
```

---

## 📦 ENTREGÁVEIS

Ao final deste sprint, você terá:

[PREENCHER: Lista de checkboxes com entregáveis concretos]

**Exemplo:**
```
✅ CRUD de Clientes (backend + frontend)
✅ CRUD de Leads (backend + frontend)
✅ CRUD de Projetos (backend + frontend)
✅ Validações de negócio implementadas
✅ Testes unitários para services
✅ Documentação API atualizada
```

---

## 🔗 DEPENDÊNCIAS

### Sprints Anteriores
[PREENCHER: Quais sprints devem estar concluídos]

**Exemplo:**
```
- [x] Sprint 01 - Fundação e Autenticação
```

### Pré-requisitos Técnicos
[PREENCHER: O que deve estar configurado/instalado]

**Exemplo:**
```
- Backend FastAPI rodando
- Autenticação funcionando
- Supabase configurado
- Frontend React rodando
```

---

## 🔍 VERIFICAÇÕES NECESSÁRIAS (Kiro)

⚠️ **IMPORTANTE:** Kiro deve executar estas verificações ANTES de iniciar o sprint.

### Banco de Dados (Supabase)

Kiro deve conectar ao Supabase e verificar:

[PREENCHER: Lista de verificações de banco de dados]

**Exemplo:**
```
- [ ] Tabela `clients` existe
- [ ] Tabela `clients` tem colunas: id, profile_id, company_name, cnpj, plan, status, created_at, updated_at
- [ ] Tabela `leads` existe
- [ ] Tabela `leads` tem colunas: id, client_id, phone, name, email, metadata, status, created_at, updated_at
- [ ] RLS está habilitado em `clients` e `leads`
- [ ] Políticas RLS para admin e client estão criadas
- [ ] Índices em `clients.profile_id` e `leads.client_id` existem
```

**Comandos para Kiro executar:**
```sql
-- Listar tabelas
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- Verificar estrutura de clients
SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'clients';

-- Verificar RLS
SELECT tablename, rowsecurity FROM pg_tables WHERE tablename IN ('clients', 'leads');

-- Verificar políticas
SELECT tablename, policyname FROM pg_policies WHERE tablename IN ('clients', 'leads');
```

### Servidor (VPS)

Kiro deve conectar via SSH e verificar:

[PREENCHER: Lista de verificações de servidor - se aplicável]

**Exemplo:**
```
- [ ] Backend está rodando na porta 8000
- [ ] Redis está rodando
- [ ] Celery worker está ativo
- [ ] Espaço em disco > 10GB disponível
```

**Comandos para Kiro executar:**
```bash
# Conectar
ssh root@72.60.151.78

# Verificar serviços
systemctl status renum-api
systemctl status redis
systemctl status renum-celery

# Verificar portas
netstat -tulpn | grep 8000

# Verificar espaço
df -h
```

### Arquivos Locais

Kiro deve verificar se estes arquivos existem:

[PREENCHER: Lista de arquivos que devem existir]

**Exemplo:**
```
- [ ] src/main.py
- [ ] src/config/settings.py
- [ ] src/api/routes/auth.py
- [ ] .env com variáveis configuradas
```

---

## 🏗️ ARQUITETURA

[PREENCHER: Diagrama ASCII mostrando o fluxo/arquitetura]

**Exemplo:**
```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                      │
│  - ClientsPage (lista, cria, edita, deleta)            │
│  - LeadsPage (lista, cria, edita, deleta)              │
│  - ProjectsPage (lista, cria, edita, deleta)           │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP + JWT
                     │
┌────────────────────▼────────────────────────────────────┐
│                 BACKEND (FastAPI)                        │
│  - /api/clients (GET, POST, PUT, DELETE)                │
│  - /api/leads (GET, POST, PUT, DELETE)                  │
│  - /api/projects (GET, POST, PUT, DELETE)               │
│  - Middleware de autenticação                           │
│  - Services com lógica de negócio                       │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              SUPABASE (Postgres)                         │
│  - clients (RLS habilitado)                             │
│  - leads (RLS habilitado)                               │
│  - projects (RLS habilitado)                            │
└─────────────────────────────────────────────────────────┘
```

---

## 📂 ESTRUTURA DE ARQUIVOS

### Arquivos Novos (Criar)

[PREENCHER: Lista de arquivos que serão criados com descrição]

**Formato:**
```
caminho/arquivo.ext - Descrição do que faz
```

**Exemplo:**
```
Backend:
- src/api/routes/clients.py - Endpoints CRUD de clientes
- src/api/routes/leads.py - Endpoints CRUD de leads
- src/api/routes/projects.py - Endpoints CRUD de projetos
- src/services/client_service.py - Lógica de negócio de clientes
- src/services/lead_service.py - Lógica de negócio de leads
- src/services/project_service.py - Lógica de negócio de projetos
- src/models/client.py - Pydantic models para clientes
- src/models/lead.py - Pydantic models para leads
- src/models/project.py - Pydantic models para projetos
- tests/test_clients.py - Testes unitários de clientes

Frontend:
- src/pages/clients/ClientsPage.tsx - Página de listagem de clientes
- src/pages/clients/ClientForm.tsx - Formulário de cliente
- src/services/clientService.ts - API calls para clientes
- src/types/client.ts - TypeScript types para clientes
```

### Arquivos Modificados (Atualizar)

[PREENCHER: Lista de arquivos existentes que serão modificados]

**Formato:**
```
caminho/arquivo.ext - O que será alterado
```

**Exemplo:**
```
Backend:
- src/main.py - Adicionar routers de clients, leads, projects
- src/api/routes/__init__.py - Exportar novos routers

Frontend:
- src/App.tsx - Adicionar rotas para clients, leads, projects
- src/components/layout/Sidebar.tsx - Adicionar links no menu
```

---

## 🔧 IMPLEMENTAÇÃO

### PASSO 1: [Nome do Passo]

[PREENCHER: Descrição do que será feito neste passo]

**Objetivo:** [PREENCHER: O que este passo alcança]

**Comandos:**
```bash
[PREENCHER: Comandos a executar, se houver]
```

**Arquivo:** `[PREENCHER: caminho/arquivo.ext]`

```[linguagem]
[PREENCHER: Código completo do arquivo]
```

**Explicação:**
[PREENCHER: Explicação linha por linha ou por blocos importantes]

**Exemplo:**
```
- Linha 1-5: Imports necessários
- Linha 10-20: Definição do router FastAPI
- Linha 25-40: Endpoint GET para listar clientes
- Linha 45-60: Endpoint POST para criar cliente
```

---

### PASSO 2: [Nome do Passo]

[REPETIR estrutura do PASSO 1 para cada passo necessário]

---

### PASSO N: [Último Passo]

[REPETIR estrutura]

---

## 🧪 VALIDAÇÃO

### Testes Automatizados

[PREENCHER: Comandos para executar testes]

**Exemplo:**
```bash
# Backend
cd renum-backend
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pytest tests/test_clients.py -v

# Frontend
cd frontend
npm test
```

### Testes Manuais (Kiro deve executar)

[PREENCHER: Lista de testes manuais com resultado esperado]

**Formato:**
```
1. [Ação] - [Resultado esperado]
```

**Exemplo:**
```
Backend (via curl ou Postman):

1. GET /api/clients
   - Deve retornar lista de clientes (pode estar vazia)
   - Status: 200

2. POST /api/clients com dados válidos
   - Deve criar cliente
   - Status: 201
   - Retorna objeto do cliente criado

3. POST /api/clients com dados inválidos
   - Deve retornar erro de validação
   - Status: 400

4. GET /api/clients/{id}
   - Deve retornar cliente específico
   - Status: 200

5. PUT /api/clients/{id}
   - Deve atualizar cliente
   - Status: 200

6. DELETE /api/clients/{id}
   - Deve deletar cliente
   - Status: 204

Frontend (via navegador):

1. Acessar /clients
   - Deve mostrar lista de clientes
   - Botão "Novo Cliente" visível

2. Clicar em "Novo Cliente"
   - Deve abrir formulário
   - Campos obrigatórios marcados

3. Preencher e salvar
   - Deve criar cliente
   - Deve redirecionar para lista
   - Cliente deve aparecer na lista

4. Clicar em "Editar"
   - Deve abrir formulário preenchido
   - Deve permitir edição

5. Clicar em "Deletar"
   - Deve pedir confirmação
   - Deve remover da lista
```

### Checklist de Conclusão

[PREENCHER: Checklist final de validação]

**Exemplo:**
```
Backend:
- [ ] Todos os endpoints respondem corretamente
- [ ] Validações de negócio funcionando
- [ ] RLS aplicado corretamente
- [ ] Testes unitários passando
- [ ] Documentação Swagger atualizada

Frontend:
- [ ] Todas as páginas renderizam
- [ ] Formulários validam corretamente
- [ ] CRUD completo funciona
- [ ] Loading states implementados
- [ ] Error handling implementado

Banco de Dados:
- [ ] Dados sendo salvos corretamente
- [ ] RLS impedindo acesso não autorizado
- [ ] Índices melhorando performance
```

---

## 🚨 TROUBLESHOOTING

[PREENCHER: Lista de erros comuns e soluções]

**Formato:**
```
### Erro: "[Mensagem de erro]"

**Causa:** [Por que acontece]

**Solução:**
[Passo a passo para resolver]
```

**Exemplo:**
```
### Erro: "relation 'clients' does not exist"

**Causa:** Tabela clients não foi criada no Supabase

**Solução:**
1. Conectar ao Supabase Dashboard
2. Ir em SQL Editor
3. Executar migration de criação da tabela
4. Verificar com: SELECT * FROM clients LIMIT 1;

---

### Erro: "CORS policy blocked"

**Causa:** Frontend não está na lista de origens permitidas

**Solução:**
1. Abrir .env do backend
2. Adicionar origem do frontend: CORS_ORIGINS=http://localhost:5173
3. Reiniciar backend
4. Testar novamente

---

### Erro: "401 Unauthorized"

**Causa:** Token JWT inválido ou expirado

**Solução:**
1. Fazer logout no frontend
2. Fazer login novamente
3. Verificar se token está sendo enviado no header
4. Verificar logs do backend para mais detalhes
```

---

## 📊 RELATÓRIO DE VERIFICAÇÃO (Kiro preenche)

⚠️ **Esta seção é preenchida por Kiro após executar as verificações**

### Estado do Banco de Dados

**Verificado em:** [DATA/HORA]

```
Tabelas:
- clients: [✅ Existe / ❌ Não existe / ⚠️ Estrutura diferente]
- leads: [✅ Existe / ❌ Não existe / ⚠️ Estrutura diferente]
- projects: [✅ Existe / ❌ Não existe / ⚠️ Estrutura diferente]

RLS:
- clients: [✅ Habilitado / ❌ Desabilitado]
- leads: [✅ Habilitado / ❌ Desabilitado]
- projects: [✅ Habilitado / ❌ Desabilitado]

Políticas:
- [Lista de políticas encontradas]

Índices:
- [Lista de índices encontrados]
```

### Divergências Encontradas

```
1. [Descrição da divergência]
   - Esperado: [X]
   - Encontrado: [Y]
   - Ação tomada: [Z]
   - Status: [✅ Resolvido / ⏳ Aguardando / ❌ Bloqueado]
```

### Estado do Servidor (se aplicável)

**Verificado em:** [DATA/HORA]

```
Serviços:
- renum-api: [✅ Rodando / ❌ Parado / ⚠️ Com erro]
- redis: [✅ Rodando / ❌ Parado]
- celery: [✅ Rodando / ❌ Parado]

Recursos:
- Disco: [X GB disponível]
- Memória: [X GB disponível]
- CPU: [X% uso]
```

### Decisões Tomadas

```
1. [Decisão tomada]
   - Motivo: [Por que]
   - Impacto: [O que muda]
   - Aprovado por: [Usuário]
```

---

## 📚 PRÓXIMO SPRINT

[PREENCHER: Breve descrição do próximo sprint]

**Exemplo:**
```
Após validar tudo neste sprint, partimos para:

**SPRINT 03 - CONVERSAÇÕES**
- WebSocket para chat em tempo real
- Sistema de mensagens
- Histórico de conversas
- Notificações em tempo real
```

---

## ✅ CHECKLIST DE VALIDAÇÃO DO TEMPLATE

**Antes de enviar este sprint ao usuário, Claude deve verificar:**

- [ ] Todas as seções `[PREENCHER]` foram substituídas
- [ ] Exemplos foram removidos ou adaptados
- [ ] Código está completo (sem `...` ou `# TODO`)
- [ ] Comandos estão corretos para Windows (se aplicável)
- [ ] Não há referências a APIs específicas (Evolution, Twilio, etc)
- [ ] Seção de verificações para Kiro está completa
- [ ] Arquivos novos e modificados estão listados
- [ ] Troubleshooting cobre erros comuns
- [ ] Testes manuais têm resultado esperado
- [ ] Arquitetura está clara e visual

---

## 📝 NOTAS PARA CLAUDE

### Boas Práticas ao Preencher

1. **Seja específico:** Não use "etc", "...", ou "e outros"
2. **Código completo:** Nunca deixe `# TODO` ou `// implementar depois`
3. **Comandos testáveis:** Todos os comandos devem poder ser copiados e colados
4. **Validação clara:** Resultado esperado deve ser inequívoco
5. **Troubleshooting real:** Apenas erros que realmente podem acontecer

### O que NÃO fazer

❌ Assumir que algo existe sem pedir para Kiro verificar
❌ Referenciar APIs específicas (Evolution, Twilio, SendGrid)
❌ Usar comandos Linux em projeto Windows
❌ Deixar código incompleto
❌ Pular seções do template
❌ Misturar responsabilidades (Claude planeja, Kiro executa)

### Estrutura de Código

Sempre fornecer arquivos completos com:
- Imports
- Type hints (Python)
- Docstrings
- Error handling
- Logging
- Comentários explicativos

### Linguagem

- **Objetivo/Descrições:** Português claro e direto
- **Código:** Inglês (variáveis, funções, comentários)
- **Comandos:** Como estão na documentação oficial

---

## 🎯 RESUMO

Este template garante:

✅ **Consistência** - Todos os sprints seguem o mesmo padrão
✅ **Completude** - Nada é esquecido
✅ **Clareza** - Responsabilidades bem definidas
✅ **Rastreabilidade** - Verificações documentadas
✅ **Qualidade** - Código completo e testável

**Versão:** 1.0  
**Última atualização:** 2025-11-25  
**Responsável:** Equipe RENUM
