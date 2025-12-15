# Design Document - SICC (Sistema de Inteligência Corporativa Contínua)

## Overview

O SICC é uma camada cognitiva adaptativa que transforma o Renum em uma plataforma de agentes que aprendem continuamente. O sistema captura padrões de interações reais, consolida conhecimento corporativo através de embeddings vetoriais e aplica aprendizados de forma controlada via supervisão da ISA.

A arquitetura é composta por:
- **Camada de Armazenamento**: PostgreSQL + pgvector para dados relacionais e embeddings
- **Camada de Processamento**: Serviços Python (FastAPI) para embeddings, análise e consolidação
- **Camada de Supervisão**: ISA como agente validador de aprendizados
- **Camada de Aplicação**: Renus e outros agentes consumindo conhecimento via similarity search
- **Camada de Interface**: Painéis React para gestão e monitoramento

O sistema opera em três camadas hierárquicas de conhecimento:
1. **Base do Nicho**: Conhecimento fundamental do setor (MMN, Gabinete, Clínicas)
2. **Empresa/Equipe**: Planos de negócio, processos e propriedade intelectual
3. **Individual**: Ajustes específicos por distribuidor/usuário

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     FRONTEND (Vercel/React)                      │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │  Evolution   │ │   Memory     │ │   Learning   │            │
│  │    Page      │ │   Manager    │ │    Queue     │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS/REST
┌────────────────────────────▼────────────────────────────────────┐
│                    BACKEND (VPS/FastAPI)                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Layer                              │  │
│  │  /sicc/memory  /sicc/learning  /sicc/embed  /sicc/status │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐          │
│  │   Memory     │ │   Learning   │ │  Embedding   │          │
│  │   Service    │ │   Service    │ │   Service    │          │
│  └──────────────┘ └──────────────┘ └──────────────┘          │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐          │
│  │  Behavior    │ │  Snapshot    │ │   Metrics    │          │
│  │   Service    │ │   Service    │ │   Service    │          │
│  └──────────────┘ └──────────────┘ └──────────────┘          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              ISA Supervisor (LangGraph)                   │  │
│  │  Análise → Validação → Consolidação                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Workers (Celery/Redis)                       │  │
│  │  - Embedding batch  - Transcription  - Analysis          │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ SQL + Vector Search
┌────────────────────────────▼────────────────────────────────────┐
│              DATABASE (Supabase/PostgreSQL + pgvector)           │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │  agent_dna   │ │agent_memory  │ │agent_behavior│            │
│  │              │ │   _chunks    │ │  _patterns   │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │agent_learning│ │agent_knowledge│ │agent_performance│         │
│  │    _logs     │ │  _snapshots  │ │   _metrics   │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
│                    + RLS Policies                                │
└──────────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. EmbeddingService
**Responsabilidade**: Gerar embeddings localmente usando GTE-small ou MiniLM-L6-v2

**Interface**:
```python
class EmbeddingService:
    async def generate_embedding(text: str) -> List[float]
    async def generate_batch(texts: List[str]) -> List[List[float]]
    async def get_cached_embedding(text: str) -> Optional[List[float]]
    def get_model_dimension() -> int
```

**Dependências**: sentence-transformers, torch, cache (Redis)

### 2. MemoryService
**Responsabilidade**: CRUD de memory_chunks e similarity search

**Interface**:
```python
class MemoryService:
    async def create_chunk(agent_id: UUID, chunk_type: str, content: str, 
                          metadata: dict, layer: str) -> MemoryChunk
    async def search_similar(agent_id: UUID, query_embedding: List[float], 
                            limit: int, layer_priority: List[str]) -> List[MemoryChunk]
    async def update_usage(chunk_id: UUID) -> None
    async def archive_old_chunks(agent_id: UUID, days: int) -> int
    async def get_by_type(agent_id: UUID, chunk_type: str) -> List[MemoryChunk]
```

**Dependências**: Supabase client, EmbeddingService

### 3. BehaviorService
**Responsabilidade**: Gestão de padrões comportamentais

**Interface**:
```python
class BehaviorService:
    async def create_pattern(agent_id: UUID, pattern_type: str, 
                            trigger_context: dict, action_config: dict) -> BehaviorPattern
    async def get_applicable_patterns(agent_id: UUID, context: dict) -> List[BehaviorPattern]
    async def record_application(pattern_id: UUID, success: bool) -> None
    async def deactivate_low_performers(threshold: float) -> int
```

**Dependências**: Supabase client

### 4. LearningService (ISA)
**Responsabilidade**: Análise de conversas e extração de aprendizados

**Interface**:
```python
class LearningService:
    async def analyze_conversations(agent_id: UUID, time_window: timedelta) -> AnalysisResult
    async def create_learning_log(agent_id: UUID, learning_type: str, 
                                  source_data: dict, confidence: float) -> LearningLog
    async def auto_approve_high_confidence(threshold: float) -> int
    async def consolidate_approved_learnings(agent_id: UUID) -> ConsolidationResult
```

**Dependências**: LangChain, OpenAI/OpenRouter, MemoryService, BehaviorService



### 5. SnapshotService
**Responsabilidade**: Criar e restaurar snapshots de conhecimento

**Interface**:
```python
class SnapshotService:
    async def create_snapshot(agent_id: UUID, snapshot_type: str) -> Snapshot
    async def restore_snapshot(snapshot_id: UUID) -> RestoreResult
    async def archive_old_snapshots(retention_days: int) -> int
```

**Dependências**: Supabase client, MemoryService, BehaviorService

### 6. MetricsService
**Responsabilidade**: Agregação de métricas de performance

**Interface**:
```python
class MetricsService:
    async def record_interaction(agent_id: UUID, success: bool, 
                                response_time_ms: int, satisfaction: float) -> None
    async def get_metrics(agent_id: UUID, period: str) -> MetricsData
    async def calculate_learning_velocity(agent_id: UUID) -> float
```

**Dependências**: Supabase client

### 7. TranscriptionService
**Responsabilidade**: Transcrição local de áudio usando Whisper

**Interface**:
```python
class TranscriptionService:
    async def transcribe_audio(file_path: str) -> TranscriptionResult
    async def detect_language(audio_data: bytes) -> str
    async def segment_by_silence(audio_data: bytes) -> List[AudioSegment]
```

**Dependências**: whisper, ffmpeg

### 8. AgentOrchestrator (Renus Integration)
**Responsabilidade**: Enriquecer prompts com memórias e padrões

**Interface**:
```python
class AgentOrchestrator:
    async def enrich_prompt(agent_id: UUID, message: str, 
                           context: dict) -> EnrichedPrompt
    async def process_with_memory(agent_id: UUID, message: str) -> Response
```

**Dependências**: MemoryService, BehaviorService, EmbeddingService

## Data Models

### agent_dna
```sql
CREATE TABLE agent_dna (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    function TEXT NOT NULL,
    principles JSONB NOT NULL DEFAULT '[]',
    restrictions JSONB NOT NULL DEFAULT '[]',
    tone_of_voice TEXT NOT NULL,
    operational_limits JSONB NOT NULL DEFAULT '{}',
    security_policies JSONB NOT NULL DEFAULT '{}',
    version INTEGER NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(agent_id, version)
);
```

### agent_memory_chunks
```sql
CREATE TABLE agent_memory_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    niche_id UUID REFERENCES niches(id),
    layer TEXT NOT NULL CHECK (layer IN ('base', 'empresa', 'individual')),
    chunk_type TEXT NOT NULL CHECK (chunk_type IN ('business_term', 'process', 'faq', 'product', 'objection', 'plan')),
    content TEXT NOT NULL,
    embedding VECTOR(384),
    metadata JSONB NOT NULL DEFAULT '{}',
    source TEXT,
    confidence_score FLOAT DEFAULT 1.0,
    usage_count INTEGER DEFAULT 0,
    last_used_at TIMESTAMPTZ,
    version INTEGER NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### agent_behavior_patterns
```sql
CREATE TABLE agent_behavior_patterns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    pattern_type TEXT NOT NULL CHECK (pattern_type IN ('response_strategy', 'tone_adjustment', 'flow_optimization')),
    trigger_context JSONB NOT NULL,
    action_config JSONB NOT NULL,
    success_rate FLOAT DEFAULT 0.0,
    total_applications INTEGER DEFAULT 0,
    successful_applications INTEGER DEFAULT 0,
    last_applied_at TIMESTAMPTZ,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### agent_learning_logs
```sql
CREATE TABLE agent_learning_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    learning_type TEXT NOT NULL CHECK (learning_type IN ('memory_added', 'pattern_detected', 'behavior_updated')),
    source_data JSONB NOT NULL,
    analysis JSONB NOT NULL,
    action_taken TEXT NOT NULL,
    confidence FLOAT NOT NULL CHECK (confidence >= 0.0 AND confidence <= 1.0),
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'applied')),
    reviewed_by UUID REFERENCES profiles(id),
    reviewed_at TIMESTAMPTZ,
    rejection_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### agent_knowledge_snapshots
```sql
CREATE TABLE agent_knowledge_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    snapshot_type TEXT NOT NULL DEFAULT 'automatic' CHECK (snapshot_type IN ('automatic', 'manual', 'milestone')),
    memory_count INTEGER NOT NULL,
    pattern_count INTEGER NOT NULL,
    total_interactions INTEGER NOT NULL,
    avg_success_rate FLOAT,
    snapshot_data JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### agent_performance_metrics
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
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(agent_id, metric_date)
);
```

### niches (nova tabela)
```sql
CREATE TABLE niches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE CHECK (name IN ('mmn', 'gabinete', 'clinicas')),
    description TEXT,
    base_knowledge JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Embedding dimension consistency
*For any* text processed by the embedding service, the returned vector dimension should be exactly 384 (GTE-small/MiniLM-L6-v2 standard)
**Validates: Requirements 1.2**

### Property 2: RLS isolation guarantee
*For any* query executed on SICC tables, results should only include records where client_id matches the authenticated user's client
**Validates: Requirements 1.5, 16.2, 16.3, 16.5**

### Property 3: Batch embedding processing
*For any* batch of texts up to 32 items, all texts should be successfully embedded without errors
**Validates: Requirements 2.4**

### Property 4: Embedding cache effectiveness
*For any* identical text requested twice, the second request should return cached result without reprocessing
**Validates: Requirements 2.5**

### Property 5: DNA immutability by learning
*For any* learning process execution, the agent's DNA cognitivo fields (function, principles, restrictions) should remain unchanged
**Validates: Requirements 3.2**

### Property 6: DNA version history
*For any* DNA modification, a new version should be created and all previous versions should remain accessible
**Validates: Requirements 3.4**

### Property 7: Memory chunk completeness
*For any* memory chunk created, it should contain all required fields: type, content, embedding, metadata, layer
**Validates: Requirements 4.1**

### Property 8: Similarity search limit
*For any* similarity search query, the result set should contain at most 5 memory chunks
**Validates: Requirements 4.2, 8.2**

### Property 9: Memory usage tracking
*For any* memory chunk used in a response, its usage_count should be incremented and last_used_at should be updated
**Validates: Requirements 4.3**

### Property 10: Memory quota enforcement
*For any* agent reaching its memory limit, attempting to add new memories should trigger archival of least-used memories
**Validates: Requirements 4.5**

### Property 11: Behavior pattern completeness
*For any* behavior pattern created, it should contain both trigger_context and action_config
**Validates: Requirements 5.1**

### Property 12: Pattern application recording
*For any* behavior pattern applied, the system should record the application with success/failure result
**Validates: Requirements 5.3**

### Property 13: Pattern success rate ordering
*For any* query for applicable patterns, results should be ordered by success_rate in descending order
**Validates: Requirements 5.5**

### Property 14: Learning log completeness
*For any* learning log created, it should contain type, source_data, analysis, and confidence score
**Validates: Requirements 6.2**

### Property 15: Confidence-based auto-approval
*For any* learning log with confidence > 0.8, status should be automatically set to 'approved'
**Validates: Requirements 6.3, 7.1**

### Property 16: Confidence-based pending review
*For any* learning log with confidence between 0.5 and 0.8, status should be set to 'pending'
**Validates: Requirements 6.4, 7.2**

### Property 17: Confidence-based rejection
*For any* learning log with confidence < 0.5, it should be automatically discarded
**Validates: Requirements 6.5**

### Property 18: Human approval creates artifacts
*For any* learning log approved by human, corresponding memory_chunk or behavior_pattern should be created
**Validates: Requirements 7.3**

### Property 19: Human rejection records reason
*For any* learning log rejected by human, status should be 'rejected' and reviewed_by should be set
**Validates: Requirements 7.4**

### Property 20: Threshold validation
*For any* auto-approval threshold configured, value should be between 0.0 and 1.0 inclusive
**Validates: Requirements 7.5, 15.2**

### Property 21: Similarity search execution
*For any* message received by agent, similarity search should be executed on agent's memories
**Validates: Requirements 8.1**

### Property 22: Prompt token limit
*For any* enriched prompt generated, total token count should not exceed 8000 tokens
**Validates: Requirements 8.4**

### Property 23: Snapshot completeness
*For any* snapshot created, it should contain memory_count, pattern_count, total_interactions, and avg_success_rate
**Validates: Requirements 9.2**

### Property 24: Rollback deactivation
*For any* rollback executed, all memories and patterns created after the snapshot timestamp should be marked is_active=false
**Validates: Requirements 9.4**

### Property 25: Interaction metrics recording
*For any* agent interaction, metrics should record total, success status, response_time, and satisfaction
**Validates: Requirements 10.1**

### Property 26: Memory usage metrics
*For any* memory chunk used, the daily metrics should increment memory_chunks_used counter
**Validates: Requirements 10.2**

### Property 27: Pattern application metrics
*For any* pattern applied, the daily metrics should increment patterns_applied counter
**Validates: Requirements 10.3**

### Property 28: Learning consolidation metrics
*For any* learning consolidated, the daily metrics should increment new_learnings counter
**Validates: Requirements 10.4**

### Property 29: Metrics aggregation
*For any* metrics query, data should be correctly aggregated by day, week, or month as requested
**Validates: Requirements 10.5**

### Property 30: Transcription memory creation
*For any* audio transcription completed, memory_chunks should be created with embeddings of the content
**Validates: Requirements 11.4**

### Property 31: Learning velocity calculation
*For any* agent, learning velocity should equal new_learnings divided by days active
**Validates: Requirements 12.3**

### Property 32: Top memories ordering
*For any* top memories query, results should be ordered by usage_count in descending order
**Validates: Requirements 12.4**

### Property 33: Pattern success rate display
*For any* active pattern displayed, its current success_rate should be shown
**Validates: Requirements 12.5**

### Property 34: Memory type filtering
*For any* filter applied by type, only memories matching that exact type should be returned
**Validates: Requirements 13.2**

### Property 35: Memory edit versioning
*For any* memory edited, a new version should be created and previous version should remain in history
**Validates: Requirements 13.4**

### Property 36: Memory deactivation preservation
*For any* memory deactivated, is_active should be false but the record should not be deleted
**Validates: Requirements 13.5**

### Property 37: Batch approval processing
*For any* batch approval operation, all selected learning logs should be processed simultaneously
**Validates: Requirements 14.3**

### Property 38: Learning processing audit
*For any* learning log processed, status and reviewed_by should be updated
**Validates: Requirements 14.5**

### Property 39: Memory quota enforcement
*For any* agent with defined memory limit, total active memories should not exceed the quota
**Validates: Requirements 15.4**

### Property 40: Layer priority ordering
*For any* memory search, results should prioritize individual layer, then empresa, then base
**Validates: Requirements 17.3**

### Property 41: Business plan layer restriction
*For any* business plan memory created, layer should be 'empresa'
**Validates: Requirements 17.4**

### Property 42: Niche knowledge propagation
*For any* base niche knowledge update, all agents of that niche should receive the update
**Validates: Requirements 17.5**

### Property 43: Learning source recording
*For any* learning log created, source_data should contain complete origin information
**Validates: Requirements 18.1**

### Property 44: Approval audit trail
*For any* approval action, reviewed_by and reviewed_at should be recorded
**Validates: Requirements 18.2**

### Property 45: Memory usage audit
*For any* memory used, the conversation_id where it was applied should be recorded in metadata
**Validates: Requirements 18.3**

### Property 46: Pattern application audit
*For any* pattern applied, context and result should be recorded
**Validates: Requirements 18.4**

### Property 47: Log filtering capability
*For any* log query with filters, results should match all specified filter criteria (agent, date, type)
**Validates: Requirements 18.5**

### Property 48: Structured logging format
*For any* log generated, it should be valid JSON with required fields
**Validates: Requirements 19.5**

### Property 49: Agent creation initialization
*For any* agent created, DNA, empty memory, and learning cycle should all be initialized
**Validates: Requirements 20.3**

### Property 50: Sub-agent knowledge inheritance
*For any* sub-agent created, it should inherit base knowledge from parent agent
**Validates: Requirements 20.4**

## Error Handling

### Embedding Service Errors
- **Model Load Failure**: Fallback to MiniLM-L6-v2, log error, alert admin
- **Embedding Generation Failure**: Return cached if available, otherwise return error with retry logic
- **Dimension Mismatch**: Reject and log, do not store invalid embeddings

### Database Errors
- **RLS Violation**: Return 403 Forbidden, log security event
- **Connection Timeout**: Retry with exponential backoff (3 attempts)
- **Constraint Violation**: Return 400 Bad Request with specific error message

### Learning Service Errors
- **ISA Analysis Failure**: Log error, mark learning as failed, do not block other learnings
- **Low Confidence**: Automatically discard (< 0.5) or queue for review (0.5-0.8)
- **Consolidation Failure**: Rollback transaction, log error, retry later

### Integration Errors
- **Renus Integration Failure**: Operate in degraded mode (no memory enrichment), log warning
- **Whisper Transcription Failure**: Log error, mark file for manual review
- **Celery Worker Failure**: Retry job with exponential backoff, alert if max retries exceeded

## Testing Strategy

### Unit Tests
- Test each service method independently with mocked dependencies
- Test data model validations and constraints
- Test utility functions (embedding cache, token counting, etc)
- Coverage target: 80%+

### Property-Based Tests
Each correctness property listed above should have a corresponding property-based test using pytest with Hypothesis library.

Example structure:
```python
from hypothesis import given, strategies as st
import pytest

@given(st.text(min_size=1, max_size=1000))
def test_property_1_embedding_dimension(text):
    """Property 1: Embedding dimension consistency"""
    embedding = embedding_service.generate_embedding(text)
    assert len(embedding) == 384
```

**Property test requirements**:
- Minimum 100 iterations per property test
- Each test tagged with: `# Feature: sprint-10-sicc, Property X: [description]`
- Tests should cover edge cases (empty strings, very long texts, special characters)
- Tests should verify both success and failure paths

### Integration Tests
- Test complete flows: message → memory search → enrichment → response
- Test ISA analysis → learning log → approval → consolidation
- Test snapshot creation → rollback → verification
- Test RLS isolation with multiple clients
- Test Whisper transcription → chunking → embedding → storage

### Performance Tests
- Similarity search with 100k embeddings should complete < 500ms
- Batch embedding of 32 texts should complete < 3 seconds
- Memory enrichment should add < 200ms to response time
- Database queries should use proper indexes (verify with EXPLAIN ANALYZE)

### Security Tests
- Verify RLS prevents cross-client data access
- Test SQL injection resistance
- Verify authentication on all SICC endpoints
- Test rate limiting on embedding endpoint

## Deployment Strategy

### Phase 1: Infrastructure (Week 1)
- Install pgvector extension
- Create all SICC tables with RLS
- Deploy embedding service with GTE-small
- Set up Celery workers for SICC jobs

### Phase 2: Core Services (Week 2-3)
- Deploy MemoryService, BehaviorService, EmbeddingService
- Deploy LearningService (ISA integration)
- Deploy SnapshotService, MetricsService
- Integration with existing Renus service

### Phase 3: UI & Monitoring (Week 4)
- Deploy Evolution, Memory, Learning Queue pages
- Deploy Settings page
- Set up monitoring and alerting
- Performance tuning

### Phase 4: Transcription & Advanced (Week 5)
- Deploy Whisper transcription service
- Implement audio processing pipeline
- Advanced features (niche propagation, layer management)

### Phase 5: Testing & Optimization (Week 6-7)
- Complete test suite execution
- Performance optimization
- Security audit
- Documentation

### Rollback Plan
- Each phase has database migration with down script
- Snapshots taken before each deployment
- Feature flags to disable SICC if issues arise
- Degraded mode: agents work without memory enrichment

## Monitoring and Observability

### Key Metrics
- Embedding generation time (p50, p95, p99)
- Similarity search latency
- Memory usage per agent
- Learning approval rate
- ISA analysis success rate
- Celery queue sizes
- Database connection pool usage

### Alerts
- Embedding service down
- pgvector query > 1 second
- Celery queue > 1000 items
- Learning approval rate < 50%
- RLS policy violation detected
- Disk space < 20% on VPS

### Logging
- Structured JSON logs
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Include: timestamp, service, agent_id, client_id, action, duration, result
- Retention: 30 days in database, 90 days archived

### Dashboards
- SICC Health Dashboard (Grafana)
- Agent Evolution Metrics
- Learning Pipeline Status
- Performance Metrics
- Error Rates

---

**Document Version**: 1.0  
**Last Updated**: 2025-12-07  
**Status**: Ready for Implementation
