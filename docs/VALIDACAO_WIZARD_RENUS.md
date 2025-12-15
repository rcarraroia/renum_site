# VALIDAÇÃO: WIZARD E RENUS

**Data:** 2025-12-05 19:46  
**Executor:** Kiro  
**Tempo:** 45 minutos  
**Modo:** Análise de código + Validação de banco

---

## PARTE 1: WIZARD

### Estado do Banco (PRÉ-TESTE)

```
📊 sub_agents: 12 registros
📊 renus_config: 0 registros
```

**Últimos 3 registros em sub_agents:**
```
ID: e6a00620-0e8e-4a46-998b-124dc021ff53
Nome: Test Agent Sprint 06
Template: customer_service
Status: active
Criado: 2025-12-05T01:29:17

ID: 902a6904-8682-45cd-ba1f-09559e34e1f0
Nome: Test Agent Sprint 06
Template: customer_service
Status: active
Criado: 2025-12-05T01:28:30

ID: 37ae9902-24bf-42b1-9d01-88c201ee0a6c
Nome: Test Agent Sprint 06
Template: customer_service
Status: active
Criado: 2025-12-05T01:27:30
```

**Observação:** Já existem agentes criados via Wizard (Test Agent Sprint 06)

---

### Análise do Código Backend

#### Arquivo: `backend/src/services/wizard_service.py`

**Função: `start_wizard()`**

```python
def start_wizard(self, client_id: UUID) -> WizardSession:
    """Create new wizard session"""
    
    wizard_id = uuid4()
    
    # ✅ CONFIRMADO: Salva em sub_agents com status='draft'
    wizard_data = {
        'id': str(wizard_id),
        'client_id': str(client_id),
        'name': f'Draft Agent {wizard_id.hex[:8]}',
        'status': 'draft',  # ← Status especial para wizard
        'template_type': 'custom',
        'is_active': False,
        'config': {
            'wizard_session': True,  # ← Flag de wizard
            'current_step': 1,
            'step_1_data': None,
            'step_2_data': None,
            'step_3_data': None,
            'step_4_data': None,
        },
        # ...
    }
    
    # Insere em sub_agents
    result = self.supabase.table('sub_agents').insert(wizard_data).execute()
```

**Função: `save_step()`**

```python
def save_step(self, wizard_id: UUID, step_number: int, data: Dict) -> WizardSession:
    """Save progress for a specific step"""
    
    # Busca registro draft
    result = self.supabase.table('sub_agents')\
        .select('*')\
        .eq('id', str(wizard_id))\
        .eq('status', 'draft')\  # ← Filtra por draft
        .single()\
        .execute()
    
    # Atualiza config com dados do step
    current_config = result.data.get('config', {})
    step_key = f'step_{step_number}_data'
    current_config[step_key] = data
    current_config['current_step'] = step_number
    
    # Atualiza registro
    update_data = {'config': current_config}
    
    # Se step 1, atualiza nome e template
    if step_number == 1 and 'name' in data:
        update_data['name'] = data['name']
        update_data['template_type'] = data['template_type']
    
    self.supabase.table('sub_agents').update(update_data).eq('id', str(wizard_id)).execute()
```

#### Arquivo: `backend/src/services/publication_service.py`

**Função: `publish_agent()`**

```python
def publish_agent(self, wizard_id: UUID) -> PublicationResult:
    """Publish agent and generate all assets"""
    
    # 1. Busca wizard session (draft)
    wizard_result = self.supabase.table('sub_agents')\
        .select('*')\
        .eq('id', str(wizard_id))\
        .eq('status', 'draft')\  # ← Busca draft
        .single()\
        .execute()
    
    # 2. Valida que todos os steps foram completados
    if not all([
        wizard_config.get('step_1_data'),
        wizard_config.get('step_2_data'),
        wizard_config.get('step_3_data'),
        wizard_config.get('step_4_data'),
    ]):
        raise ValueError("Wizard not completed")
    
    # 3. Gera slug único
    slug = self.generate_slug(step_1['name'], client_id)
    
    # 4. Gera public URL
    public_url = f"https://renum.com.br/chat/{slug}"
    
    # 5. Gera system prompt baseado no template
    system_prompt = self.template_service.generate_system_prompt(
        template_type=step_1['template_type'],
        personality=step_2['personality'],
        tone_formal=step_2['tone_formal'],
        tone_direct=step_2['tone_direct'],
        # ...
    )
    
    # 6. ✅ ATUALIZA registro de draft para active
    update_data = {
        'name': step_1['name'],
        'description': step_1.get('description'),
        'template_type': step_1['template_type'],
        'system_prompt': system_prompt,
        'slug': slug,
        'public_url': public_url,
        'status': 'active',  # ← Muda de draft para active
        'is_active': True,
        'is_public': True,
        'config': wizard_config,  # Mantém config do wizard
    }
    
    self.supabase.table('sub_agents').update(update_data).eq('id', str(wizard_id)).execute()
    
    # 7. Gera embed code e QR code
    embed_code = self.generate_embed_code(wizard_id, slug)
    qr_code_url = self.generate_qr_code(public_url)
    
    return PublicationResult(
        agent_id=wizard_id,
        slug=slug,
        public_url=public_url,
        embed_code=embed_code,
        qr_code_url=qr_code_url,
        status='active',
    )
```

---

### Endpoints da API

**Arquivo: `backend/src/api/routes/wizard.py`**

```python
# Iniciar wizard
POST /agents/wizard/start
→ Cria registro draft em sub_agents
→ Retorna wizard_id

# Salvar step
PUT /agents/wizard/{wizard_id}/step/{step_number}
→ Atualiza config do registro draft
→ Valida dados do step

# Publicar
POST /agents/wizard/{wizard_id}/publish
→ Valida wizard completo
→ Gera slug, URL, embed, QR
→ Muda status de draft → active
→ Retorna PublicationResult
```

---

### CONCLUSÃO PARTE 1

#### ✅ WIZARD SALVA EM: **sub_agents**

**Fluxo completo:**

1. **Início:** Cria registro em `sub_agents` com `status='draft'`
2. **Steps 1-4:** Atualiza campo `config` com dados de cada step
3. **Publicação:** Muda `status='draft'` → `status='active'`

**Estrutura do registro draft:**
```json
{
  "id": "uuid",
  "client_id": "uuid",
  "name": "Draft Agent abc123",
  "status": "draft",
  "template_type": "custom",
  "is_active": false,
  "config": {
    "wizard_session": true,
    "current_step": 1,
    "step_1_data": { "name": "...", "template_type": "..." },
    "step_2_data": { "personality": "...", "tone_formal": 50, ... },
    "step_3_data": { "standard_fields": {...}, "custom_fields": [...] },
    "step_4_data": { "integrations": {...} }
  }
}
```

**Estrutura após publicação:**
```json
{
  "id": "uuid",
  "client_id": "uuid",
  "name": "Nome Real do Agente",
  "status": "active",  // ← Mudou
  "template_type": "customer_service",
  "is_active": true,  // ← Mudou
  "is_public": true,  // ← Mudou
  "slug": "nome-real-do-agente",  // ← Novo
  "public_url": "https://renum.com.br/chat/nome-real-do-agente",  // ← Novo
  "system_prompt": "Você é um assistente...",  // ← Gerado
  "config": {
    // Mantém dados do wizard para referência
  }
}
```

#### ✅ Wizard funciona: **SIM**

**Evidências:**
- Código completo e bem estruturado
- Validações implementadas
- Geração de assets (slug, URL, embed, QR)
- Limite B2C implementado (1 agente por cliente)
- Registros existentes no banco (Test Agent Sprint 06)

#### ⚠️ Problemas encontrados:

1. **Tabela wizard_sessions não existe**
   - Comentário no código: "We'll store wizard sessions in a JSONB column"
   - Solução atual: Usa `sub_agents` com `status='draft'`
   - **Impacto:** Funciona, mas mistura conceitos (wizard session = agent draft)

2. **Erro em renus_config**
   - Query falhou: `column renus_config.client_id does not exist`
   - **Impacto:** Estrutura de renus_config diferente do esperado

3. **Arquitetura agents vs sub_agents**
   - Wizard cria em `sub_agents` (não em `agents`)
   - Confirma que tabela `agents` não é usada
   - **Impacto:** Nomenclatura confusa (são "agents", não "sub-agents")

---

## PARTE 2: RENUS

### Arquivos Encontrados

```
✅ backend/src/agents/renus.py (arquivo principal)
✅ backend/src/agents/base.py (classe base)
✅ backend/src/services/subagent_service.py (CRUD de sub-agents)
```

---

### Código de Roteamento

**Arquivo: `backend/src/agents/renus.py`**

**Classe: `RenusAgent`**

```python
class RenusAgent(BaseAgent):
    """
    RENUS - Main orchestrator agent for the RENUM system.
    
    Responsibilities:
    1. Analyze incoming messages and determine intent
    2. Route conversations to specialized sub-agents when appropriate
    3. Handle general conversations directly when no sub-agent is needed
    4. Maintain context across multiple turns
    5. Implement fallback logic when sub-agents fail
    6. Log all routing decisions to LangSmith
    """
    
    def __init__(self, **kwargs):
        super().__init__(
            model=kwargs.get("model", settings.DEFAULT_RENUS_MODEL),
            system_prompt=self._get_system_prompt(),
            tools=kwargs.get("tools", []),
            **kwargs
        )
        
        # ⚠️ Registry de sub-agents (em memória, não consulta banco)
        self.sub_agents: Dict[str, Any] = {}
```

**System Prompt:**

```python
def _get_system_prompt(self) -> str:
    return """You are RENUS, the main orchestrator agent for the RENUM system.

Your responsibilities:
1. Analyze incoming messages and determine user intent
2. Route conversations to specialized sub-agents when appropriate
3. Handle general conversations directly when no sub-agent is needed
4. Maintain context across multiple turns and sub-agent delegations
5. Implement fallback logic when sub-agents fail
6. Always explain your routing decisions clearly

Available sub-agents:
- Discovery: Conducts structured interviews for requirement gathering
  Use when: User wants to start an interview, provide information, or answer questions
- (More sub-agents will be added in future)

When routing, consider:
- Message topic and intent
- Conversation history
- Sub-agent capabilities
- User preferences
"""
```

**Workflow (LangGraph):**

```python
def _build_graph(self) -> StateGraph:
    workflow = StateGraph(dict)
    
    # Nodes
    workflow.add_node("analyze", self._analyze_intent)
    workflow.add_node("route", self._route_to_subagent)
    workflow.add_node("respond", self._generate_response)
    
    # Edges
    workflow.set_entry_point("analyze")
    workflow.add_conditional_edges(
        "analyze",
        self._should_route,
        {
            "route": "route",
            "respond": "respond"
        }
    )
    workflow.add_edge("route", "respond")
    workflow.add_edge("respond", END)
    
    return workflow.compile()
```

**Análise de Intent:**

```python
async def _analyze_intent(self, state: Dict) -> Dict:
    """Analyze message intent and context"""
    
    messages = state.get("messages", [])
    last_message = messages[-1] if messages else None
    content = last_message.content.lower()
    
    # ⚠️ Detecção simples por keywords (não usa LLM)
    interview_keywords = ["entrevista", "interview", "pesquisa", "survey", "perguntas", "questions"]
    
    if any(keyword in content for keyword in interview_keywords):
        state["intent"] = "discovery"
        state["confidence"] = 0.8
        state["target_subagent"] = "discovery"
    else:
        state["intent"] = "general"
        state["confidence"] = 0.6
        state["target_subagent"] = None
    
    return state
```

**Decisão de Roteamento:**

```python
def _should_route(self, state: Dict) -> str:
    """Decide if routing to sub-agent is needed"""
    
    intent = state.get("intent", "unknown")
    confidence = state.get("confidence", 0.0)
    target = state.get("target_subagent")
    
    # ✅ Roteia se confiança > 0.7 e tem target
    if target and confidence > 0.7:
        return "route"
    
    return "respond"
```

**Roteamento para Sub-Agent:**

```python
async def _route_to_subagent(self, state: Dict) -> Dict:
    """Route to appropriate sub-agent"""
    
    target = state.get("target_subagent")
    
    # ⚠️ Busca no registry em memória (não no banco)
    if target in self.sub_agents:
        sub_agent = self.sub_agents[target]
        
        try:
            result = await sub_agent.invoke(
                messages=state.get("messages", []),
                context=state.get("context", {})
            )
            
            state["subagent_response"] = result
            state["subagent_success"] = True
            
        except Exception as e:
            state["subagent_error"] = str(e)
            state["subagent_success"] = False
    else:
        # ❌ Sub-agent não encontrado no registry
        state["subagent_error"] = f"Sub-agent '{target}' not found"
        state["subagent_success"] = False
    
    return state
```

**Registro de Sub-Agents:**

```python
def register_subagent(self, name: str, agent: Any) -> None:
    """Register a sub-agent with RENUS"""
    
    # ⚠️ Adiciona ao registry em memória
    self.sub_agents[name] = agent
    print(f"✅ Registered sub-agent: {name}")

def list_subagents(self) -> List[str]:
    """List all registered sub-agents"""
    return list(self.sub_agents.keys())
```

---

### Consulta a sub_agents?

**❌ NÃO CONSULTA O BANCO**

**Evidências:**

1. **Registry em memória:**
   ```python
   self.sub_agents: Dict[str, Any] = {}
   ```

2. **Nenhuma query SQL:**
   - Busquei por `supabase.*sub_agents` no código
   - Busquei por `SELECT.*sub_agents`
   - **Resultado:** Nenhuma consulta encontrada em `renus.py`

3. **Registro manual:**
   - Sub-agents devem ser registrados via `register_subagent()`
   - Não há código que busca sub-agents do banco automaticamente

---

### Lógica de Decisão

**Método atual:**

1. **Análise de intent:** Keywords simples (não usa LLM)
2. **Decisão:** Confiança > 0.7 + target definido
3. **Roteamento:** Busca no registry em memória
4. **Fallback:** Se sub-agent não existe, responde diretamente

**Keywords reconhecidas:**
- `["entrevista", "interview", "pesquisa", "survey", "perguntas", "questions"]` → Discovery

**Limitações:**

- ❌ Não consulta banco para descobrir sub-agents disponíveis
- ❌ Não usa tópicos dos sub-agents para decisão
- ❌ Não usa LLM para análise de intent (apenas keywords)
- ❌ Hardcoded para apenas "discovery"
- ❌ Não considera sub-agents criados via Wizard

---

### Teste de Roteamento

**❌ NÃO REALIZADO**

**Motivo:** 
- Roteamento depende de sub-agents registrados manualmente
- Não há código que carrega sub-agents do banco
- Teste seria inválido sem implementar carregamento dinâmico

---

### CONCLUSÃO PARTE 2

#### ⚠️ Roteamento implementado: **PARCIALMENTE**

**O que existe:**
- ✅ Estrutura LangGraph completa
- ✅ Análise de intent (simples)
- ✅ Decisão de roteamento
- ✅ Invocação de sub-agents
- ✅ Fallback para resposta direta
- ✅ Logging com LangSmith

**O que falta:**
- ❌ Consulta ao banco `sub_agents`
- ❌ Carregamento dinâmico de sub-agents
- ❌ Uso de tópicos para decisão
- ❌ Análise de intent com LLM
- ❌ Suporte a sub-agents criados via Wizard

#### ❌ Consulta sub_agents: **NÃO**

**Evidência:** Nenhuma query SQL para `sub_agents` em `renus.py`

#### ⚠️ Lógica de decisão: **KEYWORDS SIMPLES**

**Método:**
- Busca keywords na mensagem
- Se encontrar "entrevista" → Discovery
- Caso contrário → Resposta direta

**Limitações:**
- Não usa capacidades do LLM
- Não considera contexto da conversa
- Não usa metadados dos sub-agents (tópicos, descrição)
- Hardcoded para apenas 1 sub-agent

#### ⚠️ Funciona: **PARCIAL**

**Cenário A - Sub-agent registrado manualmente:**
```python
renus = RenusAgent()
discovery_agent = DiscoveryAgent()
renus.register_subagent("discovery", discovery_agent)

# ✅ Funciona
response = await renus.invoke(
    messages=[HumanMessage(content="Quero fazer uma entrevista")],
    context={}
)
# → Roteia para discovery
```

**Cenário B - Sub-agent criado via Wizard:**
```python
# Wizard cria sub-agent no banco
wizard_service.publish_agent(wizard_id)
# → Registro em sub_agents com status='active'

# RENUS tenta rotear
renus = RenusAgent()
response = await renus.invoke(
    messages=[HumanMessage(content="Quero falar sobre vendas")],
    context={}
)
# ❌ Não funciona: sub-agent não está no registry
# → Responde diretamente (fallback)
```

#### ⚠️ Gaps identificados:

1. **Desconexão Wizard ↔ RENUS**
   - Wizard cria sub-agents no banco
   - RENUS não carrega sub-agents do banco
   - **Resultado:** Sub-agents criados via Wizard nunca são usados

2. **Registry estático**
   - Sub-agents devem ser registrados manualmente no código
   - Não há carregamento dinâmico
   - **Resultado:** Não escala, requer deploy para adicionar sub-agent

3. **Análise de intent limitada**
   - Apenas keywords simples
   - Não usa LLM para entender contexto
   - **Resultado:** Roteamento impreciso

4. **Sem uso de metadados**
   - Sub-agents têm `topics`, `description`, `system_prompt`
   - RENUS não usa esses dados para decisão
   - **Resultado:** Informação valiosa desperdiçada

5. **Hardcoded para Discovery**
   - Apenas 1 sub-agent suportado
   - Keywords específicas para "entrevista"
   - **Resultado:** Não funciona para outros tipos de sub-agents

---

## RESUMO EXECUTIVO

### Wizard

**Salva em:** `sub_agents` (com `status='draft'` → `status='active'`)

**Funciona:** ✅ **SIM**

**Fluxo:**
1. Cria draft em `sub_agents`
2. Atualiza config a cada step
3. Publica: gera slug, URL, embed, QR
4. Muda status para active

**Problemas:**
- ⚠️ Mistura conceito de wizard session com agent draft
- ⚠️ Tabela `wizard_sessions` não existe (usa sub_agents)
- ⚠️ Nomenclatura confusa (cria "agents" em tabela "sub_agents")

---

### RENUS

**Roteamento:** ⚠️ **PARCIALMENTE IMPLEMENTADO**

**Consulta sub_agents:** ❌ **NÃO**

**Funciona:** ⚠️ **PARCIAL**
- ✅ Funciona se sub-agent registrado manualmente
- ❌ Não funciona com sub-agents criados via Wizard

**Problemas:**
- ❌ Não carrega sub-agents do banco
- ❌ Registry estático (em memória)
- ❌ Análise de intent simples (keywords)
- ❌ Não usa metadados dos sub-agents
- ❌ Hardcoded para apenas "discovery"
- ❌ Sub-agents do Wizard nunca são usados

---

## PRÓXIMOS PASSOS

### 🔴 CRÍTICO

1. **Implementar carregamento dinâmico de sub-agents**
   - RENUS deve consultar `sub_agents` no banco
   - Carregar sub-agents com `status='active'` e `is_active=true`
   - Popular registry automaticamente

2. **Usar metadados para roteamento**
   - Usar `topics` dos sub-agents para decisão
   - Usar `description` para contexto
   - Melhorar análise de intent com LLM

3. **Conectar Wizard → RENUS**
   - Sub-agents criados via Wizard devem ser carregados
   - Testar fluxo completo: criar → publicar → usar

### ⚠️ MÉDIO

4. **Melhorar análise de intent**
   - Usar LLM em vez de keywords
   - Considerar contexto da conversa
   - Usar embeddings para matching de tópicos

5. **Criar tabela wizard_sessions**
   - Separar conceito de wizard session de agent draft
   - Manter histórico de criação
   - Permitir retomar wizard abandonado

6. **Resolver nomenclatura**
   - Decidir: criar tabela `agents` ou renomear `sub_agents`?
   - Atualizar documentação
   - Ajustar código e frontend

### ✅ BAIXO

7. **Testes E2E**
   - Criar sub-agent via Wizard
   - Enviar mensagem que deveria acionar sub-agent
   - Validar que RENUS roteia corretamente

8. **Monitoramento**
   - Dashboard de roteamento
   - Métricas de uso por sub-agent
   - Taxa de acerto de intent

---

## ESTIMATIVA DE ESFORÇO

| Tarefa | Esforço | Prioridade |
|--------|---------|------------|
| Carregamento dinâmico de sub-agents | 3-4h | CRÍTICA |
| Usar metadados para roteamento | 2-3h | CRÍTICA |
| Conectar Wizard → RENUS | 1-2h | CRÍTICA |
| Melhorar análise de intent | 4-6h | MÉDIA |
| Criar tabela wizard_sessions | 2-3h | MÉDIA |
| Resolver nomenclatura | 2-3h | MÉDIA |
| Testes E2E | 2-3h | BAIXA |
| **TOTAL** | **16-24h** | **~3-4 dias** |

---

## CÓDIGO NECESSÁRIO (PREVIEW)

### Carregamento Dinâmico

```python
# backend/src/agents/renus.py

class RenusAgent(BaseAgent):
    
    def __init__(self, **kwargs):
        super().__init__(...)
        self.sub_agents: Dict[str, Any] = {}
        
        # ✅ Carregar sub-agents do banco
        self._load_subagents_from_db()
    
    def _load_subagents_from_db(self):
        """Load active sub-agents from database"""
        from src.config.supabase import supabase_admin
        
        # Buscar sub-agents ativos
        result = supabase_admin.table('sub_agents')\
            .select('*')\
            .eq('status', 'active')\
            .eq('is_active', True)\
            .execute()
        
        for agent_data in result.data:
            # Criar instância do sub-agent
            sub_agent = self._create_subagent_instance(agent_data)
            
            # Registrar
            self.register_subagent(agent_data['id'], sub_agent)
            
            print(f"✅ Loaded sub-agent: {agent_data['name']}")
    
    def _create_subagent_instance(self, agent_data: Dict) -> Any:
        """Create sub-agent instance from database record"""
        # TODO: Implementar factory de sub-agents
        pass
```

### Roteamento por Tópicos

```python
async def _analyze_intent(self, state: Dict) -> Dict:
    """Analyze message intent using sub-agent topics"""
    
    messages = state.get("messages", [])
    last_message = messages[-1]
    content = last_message.content.lower()
    
    # Buscar sub-agents do banco
    result = supabase_admin.table('sub_agents')\
        .select('id, name, topics, description')\
        .eq('status', 'active')\
        .eq('is_active', True)\
        .execute()
    
    # Usar LLM para matching
    prompt = f"""
    Mensagem do usuário: "{content}"
    
    Sub-agents disponíveis:
    {json.dumps([{
        'name': a['name'],
        'topics': a['topics'],
        'description': a['description']
    } for a in result.data], indent=2)}
    
    Qual sub-agent é mais adequado? Responda com o ID ou "none".
    """
    
    response = await self.llm.ainvoke([HumanMessage(content=prompt)])
    
    # Parse resposta
    target_id = self._parse_llm_response(response.content)
    
    if target_id and target_id != "none":
        state["intent"] = "subagent"
        state["confidence"] = 0.9
        state["target_subagent"] = target_id
    else:
        state["intent"] = "general"
        state["confidence"] = 0.6
        state["target_subagent"] = None
    
    return state
```

---

**Relatório concluído em:** 2025-12-05 20:15
