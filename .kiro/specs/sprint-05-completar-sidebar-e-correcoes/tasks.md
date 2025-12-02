# Tasks - Sprint 05: Completar Menus Sidebar + Correções Críticas

## Overview

Este plano de implementação organiza as tarefas em 4 fases principais, priorizando correções críticas que bloqueiam deploy, seguidas por integrações importantes e quick wins dos menus sidebar.

**Estimativa Total:** 18-23 horas (3-4 dias)

---

## 🔴 PHASE 1: Correções Críticas (PRIORIDADE MÁXIMA)

**Tempo Estimado:** 20 minutos  
**Objetivo:** Eliminar bugs que impedem backend de iniciar

### TASK-001: Corrigir Bug de Import em interviews.py ✅
**Objective:** Adicionar imports faltantes de typing

**Steps:**
1. Abrir `backend/src/api/routes/interviews.py`
2. Localizar linha 1-10 (seção de imports)
3. Adicionar: `from typing import Dict, Any, Optional, List`
4. Verificar se há outros imports faltantes no arquivo
5. Salvar arquivo

**Acceptance Criteria:**
- [x] Import `from typing import Dict, Any, Optional, List` adicionado
- [x] Arquivo não tem erros de sintaxe
- [x] `python -m py_compile backend/src/api/routes/interviews.py` executa sem erros

**Estimated Time:** 5 minutes  
**Priority:** 🔴 CRITICAL  
**Status:** ✅ COMPLETO

---

### TASK-002: Corrigir Bug JWT_SECRET em ws_handler.py ✅
**Objective:** Usar SECRET_KEY correto para validação JWT

**Steps:**
1. Abrir `backend/src/api/websocket/ws_handler.py`
2. Localizar linha 162 (ou buscar por `JWT_SECRET`)
3. Substituir `settings.JWT_SECRET` por `settings.SECRET_KEY`
4. Verificar se há outras ocorrências de JWT_SECRET no arquivo
5. Salvar arquivo

**Acceptance Criteria:**
- [x] `settings.JWT_SECRET` substituído por `settings.SECRET_KEY`
- [x] Nenhuma outra ocorrência de JWT_SECRET no arquivo
- [x] WebSocket autentica corretamente com token válido

**Estimated Time:** 5 minutes  
**Priority:** 🔴 CRITICAL  
**Status:** ✅ COMPLETO

---

### TASK-003: Configurar ISA Agent ✅
**Objective:** Configurar ISA Agent para usar OpenAI

**Steps:**
1. Trocar ChatAnthropic por ChatOpenAI no IsaAgent
2. Atualizar DEFAULT_ISA_MODEL para gpt-4o-mini
3. Corrigir imports faltantes (List)
4. Testar backend

**Acceptance Criteria:**
- [x] IsaAgent usa ChatOpenAI
- [x] DEFAULT_ISA_MODEL = gpt-4o-mini
- [x] Imports corrigidos
- [x] Backend inicia sem erros

**Estimated Time:** 10 minutes  
**Priority:** 🔴 CRITICAL  
**Status:** ✅ COMPLETO

---

### TASK-004: Validar Backend Inicia Sem Erros ✅
**Objective:** Confirmar que correções funcionaram

**Steps:**
1. Abrir terminal na pasta `backend/`
2. Ativar venv: `venv\Scripts\activate` (Windows) ou `source venv/bin/activate` (Linux/Mac)
3. Executar: `python -m src.main`
4. Verificar logs no console
5. Confirmar mensagem "Application startup complete"
6. Acessar http://localhost:8000/health
7. Acessar http://localhost:8000/docs

**Acceptance Criteria:**
- [x] Backend inicia sem NameError
- [x] Backend inicia sem ModuleNotFoundError
- [x] Backend carrega com sucesso
- [x] ISA Agent usa OpenAI (não Anthropic)
- [x] Todos imports corretos

**Estimated Time:** 5 minutes (se tudo ok)  
**Priority:** 🔴 CRITICAL  
**Status:** ✅ COMPLETO

---

## 🟠 PHASE 2: Integrações Importantes

**Tempo Estimado:** 6-8 horas  
**Objetivo:** Conectar ISA e Public Chat aos agentes reais

### TASK-005: Conectar ISA Agent à Rota /api/isa/chat ✅
**Objective:** Substituir resposta mock por processamento real com IsaAgent

**Steps:**
1. Abrir `backend/src/api/routes/isa.py`
2. Adicionar imports:
   ```python
   from src.agents.isa import IsaAgent
   from src.services.isa_command_service import IsaCommandService
   ```
3. Criar instância do agente (fora da função ou como singleton)
4. Localizar função `chat_with_isa()` (linha ~40)
5. Remover código mock (linhas 48-60)
6. Implementar processamento real:
   - Chamar `isa_agent.invoke()` com mensagem
   - Salvar comando em `isa_commands` via service
   - Retornar resultado real
7. Adicionar tratamento de erros
8. Testar com comando "list interviews"

**Acceptance Criteria:**
- [x] IsaAgent importado e inicializado
- [x] Função `chat_with_isa()` chama agente real
- [x] Comando salvo em `isa_commands` table
- [x] Response contém `command_executed` do agente
- [x] Erros são tratados e retornam mensagem clara
- [x] Código mock removido
- [x] Histórico de comandos implementado

**Estimated Time:** 2-3 hours  
**Priority:** 🟠 HIGH  
**Status:** ✅ COMPLETO

---

### TASK-006: Implementar send_message em public_chat.py ✅
**Objective:** Processar mensagens com sub-agentes reais

**Steps:**
1. Abrir `backend/src/api/routes/public_chat.py`
2. Localizar função `send_message()` (linha ~90)
3. Adicionar imports:
   ```python
   from src.agents.discovery_agent import DiscoveryAgent
   ```
4. Implementar lógica:
   - Buscar sub-agente por slug
   - Criar ou recuperar interview
   - Salvar mensagem do usuário
   - Processar com agente (DiscoveryAgent)
   - Salvar resposta do agente
   - Calcular progresso
   - Completar entrevista se todos campos coletados
5. Retornar ChatMessageResponse com dados reais
6. Testar fluxo completo

**Acceptance Criteria:**
- [x] Endpoint carrega sub-agente por slug
- [x] Cria interview se não existir
- [x] InterviewService.process_message_with_agent implementado
- [x] Agente selecionado dinamicamente (Discovery ou MMN)
- [x] Mensagens salvas corretamente
- [x] Progresso calculado
- [x] Entrevista completa quando necessário

**Estimated Time:** 3-4 hours  
**Priority:** 🟠 HIGH  
**Status:** ✅ COMPLETO

---

### TASK-007: Implementar get_interview_history em public_chat.py ✅
**Objective:** Retornar histórico completo de mensagens

**Steps:**
1. Abrir `backend/src/api/routes/public_chat.py`
2. Localizar função `get_interview_history()` (linha ~151)
3. Remover código mock
4. Implementar:
   - Buscar interview por ID
   - Carregar messages relacionadas (ordenadas por timestamp)
   - Retornar histórico completo
5. Adicionar paginação se necessário
6. Testar com interview existente

**Acceptance Criteria:**
- [x] Endpoint retorna histórico real do banco
- [x] Mensagens ordenadas cronologicamente
- [x] Inclui role (user/assistant/system)
- [x] Inclui content e timestamp
- [x] Retorna 404 se interview não existe
- [x] Status da entrevista incluído

**Estimated Time:** 1-2 hours  
**Priority:** 🟠 HIGH  
**Status:** ✅ COMPLETO

---

## 📊 PHASE 3: Menus Sidebar (Quick Wins)

**Tempo Estimado:** 10-12 horas  
**Objetivo:** Conectar todos os menus ao backend real

### TASK-008: Criar DashboardService e Endpoint ✅
**Objective:** Implementar backend para Overview Dashboard

**Steps:**
1. Criar `backend/src/services/dashboard_service.py`
2. Implementar `DashboardService` class:
   - `get_stats()` - métricas agregadas
   - `_get_recent_activities()` - últimas 10 ações
3. Criar `backend/src/api/routes/dashboard.py`
4. Implementar endpoint `GET /api/dashboard/stats`
5. Registrar router em `main.py`
6. Testar endpoint via Swagger

**Acceptance Criteria:**
- [x] DashboardService criado
- [x] Método `get_stats()` retorna métricas corretas
- [x] Endpoint `/api/dashboard/stats` funciona
- [x] Retorna: total_clients, total_leads, total_conversations, active_interviews
- [x] Retorna: completion_rate calculado corretamente
- [x] Retorna: recent_activities (últimas 10)
- [x] Router registrado em main.py

**Estimated Time:** 2-3 hours  
**Priority:** 🟡 MEDIUM  
**Status:** ✅ COMPLETO

---

### TASK-009: Conectar Frontend Overview ao Backend ✅
**Objective:** Substituir dados mock por API real

**Steps:**
1. Criar `frontend/src/services/dashboardService.ts`
2. Implementar `getStats()` function
3. Abrir `frontend/src/pages/dashboard/AdminOverview.tsx`
4. Remover dados mock
5. Usar `dashboardService.getStats()`
6. Implementar loading states
7. Implementar error handling
8. Atualizar gráficos com dados reais (Recharts)
9. Testar no navegador

**Acceptance Criteria:**
- [x] dashboardService.ts criado
- [x] AdminOverview.tsx usa API real
- [x] Cards de métricas mostram números reais
- [x] Lista de atividades recentes aparece
- [x] Loading states funcionam
- [x] Erros são tratados e exibidos

**Estimated Time:** 2 hours  
**Priority:** 🟡 MEDIUM  
**Status:** ✅ COMPLETO

---

### TASK-010: Criar conversationService.ts no Frontend ✅
**Objective:** Implementar service para API de conversas

**Steps:**
1. Criar `frontend/src/services/conversationService.ts`
2. Implementar funções:
   - `listConversations(filters)` - GET /api/conversations
   - `getConversation(id)` - GET /api/conversations/{id}
   - `createConversation(data)` - POST /api/conversations
   - `updateConversation(id, data)` - PUT /api/conversations/{id}
   - `deleteConversation(id)` - DELETE /api/conversations/{id}
   - `markAsRead(id)` - POST /api/conversations/{id}/mark-read
3. Adicionar tipos TypeScript (Conversation interface)
4. Adicionar tratamento de erros
5. Testar cada função

**Acceptance Criteria:**
- [x] conversationService.ts criado (já existe do Sprint 03)
- [x] Todas 6 funções implementadas
- [x] Tipos TypeScript definidos
- [x] Error handling presente

**Estimated Time:** 1 hour  
**Priority:** 🟡 MEDIUM  
**Status:** ✅ COMPLETO (já existia)

---

### TASK-011: Conectar ConversationsPage ao Backend ✅
**Objective:** Substituir mock por API real

**Acceptance Criteria:**
- [x] Página implementada no Sprint 03
- [x] ConversationService conectado
- [x] WebSocket funcional

**Estimated Time:** 2-3 hours  
**Priority:** 🟡 MEDIUM  
**Status:** ✅ COMPLETO (Sprint 03)

---

### TASK-012: Conectar AdminInterviewsPage ao Backend ✅
**Objective:** Substituir mock por API real

**Acceptance Criteria:**
- [x] Página implementada no Sprint 04
- [x] InterviewService conectado
- [x] 4 entrevistas + 56 mensagens no banco

**Estimated Time:** 2 hours  
**Priority:** 🟡 MEDIUM  
**Status:** ✅ COMPLETO (Sprint 04)

---

### TASK-013: Completar Backend de renus_config ✅
**Objective:** Implementar endpoints faltantes

**Acceptance Criteria:**
- [x] Endpoints implementados no Sprint 04
- [x] RenusConfigService funcional

**Estimated Time:** 2 hours  
**Priority:** 🟡 MEDIUM  
**Status:** ✅ COMPLETO (Sprint 04)

---

### TASK-014: Conectar Frontend de Config RENUS ao Backend ✅
**Objective:** Garantir que todas as abas salvam no backend

**Acceptance Criteria:**
- [x] Todas tabs implementadas no Sprint 04
- [x] RenusConfigService conectado
- [x] SubAgentsTab funcional

**Estimated Time:** 3 hours  
**Priority:** 🟡 MEDIUM  
**Status:** ✅ COMPLETO (Sprint 04)

---

## 📈 PHASE 4: Relatórios e Configurações (Opcional)

**Tempo Estimado:** 6-8 horas  
**Objetivo:** Implementar funcionalidades adicionais

### TASK-015: Criar ReportService e Endpoints
**Objective:** Implementar backend de relatórios

**Steps:**
1. Criar `backend/src/services/report_service.py`
2. Implementar métodos:
   - `generate_conversations_report(start_date, end_date)`
   - `generate_interviews_report(start_date, end_date)`
   - `generate_agents_report(start_date, end_date)`
   - `export_to_csv(data, filename)`
3. Criar `backend/src/api/routes/reports.py`
4. Implementar endpoints:
   - `GET /api/reports/conversations`
   - `GET /api/reports/interviews`
   - `GET /api/reports/agents`
5. Registrar router em main.py
6. Testar endpoints

**Acceptance Criteria:**
- [ ] ReportService criado
- [ ] 3 métodos de geração implementados
- [ ] Método de exportação CSV implementado
- [ ] 3 endpoints funcionando
- [ ] Filtros por date range funcionam
- [ ] Dados agregados corretos

**Estimated Time:** 3-4 hours  
**Priority:** 🟢 LOW

---

### TASK-016: Criar Frontend de Relatórios
**Objective:** Implementar UI de relatórios

**Steps:**
1. Criar `frontend/src/services/reportService.ts`
2. Criar `frontend/src/pages/reports/ReportsPage.tsx`
3. Implementar seletor de tipo de relatório
4. Implementar filtros de data
5. Implementar visualização de dados (tabelas/gráficos)
6. Implementar botão "Exportar CSV"
7. Testar fluxo completo

**Acceptance Criteria:**
- [ ] reportService.ts criado
- [ ] ReportsPage.tsx criado
- [ ] Seletor de tipo funciona
- [ ] Filtros de data funcionam
- [ ] Dados carregam do backend
- [ ] Gráficos renderizam (Recharts)
- [ ] Exportar CSV funciona

**Estimated Time:** 3-4 hours  
**Priority:** 🟢 LOW

---

### TASK-017: Criar SettingsService e Endpoints
**Objective:** Implementar backend de configurações

**Steps:**
1. Criar `backend/src/models/settings.py`
2. Criar `backend/src/services/settings_service.py`
3. Criar `backend/src/api/routes/settings.py`
4. Implementar endpoints:
   - `GET /api/settings`
   - `PUT /api/settings`
5. Registrar router em main.py
6. Testar endpoints

**Acceptance Criteria:**
- [ ] Models de settings criados
- [ ] SettingsService criado
- [ ] 2 endpoints funcionando
- [ ] Configurações salvam no banco
- [ ] RLS aplicado (usuário vê apenas suas configs)

**Estimated Time:** 2 hours  
**Priority:** 🟢 LOW

---

### TASK-018: Criar Frontend de Configurações
**Objective:** Implementar UI de configurações

**Steps:**
1. Criar `frontend/src/services/settingsService.ts`
2. Criar `frontend/src/pages/settings/SettingsPage.tsx`
3. Implementar 4 tabs:
   - Perfil (nome, email, avatar)
   - Preferências (idioma, timezone, tema)
   - Notificações (email, push, som)
   - Segurança (senha, 2FA, sessões)
4. Conectar ao backend
5. Testar cada tab

**Acceptance Criteria:**
- [ ] settingsService.ts criado
- [ ] SettingsPage.tsx com 4 tabs
- [ ] Tab Perfil funciona
- [ ] Tab Preferências funciona
- [ ] Tab Notificações funciona
- [ ] Tab Segurança funciona
- [ ] Alterações salvam no backend
- [ ] Toast de sucesso/erro aparece

**Estimated Time:** 3-4 hours  
**Priority:** 🟢 LOW

---

## 🧹 PHASE 5: Limpeza e Melhorias

**Tempo Estimado:** 2-3 horas  
**Objetivo:** Remover código duplicado e consolidar

### TASK-019: Remover Código Duplicado em subagent_service.py ✅
**Objective:** Eliminar métodos síncronos duplicados

**Acceptance Criteria:**
- [x] Código duplicado não encontrado (já foi removido)
- [x] Apenas métodos async presentes

**Estimated Time:** 1 hour  
**Priority:** 🟡 MEDIUM  
**Status:** ✅ COMPLETO (já estava limpo)

---

### TASK-020: Consolidar Rotas de Sub-Agentes ✅
**Objective:** Remover arquivo duplicado

**Acceptance Criteria:**
- [x] Arquivo `subagents.py` vazio deletado
- [x] Apenas `sub_agents.py` existe
- [x] Import em main.py correto

**Estimated Time:** 30 minutes  
**Priority:** 🟡 MEDIUM  
**Status:** ✅ COMPLETO

---

### TASK-021: Implementar Filtros Avançados em CRUDs
**Objective:** Adicionar filtros por data e múltiplos campos

**Steps:**
1. Atualizar `ClientService`:
   - Adicionar filtro por date range
   - Adicionar busca por múltiplos campos
2. Atualizar `LeadService`:
   - Adicionar filtro por date range
   - Adicionar busca por múltiplos campos
3. Atualizar `ProjectService`:
   - Adicionar filtro por date range
   - Adicionar busca por múltiplos campos
4. Atualizar rotas correspondentes
5. Atualizar frontend para usar novos filtros
6. Testar cada CRUD

**Acceptance Criteria:**
- [ ] Filtros por date range funcionam
- [ ] Busca por múltiplos campos funciona
- [ ] Frontend usa novos filtros
- [ ] Performance aceitável (< 1s)
- [ ] Paginação funciona com filtros

**Estimated Time:** 2-3 hours  
**Priority:** 🟢 LOW

---

### TASK-022: Adicionar Exportação CSV em CRUDs
**Objective:** Permitir exportar dados em CSV

**Steps:**
1. Criar função utilitária `export_to_csv(data, filename)`
2. Adicionar endpoint `GET /api/clients/export`
3. Adicionar endpoint `GET /api/leads/export`
4. Adicionar endpoint `GET /api/projects/export`
5. Adicionar botão "Exportar" no frontend
6. Testar exportação

**Acceptance Criteria:**
- [ ] Função de exportação criada
- [ ] 3 endpoints de export funcionam
- [ ] Botão "Exportar" aparece no frontend
- [ ] CSV gerado corretamente
- [ ] Encoding UTF-8 correto (acentos)
- [ ] Headers corretos no CSV

**Estimated Time:** 1-2 hours  
**Priority:** 🟢 LOW

---

## ✅ PHASE 6: Validação Final

**Tempo Estimado:** 2 hours  
**Objetivo:** Garantir que tudo funciona end-to-end

### TASK-023: Executar Checklist de Validação Completo
**Objective:** Validar todos os requisitos do sprint

**Steps:**
1. **Backend:**
   - [x] Backend inicia sem erros
   - [x] ISA executa comandos reais
   - [x] Public chat processa com agentes
   - [x] Dashboard stats funciona
   - [ ] Testar todos endpoints via Swagger

2. **Frontend:**
   - [x] Overview Dashboard funciona
   - [x] ISA funciona
   - [x] Conversas funcionam (Sprint 03)
   - [x] Pesquisas funcionam (Sprint 04)
   - [x] Config RENUS funciona (Sprint 04)
   - [ ] Testar fluxo completo

3. **Database:**
   - [x] 12 tabelas existem
   - [x] RLS habilitado
   - [x] Dados salvam corretamente

4. **Integração E2E:**
   - [ ] Login → Dashboard → ISA → Conversas
   - [ ] Chat público funciona
   - [ ] Entrevistas funcionam

**Acceptance Criteria:**
- [x] Backend funcional
- [x] Frontend conectado
- [ ] Testes E2E completos

**Estimated Time:** 2 hours  
**Priority:** 🔴 CRITICAL  
**Status:** ⏳ AGUARDANDO TESTES

---

## 📊 Summary

**Total Tasks:** 23  
**Critical:** 4 (TASK-001 a TASK-004)  
**High:** 6 (TASK-005 a TASK-007, TASK-013, TASK-014)  
**Medium:** 7 (TASK-008 a TASK-012, TASK-019, TASK-020)  
**Low:** 5 (TASK-015 a TASK-018, TASK-021, TASK-022)  
**Validation:** 1 (TASK-023)

**Estimated Total Time:** 18-23 hours (3-4 dias)

**Phases:**
- Phase 1 (Correções): 20 minutos ⚡
- Phase 2 (Integrações): 6-8 horas 🟠
- Phase 3 (Menus Sidebar): 10-12 horas 📊
- Phase 4 (Relatórios/Config): 6-8 horas 📈 (Opcional)
- Phase 5 (Limpeza): 2-3 horas 🧹
- Phase 6 (Validação): 2 horas ✅

**Critical Path:**
1. Phase 1 (Correções) → Phase 2 (Integrações) → Phase 3 (Menus) → Phase 6 (Validação)
2. Phase 4 e 5 podem ser executadas em paralelo ou depois

**Dependencies:**
- Phase 2 depende de Phase 1 completa
- Phase 3 depende de Phase 2 completa
- Phase 6 depende de todas as anteriores

**Checkpoints:**
- ✅ Checkpoint 1: Backend inicia sem erros (após TASK-004)
- ✅ Checkpoint 2: ISA funciona (após TASK-005)
- ✅ Checkpoint 3: Public chat funciona (após TASK-007)
- ✅ Checkpoint 4: Todos menus funcionam (após TASK-014)
- ✅ Checkpoint 5: Sistema validado (após TASK-023)

---

**Implementation Plan Version:** 1.0  
**Last Updated:** 2025-11-30  
**Status:** Ready for Execution
