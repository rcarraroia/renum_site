# Design Document - Sprint 05A: Validação e Correção Completa do Sistema

## Overview

Este sprint implementa uma validação sistemática e completa de 100% do sistema RENUM. A análise inicial mostrou 82% de funcionalidade, mas apenas testou operações GET (leitura). Este design cobre validação de CRUD completo, agentes, WebSocket e frontend.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VALIDAÇÃO SISTEMÁTICA                     │
│                                                              │
│  Fase 1: Correção de Bugs (2.5h)                           │
│  ├── Health Check                                           │
│  ├── ISA Agent                                              │
│  ├── Client Model                                           │
│  └── Rotas Redirect                                         │
│                                                              │
│  Fase 2: CRUD Completo (4h)                                │
│  ├── Clients (POST, GET/:id, PUT, DELETE)                  │
│  ├── Leads (POST, GET/:id, PUT, DELETE)                    │
│  ├── Projects (POST, GET/:id, PUT, DELETE)                 │
│  ├── Conversations (POST, GET/:id, POST messages)          │
│  └── Interviews (POST start, GET/:id)                      │
│                                                              │
│  Fase 3: Agentes (3h)                                       │
│  ├── RENUS Agent (inicializar, responder, trace)           │
│  ├── ISA Agent (comando, executar, salvar)                 │
│  └── Discovery Agent (processar, extrair, relatório)       │
│                                                              │
│  Fase 4: WebSocket (2h)                                     │
│  ├── Conexão                                                │
│  ├── Enviar/Receber mensagens                              │
│  ├── Salvar no banco                                        │
│  ├── Typing indicators                                      │
│  └── Presence status                                        │
│                                                              │
│  Fase 5: Frontend (3h)                                      │
│  └── Testar 10 menus com CRUD completo                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ RELATÓRIO FINAL  │
                    │  - % Funcional   │
                    │  - Bugs          │
                    │  - Recomendação  │
                    └──────────────────┘
```

## Components and Interfaces

### 1. Scripts de Validação

**validate_crud.py**
- Testa CRUD completo de todas entidades
- Retorna % de sucesso por entidade
- Documenta erros encontrados

**validate_agents.py**
- Testa inicialização e resposta de cada agente
- Verifica traces no LangSmith
- Valida salvamento de comandos

**validate_websocket.py**
- Testa conexão, envio, recebimento
- Valida salvamento no banco
- Testa typing e presence

**validate_frontend.py**
- Guia manual de testes por menu
- Checklist de funcionalidades
- Captura de evidências

### 2. Correções de Bugs

**Bug 1: Health Check**
- Já funciona (< 2s)
- Nenhuma ação necessária

**Bug 2: ISA Agent**
- Problema: invoke() recebe dict mas espera messages + context separados
- Solução: Ajustar chamada em isa.py routes

**Bug 3: Client Model**
- Problema: Campo "segment" pode estar sendo exigido
- Solução: Tornar opcional ou remover validação

**Bug 4: Rotas Redirect**
- Problema: 307 em /api/sub-agents e /api/renus-config
- Solução: Remover trailing slash ou ajustar configuração

## Data Models

Nenhum modelo novo. Validação usa modelos existentes.

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system.*

### Property 1: CRUD Completeness
*For any* entity (Client, Lead, Project, Conversation, Interview), all CRUD operations (Create, Read, Update, Delete) should succeed without errors when given valid data.
**Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5**

### Property 2: Agent Response Consistency
*For any* agent (RENUS, ISA, Discovery), when given a valid message, the agent should return a response without timeout or error 500.
**Validates: Requirements 3.1, 3.2, 3.3**

### Property 3: WebSocket Bidirectionality
*For any* WebSocket connection, when a message is sent, a response should be received within reasonable time (< 10s).
**Validates: Requirements 4.2**

### Property 4: Data Persistence
*For any* create or update operation, the data should be retrievable from the database immediately after the operation.
**Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5**

### Property 5: Frontend-Backend Consistency
*For any* frontend operation (create, update, delete), the backend API should reflect the change and the frontend should display updated data.
**Validates: Requirements 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8**

### Property 6: Bug Documentation Completeness
*For any* bug found, documentation should include: what broke, how to reproduce, exact error, and estimated fix time.
**Validates: Requirements 6.1, 6.2, 6.3**

### Property 7: Validation Report Accuracy
*For any* component validated, the final report should accurately reflect the % of functionality working.
**Validates: Requirements 7.1, 7.2**

## Error Handling

### Validation Errors
- Se endpoint retorna erro, documentar e continuar
- Não parar validação por um erro
- Acumular todos os erros para relatório final

### Timeout Handling
- Timeout de 10s para operações normais
- Timeout de 30s para agentes (LLM pode demorar)
- Timeout de 5s para WebSocket

### Data Cleanup
- Todos os dados de teste DEVEM ter prefixo "TEST_" no campo name/company_name
- Exemplo: "TEST_Cliente_ABC", "TEST_Lead_XYZ"
- Ao final da validação (Fase 5.5), deletar TODOS os registros TEST_*
- Verificar limpeza nas tabelas: clients, leads, projects, conversations, interviews, messages
- Confirmar zero registros TEST_* antes de gerar relatório final

## Testing Strategy

### Unit Tests
Não aplicável - este sprint É o teste do sistema.

### Integration Tests
Cada script de validação é um teste de integração:
- validate_crud.py testa integração backend + banco
- validate_agents.py testa integração agentes + LLM + banco
- validate_websocket.py testa integração WebSocket + backend + banco
- validate_frontend.py testa integração frontend + backend

### Manual Tests
Frontend requer testes manuais:
- Abrir navegador
- Navegar pelos menus
- Executar operações
- Verificar resultados

### Validation Criteria
- ✅ 90%+ funcional = Pronto para Sprint 06
- ⚠️ 70-90% funcional = Corrigir bugs críticos primeiro
- ❌ < 70% funcional = Focar em correções antes de avançar
