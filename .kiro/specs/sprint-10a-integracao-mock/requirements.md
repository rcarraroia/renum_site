# SPRINT 10A - INTEGRAÇÃO MOCK → REAL - REQUIREMENTS

## 🎯 OBJETIVO

O sistema RENUM possui várias páginas que ainda utilizam dados mock (hardcoded) ao invés de se conectarem aos services reais que já existem. Este sprint visa eliminar TODOS os dados mock e conectar 100% das páginas aos backends reais.

---

## 📋 REQUIREMENTS

### RF-MOCK-01: Eliminação de Dados Mock
**WHEN** o sistema carrega qualquer página  
**THEN** todos os dados devem vir do backend real via services  
**AND** nenhum dado mock deve ser utilizado

### RF-MOCK-02: Conexão de Páginas Existentes
**WHEN** uma página existe mas usa dados mock  
**THEN** ela deve ser conectada ao service real correspondente  
**AND** manter a mesma interface visual

### RF-MOCK-03: Criação de Páginas Faltantes
**WHEN** uma funcionalidade não tem página correspondente  
**THEN** a página deve ser criada  
**AND** conectada ao service real desde o início

### RF-MOCK-04: Services Existentes Utilizados
**WHEN** um service já existe no backend  
**THEN** ele deve ser utilizado pelas páginas  
**AND** não deve ser recriado

### RF-MOCK-05: Estados de Loading e Erro
**WHEN** uma página carrega dados do backend  
**THEN** deve mostrar estado de loading  
**AND** tratar erros graciosamente

---

## 🔍 PÁGINAS IDENTIFICADAS COM MOCK

### 1. LEADS
- **Arquivo:** `src/pages/leads/LeadsPage.tsx`
- **Problema:** Usa `MOCK_LEADS` hardcoded
- **Service Existente:** `src/services/leadService.ts` ✅
- **Ação:** Conectar página ao service real

### 2. CLIENTES  
- **Arquivo:** `src/pages/clients/ClientsPage.tsx`
- **Problema:** Usa `MOCK_CLIENTS_DATA` hardcoded
- **Service Existente:** `src/services/clientService.ts` ✅
- **Ação:** Conectar página ao service real

### 3. PESQUISAS (3 páginas)
- **Arquivos:** 
  - `src/pages/interviews/InterviewsPage.tsx`
  - `src/pages/interviews/InterviewDetailPage.tsx`
  - `src/pages/interviews/InterviewResultsPage.tsx`
- **Problema:** Todas usam dados mock
- **Service Existente:** `src/services/interviewService.ts` ✅
- **Ação:** Conectar todas as 3 páginas ao service real

### 4. RELATÓRIOS
- **Arquivo:** `src/pages/reports/ReportsPage.tsx`
- **Problema:** Interface real mas dados mock
- **Service Existente:** `src/services/reportService.ts` ✅
- **Ação:** Conectar gráficos aos dados reais

### 5. ASSISTENTE ISA
- **Arquivo:** `src/pages/dashboard/AdminAssistantPage.tsx`
- **Problema:** Respostas simuladas
- **Service Necessário:** Integração com AI service
- **Ação:** Conectar ao backend de IA real

### 6. CONFIGURAÇÕES GLOBAIS
- **Arquivo:** `src/pages/settings/GlobalSettingsPage.tsx`
- **Problema:** Estado simulado
- **Service Necessário:** `configService` ou `settingsService`
- **Ação:** Criar service e conectar

### 7. CONFIGURAÇÕES GERAIS
- **Arquivo:** `src/pages/settings/SettingsPage.tsx`
- **Problema:** Save/cancel simulado
- **Service Necessário:** `settingsService`
- **Ação:** Implementar persistência real

### 8. ADMIN CLIENTES
- **Arquivo:** `src/pages/dashboard/AdminClientsPage.tsx`
- **Problema:** Não usa clientService
- **Service Existente:** `src/services/clientService.ts` ✅
- **Ação:** Conectar página ao service real

### 9. ADMIN LEADS (VERSÃO ANTIGA)
- **Arquivo:** `src/pages/dashboard/AdminLeadsPage.tsx`
- **Problema:** Versão antiga, não usa leadService
- **Service Existente:** `src/services/leadService.ts` ✅
- **Ação:** Conectar ao service ou migrar para AdminLeadsPageNew

### 10. ADMIN RELATÓRIOS
- **Arquivo:** `src/pages/dashboard/AdminReportsPage.tsx`
- **Problema:** Não usa reportService
- **Service Existente:** `src/services/reportService.ts` ✅
- **Ação:** Conectar gráficos aos dados reais

### 11. PESQUISAS - ANÁLISE
- **Arquivo:** `src/pages/dashboard/PesquisasAnalisePage.tsx`
- **Problema:** Não usa interviewService
- **Service Existente:** `src/services/interviewService.ts` ✅
- **Ação:** Conectar ao service real

### 12. PESQUISAS - ENTREVISTAS
- **Arquivo:** `src/pages/dashboard/PesquisasEntrevistasPage.tsx`
- **Problema:** Não usa interviewService
- **Service Existente:** `src/services/interviewService.ts` ✅
- **Ação:** Conectar ao service real

### 13. PESQUISAS - RESULTADOS
- **Arquivo:** `src/pages/dashboard/PesquisasResultadosPage.tsx`
- **Problema:** Não usa interviewService
- **Service Existente:** `src/services/interviewService.ts` ✅
- **Ação:** Conectar ao service real

### 14. CLIENT OVERVIEW
- **Arquivo:** `src/pages/dashboard/ClientOverview.tsx`
- **Problema:** Não usa dashboardService
- **Service Existente:** `src/services/dashboardService.ts` ✅
- **Ação:** Conectar ao service real

### 15. RENUS CONFIG
- **Arquivo:** `src/pages/dashboard/RenusConfigPage.tsx`
- **Problema:** Não usa configService
- **Service Necessário:** Criar configService ou usar agentService
- **Ação:** Conectar configurações ao backend

### 16. SICC - EVOLUTION PAGE
- **Arquivo:** `src/pages/sicc/EvolutionPage.tsx`
- **Problema:** Métricas hardcoded (não usa siccService)
- **Service Existente:** `src/services/siccService.ts` ✅
- **Ação:** Conectar ao siccService.getMetrics()

### 17. SICC - LEARNING QUEUE PAGE
- **Arquivo:** `src/pages/sicc/LearningQueuePage.tsx`
- **Problema:** Dados hardcoded (não usa siccService)
- **Service Existente:** `src/services/siccService.ts` ✅
- **Ação:** Conectar ao siccService.getLearningQueue()

### 18. SICC - MEMORY MANAGER PAGE
- **Arquivo:** `src/pages/sicc/MemoryManagerPage.tsx`
- **Problema:** Valores hardcoded (não usa siccService)
- **Service Existente:** `src/services/siccService.ts` ✅
- **Ação:** Conectar ao siccService.getMemories()

### 19. SICC - SETTINGS PAGE
- **Arquivo:** `src/pages/sicc/SettingsPage.tsx`
- **Problema:** Estados mock (não usa siccService)
- **Service Existente:** `src/services/siccService.ts` ✅
- **Ação:** Conectar ao siccService.getSettings()

---

## 🗂️ ARQUIVOS MOCK A REMOVER

### Arquivos de Mock Centralizados
- **Arquivo:** `src/data/mockReports.ts` - 17 constantes MOCK_
- **Arquivo:** `src/data/mockProjects.ts` - 3 constantes MOCK_
- **Arquivo:** `src/data/mockConversations.ts` - 4 constantes MOCK_
- **Ação:** Deletar após migração completa para services

---

## ✅ PÁGINAS JÁ FUNCIONAIS

### Páginas que JÁ usam dados reais:
- ✅ `src/pages/dashboard/AdminOverview.tsx` - Conectada ao dashboardService
- ✅ `src/pages/dashboard/AdminProjectsPage.tsx` - Conectada ao projectService
- ✅ `src/pages/dashboard/AdminConversationsPage.tsx` - Conectada ao conversationService + WebSocket
- ✅ `src/pages/dashboard/AdminLeadsPageNew.tsx` - Conectada ao leadService
- ✅ `src/pages/agents/AgentsPage.tsx` - Conectada ao agentService
- ✅ `src/pages/agents/AgentDetailPage.tsx` - Conectada ao agentService
- ✅ `src/pages/agents/SubAgentsPage.tsx` - Conectada ao agentService

### Páginas Admin Agents (já existem):
- ✅ `src/pages/admin/agents/AgentCreatePage.tsx` - JÁ EXISTE
- ✅ `src/pages/admin/agents/AgentDetailsPage.tsx` - JÁ EXISTE
- ✅ `src/pages/admin/agents/AgentsListPage.tsx` - JÁ EXISTE

**NOTA:** AdminLeadsPageNew já está conectada ao leadService - priorizar sobre AdminLeadsPage

---

## ✅ PÁGINAS JÁ FUNCIONAIS

### Páginas que JÁ usam dados reais:
- ✅ `src/pages/dashboard/AdminDashboardPage.tsx` - Conectada
- ✅ `src/pages/projects/ProjectsPage.tsx` - Conectada (Sprint 08)
- ✅ `src/pages/dashboard/AdminConversationsPage.tsx` - Conectada + WebSocket
- ✅ `src/pages/agents/AgentsPage.tsx` - Conectada (Sprint 09)
- ✅ `src/pages/agents/AgentDetailPage.tsx` - Conectada (Sprint 09)

### Alternativas existentes:
- ✅ `src/pages/leads/AdminLeadsPageNew.tsx` - Usa dados reais mas não está no sidebar

---

## 🎯 CRITÉRIOS DE SUCESSO

### CS-01: Zero Dados Mock
**GIVEN** qualquer página do sistema  
**WHEN** ela é carregada  
**THEN** todos os dados devem vir do backend  
**AND** nenhum mock deve estar presente no código

### CS-02: Services Utilizados
**GIVEN** um service existente  
**WHEN** há uma página relacionada  
**THEN** a página deve usar o service  
**AND** não duplicar lógica

### CS-03: Páginas Completas
**GIVEN** uma funcionalidade no sidebar  
**WHEN** o usuário clica no link  
**THEN** uma página funcional deve abrir  
**AND** mostrar dados reais

### CS-04: Performance Adequada
**GIVEN** uma página carregando dados reais  
**WHEN** ela é acessada  
**THEN** deve carregar em menos de 3 segundos  
**AND** mostrar loading state durante carregamento

### CS-05: Tratamento de Erros
**GIVEN** um erro no backend  
**WHEN** a página tenta carregar dados  
**THEN** deve mostrar mensagem de erro clara  
**AND** permitir retry da operação

---

## 🔗 DEPENDÊNCIAS

### Dependências Internas:
- ✅ Sprint 08 completo (services existem)
- ✅ Sprint 09 completo (agents funcionam)
- ✅ Backend funcionando
- ✅ Autenticação funcionando

### Dependências Externas:
- ✅ Supabase configurado
- ✅ Dados de teste no banco
- ✅ Services implementados

---

## 📊 MÉTRICAS DE VALIDAÇÃO

### Métricas Quantitativas:
- **Páginas com mock:** 0/10 (objetivo: eliminar todas)
- **Services utilizados:** 10/10 (objetivo: usar todos)
- **Links funcionais:** 10/10 (objetivo: todos funcionais)
- **Tempo de carregamento:** < 3s (objetivo: performance)

### Métricas Qualitativas:
- **UX consistente:** Todas as páginas seguem mesmo padrão
- **Tratamento de erros:** Mensagens claras e acionáveis
- **Estados de loading:** Feedback visual adequado
- **Navegação fluida:** Transições sem quebras

---

## 🚨 RISCOS E MITIGAÇÕES

### Risco 1: Services Incompletos
**Risco:** Service existe mas não tem todos os métodos necessários  
**Mitigação:** Validar e completar services antes de conectar páginas

### Risco 2: Dados Insuficientes
**Risco:** Banco não tem dados suficientes para testar  
**Mitigação:** Criar dados de teste adequados

### Risco 3: Performance
**Risco:** Páginas ficarem lentas com dados reais  
**Mitigação:** Implementar paginação e otimizações

### Risco 4: Quebra de UX
**Risco:** Mudança de mock para real quebrar interface  
**Mitigação:** Manter estrutura de dados compatível

---

**Versão:** 1.0  
**Data:** 2025-12-10  
**Responsável:** Kiro (Agente de IA)