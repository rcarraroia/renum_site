# SPRINT 09 - DESIGN

## ARQUITETURA GERAL

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                          │
│  - ConversationsPage (WebSocket client)                     │
│  - AgentsPage (CRUD agents)                                 │
│  - SubAgentsPage (CRUD sub-agents)                          │
│  - WizardFlow (cria agents)                                 │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP + WebSocket + JWT
                     │
┌────────────────────▼────────────────────────────────────────┐
│                 BACKEND (FastAPI)                            │
│  - WebSocket Handler (/ws)                                  │
│  - Agents Routes (/agents)                                  │
│  - Sub-Agents Routes (/agents/{id}/sub-agents)             │
│  - Wizard Routes (/agents/wizard)                           │
│  - RENUS Orchestrator (carrega do banco)                    │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│              SUPABASE (PostgreSQL)                           │
│  - clients (empresas)                                        │
│  - agents (agentes principais) ← NOVA                        │
│  - sub_agents (especializações) ← ALTERADA                  │
│  - conversations (conversas)                                 │
│  - messages (mensagens)                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## PARTE 1: WEBSOCKET

### Arquitetura WebSocket

```
┌──────────────┐                    ┌──────────────┐
│   Client 1   │◄──────────────────►│   Client 2   │
│  (Browser)   │                    │  (Browser)   │
└──────┬───────┘                    └──────┬───────┘
       │                                   │
       │ WebSocket                         │ WebSocket
       │ ws://api/ws?token=JWT             │ ws://api/ws?token=JWT
       │                                   │
       └───────────────┬───────────────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │  ConnectionManager   │
            │  (Backend)           │
            │  - active_connections│
            │  - broadcast()       │
            │  - send_personal()   │
            └──────────┬───────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │   Message Handler    │
            │  - on_connect()      │
            │  - on_message()      │
            │  - on_disconnect()   │
            │  - on_typing()       │
            └──────────┬───────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │   Database           │
            │  - messages          │
            │  - conversations     │
            └──────────────────────┘
```

### Fluxo de Conexão

**1. Estabelecimento de Conexão:**
```
Client                          Backend
  │                               │
  ├─ GET /ws?token=JWT ──────────►│
  │                               ├─ Validate JWT
  │                               ├─ Extract user_id
  │                               ├─ Add to active_connections
  │◄─ 101 Switching Protocols ───┤
  │                               │
  ├─ Connected ───────────────────┤
  │                               │
  │◄─ {"type": "connected"} ──────┤
```

**2. Envio de Mensagem:**
```
Client 1                        Backend                         Client 2
  │                               │                               │
  ├─ {"type": "message"} ────────►│                               │
  │   {"content": "Olá"}          ├─ Save to DB                  │
  │                               ├─ Broadcast ──────────────────►│
  │                               │                               │
  │◄─ {"type": "message_sent"} ──┤                               │
  │                               │                               │
```

**3. Indicador de Digitação:**
```
Client 1                        Backend                         Client 2
  │                               │                               │
  ├─ {"type": "typing"} ─────────►│                               │
  │   {"conversation_id": "123"}  ├─ Broadcast ──────────────────►│
  │                               │                               │
  │                               │                               ├─ Show "typing..."
```

**4. Reconexão:**
```
Client                          Backend
  │                               │
  ├─ Connection Lost ─────────────┤
  │                               │
  ├─ Wait 1s                      │
  ├─ Retry GET /ws?token=JWT ────►│
  │                               ├─ Validate JWT
  │◄─ 101 Switching Protocols ───┤
  │                               │
  ├─ {"type": "sync"} ────────────►│
  │   {"last_message_id": "456"}  ├─ Query missed messages
  │◄─ {"type": "sync_data"} ──────┤
  │   {"messages": [...]}         │
```

### Estrutura de Mensagens WebSocket

**Tipos de Mensagens:**

```typescript
// Cliente → Servidor
type ClientMessage = 
  | { type: 'message', conversation_id: string, content: string }
  | { type: 'typing', conversation_id: string, is_typing: boolean }
  | { type: 'read', conversation_id: string, message_id: string }
  | { type: 'sync', last_message_id: string }
  | { type: 'ping' }

// Servidor → Cliente
type ServerMessage = 
  | { type: 'connected', user_id: string }
  | { type: 'message', message: Message }
  | { type: 'typing', user_id: string, conversation_id: string }
  | { type: 'presence', user_id: string, status: 'online' | 'offline' | 'away' }
  | { type: 'sync_data', messages: Message[] }
  | { type: 'error', error: string }
  | { type: 'pong' }
```

### Gerenciamento de Conexões

**ConnectionManager (Backend):**

```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_conversations: Dict[str, List[str]] = {}
    
    async def connect(self, user_id: str, websocket: WebSocket):
        """Adiciona conexão ativa"""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        await self.broadcast_presence(user_id, 'online')
    
    async def disconnect(self, user_id: str):
        """Remove conexão ativa"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        await self.broadcast_presence(user_id, 'offline')
    
    async def send_personal(self, user_id: str, message: dict):
        """Envia mensagem para usuário específico"""
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            await websocket.send_json(message)
    
    async def broadcast_to_conversation(self, conversation_id: str, message: dict):
        """Envia mensagem para todos participantes de uma conversa"""
        participants = await self.get_conversation_participants(conversation_id)
        for user_id in participants:
            await self.send_personal(user_id, message)
```

### Autenticação WebSocket

**Fluxo:**
1. Cliente obtém JWT token via login
2. Cliente conecta: `ws://api/ws?token=JWT_TOKEN`
3. Backend valida token
4. Se válido: aceita conexão
5. Se inválido: rejeita com 401

**Validação:**
```python
async def websocket_endpoint(websocket: WebSocket, token: str):
    try:
        # Decode JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        
        # Aceitar conexão
        await manager.connect(user_id, websocket)
        
        # Loop de mensagens
        while True:
            data = await websocket.receive_json()
            await handle_message(user_id, data)
            
    except JWTError:
        await websocket.close(code=1008, reason="Invalid token")
    except WebSocketDisconnect:
        await manager.disconnect(user_id)
```

---

## PARTE 2: ARQUITETURA AGENTS/SUB-AGENTS

### Estrutura de Tabelas

#### Tabela: agents (NOVA)

```sql
CREATE TABLE agents (
    -- Identificação
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    
    -- Informações Básicas
    name TEXT NOT NULL,
    description TEXT,
    slug TEXT UNIQUE NOT NULL,
    
    -- Configuração
    model TEXT NOT NULL DEFAULT 'gpt-4o-mini',
    system_prompt TEXT NOT NULL,
    channel TEXT NOT NULL DEFAULT 'whatsapp',
    template_type TEXT,
    
    -- Status e Publicação
    status TEXT NOT NULL DEFAULT 'draft', -- draft, active, inactive
    is_public BOOLEAN DEFAULT FALSE,
    public_url TEXT,
    
    -- Dados do Wizard
    config JSONB DEFAULT '{}',
    
    -- Métricas
    access_count INTEGER DEFAULT 0,
    
    -- Auditoria
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_agents_client_id ON agents(client_id);
CREATE INDEX idx_agents_status ON agents(status);
CREATE INDEX idx_agents_slug ON agents(slug);
CREATE INDEX idx_agents_is_public ON agents(is_public);

-- RLS
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;

-- Políticas
CREATE POLICY "Admins have full access to agents"
    ON agents FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );

CREATE POLICY "Clients can view own agents"
    ON agents FOR SELECT
    TO authenticated
    USING (
        client_id IN (
            SELECT id FROM clients
            WHERE clients.id = (
                SELECT client_id FROM profiles WHERE id = auth.uid()
            )
        )
    );

-- Trigger para updated_at
CREATE TRIGGER update_agents_updated_at
    BEFORE UPDATE ON agents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

#### Tabela: sub_agents (ALTERADA)

**Alterações Necessárias:**
1. Adicionar coluna `agent_id`
2. Remover coluna `client_id`
3. Atualizar RLS
4. Recriar índices

```sql
-- Adicionar nova coluna
ALTER TABLE sub_agents ADD COLUMN agent_id UUID REFERENCES agents(id) ON DELETE CASCADE;

-- Migrar dados (será feito em migration separada)
-- UPDATE sub_agents SET agent_id = (SELECT id FROM agents WHERE ...)

-- Remover coluna antiga
ALTER TABLE sub_agents DROP COLUMN client_id;

-- Tornar agent_id obrigatório
ALTER TABLE sub_agents ALTER COLUMN agent_id SET NOT NULL;

-- Recriar índices
DROP INDEX IF EXISTS idx_sub_agents_client_id;
CREATE INDEX idx_sub_agents_agent_id ON sub_agents(agent_id);

-- Atualizar RLS
DROP POLICY IF EXISTS "Clients can view own sub_agents" ON sub_agents;

CREATE POLICY "Users can view sub_agents of their agents"
    ON sub_agents FOR SELECT
    TO authenticated
    USING (
        agent_id IN (
            SELECT id FROM agents
            WHERE client_id IN (
                SELECT id FROM clients
                WHERE clients.id = (
                    SELECT client_id FROM profiles WHERE id = auth.uid()
                )
            )
        )
    );
```

### Migração de Dados

**Estratégia:**
1. Criar tabela `agents`
2. Copiar 12 registros de `sub_agents` para `agents`
3. Criar registros em `sub_agents` vazios (para manter estrutura)
4. Atualizar referências
5. Validar integridade

**Script de Migração:**

```sql
-- 1. Criar tabela agents (já feito acima)

-- 2. Copiar dados de sub_agents para agents
INSERT INTO agents (
    id,
    client_id,
    name,
    description,
    slug,
    model,
    system_prompt,
    channel,
    template_type,
    status,
    is_public,
    public_url,
    config,
    access_count,
    created_at,
    updated_at
)
SELECT 
    id,
    client_id,
    name,
    description,
    slug,
    model,
    system_prompt,
    channel,
    template_type,
    status,
    is_public,
    public_url,
    config,
    access_count,
    created_at,
    updated_at
FROM sub_agents
WHERE client_id IS NOT NULL; -- Apenas registros com client_id

-- 3. Limpar sub_agents (serão recriados conforme necessário)
DELETE FROM sub_agents WHERE client_id IS NOT NULL;

-- 4. Adicionar agent_id em sub_agents
ALTER TABLE sub_agents ADD COLUMN agent_id UUID REFERENCES agents(id) ON DELETE CASCADE;

-- 5. Remover client_id de sub_agents
ALTER TABLE sub_agents DROP COLUMN client_id;

-- 6. Validar
SELECT 
    (SELECT COUNT(*) FROM agents) as agents_count,
    (SELECT COUNT(*) FROM sub_agents) as sub_agents_count;
```

### RENUS Dinâmico

**Arquitetura Atual (Estática):**
```python
class RenusAgent:
    def __init__(self):
        self.sub_agents = {}  # Registry em memória
    
    def register_subagent(self, name, agent):
        """Registro manual"""
        self.sub_agents[name] = agent
```

**Arquitetura Nova (Dinâmica):**
```python
class RenusAgent:
    def __init__(self):
        self.agents = {}  # Registry de agents
        self.sync_interval = 60  # Sync a cada 60 segundos
        self.last_sync = None
    
    async def load_agents_from_db(self):
        """Carrega agents ativos do banco"""
        agents = await db.query(
            "SELECT * FROM agents WHERE status = 'active'"
        )
        
        for agent_data in agents:
            agent_id = agent_data['id']
            
            # Carregar sub-agents do agent
            sub_agents = await db.query(
                "SELECT * FROM sub_agents WHERE agent_id = %s AND is_active = true",
                agent_id
            )
            
            # Criar instância do agent
            agent = self._create_agent_instance(agent_data, sub_agents)
            self.agents[agent_id] = agent
    
    async def sync_agents(self):
        """Sincroniza agents periodicamente"""
        if self.last_sync and (time.now() - self.last_sync) < self.sync_interval:
            return
        
        await self.load_agents_from_db()
        self.last_sync = time.now()
    
    async def route_message(self, message, agent_id):
        """Roteia mensagem para agent/sub-agent apropriado"""
        # Sync se necessário
        await self.sync_agents()
        
        # Buscar agent
        agent = self.agents.get(agent_id)
        if not agent:
            raise AgentNotFoundError(f"Agent {agent_id} not found")
        
        # Analisar tópico da mensagem
        topic = await self._analyze_topic(message)
        
        # Buscar sub-agent com tópico correspondente
        sub_agent = agent.find_subagent_by_topic(topic)
        
        if sub_agent:
            # Rotear para sub-agent
            return await sub_agent.process(message)
        else:
            # Processar com agent principal
            return await agent.process(message)
```

### Roteamento por Tópicos

**Estrutura de Tópicos:**

```python
# Sub-agent com tópicos
sub_agent = {
    "id": "uuid",
    "name": "Cobrança",
    "topics": ["pagamento", "cobrança", "fatura", "comissão", "dinheiro"],
    "system_prompt": "Você é especialista em cobrança..."
}

# Análise de tópico
def analyze_topic(message: str) -> str:
    """Extrai tópico principal da mensagem"""
    # Usar LLM para análise
    prompt = f"""
    Analise a mensagem abaixo e identifique o tópico principal.
    Retorne apenas uma palavra-chave.
    
    Mensagem: {message}
    
    Tópico:
    """
    
    topic = llm.generate(prompt)
    return topic.strip().lower()

# Matching de tópico
def find_subagent_by_topic(agent, topic: str):
    """Encontra sub-agent com tópico correspondente"""
    for sub_agent in agent.sub_agents:
        if topic in sub_agent.topics:
            return sub_agent
    return None
```

### Fluxos Principais

#### Fluxo 1: Criação de Agent via Wizard

```
1. Admin clica "Criar Agente"
   ↓
2. POST /agents/wizard/start
   → Cria registro em agents (status='draft')
   → Retorna wizard_id (= agent.id)
   ↓
3. Admin preenche Step 1 (nome, template, nicho)
   ↓
4. PUT /agents/wizard/{id}/step/1
   → Salva em agents.config.step_1_data
   ↓
5. Admin preenche Step 2 (personalidade, tom)
   ↓
6. PUT /agents/wizard/{id}/step/2
   → Salva em agents.config.step_2_data
   → Gera system_prompt baseado em personalidade
   ↓
7. Admin preenche Step 3 (campos customizados)
   ↓
8. PUT /agents/wizard/{id}/step/3
   → Salva em agents.config.step_3_data
   ↓
9. Admin preenche Step 4 (integrações)
   ↓
10. PUT /agents/wizard/{id}/step/4
    → Salva em agents.config.step_4_data
    ↓
11. Admin testa no Sandbox
    ↓
12. POST /agents/wizard/{id}/publish
    → Muda status para 'active'
    → Gera slug único
    → Gera public_url
    → Gera QR code
    → Retorna dados de publicação
    ↓
13. RENUS detecta novo agent (sync)
    → Carrega agent do banco
    → Adiciona ao registry
    ↓
14. Agent está pronto para receber mensagens
```

#### Fluxo 2: Criação de Sub-Agent

```
1. Admin acessa agent existente
   ↓
2. Admin clica "Adicionar Sub-Agent"
   ↓
3. Admin preenche formulário:
   - Nome: "Cobrança"
   - Tópicos: ["pagamento", "cobrança", "fatura"]
   - System Prompt: "Você é especialista em..."
   - Model: "gpt-4o-mini"
   ↓
4. POST /agents/{agent_id}/sub-agents
   → Valida agent_id existe
   → Cria registro em sub_agents
   → Retorna sub_agent criado
   ↓
5. RENUS detecta novo sub-agent (sync)
   → Carrega sub-agent do banco
   → Adiciona ao agent correspondente
   ↓
6. Sub-agent está pronto para roteamento
```

#### Fluxo 3: Roteamento de Mensagem

```
1. Mensagem chega: "Quanto vou receber de comissão?"
   ↓
2. RENUS recebe mensagem
   ↓
3. RENUS identifica agent_id da conversa
   ↓
4. RENUS carrega agent do registry
   ↓
5. RENUS analisa tópico da mensagem
   → LLM extrai: "comissão"
   ↓
6. RENUS busca sub-agent com tópico "comissão"
   → Encontra: Sub-Agent "Cobrança"
   ↓
7. RENUS roteia para Sub-Agent "Cobrança"
   ↓
8. Sub-Agent processa mensagem
   → Usa system_prompt especializado
   → Gera resposta sobre comissões
   ↓
9. Sub-Agent retorna resposta
   ↓
10. RENUS envia resposta ao usuário
```

---

## ESTRUTURA DE DADOS

### Agent (Tabela agents)

```typescript
interface Agent {
  // Identificação
  id: string;
  client_id: string;
  
  // Informações
  name: string;
  description?: string;
  slug: string;
  
  // Configuração
  model: string;
  system_prompt: string;
  channel: 'whatsapp' | 'web' | 'sms' | 'email';
  template_type?: string;
  
  // Status
  status: 'draft' | 'active' | 'inactive';
  is_public: boolean;
  public_url?: string;
  
  // Wizard Data
  config: {
    step_1_data?: WizardStep1Data;
    step_2_data?: WizardStep2Data;
    step_3_data?: WizardStep3Data;
    step_4_data?: WizardStep4Data;
  };
  
  // Métricas
  access_count: number;
  
  // Auditoria
  created_at: string;
  updated_at: string;
}
```

### Sub-Agent (Tabela sub_agents)

```typescript
interface SubAgent {
  // Identificação
  id: string;
  agent_id: string; // FK para agents
  
  // Informações
  name: string;
  description?: string;
  
  // Roteamento
  topics: string[]; // ["pagamento", "cobrança", "fatura"]
  
  // Configuração
  model: string;
  system_prompt: string;
  channel: string;
  
  // Status
  is_active: boolean;
  
  // Configuração Avançada
  fine_tuning_config?: any;
  knowledge_base?: any;
  
  // Auditoria
  created_at: string;
  updated_at: string;
}
```

---

## ERROR HANDLING

### WebSocket Errors

**Erro: Token Inválido**
```json
{
  "type": "error",
  "error": "Invalid or expired token",
  "code": "AUTH_ERROR"
}
```
**Ação:** Cliente deve fazer logout e login novamente

**Erro: Conexão Perdida**
```json
{
  "type": "error",
  "error": "Connection lost",
  "code": "CONNECTION_ERROR"
}
```
**Ação:** Cliente tenta reconectar automaticamente

**Erro: Mensagem Inválida**
```json
{
  "type": "error",
  "error": "Invalid message format",
  "code": "VALIDATION_ERROR"
}
```
**Ação:** Cliente loga erro e notifica usuário

### Agent/Sub-Agent Errors

**Erro: Agent Não Encontrado**
```json
{
  "error": "Agent not found",
  "agent_id": "uuid",
  "code": "AGENT_NOT_FOUND"
}
```
**Ação:** Retornar 404

**Erro: Sub-Agent Sem Agent**
```json
{
  "error": "Cannot create sub-agent without valid agent_id",
  "code": "INVALID_AGENT_ID"
}
```
**Ação:** Retornar 400

**Erro: Roteamento Falhou**
```json
{
  "error": "Failed to route message",
  "reason": "No matching sub-agent found",
  "code": "ROUTING_ERROR"
}
```
**Ação:** Fallback para agent principal

---

## TESTING STRATEGY

### WebSocket Tests

**Unit Tests:**
- ConnectionManager.connect()
- ConnectionManager.disconnect()
- ConnectionManager.broadcast()
- Message validation
- Token validation

**Integration Tests:**
- Conexão com token válido
- Rejeição com token inválido
- Envio de mensagem
- Broadcast para múltiplos clientes
- Reconexão automática

### Agent/Sub-Agent Tests

**Unit Tests:**
- Agent creation
- Sub-agent creation
- Topic matching
- Routing logic
- RENUS sync

**Integration Tests:**
- Wizard cria agent em agents
- Sub-agent criado com agent_id correto
- RENUS carrega do banco
- Roteamento end-to-end
- Migration de dados

---

**Versão:** 1.0  
**Data:** 2025-12-06  
**Responsável:** Kiro (Agente de IA)
