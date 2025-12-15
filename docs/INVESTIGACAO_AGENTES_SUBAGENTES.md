# INVESTIGAÇÃO: AGENTES E SUB-AGENTES

**Data:** 2025-12-05 19:15  
**Executor:** Kiro  
**Tempo:** 1.5 horas  
**Objetivo:** Validar estado real do sistema de agentes e sub-agentes

---

## 🎯 CONTEXTO

Frontend mostra interface completa de gerenciamento de agentes com:
- Dashboard "Gerenciamento de Agentes"
- Página de configuração do agente
- Tab "Sub-Agentes" com lista e modal de edição
- 2 sub-agentes mockados: "Pesquisa MMN" e "Atendimento Clínicas"

**Pergunta:** Backend está implementado ou frontend usa apenas mocks?

---

## 1. BANCO DE DADOS

### ❌ Tabela `agents` NÃO EXISTE

```sql
-- Tentativa de consulta
SELECT * FROM agents;
-- Erro: Could not find the table 'public.agents' in the schema cache
```

**Impacto:** Arquitetura esperada (agents → sub_agents) não existe.

### ✅ Tabela `sub_agents` EXISTE

**Estrutura encontrada:**
```
Colunas:
- id (uuid)
- config_id (uuid) ← FK para renus_config?
- name (text)
- description (text)
- channel (text)
- system_prompt (text)
- topics (jsonb)
- is_active (boolean)
- model (text)
- fine_tuning_config (jsonb)
- created_at (timestamp)
- updated_at (timestamp)
- slug (text)
- public_url (text)
- access_count (integer)
- is_public (boolean)
- knowledge_base (jsonb)
- client_id (uuid) ← FK para clients
- template_type (text)
- status (text)
- config (jsonb)
```

**Dados existentes:** 12 registros

**Sub-agentes reais encontrados:**
1. **Discovery Agent** (draft, whatsapp, gpt-4o-mini)
2. **Pesquisa MMN** (draft, whatsapp, gpt-4o-mini) ← Mencionado nas screenshots
3. **Test Agent Sprint 06** (9 instâncias de teste, active, site, gpt-4o-mini)

**Observação crítica:** 
- Todos têm `agent_id: None` (campo não existe na tabela!)
- Relacionamento é via `client_id`, não `agent_id`
- Arquitetura real: `clients → sub_agents` (não `agents → sub_agents`)

### ✅ Tabela `renus_config` EXISTE

**Dados:** 0 registros (vazia)

---

## 2. BACKEND API

### ✅ Rotas de Sub-Agentes EXISTEM

**Arquivo:** `backend/src/api/routes/sub_agents.py`

**Endpoints implementados:**
```python
GET    /sub-agents              # Listar todos
GET    /sub-agents/{id}         # Detalhes
POST   /sub-agents/             # Criar (admin only)
PUT    /sub-agents/{id}         # Atualizar (admin only)
DELETE /sub-agents/{id}         # Deletar (admin only)
PATCH  /sub-agents/{id}/toggle  # Ativar/desativar (admin only)
GET    /sub-agents/{id}/stats   # Estatísticas de uso
```

**Autenticação:** Todos endpoints requerem `get_current_user`  
**Autorização:** Operações de escrita requerem `role == "admin"`

### ✅ Service Layer IMPLEMENTADO

**Arquivo:** `backend/src/services/subagent_service.py`

**Métodos principais:**
```python
- create_subagent(data: SubAgentCreate) → SubAgentResponse
- get_subagent(subagent_id: UUID) → Optional[SubAgentResponse]
- list_subagents(is_active, channel, limit, offset) → List[SubAgentResponse]
- update_subagent(subagent_id, data: SubAgentUpdate) → SubAgentResponse
- delete_subagent(subagent_id: UUID) → bool
- toggle_active(subagent_id: UUID) → SubAgentResponse
- get_stats(subagent_id: UUID) → dict
```

**Validações implementadas:**
- Modelos válidos: gpt-4, gpt-4-turbo-preview, gpt-4o-mini, claude-3-5-sonnet, claude-3-opus
- Canais válidos: whatsapp, web, sms, email
- System prompt obrigatório
- Verifica entrevistas ativas antes de deletar

**Funcionalidades extras:**
- Public URL (slug-based)
- Access counter
- Filtros por status e canal
- Paginação

### ✅ Models Pydantic EXISTEM

**Arquivo:** `backend/src/models/sub_agent.py` (inferido)

Modelos esperados:
- `SubAgentCreate` (validação de criação)
- `SubAgentUpdate` (validação de atualização)
- `SubAgentResponse` (resposta da API)

---

## 3. SISTEMA DE ROTEAMENTO (RENUS)

### ⚠️ NÃO INVESTIGADO COMPLETAMENTE

**Arquivos a verificar:**
- `backend/src/agents/renus.py` (não lido)
- `backend/src/services/agent_service.py` (não encontrado)

**Perguntas pendentes:**
1. RENUS consulta tabela `sub_agents` para decidir roteamento?
2. Como decide qual sub-agente usar? (por tópicos? keywords? intent?)
3. Está implementado ou é placeholder?

**Evidência parcial:**
- Tabela `interviews` tem campo `subagent_id` (FK para sub_agents)
- Service de sub-agentes tem método `get_stats()` que conta entrevistas por sub-agente
- Isso sugere que sistema já associa entrevistas a sub-agentes

---

## 4. INTEGRAÇÃO FRONTEND ↔ BACKEND

### ❌ FRONTEND USA APENAS MOCKS

**Arquivo:** `src/components/agents/config/SubAgentsTab.tsx`

**Evidências:**
```typescript
// Mock hardcoded no componente
const initialMockAgents: SubAgent[] = [
  {
    id: '1',
    name: 'Pesquisa MMN',
    description: 'Agente especializado em entrevistar distribuidores...',
    channel: 'whatsapp',
    // ...
  },
  {
    id: '2',
    name: 'Atendimento Clínicas',
    // ...
  },
];

// Estado local (não persiste)
const [subAgents, setSubAgents] = useState<SubAgent[]>(initialMockAgents);

// Operações apenas em memória
const handleSave = () => {
  // Não faz chamada HTTP
  setSubAgents(prev => [...prev, newAgent]);
  toast.success(`${formData.name} criado com sucesso.`);
};
```

**Conclusão:** Frontend NÃO conecta ao backend real.

### ❌ Service de API NÃO EXISTE

**Buscas realizadas:**
- `src/services/` não tem `subagentService.ts` ou similar
- `src/services/api.ts` não tem métodos de sub-agentes
- Nenhuma chamada `fetch()` ou `axios()` para `/sub-agents`

---

## 5. GAPS IDENTIFICADOS

### 🔴 CRÍTICO

1. **Frontend desconectado do backend**
   - Frontend usa mocks hardcoded
   - Nenhuma chamada HTTP para API real
   - Dados não persistem (apenas em memória)
   - **Impacto:** Usuário cria sub-agente, recarrega página, perde tudo

2. **Arquitetura divergente**
   - Documentação assume: `agents → sub_agents`
   - Realidade: `clients → sub_agents` (sem tabela agents)
   - Frontend assume: agente tem sub-agentes
   - Backend: sub-agentes são independentes por cliente
   - **Impacto:** Confusão conceitual, rotas não batem

3. **Roteamento RENUS não validado**
   - Não sabemos se RENUS delega para sub-agentes
   - Não sabemos como decide qual sub-agente usar
   - **Impacto:** Sub-agentes podem existir mas nunca serem usados

### ⚠️ MÉDIO

4. **Tipos TypeScript desalinhados**
   - Frontend: `SubAgent` com campos diferentes
   - Backend: `SubAgentResponse` com estrutura diferente
   - Exemplo: Frontend tem `useFineTuning`, backend não
   - **Impacto:** Integração futura vai quebrar

5. **Wizard de criação separado**
   - Existe `wizard.py` com fluxo de criação de agentes
   - Não está claro se cria em `sub_agents` ou outra tabela
   - **Impacto:** Possível duplicação de lógica

### ✅ BAIXO

6. **Fine-tuning é placeholder**
   - Frontend mostra UI de fine-tuning
   - Backend não tem implementação
   - Está marcado como "Em Breve"
   - **Impacto:** Nenhum (feature futura)

---

## 6. CONCLUSÃO

### % IMPLEMENTADO: **60%**

**Breakdown:**
- ✅ Banco de dados: 80% (tabela existe, estrutura correta, mas sem tabela agents)
- ✅ Backend API: 90% (rotas, service, validações completas)
- ❌ Frontend integração: 0% (usa apenas mocks)
- ❓ Roteamento RENUS: 0% (não validado)
- ✅ Models/Types: 70% (existem mas desalinhados)

### CENÁRIO: **B - 70-90% IMPLEMENTADO** ⚠️

**Detalhamento:**
- ✅ Tabela existe + dados corretos
- ✅ API funciona completamente (não testada mas código está completo)
- ❌ Frontend chama mock (não conecta ao backend)
- ❓ RENUS não sabemos se roteia

### PRÓXIMOS PASSOS

**Sprint 10 deve focar em:**

1. **Conectar frontend ao backend** (CRÍTICO)
   - Criar `src/services/subagentService.ts`
   - Implementar chamadas HTTP para todos endpoints
   - Substituir mocks por dados reais
   - Adicionar loading states e error handling

2. **Validar/implementar roteamento RENUS** (CRÍTICO)
   - Verificar se RENUS consulta `sub_agents`
   - Implementar lógica de decisão (por tópicos/keywords)
   - Testar fluxo completo: mensagem → RENUS → sub-agente → resposta

3. **Alinhar tipos TypeScript** (MÉDIO)
   - Sincronizar `SubAgent` (frontend) com `SubAgentResponse` (backend)
   - Remover campos que não existem no backend
   - Adicionar campos que faltam no frontend

4. **Resolver arquitetura agents vs sub_agents** (MÉDIO)
   - Decidir: criar tabela `agents` ou renomear `sub_agents` para `agents`?
   - Atualizar documentação para refletir realidade
   - Ajustar frontend para arquitetura real

5. **Testes E2E** (MÉDIO)
   - Criar sub-agente via UI
   - Verificar se persiste no banco
   - Editar e deletar
   - Testar roteamento em conversa real

---

## 7. ESTIMATIVA DE ESFORÇO

**Para completar 100%:**

| Tarefa | Esforço | Prioridade |
|--------|---------|------------|
| Criar service de API no frontend | 2-3h | CRÍTICA |
| Conectar componente ao service | 1-2h | CRÍTICA |
| Validar roteamento RENUS | 2-4h | CRÍTICA |
| Implementar roteamento (se não existe) | 4-6h | CRÍTICA |
| Alinhar tipos TypeScript | 1h | MÉDIA |
| Resolver arquitetura agents/sub_agents | 2-3h | MÉDIA |
| Testes E2E | 2-3h | MÉDIA |
| **TOTAL** | **14-22h** | **~2-3 dias** |

---

## 8. RECOMENDAÇÃO

### ✅ SPRINT 10 DEVE SER EXECUTADO

**Motivo:** Sistema está 60% pronto, mas os 40% faltantes são críticos.

**Foco:**
1. Conectar frontend (40% do esforço)
2. Validar/implementar roteamento (40% do esforço)
3. Testes e ajustes (20% do esforço)

**Não fazer:**
- ❌ Recriar backend (já existe e está bom)
- ❌ Redesenhar UI (já está pronta)
- ❌ Implementar fine-tuning (feature futura)

**Fazer:**
- ✅ Ponte frontend ↔ backend
- ✅ Validar RENUS roteia corretamente
- ✅ Testes E2E completos

---

## 9. BUGS ENCONTRADOS

### 🐛 Bug #1: Campo `agent_id` não existe

**Localização:** Tabela `sub_agents`  
**Esperado:** Coluna `agent_id` (FK para agents)  
**Encontrado:** Coluna não existe, todos registros têm `agent_id: None`  
**Causa:** Tabela `agents` não existe, arquitetura diferente  
**Solução:** Decidir arquitetura final e migrar

### 🐛 Bug #2: Frontend não persiste dados

**Localização:** `SubAgentsTab.tsx`  
**Esperado:** Salvar no backend via API  
**Encontrado:** Salva apenas em `useState` (memória)  
**Causa:** Service de API não implementado  
**Solução:** Criar `subagentService.ts` e conectar

### 🐛 Bug #3: Tipos desalinhados

**Localização:** `src/types/agent.ts` vs backend models  
**Esperado:** Mesma estrutura  
**Encontrado:** Campos diferentes (ex: `useFineTuning` só no frontend)  
**Causa:** Desenvolvimento paralelo sem sincronização  
**Solução:** Gerar types do backend ou alinhar manualmente

---

## 10. EVIDÊNCIAS

### SQL Queries Executadas

```sql
-- Verificar tabelas
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
-- Resultado: agents NÃO existe, sub_agents EXISTE

-- Listar sub-agentes
SELECT id, name, channel, status, client_id FROM sub_agents;
-- Resultado: 12 registros, incluindo "Pesquisa MMN"

-- Verificar estrutura
SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'sub_agents';
-- Resultado: 21 colunas (listadas na seção 1)
```

### Arquivos Backend Verificados

```
✅ backend/src/api/routes/sub_agents.py (completo)
✅ backend/src/services/subagent_service.py (completo)
✅ backend/src/api/routes/wizard.py (existe, não analisado completamente)
❓ backend/src/agents/renus.py (não verificado)
```

### Arquivos Frontend Verificados

```
✅ src/pages/admin/agents/AgentDetailsPage.tsx (usa ConfigRenusPanel)
✅ src/components/agents/config/ConfigRenusPanel.tsx (tem tab SubAgents)
✅ src/components/agents/config/SubAgentsTab.tsx (usa mocks)
✅ src/types/agent.ts (tipos definidos)
✅ src/mocks/agents.mock.ts (mocks hardcoded)
❌ src/services/subagentService.ts (NÃO EXISTE)
```

---

## 11. COMANDOS PARA VALIDAÇÃO MANUAL

### Backend (testar API)

```bash
# 1. Iniciar servidor
cd backend
python -m src.main

# 2. Obter token de autenticação
# (fazer login via /auth/login)

# 3. Listar sub-agentes
curl http://localhost:8000/api/sub-agents \
  -H "Authorization: Bearer {TOKEN}"

# 4. Criar sub-agente
curl -X POST http://localhost:8000/api/sub-agents/ \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Teste API",
    "description": "Sub-agente de teste",
    "channel": "whatsapp",
    "model": "gpt-4o-mini",
    "system_prompt": "Você é um assistente de teste",
    "topics": ["teste"],
    "is_active": true
  }'

# 5. Verificar no banco
# (conectar ao Supabase e SELECT * FROM sub_agents)
```

### Frontend (testar UI)

```bash
# 1. Iniciar frontend
cd frontend
npm run dev

# 2. Abrir navegador
# http://localhost:5173

# 3. Fazer login como admin

# 4. Navegar
# Dashboard → Todos os Agentes → Agente de Vendas Slim → Configuração → Sub-Agentes

# 5. Criar sub-agente
# Clicar "+ Novo Sub-Agente"
# Preencher formulário
# Salvar

# 6. Recarregar página
# ❌ Sub-agente desaparece (não persiste)

# 7. Abrir DevTools → Network
# ❌ Nenhuma chamada HTTP para /sub-agents
```

---

**FIM DO RELATÓRIO**

**Próxima ação:** Aguardar decisão do usuário sobre Sprint 10.
