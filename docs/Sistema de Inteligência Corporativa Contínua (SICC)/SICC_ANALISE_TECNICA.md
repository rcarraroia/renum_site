# ANÁLISE TÉCNICA - Sistema de Inteligência Corporativa Contínua (SICC)

**Data:** 07/12/2025  
**Análise:** Banco de Dados Real + Arquitetura Atual

---

## 1. ESTADO ATUAL DO BANCO DE DADOS

### Tabelas Existentes (16)
- **agents** (3 registros) - Agentes criados pelos clientes
- **clients** (1 registro) - Empresas clientes
- **conversations** (1 registro) - Conversas gerais
- **integrations** (0 registros) - Integrações externas
- **interview_messages** (58 registros) - Mensagens de entrevistas
- **interviews** (7 registros) - Metadados de entrevistas
- **isa_commands** (0 registros) - Comandos ISA
- **leads** (1 registro) - Contatos/leads
- **messages** (1 registro) - Mensagens de conversas
- **profiles** (2 registros) - Usuários do sistema
- **projects** (1 registro) - Projetos
- **renus_config** (0 registros) - Configuração RENUS
- **sub_agents** (3 registros) - Sub-agentes especializados
- **tools** (0 registros) - Ferramentas disponíveis
- **trigger_executions** (0 registros) - Execuções de triggers
- **triggers** (0 registros) - Triggers configurados

### Infraestrutura Atual
- **RLS:** Habilitado em TODAS as tabelas ✅
- **Políticas RLS:** 38 políticas ativas ✅
- **Índices:** 70 índices otimizados ✅
- **Triggers:** 12 triggers para updated_at ✅
- **Functions:** 4 functions (slug, timestamp, new_user) ✅
- **Foreign Keys:** 18 relacionamentos ✅
- **Tamanho Total:** 1.54 MB

### CRÍTICO: Vector Database
❌ **Extensão pgvector NÃO INSTALADA**
- Necessário para embeddings
- Bloqueador para implementação do SICC

---

## 2. ARQUITETURA PROPOSTA PARA O SICC

### 2.1 Núcleo Cognitivo (DNA Fixo)
**Tabela:** `agent_dna`
```sql
CREATE TABLE agent_dna (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    function TEXT NOT NULL,
    principles JSONB NOT NULL DEFAULT '[]',
    restrictions JSONB NOT NULL DEFAULT '[]',
    tone_of_voice TEXT NOT NULL,
    operational_limits JSONB NOT NULL DEFAULT '{}',
    security_policies JSONB NOT NULL DEFAULT '{}',
    version INTEGER NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Características:**
- Imutável por aprendizado automático
- Apenas admin pode modificar
- Versionado para auditoria


### 2.2 Memória Adaptativa (Knowledge Memory)
**Tabela:** `agent_memory_chunks`
```sql
CREATE TABLE agent_memory_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    chunk_type TEXT NOT NULL, -- 'business_term', 'process', 'faq', 'product', 'objection'
    content TEXT NOT NULL,
    embedding VECTOR(1536), -- OpenAI ada-002 ou similar
    metadata JSONB NOT NULL DEFAULT '{}',
    source TEXT, -- 'conversation', 'document', 'manual', 'isa_analysis'
    confidence_score FLOAT DEFAULT 1.0,
    usage_count INTEGER DEFAULT 0,
    last_used_at TIMESTAMPTZ,
    version INTEGER NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX idx_memory_agent ON agent_memory_chunks(agent_id, is_active);
CREATE INDEX idx_memory_type ON agent_memory_chunks(chunk_type);
CREATE INDEX idx_memory_embedding ON agent_memory_chunks USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_memory_usage ON agent_memory_chunks(usage_count DESC);
```

**Características:**
- Armazena conhecimento aprendido
- Embeddings para similarity search
- Versionamento para rollback
- Tracking de uso para relevância

### 2.3 Heurísticas Comportamentais
**Tabela:** `agent_behavior_patterns`
```sql
CREATE TABLE agent_behavior_patterns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    pattern_type TEXT NOT NULL, -- 'response_strategy', 'tone_adjustment', 'flow_optimization'
    trigger_context JSONB NOT NULL, -- Quando aplicar
    action_config JSONB NOT NULL, -- O que fazer
    success_rate FLOAT DEFAULT 0.0,
    total_applications INTEGER DEFAULT 0,
    successful_applications INTEGER DEFAULT 0,
    last_applied_at TIMESTAMPTZ,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_behavior_agent ON agent_behavior_patterns(agent_id, is_active);
CREATE INDEX idx_behavior_success ON agent_behavior_patterns(success_rate DESC);
```

**Características:**
- Captura estratégias que funcionam
- Métricas de sucesso
- Aplicação condicional

### 2.4 Logs de Aprendizado (ISA Supervisor)
**Tabela:** `agent_learning_logs`
```sql
CREATE TABLE agent_learning_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    learning_type TEXT NOT NULL, -- 'memory_added', 'pattern_detected', 'behavior_updated'
    source_data JSONB NOT NULL, -- Dados que geraram o aprendizado
    analysis JSONB NOT NULL, -- Análise da ISA
    action_taken TEXT NOT NULL,
    confidence FLOAT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending', -- 'pending', 'approved', 'rejected', 'applied'
    reviewed_by UUID REFERENCES profiles(id),
    reviewed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_learning_agent ON agent_learning_logs(agent_id, status);
CREATE INDEX idx_learning_date ON agent_learning_logs(created_at DESC);
```

**Características:**
- Auditoria completa
- Aprovação manual opcional
- Rastreabilidade

### 2.5 Snapshots de Conhecimento
**Tabela:** `agent_knowledge_snapshots`
```sql
CREATE TABLE agent_knowledge_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    snapshot_type TEXT NOT NULL DEFAULT 'automatic', -- 'automatic', 'manual', 'milestone'
    memory_count INTEGER NOT NULL,
    pattern_count INTEGER NOT NULL,
    total_interactions INTEGER NOT NULL,
    avg_success_rate FLOAT,
    snapshot_data JSONB NOT NULL, -- Resumo do estado
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_snapshot_agent ON agent_knowledge_snapshots(agent_id, created_at DESC);
```

**Características:**
- Backup do estado de aprendizado
- Rollback se necessário
- Análise de evolução

### 2.6 Métricas de Performance
**Tabela:** `agent_performance_metrics`
```sql
CREATE TABLE agent_performance_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    metric_date DATE NOT NULL,
    total_interactions INTEGER DEFAULT 0,
    successful_interactions INTEGER DEFAULT 0,
    avg_response_time_ms INTEGER,
    user_satisfaction_score FLOAT,
    conversion_rate FLOAT,
    memory_chunks_used INTEGER DEFAULT 0,
    patterns_applied INTEGER DEFAULT 0,
    new_learnings INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_metrics_agent_date ON agent_performance_metrics(agent_id, metric_date DESC);
CREATE UNIQUE INDEX idx_metrics_unique ON agent_performance_metrics(agent_id, metric_date);
```

---

## 3. VECTOR DATABASE - DECISÃO TÉCNICA

### Opção Recomendada: Supabase Vector (pgvector)

**Vantagens:**
- ✅ Nativo ao stack atual (PostgreSQL)
- ✅ Sem custo adicional de infraestrutura
- ✅ RLS nativo para isolamento multi-tenant
- ✅ Integração direta com Supabase Client
- ✅ Backup automático junto com dados relacionais

**Instalação:**
```sql
-- Executar no SQL Editor do Supabase
CREATE EXTENSION IF NOT EXISTS vector;
```

**Alternativas Avaliadas:**
- **Pinecone:** Custo adicional, vendor lock-in
- **Weaviate:** Infraestrutura separada, complexidade
- **Qdrant:** Bom, mas adiciona dependência externa

**Decisão:** pgvector é suficiente para 100k+ embeddings com performance adequada.

---

## 4. FLUXO DE APRENDIZADO CONTÍNUO

### Ciclo Automático (Executado pela ISA)

```
1. COLETA (Tempo Real)
   ↓
   - Conversas dos agentes
   - Feedbacks de usuários
   - Resultados de conversões
   - Documentos enviados
   
2. ANÁLISE (ISA - A cada 1 hora)
   ↓
   - Detectar padrões recorrentes
   - Identificar novos termos/conceitos
   - Avaliar estratégias bem-sucedidas
   - Filtrar ruído e informações falsas
   
3. VALIDAÇÃO (ISA - Automática)
   ↓
   - Confidence score > 0.8 → Auto-aprovar
   - Confidence score 0.5-0.8 → Revisar
   - Confidence score < 0.5 → Descartar
   
4. CONSOLIDAÇÃO (ISA - Diária)
   ↓
   - Atualizar agent_memory_chunks
   - Criar/atualizar behavior_patterns
   - Gerar snapshot
   - Atualizar métricas
   
5. APLICAÇÃO (Tempo Real)
   ↓
   - Agentes consultam memória via similarity search
   - Aplicam padrões comportamentais
   - Registram uso para feedback loop
```

### Exemplo Prático

**Situação:** Cliente de clínica odontológica

**Dia 1:**
- Agente conversa com 10 pacientes
- 7 perguntam sobre "clareamento dental"
- ISA detecta termo recorrente

**Dia 2:**
- ISA cria memory_chunk:
  ```json
  {
    "chunk_type": "business_term",
    "content": "Clareamento dental: procedimento estético...",
    "metadata": {
      "frequency": 7,
      "context": "pergunta_comum",
      "related_terms": ["branqueamento", "dentes brancos"]
    }
  }
  ```

**Dia 3:**
- Novo paciente pergunta sobre "branqueamento"
- Agente usa similarity search
- Encontra memory_chunk de "clareamento"
- Responde com conhecimento consolidado

---

## 5. INTEGRAÇÃO COM MÓDULOS EXISTENTES

### 5.1 RENUS (Atendimento ao Cliente)
**Modificações necessárias:**

```python
# src/services/renus_service.py

class RenusService:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.memory_service = MemoryService(agent_id)
        self.behavior_service = BehaviorService(agent_id)
    
    async def process_message(self, message: str, context: dict):
        # 1. Buscar memórias relevantes
        relevant_memories = await self.memory_service.search_similar(
            query=message,
            limit=5
        )
        
        # 2. Buscar padrões comportamentais aplicáveis
        applicable_patterns = await self.behavior_service.get_patterns(
            context=context
        )
        
        # 3. Enriquecer prompt com conhecimento
        enriched_prompt = self._build_prompt(
            message=message,
            memories=relevant_memories,
            patterns=applicable_patterns
        )
        
        # 4. Processar com LLM
        response = await self.llm.generate(enriched_prompt)
        
        # 5. Registrar uso de memórias/padrões
        await self._track_usage(relevant_memories, applicable_patterns)
        
        return response
```

### 5.2 ISA (Assistente Interna)
**Novo papel: Supervisora de Aprendizado**

```python
# src/services/isa_learning_service.py

class ISALearningService:
    async def analyze_conversations(self, agent_id: str, time_window: str):
        """Analisa conversas e extrai aprendizados"""
        
        # 1. Buscar conversas recentes
        conversations = await self.get_recent_conversations(
            agent_id=agent_id,
            window=time_window
        )
        
        # 2. Análise com LLM
        analysis = await self.llm.analyze(
            conversations=conversations,
            task="extract_learnings"
        )
        
        # 3. Criar learning_logs
        for learning in analysis['learnings']:
            await self.create_learning_log(
                agent_id=agent_id,
                learning_type=learning['type'],
                data=learning['data'],
                confidence=learning['confidence']
            )
        
        # 4. Auto-aprovar high confidence
        await self.auto_approve_high_confidence()
        
        return analysis
    
    async def consolidate_learnings(self, agent_id: str):
        """Consolida aprendizados aprovados"""
        
        # 1. Buscar logs aprovados
        approved_logs = await self.get_approved_logs(agent_id)
        
        # 2. Criar memory_chunks
        for log in approved_logs:
            if log['learning_type'] == 'new_term':
                await self.memory_service.create_chunk(
                    agent_id=agent_id,
                    chunk_type='business_term',
                    content=log['source_data']['term'],
                    metadata=log['analysis']
                )
            
            elif log['learning_type'] == 'successful_pattern':
                await self.behavior_service.create_pattern(
                    agent_id=agent_id,
                    pattern_type='response_strategy',
                    trigger=log['source_data']['trigger'],
                    action=log['source_data']['action']
                )
        
        # 3. Criar snapshot
        await self.create_snapshot(agent_id)
```

### 5.3 Módulo de Criação de Agentes
**Modificações:**

```python
# src/services/agent_creation_service.py

class AgentCreationService:
    async def create_agent(self, client_id: str, config: dict):
        # 1. Criar agente (já existe)
        agent = await self.agents_repo.create(client_id, config)
        
        # 2. NOVO: Criar DNA Cognitivo
        await self.create_agent_dna(
            agent_id=agent.id,
            function=config['function'],
            principles=config['principles'],
            restrictions=config['restrictions']
        )
        
        # 3. NOVO: Inicializar memória vazia
        await self.memory_service.initialize(agent.id)
        
        # 4. NOVO: Configurar ciclo de aprendizado
        await self.learning_service.setup_learning_cycle(
            agent_id=agent.id,
            frequency='hourly',
            auto_approve_threshold=0.8
        )
        
        return agent
```

---

## 6. ARQUITETURA DE SERVIÇOS

### Novos Serviços Necessários

```
src/services/sicc/
├── __init__.py
├── memory_service.py          # Gestão de memória adaptativa
├── behavior_service.py         # Gestão de padrões comportamentais
├── learning_service.py         # Ciclo de aprendizado (ISA)
├── embedding_service.py        # Geração de embeddings
├── snapshot_service.py         # Snapshots e rollback
└── metrics_service.py          # Métricas de performance
```

### Dependências Adicionais

```txt
# requirements.txt - ADICIONAR

# Embeddings
sentence-transformers==2.2.2  # Alternativa local
tiktoken==0.5.2               # Tokenização OpenAI

# Vector operations
numpy==1.24.3
pgvector==0.2.3               # Cliente Python para pgvector
```

---

## 7. INTERFACE DE USUÁRIO (UX/UI)

### 7.1 Painel de Evolução do Agente
**Rota:** `/agents/{agent_id}/evolution`

**Componentes:**
```typescript
// frontend/src/pages/agents/AgentEvolutionPage.tsx

interface EvolutionMetrics {
  totalMemories: number;
  totalPatterns: number;
  totalInteractions: number;
  avgSuccessRate: number;
  learningVelocity: number; // Novos aprendizados/dia
}

interface MemoryChunk {
  id: string;
  type: string;
  content: string;
  usageCount: number;
  confidenceScore: number;
  createdAt: string;
}
```

**Visualizações:**
- Gráfico de evolução temporal (memórias x tempo)
- Top 10 memórias mais usadas
- Padrões comportamentais ativos
- Taxa de sucesso por tipo de interação

### 7.2 Painel de Memória
**Rota:** `/agents/{agent_id}/memory`

**Funcionalidades:**
- Listar todas as memórias (paginado)
- Filtrar por tipo (termos, processos, FAQs, etc)
- Buscar por conteúdo
- Ver histórico de uso
- Editar/desativar memórias manualmente
- Adicionar memórias manualmente

### 7.3 Painel de Aprendizados Pendentes
**Rota:** `/agents/{agent_id}/learning-queue`

**Funcionalidades:**
- Listar aprendizados com confidence 0.5-0.8
- Aprovar/rejeitar em lote
- Ver análise da ISA
- Ver dados de origem

### 7.4 Configurações de Aprendizado
**Rota:** `/agents/{agent_id}/learning-settings`

**Opções:**
- Frequência de análise (hourly, daily, weekly)
- Threshold de auto-aprovação (0.0-1.0)
- Tipos de aprendizado habilitados
- Limite de memórias (quota)
- Ativar/desativar aprendizado

---

## 8. RISCOS E MITIGAÇÕES

### Risco 1: Alucinação/Informação Falsa
**Mitigação:**
- Confidence score obrigatório
- Revisão manual para confidence < 0.8
- Tracking de fonte de dados
- Rollback via snapshots

### Risco 2: Degradação de Performance
**Mitigação:**
- Índices otimizados em embeddings
- Limite de memórias por agente (ex: 10k)
- Arquivamento de memórias antigas não usadas
- Cache de embeddings frequentes

### Risco 3: Vazamento entre Clientes
**Mitigação:**
- RLS em todas as tabelas SICC
- client_id obrigatório em todas queries
- Testes de isolamento automatizados
- Auditoria de acessos

### Risco 4: Custo de Embeddings
**Mitigação:**
- Usar modelo local (sentence-transformers) para embeddings
- Batch processing para reduzir chamadas
- Cache de embeddings já gerados
- Deduplicação de conteúdo similar

### Risco 5: Complexidade de Manutenção
**Mitigação:**
- Documentação completa
- Testes automatizados
- Painel de monitoramento
- Alertas para anomalias

---

## 9. CRONOGRAMA DE IMPLEMENTAÇÃO

### FASE 1: Fundação (2 semanas)
**Objetivo:** Infraestrutura base

- [ ] Instalar pgvector no Supabase
- [ ] Criar tabelas do SICC
- [ ] Implementar MemoryService básico
- [ ] Implementar EmbeddingService
- [ ] Testes unitários

### FASE 2: Aprendizado Básico (2 semanas)
**Objetivo:** Ciclo de aprendizado funcional

- [ ] Implementar LearningService (ISA)
- [ ] Implementar BehaviorService
- [ ] Criar job Celery para análise periódica
- [ ] Integrar com RENUS
- [ ] Testes de integração

### FASE 3: Interface (1 semana)
**Objetivo:** Painéis de gestão

- [ ] Painel de Evolução
- [ ] Painel de Memória
- [ ] Painel de Aprendizados Pendentes
- [ ] Configurações de Aprendizado

### FASE 4: Otimização (1 semana)
**Objetivo:** Performance e segurança

- [ ] Otimizar queries de similarity search
- [ ] Implementar cache
- [ ] Testes de carga
- [ ] Auditoria de segurança RLS

### FASE 5: Integração Completa (1 semana)
**Objetivo:** Todos os módulos integrados

- [ ] Integrar com ISA completamente
- [ ] Integrar com módulo de criação de agentes
- [ ] Snapshots e rollback
- [ ] Métricas e monitoramento

**Total:** 7 semanas

---

## 10. MÉTRICAS DE SUCESSO

### Técnicas
- Tempo de resposta < 500ms (com similarity search)
- Uptime > 99.5%
- 0 vazamentos entre clientes
- Custo de embeddings < $50/mês por agente

### Negócio
- Taxa de sucesso dos agentes aumenta 20%+ após 30 dias
- Redução de 50%+ em edições manuais de prompts
- Satisfação do usuário aumenta 15%+
- Tempo de especialização do agente < 7 dias

---

## 11. DEPENDÊNCIAS EXTERNAS

### Obrigatórias
- ✅ PostgreSQL 15+ (já temos via Supabase)
- ✅ Redis (já temos)
- ✅ Celery (já temos)
- ❌ pgvector (precisa instalar)

### Opcionais
- OpenAI API (para embeddings) - pode usar modelo local
- Sentry (monitoramento) - recomendado

---

## 12. MODIFICAÇÕES NO SISTEMA ATUAL

### Backend

**Arquivos a criar:**
```
backend/src/services/sicc/
├── __init__.py
├── memory_service.py
├── behavior_service.py
├── learning_service.py
├── embedding_service.py
├── snapshot_service.py
└── metrics_service.py

backend/src/models/sicc/
├── __init__.py
├── memory.py
├── behavior.py
├── learning.py
└── snapshot.py

backend/src/workers/sicc_tasks.py
```

**Arquivos a modificar:**
```
backend/src/services/renus_service.py
backend/src/services/isa_service.py
backend/src/services/agent_service.py
backend/src/api/routes/agents.py (adicionar rotas SICC)
```

### Frontend

**Arquivos a criar:**
```
frontend/src/pages/agents/
├── AgentEvolutionPage.tsx
├── AgentMemoryPage.tsx
├── AgentLearningQueuePage.tsx
└── AgentLearningSettingsPage.tsx

frontend/src/components/sicc/
├── EvolutionChart.tsx
├── MemoryList.tsx
├── LearningLogCard.tsx
└── PatternCard.tsx

frontend/src/services/
├── siccService.ts
└── embeddingService.ts
```

### Migrations

**Arquivos a criar:**
```
backend/migrations/
├── 011_install_pgvector.sql
├── 012_create_sicc_tables.sql
├── 013_create_sicc_indexes.sql
└── 014_create_sicc_rls.sql
```

---

## 13. CONCLUSÃO

### Viabilidade Técnica: ✅ ALTA

O sistema atual está bem estruturado para receber o SICC:
- RLS já implementado
- Arquitetura de serviços clara
- Celery para jobs assíncronos
- Frontend modular

### Principais Desafios

1. **Instalação do pgvector** - Requer acesso admin ao Supabase
2. **Tuning de embeddings** - Encontrar modelo ideal (custo x qualidade)
3. **UX de aprovação** - Interface intuitiva para revisar aprendizados

### Diferencial Competitivo

Com o SICC, o Renum terá:
- ✅ Agentes que evoluem automaticamente
- ✅ Especialização sem intervenção manual
- ✅ Conhecimento corporativo consolidado
- ✅ Performance crescente com uso
- ✅ ROI mensurável e visível

### Próximos Passos Imediatos

1. Aprovar arquitetura proposta
2. Instalar pgvector no Supabase
3. Iniciar Fase 1 (Fundação)
4. Definir modelo de embeddings (local vs API)

---

**Documento preparado por:** Kiro  
**Data:** 07/12/2025  
**Versão:** 1.0  
**Status:** Aguardando aprovação
