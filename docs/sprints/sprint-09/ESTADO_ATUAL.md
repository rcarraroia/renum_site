# ESTADO ATUAL DO SISTEMA - SPRINT 09

**Data da Verificação:** 2025-12-06 21:27:06

---

## 1. BANCO DE DADOS (Supabase)

### Tabela: agents
- **Status:** ❌ NÃO EXISTE
- **Erro:** "Could not find the table 'public.agents' in the schema cache"
- **Hint do Supabase:** "Perhaps you meant the table 'public.sub_agents'"
- **Conclusão:** A tabela `agents` nunca foi criada. O sistema usa apenas `sub_agents`.

### Tabela: sub_agents
- **Status:** ✅ EXISTE
- **Registros:** 12 agentes criados
- **FK Atual:** `client_id` (UUID, nullable)
- **Estrutura Completa:**
  ```
  - id (UUID, PK)
  - config_id (UUID, nullable)
  - name (text)
  - description (text)
  - channel (text) - valores: 'whatsapp', 'site'
  - system_prompt (text)
  - topics (array)
  - is_active (boolean)
  - model (text) - valores: 'gpt-4o-mini', etc
  - fine_tuning_config (jsonb)
  - created_at (timestamp)
  - updated_at (timestamp)
  - slug (text)
  - public_url (text)
  - access_count (integer)
  - is_public (boolean)
  - knowledge_base (jsonb)
  - client_id (UUID, nullable) ← FK para clients
  - template_type (text) - valores: 'custom', 'customer_service'
  - status (text) - valores: 'draft', 'active'
  - config (jsonb)
  ```

**Exemplo de Registro:**
```json
{
  "id": "c58025e3-4751-45e0-96e6-e760fdb57dde",
  "name": "Discovery Agent",
  "description": "Agente especializado em conduzir entrevistas...",
  "channel": "whatsapp",
  "system_prompt": "Você é o Discovery Agent...",
  "topics": ["entrevistas", "pesquisas", "levantamento de requisitos"],
  "is_active": true,
  "model": "gpt-4o-mini",
  "slug": "discovery-agent",
  "public_url": "/chat/discovery-agent",
  "access_count": 3,
  "is_public": true,
  "client_id": null,
  "template_type": "custom",
  "status": "draft"
}
```

**Observação Crítica:** 
- Atualmente `sub_agents` tem FK `client_id` (para clients)
- Não tem FK `agent_id` (porque tabela agents não existe)
- Isso significa que `sub_agents` está sendo usado como tabela principal de agentes

### Tabela: conversations
- **Status:** ✅ EXISTE
- **Registros:** 1
- **Estrutura:**
  ```
  - id (UUID, PK)
  - client_id (UUID, FK → clients)
  - status (text) - valores: 'active'
  - channel (text) - valores: 'whatsapp'
  - assigned_agent_id (UUID, nullable)
  - unread_count (integer)
  - priority (text) - valores: 'Medium'
  - start_date (timestamp)
  - last_update (timestamp)
  - summary (text, nullable)
  - tags (array)
  - created_at (timestamp)
  - updated_at (timestamp)
  ```

**Observação:** Campo `channel` existe e tem valores como 'whatsapp'

### Tabela: messages
- **Status:** ✅ EXISTE
- **Registros:** 1
- **Estrutura:**
  ```
  - id (UUID, PK)
  - conversation_id (UUID, FK → conversations)
  - sender (text) - valores: 'client'
  - type (text) - valores: 'text'
  - content (text)
  - timestamp (timestamp)
  - is_read (boolean)
  - metadata (jsonb, nullable)
  - created_at (timestamp)
  - channel (text, nullable)
  ```

**Observação:** FK para `conversation_id` existe e funciona

### Tabela: clients
- **Status:** ✅ EXISTE
- **Registros:** 4
- **Estrutura:**
  ```
  - id (UUID, PK)
  - company_name (text)
  - document (text, nullable)
  - website (text, nullable)
  - segment (text)
  - status (text) - valores: 'active'
  - contact (jsonb, nullable)
  - address (jsonb, nullable)
  - last_interaction (timestamp, nullable)
  - tags (array, nullable)
  - notes (text, nullable)
  - created_at (timestamp)
  - updated_at (timestamp)
  ```

### Tabela: leads
- **Status:** ✅ EXISTE
- **Registros:** 1
- **Estrutura:**
  ```
  - id (UUID, PK)
  - name (text)
  - phone (text)
  - email (text)
  - source (text)
  - status (text)
  - subagent_id (UUID, nullable)
  - first_contact_at (timestamp)
  - last_interaction_at (timestamp)
  - notes (text, nullable)
  - score (integer, nullable)
  - created_at (timestamp)
  - updated_at (timestamp)
  ```

**Observação:** Tem campo `subagent_id` (FK para sub_agents)

### Tabela: profiles
- **Status:** ✅ EXISTE
- **Registros:** 2 (Admin Renum, Kiro Auditoria)
- **Estrutura:**
  ```
  - id (UUID, PK)
  - first_name (text)
  - last_name (text)
  - role (text) - valores: 'admin'
  - avatar_url (text, nullable)
  - updated_at (timestamp)
  - email (text)
  - created_at (timestamp)
  ```

### Tabela: projects
- **Status:** ✅ EXISTE
- **Registros:** 1
- **Estrutura:**
  ```
  - id (UUID, PK)
  - name (text)
  - client_id (UUID, nullable, FK → clients)
  - status (text)
  - type (text)
  - start_date (timestamp, nullable)
  - due_date (timestamp, nullable)
  - progress (integer)
  - responsible_id (UUID, nullable)
  - budget (numeric, nullable)
  - description (text, nullable)
  - scope (text, nullable)
  - created_at (timestamp)
  - updated_at (timestamp)
  ```

### Tabela: renus_config
- **Status:** ✅ EXISTE
- **Registros:** 0 (vazia)
- **Estrutura:** Não pode ser inferida (sem dados)

### Tabela: tools
- **Status:** ✅ EXISTE
- **Registros:** 0 (vazia)
- **Estrutura:** Não pode ser inferida (sem dados)

---

## 2. BACKEND (Python/FastAPI)

### Routes

#### ✅ backend/src/api/routes/sub_agents.py
**Status:** EXISTE e COMPLETO

**Endpoints Implementados:**
- `GET /sub-agents` - Listar sub-agents
- `GET /sub-agents/{id}` - Buscar por ID
- `POST /sub-agents/` - Criar sub-agent
- `PUT /sub-agents/{id}` - Atualizar sub-agent
- `DELETE /sub-agents/{id}` - Deletar sub-agent
- `PATCH /sub-agents/{id}/toggle` - Ativar/desativar
- `GET /sub-agents/{id}/stats` - Estatísticas de uso

**Observações:**
- Todos os endpoints funcionam com `sub_agents` (não `agents`)
- Usa `SubAgentService` para lógica de negócio
- Tem autenticação e autorização (apenas admins podem criar/editar)

#### ❌ backend/src/api/routes/agents.py
**Status:** NÃO EXISTE

**Conclusão:** Não há rota separada para `agents`. O sistema usa apenas `sub_agents`.

#### ✅ backend/src/api/routes/conversations.py
**Status:** EXISTE

#### ✅ backend/src/api/routes/websocket.py
**Status:** EXISTE

#### ✅ backend/src/api/routes/wizard.py
**Status:** EXISTE e COMPLETO

**Endpoints Implementados:**
- `POST /agents/wizard/start` - Iniciar wizard
- `GET /agents/wizard/{id}` - Buscar sessão
- `PUT /agents/wizard/{id}/step/{step}` - Salvar passo
- `DELETE /agents/wizard/{id}` - Deletar sessão
- `GET /agents/wizard/templates/list` - Listar templates
- `GET /agents/wizard/templates/{type}` - Buscar template
- `POST /agents/wizard/{id}/sandbox/start` - Iniciar sandbox
- `POST /agents/wizard/{id}/sandbox/message` - Enviar mensagem sandbox
- `GET /agents/wizard/{id}/sandbox/history` - Histórico sandbox
- `GET /agents/wizard/{id}/sandbox/data` - Dados coletados
- `DELETE /agents/wizard/{id}/sandbox` - Limpar sandbox
- `POST /agents/wizard/{id}/publish` - Publicar agente

**Observação:** Wizard salva em `sub_agents` (não em `agents`)

### Services

#### ✅ backend/src/services/subagent_service.py
**Status:** EXISTE e COMPLETO

**Funções Principais:**
- `create_subagent(data)` - Criar sub-agent
- `get_subagent(id)` - Buscar por ID
- `list_subagents(filters)` - Listar com filtros
- `update_subagent(id, data)` - Atualizar
- `delete_subagent(id)` - Deletar
- `toggle_active(id)` - Ativar/desativar
- `get_stats(id)` - Estatísticas
- `get_by_slug(slug)` - Buscar por slug
- `increment_access_count(id)` - Incrementar contador
- `list_public_agents()` - Listar públicos
- `generate_public_url(id, base_url)` - Gerar URL pública

**Observações:**
- Trabalha diretamente com tabela `sub_agents`
- Não há referência a tabela `agents`
- Validações completas implementadas

#### ❌ backend/src/services/agent_service.py
**Status:** NÃO EXISTE

**Conclusão:** Não há service separado para `agents`.

#### ✅ backend/src/services/conversation_service.py
**Status:** EXISTE

#### ✅ backend/src/services/wizard_service.py
**Status:** EXISTE

**Como Funciona:**
- Cria registro em `sub_agents` com `status='draft'`
- Salva dados do wizard em campos `config`, `step_1_data`, etc
- Ao publicar, muda `status='active'` e gera URL pública

### Models

#### ✅ backend/src/models/sub_agent.py
**Status:** EXISTE (inferido pelo uso em routes/services)

**Classes Pydantic:**
- `SubAgentCreate` - Para criação
- `SubAgentUpdate` - Para atualização
- `SubAgentResponse` - Para resposta

#### ❌ backend/src/models/agent.py
**Status:** NÃO EXISTE

#### ✅ backend/src/models/conversation.py
**Status:** EXISTE (inferido)

#### ✅ backend/src/models/message.py
**Status:** EXISTE (inferido)

### Agents (RENUS)

#### ✅ backend/src/agents/renus.py
**Status:** EXISTE e IMPLEMENTADO

**Estrutura Atual:**
```python
class RenusAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(...)
        self.sub_agents: Dict[str, Any] = {}  # Registry em memória
    
    def register_subagent(self, name: str, agent: Any) -> None:
        """Registra sub-agent no registry em memória"""
        self.sub_agents[name] = agent
    
    def list_subagents(self) -> List[str]:
        """Lista sub-agents registrados"""
        return list(self.sub_agents.keys())
    
    async def _route_to_subagent(self, state: Dict) -> Dict:
        """Roteia para sub-agent apropriado"""
        target = state.get("target_subagent")
        if target in self.sub_agents:
            sub_agent = self.sub_agents[target]
            # Invoca sub-agent...
```

**Como Carrega Sub-agents Atualmente:**
- Registry **EM MEMÓRIA** (`self.sub_agents = {}`)
- Sub-agents são registrados manualmente via `register_subagent()`
- **NÃO consulta banco de dados** para carregar sub-agents
- **NÃO carrega dinamicamente** de `sub_agents` table

**Função de Roteamento:**
- `_analyze_intent()` - Analisa intenção da mensagem
- `_should_route()` - Decide se roteia ou responde direto
- `_route_to_subagent()` - Roteia para sub-agent registrado
- `_generate_response()` - Gera resposta final

**Problema Identificado:**
- RENUS não carrega sub-agents do banco automaticamente
- Sub-agents precisam ser registrados manualmente no código
- Não há integração dinâmica com tabela `sub_agents`

#### ✅ backend/src/agents/discovery_agent.py
**Status:** EXISTE (sub-agent específico)

#### ✅ backend/src/agents/mmn_agent_simple.py
**Status:** EXISTE (sub-agent específico)

### WebSocket

#### ✅ backend/src/websocket/
**Status:** EXISTE (inferido pela rota)

**Arquivos Esperados:**
- `connection_manager.py` - Gerenciamento de conexões
- `handlers.py` - Handlers de mensagens

**Estado:** Implementado no Sprint 03 (validado em Sprint 05b)

---

## 3. FRONTEND (React/TypeScript)

### Services

#### ❌ src/services/agentService.ts
**Status:** NÃO EXISTE

**Conclusão:** Não há service dedicado para `agents`. Wizard usa `wizardService.ts`.

#### ❌ src/services/subAgentService.ts
**Status:** NÃO EXISTE

**Conclusão:** Não há service dedicado para `sub_agents`.

#### ✅ src/services/conversationService.ts
**Status:** EXISTE

#### ✅ src/services/wizardService.ts
**Status:** EXISTE e COMPLETO

**Funções Principais:**
- `startWizard(clientId)` - Iniciar wizard
- `saveStep(wizardId, stepNumber, data)` - Salvar passo
- `getWizard(wizardId)` - Buscar sessão
- `deleteWizard(wizardId)` - Deletar sessão
- `listTemplates()` - Listar templates
- `getTemplate(templateType)` - Buscar template
- `startSandbox(wizardId)` - Iniciar sandbox
- `sendSandboxMessage(wizardId, message)` - Enviar mensagem
- `getSandboxHistory(wizardId)` - Histórico
- `getSandboxData(wizardId)` - Dados coletados
- `cleanupSandbox(wizardId)` - Limpar sandbox
- `publishAgent(wizardId)` - Publicar agente

**Observação:** Chama endpoints `/agents/wizard/*` que salvam em `sub_agents`

### Types

#### ✅ src/types/agent.ts
**Status:** EXISTE

**Interfaces Definidas:**
```typescript
export interface Agent {
  id: string;
  name: string;
  description: string;
  client_id: string;
  project_id: string;
  type: AgentType;
  category: AgentCategory;
  slug: string;
  domain: string;
  channel: AgentChannel[];
  model: string;
  status: AgentStatus;
  instances_count: number;
  conversations_today: number;
  created_at: string;
  version: string;
}

// Wizard Types
export interface WizardStep1Data { ... }
export interface WizardStep2Data { ... }
export interface WizardStep3Data { ... }
export interface WizardStep4Data { ... }
export interface WizardFormData { ... }
export interface PublicationResult { ... }
```

**Observação:** 
- Interface `Agent` existe mas não corresponde à estrutura real de `sub_agents`
- Campos como `project_id`, `domain`, `instances_count` não existem em `sub_agents`
- Falta interface `SubAgent` que corresponda à estrutura real

#### ❌ src/types/subAgent.ts
**Status:** NÃO EXISTE

#### ✅ src/types/conversation.ts
**Status:** EXISTE

#### ✅ src/types/message.ts
**Status:** EXISTE (inferido)

### Components/Pages

#### ❌ src/components/agents/
**Status:** NÃO EXISTE

#### ✅ src/components/wizard/
**Status:** EXISTE (implementado no Sprint 06)

#### ❌ src/pages/agents/
**Status:** NÃO EXISTE

#### ✅ src/pages/wizard/
**Status:** EXISTE (implementado no Sprint 06)

#### ✅ src/pages/conversations/
**Status:** EXISTE (implementado no Sprint 03)

### Hooks

#### ❌ src/hooks/useWebSocket.ts
**Status:** PRECISA VERIFICAR (implementado no Sprint 03)

---

## 4. WIZARD - COMO FUNCIONA ATUALMENTE

### Backend (wizard_service.py)

**Fluxo de Criação:**
1. `POST /agents/wizard/start` → Cria registro em `sub_agents` com `status='draft'`
2. `PUT /agents/wizard/{id}/step/{step}` → Salva dados em campos `step_X_data` ou `config`
3. `POST /agents/wizard/{id}/publish` → Muda `status='active'`, gera `slug`, `public_url`, `qr_code`

**Onde Salva:**
- Tabela: `sub_agents`
- Campos usados:
  - `name` - Nome do agente (Step 1)
  - `description` - Descrição (Step 1)
  - `template_type` - Tipo de template (Step 1)
  - `system_prompt` - Gerado a partir de Step 2 (personalidade)
  - `config` - JSON com todos os dados do wizard
  - `status` - 'draft' durante wizard, 'active' após publicar
  - `slug` - Gerado ao publicar
  - `public_url` - Gerado ao publicar
  - `client_id` - ID do cliente

**Estrutura de Dados:**
```json
{
  "id": "uuid",
  "name": "Agente de Vendas",
  "description": "Agente para qualificação de leads",
  "template_type": "sales",
  "status": "draft",
  "config": {
    "step_1_data": {
      "template_type": "sales",
      "name": "Agente de Vendas",
      "description": "...",
      "niche": "ecommerce"
    },
    "step_2_data": {
      "personality": "friendly",
      "tone_formal": 50,
      "tone_direct": 70,
      "custom_instructions": "..."
    },
    "step_3_data": {
      "standard_fields": {...},
      "custom_fields": [...]
    },
    "step_4_data": {
      "integrations": {...}
    }
  },
  "client_id": "uuid",
  "created_at": "...",
  "updated_at": "..."
}
```

### Frontend (wizardService.ts)

**Fluxo:**
1. Usuário clica "Criar Agente"
2. `wizardService.startWizard(clientId)` → Chama backend
3. Backend retorna `wizard_id` (que é o `id` do registro em `sub_agents`)
4. Usuário preenche steps
5. `wizardService.saveStep(wizardId, stepNumber, data)` → Salva cada step
6. Usuário testa no sandbox
7. `wizardService.publishAgent(wizardId)` → Publica agente

**Endpoints Chamados:**
- `POST /agents/wizard/start`
- `PUT /agents/wizard/{id}/step/{step}`
- `POST /agents/wizard/{id}/publish`

---

## 5. GAPS IDENTIFICADOS

### Criar

#### Banco de Dados
- [ ] **Tabela `agents`** - Tabela principal de agentes (se necessário)
  - Decisão: Criar ou continuar usando apenas `sub_agents`?

#### Backend - Routes
- [ ] **agents.py** - Endpoints CRUD para agents (se criar tabela agents)
  - `GET /agents` - Listar agents
  - `GET /agents/{id}` - Buscar por ID
  - `POST /agents` - Criar agent
  - `PUT /agents/{id}` - Atualizar agent
  - `DELETE /agents/{id}` - Deletar agent

#### Backend - Services
- [ ] **agent_service.py** - Lógica de negócio para agents (se criar tabela agents)

#### Backend - Models
- [ ] **agent.py** - Pydantic models para agents (se criar tabela agents)

#### Frontend - Services
- [ ] **agentService.ts** - API calls para agents
- [ ] **subAgentService.ts** - API calls para sub-agents (se separar)

#### Frontend - Types
- [ ] **subAgent.ts** - Interface TypeScript para SubAgent
  - Deve corresponder à estrutura real de `sub_agents` no banco

#### Frontend - Components/Pages
- [ ] **src/pages/agents/** - Páginas de listagem/gerenciamento de agents
- [ ] **src/components/agents/** - Componentes de agents

### Modificar

#### Banco de Dados
- [ ] **sub_agents.client_id → sub_agents.agent_id** (se criar tabela agents)
  - Mudar FK de `client_id` para `agent_id`
  - Adicionar migration para alterar estrutura
  - Atualizar dados existentes

#### Backend - RENUS
- [ ] **renus.py - Carregamento de sub-agents**
  - Mudar de registry em memória para consulta dinâmica ao banco
  - Implementar `load_subagents_from_db()`
  - Atualizar `_route_to_subagent()` para usar dados do banco
  - Adicionar cache para performance

#### Backend - Services
- [ ] **subagent_service.py**
  - Atualizar para trabalhar com nova estrutura (se mudar FK)
  - Adicionar métodos para integração com RENUS

#### Frontend - Types
- [ ] **agent.ts**
  - Atualizar interface `Agent` para corresponder à estrutura real
  - Remover campos que não existem (`project_id`, `domain`, `instances_count`)
  - Adicionar campos que existem (`slug`, `public_url`, `access_count`, etc)

### Deletar
- [ ] **Código duplicado** (se houver)
- [ ] **Mocks antigos** (se houver)
- [ ] **Imports não utilizados**

---

## 6. RECOMENDAÇÕES

### Decisão Crítica: Criar tabela `agents` ou não?

#### Opção A: Criar tabela `agents` (Arquitetura Original)
**Estrutura:**
```
agents (1:N) → sub_agents
```

**Vantagens:**
- Separação clara entre agente principal e especializações
- Permite múltiplos sub-agents por agent
- Alinhado com documentação original (product.md, structure.md)
- Escalável para futuro

**Desvantagens:**
- Requer migration complexa
- Precisa migrar dados existentes de `sub_agents`
- Mais trabalho de implementação
- Risco de quebrar código existente

**Impacto:**
- Alto: Requer mudanças em banco, backend e frontend
- Tempo estimado: 8-12 horas

#### Opção B: Continuar com apenas `sub_agents` (Estado Atual)
**Estrutura:**
```
sub_agents (standalone)
```

**Vantagens:**
- Nenhuma migration necessária
- Código existente continua funcionando
- Implementação mais rápida
- Menor risco

**Desvantagens:**
- Não alinhado com documentação original
- Nomenclatura confusa (`sub_agents` sem `agents`)
- Menos escalável
- Pode precisar refatorar no futuro

**Impacto:**
- Baixo: Apenas ajustes de nomenclatura e documentação
- Tempo estimado: 2-4 horas

### Recomendação Final

**Recomendo Opção B (Continuar com `sub_agents`)** pelos seguintes motivos:

1. **Sistema já funciona:** 12 agentes criados, wizard funcionando, publicação funcionando
2. **Menor risco:** Não quebra código existente
3. **Mais rápido:** Sprint 09 pode focar em melhorias, não em refatoração
4. **Pode refatorar depois:** Se necessário, criar `agents` em sprint futuro

**Ajustes Necessários (Opção B):**
1. Renomear `sub_agents` para `agents` (apenas nomenclatura)
2. Atualizar documentação para refletir estrutura real
3. Implementar carregamento dinâmico no RENUS
4. Criar interfaces TypeScript corretas no frontend

---

## 7. PRÓXIMOS PASSOS SUGERIDOS

### Se escolher Opção A (Criar `agents`):
1. Criar migration para tabela `agents`
2. Migrar dados de `sub_agents` para `agents`
3. Adicionar FK `agent_id` em `sub_agents`
4. Atualizar todos os services e routes
5. Atualizar frontend
6. Testar extensivamente

### Se escolher Opção B (Continuar com `sub_agents`):
1. Atualizar RENUS para carregar de `sub_agents` dinamicamente
2. Criar `agentService.ts` no frontend (que chama `/sub-agents`)
3. Criar interface `SubAgent` correta no frontend
4. Atualizar documentação (product.md, structure.md)
5. Implementar páginas de listagem/gerenciamento
6. Testar integração RENUS + sub-agents

---

## 8. RISCOS IDENTIFICADOS

### Risco Alto
- **Criar tabela `agents` pode quebrar wizard:** Wizard salva em `sub_agents`, precisaria atualizar
- **Migration de dados pode falhar:** 12 registros existentes precisam ser migrados
- **RENUS pode não rotear corretamente:** Carregamento dinâmico precisa ser bem testado

### Risco Médio
- **Nomenclatura confusa:** `sub_agents` sem `agents` pode confundir desenvolvedores
- **Documentação desatualizada:** Docs falam de `agents` mas sistema usa `sub_agents`
- **Frontend desalinhado:** Interface `Agent` não corresponde à estrutura real

### Risco Baixo
- **Performance:** Carregar sub-agents do banco pode ser lento (mitigado com cache)
- **Testes:** Código existente pode não ter testes suficientes

---

## 9. CONCLUSÃO

**Estado Atual:**
- Sistema funciona com apenas `sub_agents` (sem tabela `agents`)
- Wizard cria agentes em `sub_agents` com sucesso
- RENUS usa registry em memória (não carrega do banco)
- Frontend tem interfaces desatualizadas

**Decisão Necessária:**
- Criar tabela `agents` (Opção A) ou continuar com `sub_agents` (Opção B)?

**Recomendação:**
- **Opção B** (continuar com `sub_agents`) para Sprint 09
- Focar em melhorias e integração dinâmica
- Deixar refatoração para `agents` em sprint futuro (se necessário)

**Próximo Passo:**
- Aguardar decisão do usuário (Renato) sobre qual opção seguir
- Criar SPEC baseada na opção escolhida

---

**Verificação Completa:** ✅  
**Documento Criado:** 2025-12-06 21:30:00  
**Responsável:** Kiro (Agente de IA)
