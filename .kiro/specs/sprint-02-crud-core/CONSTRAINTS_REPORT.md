# 🔍 RELATÓRIO DE INVESTIGAÇÃO - CONSTRAINTS DO BANCO DE DADOS

**Data:** 2025-11-25 22:40  
**Investigador:** Kiro  
**Sprint:** 02 - CRUD Core  
**Status:** ✅ Investigação Completa

---

## 📊 RESUMO EXECUTIVO

Investigação revelou **DIVERGÊNCIAS CRÍTICAS** entre os models Pydantic e os constraints do banco de dados.

**Problema:** Models foram criados baseados em suposições, mas o banco tem constraints específicos em português.

**Impacto:** 
- ❌ CRUD de Leads bloqueado
- ❌ CRUD de Projects bloqueado
- ✅ CRUD de Clients funcionando

---

## 🔴 DIVERGÊNCIA 1: LEADS.SOURCE

### Constraint no Banco (REAL)
```sql
CHECK (source = ANY (ARRAY[
    'pesquisa'::text,
    'home'::text,
    'campanha'::text,
    'indicacao'::text
]))
```

**Valores Aceitos:**
- ✅ `pesquisa`
- ✅ `home`
- ✅ `campanha`
- ✅ `indicacao`

### Model Pydantic (ATUAL - ERRADO)
```python
source: str = Field(..., description="Origem do lead (whatsapp, site, indicação, etc)")
```

**Problema:** Aceita QUALQUER string, mas banco rejeita tudo exceto os 4 valores acima.

### Correção Necessária
```python
# backend/src/models/lead.py
from typing import Literal

source: Literal["pesquisa", "home", "campanha", "indicacao"] = Field(
    ..., 
    description="Origem do lead"
)
```

---

## 🔴 DIVERGÊNCIA 2: LEADS.STATUS

### Constraint no Banco (REAL)
```sql
CHECK (status = ANY (ARRAY[
    'novo'::text,
    'qualificado'::text,
    'em_negociacao'::text,
    'perdido'::text
]))
```

**Valores Aceitos:**
- ✅ `novo`
- ✅ `qualificado`
- ✅ `em_negociacao`
- ✅ `perdido`

### Model Pydantic (ATUAL - ERRADO)
```python
status: Literal["new", "contacted", "qualified", "converted", "lost"] = "new"
```

**Problema:** 
- ❌ Usa valores em inglês
- ❌ Valor padrão "new" não existe no banco
- ❌ Tem valores que não existem no banco (contacted, converted)

### Correção Necessária
```python
# backend/src/models/lead.py
status: Literal["novo", "qualificado", "em_negociacao", "perdido"] = "novo"
```

---

## 🔴 DIVERGÊNCIA 3: PROJECTS.STATUS

### Constraint no Banco (REAL)
```sql
CHECK (status = ANY (ARRAY[
    'Em Andamento'::text,
    'Concluído'::text,
    'Pausado'::text,
    'Atrasado'::text,
    'Em Revisão'::text
]))
```

**Valores Aceitos:**
- ✅ `Em Andamento`
- ✅ `Concluído`
- ✅ `Pausado`
- ✅ `Atrasado`
- ✅ `Em Revisão`

### Model Pydantic (ATUAL - ERRADO)
```python
status: Literal["planning", "active", "paused", "completed", "cancelled"] = "planning"
```

**Problema:**
- ❌ Usa valores em inglês
- ❌ Valor padrão "planning" não existe no banco
- ❌ Nenhum valor do model existe no banco!

### Correção Necessária
```python
# backend/src/models/project.py
status: Literal["Em Andamento", "Concluído", "Pausado", "Atrasado", "Em Revisão"] = "Em Andamento"
```

---

## 🔴 DIVERGÊNCIA 4: PROJECTS.TYPE

### Constraint no Banco (REAL)
```sql
CHECK (type = ANY (ARRAY[
    'AI Native'::text,
    'Workflow'::text,
    'Agente Solo'::text
]))
```

**Valores Aceitos:**
- ✅ `AI Native`
- ✅ `Workflow`
- ✅ `Agente Solo`

### Model Pydantic (ATUAL - ERRADO)
```python
type: str = Field(..., description="Tipo do projeto (survey, campaign, support, etc)")
```

**Problema:** Aceita QUALQUER string, mas banco só aceita 3 valores específicos.

### Correção Necessária
```python
# backend/src/models/project.py
type: Literal["AI Native", "Workflow", "Agente Solo"] = Field(
    ...,
    description="Tipo do projeto"
)
```

---

## ✅ OUTROS CONSTRAINTS ENCONTRADOS

### LEADS
```sql
-- Status (já documentado acima)
leads_status_check: CHECK (status IN ('novo', 'qualificado', 'em_negociacao', 'perdido'))

-- Foreign Key
leads_subagent_id_fkey: FOREIGN KEY (subagent_id) REFERENCES sub_agents(id) ON DELETE SET NULL
```

### PROJECTS
```sql
-- Foreign Keys
projects_client_id_fkey: FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
projects_responsible_id_fkey: FOREIGN KEY (responsible_id) REFERENCES profiles(id)
```

**Observação:** Foreign keys estão corretos nos models (UUID opcional).

---

## 🎯 PLANO DE CORREÇÃO

### PRIORIDADE 1: Corrigir Models Pydantic

#### Arquivo: `backend/src/models/lead.py`

**Mudanças:**
```python
# ANTES (ERRADO)
source: str = Field(...)
status: Literal["new", "contacted", "qualified", "converted", "lost"] = "new"

# DEPOIS (CORRETO)
source: Literal["pesquisa", "home", "campanha", "indicacao"] = Field(...)
status: Literal["novo", "qualificado", "em_negociacao", "perdido"] = "novo"
```

#### Arquivo: `backend/src/models/project.py`

**Mudanças:**
```python
# ANTES (ERRADO)
type: str = Field(...)
status: Literal["planning", "active", "paused", "completed", "cancelled"] = "planning"

# DEPOIS (CORRETO)
type: Literal["AI Native", "Workflow", "Agente Solo"] = Field(...)
status: Literal["Em Andamento", "Concluído", "Pausado", "Atrasado", "Em Revisão"] = "Em Andamento"
```

### PRIORIDADE 2: Atualizar Documentação

#### Arquivo: `.kiro/specs/sprint-02-crud-core/design.md`

Atualizar seção de Data Models com valores corretos.

#### Arquivo: `.kiro/specs/sprint-02-crud-core/requirements.md`

Atualizar acceptance criteria com valores corretos.

### PRIORIDADE 3: Atualizar Testes

Todos os testes que usam valores em inglês devem ser atualizados.

---

## 📝 DECISÕES TÉCNICAS

### Por que não mudar o banco?

**Opção A:** Mudar constraints do banco para inglês  
❌ **Rejeitada** - Banco já tem dados, pode quebrar sistema existente

**Opção B:** Mudar models para português  
✅ **Aprovada** - Models são novos, sem impacto em produção

### Impacto no Frontend

Se o frontend já usa valores em inglês, será necessário:
1. Criar mapeamento (inglês → português) antes de enviar ao backend
2. Criar mapeamento (português → inglês) ao receber do backend

**OU**

Atualizar frontend para usar valores em português diretamente.

---

## 🚨 BLOQUEIOS ATUAIS

### Endpoints Bloqueados

**Leads:**
- ❌ POST /api/leads (source inválido)
- ❌ PUT /api/leads/{id} (status inválido)

**Projects:**
- ❌ POST /api/projects (type e status inválidos)
- ❌ PUT /api/projects/{id} (status inválido)

### Endpoints Funcionando

**Clients:**
- ✅ GET /api/clients
- ✅ GET /api/clients/{id}
- ✅ POST /api/clients
- ✅ PUT /api/clients/{id}
- ✅ DELETE /api/clients/{id}

---

## 📊 TABELA COMPARATIVA

| Campo | Model (Errado) | Banco (Correto) | Status |
|-------|---------------|-----------------|--------|
| leads.source | Qualquer string | pesquisa, home, campanha, indicacao | ❌ Divergente |
| leads.status | new, contacted, qualified, converted, lost | novo, qualificado, em_negociacao, perdido | ❌ Divergente |
| projects.type | Qualquer string | AI Native, Workflow, Agente Solo | ❌ Divergente |
| projects.status | planning, active, paused, completed, cancelled | Em Andamento, Concluído, Pausado, Atrasado, Em Revisão | ❌ Divergente |
| clients.* | Sem constraints específicos | Sem constraints específicos | ✅ OK |

---

## ✅ PRÓXIMOS PASSOS

1. **Aguardar aprovação** do usuário para correções
2. **Corrigir models** Pydantic (15 minutos)
3. **Testar endpoints** novamente
4. **Atualizar documentação** (30 minutos)
5. **Validar com equipe** de frontend sobre mapeamento

---

## 📞 RECOMENDAÇÕES

### Curto Prazo
- ✅ Corrigir models imediatamente
- ✅ Testar CRUD completo
- ✅ Documentar valores aceitos

### Médio Prazo
- 📝 Criar enums compartilhados (backend + frontend)
- 📝 Adicionar validação de constraints na migration
- 📝 Documentar todos os enums no README

### Longo Prazo
- 🔄 Considerar internacionalização (i18n)
- 🔄 Criar sistema de tradução de enums
- 🔄 Padronizar nomenclatura (português ou inglês)

---

**Relatório Completo:** ✅  
**Ação Necessária:** Aguardando aprovação para correções  
**Tempo Estimado de Correção:** 30-45 minutos  
**Impacto:** Desbloqueio completo do Sprint 02
