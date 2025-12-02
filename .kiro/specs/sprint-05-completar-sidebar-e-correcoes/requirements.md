# Requirements - Sprint 05: Completar Menus Sidebar + Correções Críticas

## Overview

Este sprint foca em **corrigir bugs críticos** que impedem o deploy e **completar funcionalidades dos menus sidebar** do dashboard admin, conectando frontend mock ao backend real implementado nos sprints anteriores.

**Prioridade:** 🔴 ALTA - Bloqueadores de deploy + Quick wins para MVP

---

## 🔴 PARTE 1: Correções Críticas (Bloqueadores)

### REQ-1: Corrigir Bugs de Import e Configuração

**ID:** REQ-SPRINT05-001  
**Priority:** Critical  
**Type:** Bug Fix

**Description:**
WHEN o backend é iniciado  
THEN deve iniciar sem erros de import ou configuração  
AND todas as dependências devem estar corretamente importadas  
AND todas as variáveis de ambiente obrigatórias devem estar configuradas

**Acceptance Criteria:**
1. Backend inicia sem `NameError: name 'Dict' is not defined`
2. Backend inicia sem `NameError: name 'JWT_SECRET' is not defined`
3. Backend inicia sem warning de `ANTHROPIC_API_KEY` faltando
4. Comando `python -m src.main` executa com sucesso
5. Logs mostram "Application startup complete" sem erros

**Related Requirements:** REQ-SPRINT05-002, REQ-SPRINT05-003

---

### REQ-2: Conectar ISA Agent à Rota Real

**ID:** REQ-SPRINT05-002  
**Priority:** High  
**Type:** Feature Integration

**Description:**
WHEN um admin envia mensagem para ISA via `/api/isa/chat`  
THEN a mensagem deve ser processada pelo IsaAgent real (não mock)  
AND comandos devem ser executados via LangChain  
AND resultados devem ser salvos em `isa_commands` para auditoria  
AND resposta deve conter dados reais do sistema

**Acceptance Criteria:**
1. Endpoint `/api/isa/chat` chama `IsaAgent.process_message()`
2. Comando "list interviews" retorna entrevistas reais do banco
3. Comando "list sub-agents" retorna sub-agentes reais do banco
4. Comando "generate report" executa query e retorna dados
5. Cada comando é registrado em `isa_commands` com timestamp
6. Resposta contém `command_executed: true` quando comando é executado
7. Erros são tratados e retornam mensagem clara ao usuário

**Related Requirements:** REQ-SPRINT05-001

---

### REQ-3: Implementar Processamento de Mensagens no Chat Público

**ID:** REQ-SPRINT05-003  
**Priority:** High  
**Type:** Feature Implementation

**Description:**
WHEN um usuário envia mensagem via `/chat/{agent_slug}/message`  
THEN a mensagem deve ser processada pelo sub-agente correspondente  
AND resposta deve ser gerada via LangChain/LangGraph  
AND mensagens devem ser salvas em `interview_messages`  
AND progresso da entrevista deve ser atualizado

**Acceptance Criteria:**
1. Endpoint `/chat/{agent_slug}/message` carrega sub-agente por slug
2. Mensagem é processada pelo agente (Discovery, MMN, etc)
3. Resposta é gerada via LLM configurado no sub-agente
4. Mensagem do usuário é salva em `interview_messages` com role="user"
5. Resposta do agente é salva em `interview_messages` com role="assistant"
6. Campo `progress` retorna status de campos coletados vs faltantes
7. Campo `is_complete` retorna true quando todos campos obrigatórios coletados
8. Histórico de mensagens pode ser recuperado via `/chat/{slug}/interview/{id}`

**Related Requirements:** REQ-SPRINT05-004

---

## 🟠 PARTE 2: Menus Sidebar - Conversas

### REQ-4: Conectar Menu Conversas ao Backend

**ID:** REQ-SPRINT05-004  
**Priority:** High  
**Type:** Feature Integration

**Description:**
WHEN admin acessa menu "Conversas"  
THEN deve ver lista de conversas reais do banco `conversations`  
AND deve poder criar, editar, visualizar e deletar conversas  
AND deve poder filtrar por status, prioridade, cliente  
AND deve poder buscar por nome ou telefone

**Acceptance Criteria:**
1. `ConversationsPage.tsx` usa `conversationService.ts` (não mock)
2. Lista carrega conversas do endpoint `/api/conversations`
3. Botão "Nova Conversa" abre modal e cria via POST `/api/conversations`
4. Clicar em conversa abre detalhes com histórico de mensagens
5. Filtros por status (active, closed, pending) funcionam
6. Filtros por prioridade (Low, Medium, High) funcionam
7. Busca por nome/telefone filtra resultados
8. Paginação funciona (limit, offset)
9. Contador de mensagens não lidas aparece corretamente
10. Deletar conversa remove do banco e atualiza lista

**Related Requirements:** REQ-SPRINT05-003

---

## 🟡 PARTE 3: Menus Sidebar - Pesquisas/Entrevistas

### REQ-5: Conectar Menu Pesquisas ao Backend

**ID:** REQ-SPRINT05-005  
**Priority:** High  
**Type:** Feature Integration

**Description:**
WHEN admin acessa menu "Pesquisas"  
THEN deve ver lista de entrevistas reais do banco `interviews`  
AND deve poder visualizar detalhes e histórico de cada entrevista  
AND deve poder filtrar por status, data, sub-agente  
AND deve poder exportar resultados

**Acceptance Criteria:**
1. `AdminInterviewsPage.tsx` usa `interviewService.ts` (não mock)
2. Lista carrega entrevistas do endpoint `/api/interviews`
3. Mostra: lead name, sub-agent, status, start date, completion date
4. Filtros por status (pending, in_progress, completed, cancelled) funcionam
5. Filtros por date range funcionam
6. Filtros por sub-agente funcionam
7. Busca por nome ou telefone funciona
8. Clicar em entrevista abre detalhes com thread completo de mensagens
9. AI analysis é exibida destacada quando entrevista completa
10. Botão "Exportar" gera CSV com dados da entrevista

**Related Requirements:** REQ-SPRINT05-003

---

## 📊 PARTE 4: Menus Sidebar - Overview Dashboard

### REQ-6: Implementar Dashboard Overview com Métricas Reais

**ID:** REQ-SPRINT05-006  
**Priority:** Medium  
**Type:** Feature Implementation

**Description:**
WHEN admin acessa menu "Overview"  
THEN deve ver dashboard com métricas reais do sistema  
AND deve ver gráficos de atividade  
AND deve ver lista de atividades recentes  
AND métricas devem atualizar em tempo real

**Acceptance Criteria:**
1. Endpoint `/api/dashboard/stats` retorna métricas agregadas
2. Métricas incluem: total_clients, total_leads, total_conversations, active_interviews
3. `AdminOverview.tsx` carrega dados do endpoint (não mock)
4. Cards de métricas mostram números reais do banco
5. Gráfico de conversas por dia renderiza com Recharts
6. Gráfico de entrevistas por status renderiza
7. Lista de "Atividades Recentes" mostra últimas 10 ações
8. Métricas atualizam ao fazer refresh da página
9. Loading states aparecem durante carregamento
10. Erros são tratados e exibidos ao usuário

**Related Requirements:** None

---

## ⚙️ PARTE 5: Menus Sidebar - Configuração RENUS

### REQ-7: Completar Backend de Configuração RENUS

**ID:** REQ-SPRINT05-007  
**Priority:** High  
**Type:** Feature Implementation

**Description:**
WHEN admin edita configuração do RENUS  
THEN alterações devem ser salvas no banco `renus_config`  
AND Discovery Agent deve usar configuração do banco  
AND botão "Salvar e Publicar" deve aplicar mudanças imediatamente

**Acceptance Criteria:**
1. Endpoint `GET /api/renus-config` retorna configuração do cliente
2. Endpoint `PUT /api/renus-config` atualiza configuração completa
3. Endpoint `PATCH /api/renus-config/instructions` atualiza apenas system_prompt
4. Endpoint `PATCH /api/renus-config/guardrails` atualiza apenas guardrails
5. Endpoint `PATCH /api/renus-config/advanced` atualiza temperature, max_tokens, etc
6. Endpoint `POST /api/renus-config/publish` marca config como publicada
7. Discovery Agent carrega system_prompt de `renus_config` (não hardcoded)
8. Alterações aplicam imediatamente após publicar (sem restart)
9. Histórico de alterações é mantido (created_at, updated_at)
10. RLS garante que cliente só vê sua própria configuração

**Related Requirements:** REQ-SPRINT05-008

---

### REQ-8: Conectar Frontend de Configuração RENUS ao Backend

**ID:** REQ-SPRINT05-008  
**Priority:** High  
**Type:** Feature Integration

**Description:**
WHEN admin edita qualquer aba de configuração RENUS  
THEN alterações devem ser salvas no backend  
AND badge "Alterações Não Salvas" deve aparecer  
AND botão "Salvar e Publicar" deve persistir todas as mudanças

**Acceptance Criteria:**
1. `InstructionsTab.tsx` carrega dados de `renusConfigService.getConfig()`
2. `InstructionsTab.tsx` salva via `renusConfigService.updateInstructions()`
3. `GuardrailsTab.tsx` carrega e salva via service
4. `AdvancedTab.tsx` carrega e salva via service
5. `ToolsTab.tsx` carrega tools de `toolService.getAll()`
6. `SubAgentsTab.tsx` carrega sub-agentes de `subagentService.getAll()`
7. Badge "Alterações Não Salvas" aparece quando há mudanças não salvas
8. Badge "Configuração Publicada" aparece quando tudo está salvo
9. Botão "Salvar e Publicar" chama `publish()` e atualiza badge
10. Toast de sucesso/erro aparece após cada operação

**Related Requirements:** REQ-SPRINT05-007

---

## 📈 PARTE 6: Menus Sidebar - Relatórios

### REQ-9: Implementar Sistema de Relatórios Básicos

**ID:** REQ-SPRINT05-009  
**Priority:** Medium  
**Type:** Feature Implementation

**Description:**
WHEN admin acessa menu "Relatórios"  
THEN deve poder gerar relatórios de conversas, entrevistas e agentes  
AND deve poder filtrar por período  
AND deve poder exportar em CSV

**Acceptance Criteria:**
1. Endpoint `GET /api/reports/conversations` retorna dados agregados de conversas
2. Endpoint `GET /api/reports/interviews` retorna dados agregados de entrevistas
3. Endpoint `GET /api/reports/agents` retorna estatísticas de uso de agentes
4. `ReportsPage.tsx` permite selecionar tipo de relatório
5. Filtros por date range funcionam
6. Gráficos renderizam com dados reais (Recharts)
7. Botão "Exportar CSV" gera arquivo com dados do relatório
8. Relatório de conversas inclui: total, por status, por canal, tempo médio
9. Relatório de entrevistas inclui: total, completion rate, tempo médio, por sub-agente
10. Relatório de agentes inclui: uso por agente, tokens consumidos, custo estimado

**Related Requirements:** None

---

## ⚙️ PARTE 7: Menus Sidebar - Configurações do Sistema

### REQ-10: Implementar Configurações do Sistema

**ID:** REQ-SPRINT05-010  
**Priority:** Low  
**Type:** Feature Implementation

**Description:**
WHEN admin acessa menu "Configurações"  
THEN deve poder editar perfil, preferências, notificações e segurança  
AND alterações devem ser salvas no banco  
AND preferências devem aplicar imediatamente

**Acceptance Criteria:**
1. Endpoint `GET /api/settings` retorna configurações do usuário
2. Endpoint `PUT /api/settings` atualiza configurações
3. `SettingsPage.tsx` tem 4 tabs: Perfil, Preferências, Notificações, Segurança
4. Tab Perfil permite editar: nome, email, avatar, telefone
5. Tab Preferências permite editar: idioma, timezone, tema (light/dark)
6. Tab Notificações permite configurar: email, push, som
7. Tab Segurança permite: alterar senha, habilitar 2FA, ver sessões ativas
8. Alterações salvam via PUT `/api/settings`
9. Toast de sucesso/erro aparece após salvar
10. Preferências aplicam imediatamente (ex: tema muda sem refresh)

**Related Requirements:** None

---

## 🧹 PARTE 8: Limpeza e Melhorias

### REQ-11: Remover Código Duplicado e Consolidar Rotas

**ID:** REQ-SPRINT05-011  
**Priority:** Medium  
**Type:** Code Quality

**Description:**
WHEN desenvolvedor revisa código  
THEN não deve haver código duplicado  
AND não deve haver rotas duplicadas  
AND código deve seguir padrões do projeto

**Acceptance Criteria:**
1. `subagent_service.py` não tem métodos duplicados (async vs sync)
2. Apenas um arquivo de rotas de sub-agentes existe (`sub_agents.py`)
3. Arquivo `subagents.py` foi deletado ou consolidado
4. Imports em `main.py` estão corretos
5. Todos os services usam apenas métodos async
6. Código segue padrões de type hints (Python 3.11+)
7. Docstrings estão presentes em funções públicas
8. Nenhum import não utilizado
9. Nenhuma variável não utilizada
10. Código passa em linter (ruff, black)

**Related Requirements:** None

---

## Summary

**Total Requirements:** 11  
**Critical:** 1 (REQ-001)  
**High:** 5 (REQ-002, REQ-003, REQ-004, REQ-005, REQ-007, REQ-008)  
**Medium:** 3 (REQ-006, REQ-009, REQ-011)  
**Low:** 1 (REQ-010)

**Estimated Effort:**
- Parte 1 (Correções): 20 minutos
- Parte 2 (Integrações): 6-8 horas
- Parte 3 (Menus Sidebar): 10-12 horas
- Parte 4 (Limpeza): 2-3 horas
- **Total:** 18-23 horas (3-4 dias)

**Dependencies:**
- Sprint 01 (Auth) - Completo ✅
- Sprint 02 (CRUD) - Completo ✅
- Sprint 03 (WebSocket) - Completo ✅
- Sprint 04 (Multi-Agente) - 75% Completo ⚠️

**Risks:**
- API keys podem não estar disponíveis (ANTHROPIC_API_KEY)
- LangChain/LangGraph podem ter breaking changes
- Performance de queries agregadas pode ser lenta

**Success Criteria:**
- Backend inicia sem erros ✅
- Todos os 10 menus sidebar funcionam ✅
- Dados vêm do backend (não mock) ✅
- ISA executa comandos reais ✅
- Chat público processa com agentes ✅
- Sistema pronto para deploy MVP ✅
