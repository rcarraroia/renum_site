# 🐛 BUGS CONSOLIDADOS - SPRINT 05B

**Data:** 05/12/2025  
**Fonte:** Sprint 05A + Sprint 05B  
**Total:** 12 bugs (1 crítico, 7 médios, 4 baixos)

---

## 🔴 CRÍTICOS (0)

**Nenhum bug crítico pendente** ✅

### BUG #10: Servidor trava periodicamente - ✅ CORRIGIDO
- **Sprint:** 05A
- **Severidade:** 🔴 CRÍTICA → ✅ CORRIGIDO
- **Status:** ✅ CORRIGIDO (05/12/2025)
- **Esforço:** 2.5h (estimado: 4-6h)
- **Causa:** httpx.AsyncClient não fechado (memory leak)
- **Correção:** Context manager + lazy initialization + connection pooling
- **Validação:** 1200 requests, 0 timeouts, 100% success rate
- **Arquivos:** uazapi_client.py, message_tasks.py, integration_service.py, whatsapp_tool.py
- **Documentação:** `docs/BUG_10_CORRECAO.md`

---

## 🟡 MÉDIOS (7)

### BUG #3: Campo "segment" obrigatório no banco
- **Sprint:** 05A
- **Severidade:** 🟡 MÉDIA
- **Status:** ⚠️ PENDENTE
- **Esforço:** 30min
- **Sprint correção:** 08
- **Solução:** `ALTER TABLE clients ALTER COLUMN segment SET DEFAULT 'geral';`

### BUG #4: Campos enum não documentados em Leads
- **Sprint:** 05A
- **Severidade:** 🟡 MÉDIA
- **Status:** ⚠️ PENDENTE
- **Esforço:** 1h
- **Sprint correção:** 08
- **Valores:** source ('pesquisa', 'home', 'campanha', 'indicacao'), status ('novo', 'qualificado', 'em_negociacao', 'perdido')

### BUG #5: Campos enum não documentados em Projects
- **Sprint:** 05A
- **Severidade:** 🟡 MÉDIA
- **Status:** ⚠️ PENDENTE
- **Esforço:** 1h
- **Sprint correção:** 08
- **Valores:** type ('AI Native', 'Workflow', 'Agente Solo'), status ('Em Andamento', 'Concluído', 'Pausado', 'Atrasado', 'Em Revisão')

### BUG #6: Campos enum não documentados em Conversations
- **Sprint:** 05A
- **Severidade:** 🟡 MÉDIA
- **Status:** ⚠️ PENDENTE
- **Esforço:** 1h
- **Sprint correção:** 08
- **Valores:** status ('active', 'closed', 'pending'), channel (obrigatório, valores a descobrir)

### BUG #7: Endpoint POST /api/interviews/start retorna 405
- **Sprint:** 05A
- **Severidade:** 🟡 MÉDIA
- **Status:** ⚠️ PENDENTE
- **Esforço:** 2h
- **Sprint correção:** 08
- **Impacto:** Não é possível criar entrevistas via API

### BUG #8: LangSmith não configurado
- **Sprint:** 05A
- **Severidade:** 🟡 MÉDIA
- **Status:** ⚠️ PENDENTE
- **Esforço:** 30min
- **Sprint correção:** 08
- **Impacto:** Traces não são registrados, debugging difícil

### BUG #11: Página de Interviews não encontrada no Frontend
- **Sprint:** 05A
- **Severidade:** 🟡 MÉDIA
- **Status:** ⚠️ PENDENTE
- **Esforço:** 3h
- **Sprint correção:** 08
- **Impacto:** Menu "Pesquisas/Entrevistas" pode não funcionar

---

## 🟢 BAIXOS (4)

### BUG #1: Health check demora 2.06s (critério < 2s)
- **Sprint:** 05A
- **Severidade:** 🟢 BAIXA
- **Status:** ⚠️ PENDENTE
- **Esforço:** 2h
- **Sprint correção:** 09
- **Nota:** Diferença de 60ms é aceitável

### BUG #2: ISA Agent erro 500
- **Sprint:** 05A
- **Severidade:** 🟢 BAIXA
- **Status:** ✅ CÓDIGO CORRIGIDO (teste pendente)
- **Esforço:** 30min (apenas teste)
- **Sprint correção:** 08

### BUG #9: Agentes usam async mas testes não aguardam
- **Sprint:** 05A
- **Severidade:** 🟢 BAIXA
- **Status:** ⚠️ PENDENTE
- **Esforço:** 1h
- **Sprint correção:** 09
- **Nota:** Apenas warning, não erro

### BUG #12: Double websocket.accept()
- **Sprint:** 05B
- **Severidade:** 🔴 CRÍTICA → ✅ CORRIGIDO
- **Status:** ✅ CORRIGIDO
- **Esforço:** 15min
- **Arquivo:** `backend/src/utils/websocket_manager.py` linha 33
- **Correção:** Removida linha duplicada

---

## 📊 ESTATÍSTICAS

- **Total:** 12 bugs
- **Críticos:** 0 pendentes (0%) ✅
- **Médios:** 7 pendentes (58%)
- **Baixos:** 3 pendentes (25%)
- **Corrigidos:** 4 (33%)
- **Pendentes:** 8 (67%)

---

## 🎯 PRIORIZAÇÃO

### Sprint 07B (Deploy)
- ✅ Nenhum bug bloqueador
- ✅ BUG #10 corrigido
- ✅ Deploy pode prosseguir IMEDIATAMENTE

### Sprint 08 (Bugs + Performance)
- BUG #7 (Interviews 405) - HIGH
- BUG #3-6 (Enums) - MEDIUM
- BUG #8 (LangSmith) - MEDIUM
- BUG #11 (Frontend) - MEDIUM
- BUG #2 (ISA teste) - LOW

### Sprint 09 (Melhorias)
- BUG #1 (Health check) - LOW
- BUG #9 (Async tests) - LOW
