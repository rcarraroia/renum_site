# 🧪 SOLICITAÇÃO TÉCNICA - TESTES SPRINT 02: CRUD CORE

**Data:** 2025-11-25  
**Sprint:** 02 - CRUD Core  
**Solicitante:** Equipe de Desenvolvimento  
**Destinatário:** Equipe de Testes

---

## 📋 RESUMO EXECUTIVO

Este documento especifica todos os testes necessários para validar a implementação do Sprint 02 - CRUD Core. O sprint implementa operações CRUD completas para três entidades: **Clientes**, **Leads** e **Projetos**.

**Escopo de Testes:**
- ✅ Testes de Propriedade (Property-Based Tests) - 5 tarefas
- ✅ Testes Unitários - 1 tarefa
- ✅ Testes de Integração - 1 tarefa

**Framework Requerido:** Hypothesis (Python) para property-based testing

---

## 🎯 TAREFAS DE TESTES

### TASK 2.1 - Property Tests para Client Models ⚠️ OPCIONAL

**Status:** Opcional (marcada com *)  
**Prioridade:** Média  
**Tempo Estimado:** 2-3 horas

**Objetivo:** Validar que a criação de clientes retorna dados completos e consistentes

**Property a Testar:**
- **Property 1:** Criação de cliente retorna dados completos
  - *Para qualquer* ClientCreate válido, criar um cliente deve retornar ClientResponse com:
    - `id` gerado (UUID válido)
    - `created_at` preenchido
    - `status` = "active"
  - **Valida:** Requirements 1.1

**Arquivo de Teste:** `backend/tests/test_client_models.py`

**Código Exemplo:**
```python
from hypothesis import given, strategies as st
from src.models.client import ClientCreate, ContactInfo, AddressInfo
import pytest

@given(
    company_name=st.text(min_size=3, max_size=200),
    segment=st.sampled_from(["tecnologia", "saude", "educacao", "financeiro"])
)
def test_client_create_returns_complete_data(company_name, segment):
    """Property 1: Criação retorna dados completos"""
    # Arrange
    client_data = ClientCreate(
        company_name=company_name,
        segment=segment
    )
    
    # Act
    result = await client_service.create(client_data)
    
    # Assert
    assert result.id is not None
    assert result.created_at is not None
    assert result.status == "active"
```

**Critérios de Aceitação:**
- [ ] Teste executa 100+ iterações
- [ ] Teste passa com dados aleatórios válidos
- [ ] Teste falha apropriadamente com dados inválidos

---

### TASK 3.1 - Property Tests para Lead Models ⚠️ OPCIONAL

**Status:** Opcional (marcada com *)  
**Prioridade:** Alta  
**Tempo Estimado:** 3-4 horas

**Objetivo:** Validar validações de telefone e score de leads

**Properties a Testar:**

**Property 5:** Validação de telefone rejeita formatos inválidos
- *Para qualquer* string que não seja telefone válido, a validação deve retornar False
- **Valida:** Requirements 2.6, 4.1

**Property 9:** Score de lead deve estar entre 0 e 100
- *Para qualquer* lead com score, o valor deve ser >= 0 e <= 100
- **Valida:** Requirements 2.8

**Arquivo de Teste:** `backend/tests/test_lead_models.py`

**Código Exemplo:**
```python
from hypothesis import given, strategies as st
from src.utils.validators import validate_phone
from src.models.lead import LeadCreate
import re

@given(phone=st.text())
def test_phone_validation_property(phone):
    """Property 5: Validação de telefone"""
    is_valid = validate_phone(phone)
    
    if is_valid:
        clean = re.sub(r'\D', '', phone)
        assert len(clean) in [10, 11, 13]
    else:
        # Deve rejeitar formatos inválidos
        clean = re.sub(r'\D', '', phone)
        assert len(clean) not in [10, 11, 13]

@given(score=st.integers())
def test_lead_score_validation_property(score):
    """Property 9: Score válido"""
    if 0 <= score <= 100:
        # Deve aceitar
        lead = LeadCreate(
            name="Test",
            phone="11999999999",
            source="test",
            score=score
        )
        assert lead.score == score
    else:
        # Deve rejeitar
        with pytest.raises(ValidationError):
            LeadCreate(
                name="Test",
                phone="11999999999",
                source="test",
                score=score
            )
```

**Critérios de Aceitação:**
- [ ] Teste de telefone valida formatos brasileiros
- [ ] Teste de score rejeita valores fora do range
- [ ] Ambos executam 100+ iterações

---


### TASK 4.1 - Property Tests para Project Models ⚠️ OPCIONAL

**Status:** Opcional (marcada com *)  
**Prioridade:** Média  
**Tempo Estimado:** 2-3 horas

**Objetivo:** Validar constraints de progresso e orçamento de projetos

**Properties a Testar:**

**Property 10:** Progresso de projeto deve estar entre 0 e 100
- *Para qualquer* projeto, o progresso deve ser >= 0 e <= 100
- **Valida:** Requirements 3.6

**Property 11:** Orçamento de projeto deve ser positivo
- *Para qualquer* projeto com budget, o valor deve ser >= 0
- **Valida:** Requirements 3.7

**Arquivo de Teste:** `backend/tests/test_project_models.py`

**Código Exemplo:**
```python
from hypothesis import given, strategies as st
from src.models.project import ProjectCreate
from decimal import Decimal
import pytest

@given(progress=st.integers())
def test_project_progress_validation_property(progress):
    """Property 10: Progresso válido"""
    if 0 <= progress <= 100:
        project = ProjectCreate(
            name="Test Project",
            type="survey",
            progress=progress
        )
        assert project.progress == progress
    else:
        with pytest.raises(ValidationError):
            ProjectCreate(
                name="Test Project",
                type="survey",
                progress=progress
            )

@given(budget=st.decimals(allow_nan=False, allow_infinity=False))
def test_project_budget_validation_property(budget):
    """Property 11: Orçamento positivo"""
    if budget >= 0:
        project = ProjectCreate(
            name="Test Project",
            type="survey",
            budget=budget
        )
        assert project.budget == budget
    else:
        with pytest.raises(ValidationError):
            ProjectCreate(
                name="Test Project",
                type="survey",
                budget=budget
            )
```

**Critérios de Aceitação:**
- [ ] Progresso aceita apenas 0-100
- [ ] Orçamento aceita apenas valores >= 0
- [ ] Testes executam 100+ iterações

---

### TASK 5.1 - Property Tests para ClientService ⚠️ OPCIONAL

**Status:** Opcional (marcada com *)  
**Prioridade:** Alta  
**Tempo Estimado:** 4-5 horas

**Objetivo:** Validar comportamento do serviço de clientes

**Properties a Testar:**

**Property 2:** Listagem paginada respeita limites
- *Para qualquer* requisição com limit=N, retornar no máximo N items
- **Valida:** Requirements 5.2, 5.3

**Property 3:** Busca por ID inexistente retorna 404
- *Para qualquer* ID que não existe, deve retornar NotFoundError
- **Valida:** Requirements 7.2

**Property 4:** Atualização parcial preserva campos não fornecidos
- *Para qualquer* cliente, atualizar apenas um campo preserva os outros
- **Valida:** Requirements 1.4

**Property 7:** Paginação calcula has_next corretamente
- *Para qualquer* listagem, has_next = True se total > (page * limit)
- **Valida:** Requirements 5.1

**Property 8:** Filtro por status retorna apenas registros com aquele status
- *Para qualquer* status, todos items devem ter exatamente aquele status
- **Valida:** Requirements 1.2

**Arquivo de Teste:** `backend/tests/test_client_service.py`

**Código Exemplo:**
```python
from hypothesis import given, strategies as st
from src.services.client_service import client_service
import pytest

@given(limit=st.integers(min_value=1, max_value=100))
async def test_list_respects_limit_property(limit):
    """Property 2: Listagem respeita limites"""
    result = await client_service.get_all(page=1, limit=limit)
    assert len(result.items) <= limit

@given(
    total=st.integers(min_value=0, max_value=1000),
    page=st.integers(min_value=1, max_value=10),
    limit=st.integers(min_value=1, max_value=100)
)
def test_has_next_calculation_property(total, page, limit):
    """Property 7: has_next correto"""
    expected_has_next = total > (page * limit)
    # Simular cálculo
    has_next = total > (page * limit)
    assert has_next == expected_has_next

@given(status=st.sampled_from(["active", "inactive", "suspended"]))
async def test_filter_by_status_property(status):
    """Property 8: Filtro por status"""
    result = await client_service.get_all(status=status)
    for item in result.items:
        assert item.status == status
```

**Critérios de Aceitação:**
- [ ] Paginação funciona corretamente
- [ ] Filtros retornam apenas dados corretos
- [ ] Atualização parcial preserva dados
- [ ] Busca por ID inexistente retorna 404

---

### TASK 6.1 - Property Tests para LeadService ⚠️ OPCIONAL

**Status:** Opcional (marcada com *)  
**Prioridade:** Média  
**Tempo Estimado:** 3-4 horas

**Objetivo:** Validar comportamento do serviço de leads

**Properties a Testar:**

**Property 2:** Listagem paginada respeita limites
**Property 7:** Paginação calcula has_next corretamente
**Property 8:** Filtro por status retorna apenas registros com aquele status
**Property 12:** Busca case-insensitive funciona

**Arquivo de Teste:** `backend/tests/test_lead_service.py`

**Código Exemplo:**
```python
from hypothesis import given, strategies as st
from src.services.lead_service import lead_service

@given(
    search_term=st.text(min_size=1, max_size=50),
    case_variant=st.sampled_from(["lower", "upper", "mixed"])
)
async def test_search_case_insensitive_property(search_term, case_variant):
    """Property 12: Busca case-insensitive"""
    # Criar lead com nome específico
    lead = await lead_service.create(LeadCreate(
        name=search_term,
        phone="11999999999",
        source="test"
    ))
    
    # Buscar com case diferente
    if case_variant == "lower":
        search = search_term.lower()
    elif case_variant == "upper":
        search = search_term.upper()
    else:
        search = search_term.title()
    
    result = await lead_service.get_all(search=search)
    
    # Deve encontrar o lead independente do case
    assert any(item.id == lead.id for item in result.items)
```

**Critérios de Aceitação:**
- [ ] Busca funciona independente de maiúsculas/minúsculas
- [ ] Paginação e filtros funcionam corretamente

---

### TASK 7.1 - Property Tests para ProjectService ⚠️ OPCIONAL

**Status:** Opcional (marcada com *)  
**Prioridade:** Baixa  
**Tempo Estimado:** 2-3 horas

**Objetivo:** Validar comportamento do serviço de projetos

**Properties a Testar:**
- Property 2: Listagem respeita limites
- Property 7: has_next correto
- Property 8: Filtro por status

**Arquivo de Teste:** `backend/tests/test_project_service.py`

**Estrutura similar aos testes anteriores**

---

### TASK 13 - Testes Unitários para Validators ⚠️ OPCIONAL

**Status:** Opcional (marcada com *)  
**Prioridade:** Alta  
**Tempo Estimado:** 3-4 horas

**Objetivo:** Validar funções de validação isoladamente

**Funções a Testar:**
- `validate_phone()` - Formatos válidos e inválidos
- `validate_cpf()` - CPFs válidos e inválidos
- `validate_cnpj()` - CNPJs válidos e inválidos
- `validate_document()` - CPF e CNPJ
- `validate_email()` - Emails válidos e inválidos
- `format_phone()` - Formatação correta
- `format_cpf()` - Formatação correta
- `format_cnpj()` - Formatação correta

**Arquivo de Teste:** `backend/tests/test_validators.py`

**Código Exemplo:**
```python
import pytest
from src.utils.validators import (
    validate_phone, validate_cpf, validate_cnpj,
    validate_document, validate_email,
    format_phone, format_cpf, format_cnpj
)

class TestPhoneValidation:
    """Testes de validação de telefone"""
    
    def test_valid_phone_formats(self):
        """Testa formatos válidos"""
        assert validate_phone("(11) 98765-4321") == True
        assert validate_phone("11987654321") == True
        assert validate_phone("+55 11 98765-4321") == True
        assert validate_phone("1198765432") == True  # 10 dígitos
    
    def test_invalid_phone_formats(self):
        """Testa formatos inválidos"""
        assert validate_phone("123") == False
        assert validate_phone("abc") == False
        assert validate_phone("") == False
        assert validate_phone("11 9876") == False

class TestCPFValidation:
    """Testes de validação de CPF"""
    
    def test_valid_cpf(self):
        """Testa CPFs válidos"""
        assert validate_cpf("123.456.789-00") == True
        assert validate_cpf("12345678900") == True
    
    def test_invalid_cpf(self):
        """Testa CPFs inválidos"""
        assert validate_cpf("123") == False
        assert validate_cpf("11111111111") == False  # Sequência repetida
        assert validate_cpf("abc.def.ghi-jk") == False

class TestCNPJValidation:
    """Testes de validação de CNPJ"""
    
    def test_valid_cnpj(self):
        """Testa CNPJs válidos"""
        assert validate_cnpj("12.345.678/0001-90") == True
        assert validate_cnpj("12345678000190") == True
    
    def test_invalid_cnpj(self):
        """Testa CNPJs inválidos"""
        assert validate_cnpj("123") == False
        assert validate_cnpj("11111111111111") == False  # Sequência repetida

class TestEmailValidation:
    """Testes de validação de email"""
    
    def test_valid_emails(self):
        """Testa emails válidos"""
        assert validate_email("user@example.com") == True
        assert validate_email("test.user@domain.co.uk") == True
    
    def test_invalid_emails(self):
        """Testa emails inválidos"""
        assert validate_email("invalid") == False
        assert validate_email("@example.com") == False
        assert validate_email("user@") == False

class TestFormatting:
    """Testes de formatação"""
    
    def test_format_phone(self):
        """Testa formatação de telefone"""
        assert format_phone("11987654321") == "(11) 98765-4321"
        assert format_phone("1198765432") == "(11) 9876-5432"
    
    def test_format_cpf(self):
        """Testa formatação de CPF"""
        assert format_cpf("12345678900") == "123.456.789-00"
    
    def test_format_cnpj(self):
        """Testa formatação de CNPJ"""
        assert format_cnpj("12345678000190") == "12.345.678/0001-90"
```

**Critérios de Aceitação:**
- [ ] Todos os formatos válidos são aceitos
- [ ] Todos os formatos inválidos são rejeitados
- [ ] Formatação retorna strings corretas
- [ ] Coverage > 90% nas funções de validação

---

### TASK 14 - Testes de Integração ⚠️ OPCIONAL

**Status:** Opcional (marcada com *)  
**Prioridade:** Crítica  
**Tempo Estimado:** 6-8 horas

**Objetivo:** Validar fluxos completos end-to-end

**Cenários a Testar:**

#### 1. Fluxo CRUD Completo - Clientes
```python
async def test_client_full_crud_flow():
    """Testa fluxo completo: create → read → update → delete"""
    
    # 1. CREATE
    client_data = ClientCreate(
        company_name="Test Company",
        segment="tecnologia",
        contact=ContactInfo(
            phone="11999999999",
            email="test@example.com"
        )
    )
    created = await client_service.create(client_data)
    assert created.id is not None
    
    # 2. READ
    retrieved = await client_service.get_by_id(created.id)
    assert retrieved.company_name == "Test Company"
    
    # 3. UPDATE
    update_data = ClientUpdate(company_name="Updated Company")
    updated = await client_service.update(created.id, update_data)
    assert updated.company_name == "Updated Company"
    assert updated.segment == "tecnologia"  # Preservado
    
    # 4. DELETE
    await client_service.delete(created.id)
    
    # 5. Verificar que foi deletado
    with pytest.raises(NotFoundError):
        await client_service.get_by_id(created.id)
```

#### 2. Teste de Paginação
```python
async def test_pagination_with_real_data():
    """Testa paginação com dados reais"""
    
    # Criar 25 clientes
    for i in range(25):
        await client_service.create(ClientCreate(
            company_name=f"Company {i}",
            segment="tecnologia"
        ))
    
    # Página 1 (10 items)
    page1 = await client_service.get_all(page=1, limit=10)
    assert len(page1.items) == 10
    assert page1.total == 25
    assert page1.has_next == True
    
    # Página 2 (10 items)
    page2 = await client_service.get_all(page=2, limit=10)
    assert len(page2.items) == 10
    assert page2.has_next == True
    
    # Página 3 (5 items)
    page3 = await client_service.get_all(page=3, limit=10)
    assert len(page3.items) == 5
    assert page3.has_next == False
```

#### 3. Teste de Filtros
```python
async def test_filters_work_correctly():
    """Testa que filtros funcionam"""
    
    # Criar clientes com diferentes status
    await client_service.create(ClientCreate(
        company_name="Active Client",
        segment="tecnologia",
        status="active"
    ))
    await client_service.create(ClientCreate(
        company_name="Inactive Client",
        segment="tecnologia",
        status="inactive"
    ))
    
    # Filtrar por active
    active_clients = await client_service.get_all(status="active")
    assert all(c.status == "active" for c in active_clients.items)
    
    # Filtrar por inactive
    inactive_clients = await client_service.get_all(status="inactive")
    assert all(c.status == "inactive" for c in inactive_clients.items)
```

#### 4. Teste de Autenticação
```python
async def test_authentication_required():
    """Testa que endpoints requerem autenticação"""
    
    # Sem token
    response = client.get("/api/clients")
    assert response.status_code == 401
    
    # Com token inválido
    response = client.get(
        "/api/clients",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    
    # Com token válido
    token = get_valid_token()
    response = client.get(
        "/api/clients",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
```

#### 5. Teste de Erros
```python
async def test_error_handling():
    """Testa tratamento de erros"""
    
    # 404 - Not Found
    with pytest.raises(NotFoundError):
        await client_service.get_by_id("invalid-uuid")
    
    # 400 - Validation Error
    with pytest.raises(ValidationError):
        await client_service.create(ClientCreate(
            company_name="AB",  # Muito curto (min 3)
            segment="tecnologia"
        ))
    
    # 400 - Invalid phone
    with pytest.raises(ValidationError):
        await lead_service.create(LeadCreate(
            name="Test",
            phone="123",  # Inválido
            source="test"
        ))
```

**Critérios de Aceitação:**
- [ ] Fluxo CRUD completo funciona para todas entidades
- [ ] Paginação funciona com dados reais
- [ ] Filtros retornam dados corretos
- [ ] Autenticação bloqueia acesso não autorizado
- [ ] Erros são tratados apropriadamente
- [ ] Coverage > 70% no código de integração

---

## 📊 CONFIGURAÇÃO DO AMBIENTE DE TESTES

### Dependências Necessárias

Adicionar ao `backend/requirements.txt`:
```txt
# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
pytest-mock==3.12.0
hypothesis==6.92.0
```

### Instalação
```bash
cd backend
pip install -r requirements.txt
```

### Configuração do pytest

Criar `backend/pytest.ini`:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
addopts = 
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=70
    -v
```

### Estrutura de Diretórios

```
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Fixtures compartilhadas
│   ├── test_validators.py       # Task 13
│   ├── test_client_models.py    # Task 2.1
│   ├── test_lead_models.py      # Task 3.1
│   ├── test_project_models.py   # Task 4.1
│   ├── test_client_service.py   # Task 5.1
│   ├── test_lead_service.py     # Task 6.1
│   ├── test_project_service.py  # Task 7.1
│   └── test_integration.py      # Task 14
```

---

## 🎯 EXECUÇÃO DOS TESTES

### Executar Todos os Testes
```bash
cd backend
pytest
```

### Executar Testes Específicos
```bash
# Apenas testes unitários
pytest tests/test_validators.py

# Apenas property tests
pytest tests/test_client_models.py tests/test_lead_models.py

# Apenas testes de integração
pytest tests/test_integration.py

# Com coverage
pytest --cov=src --cov-report=html
```

### Executar Property Tests com Mais Iterações
```bash
# Padrão: 100 iterações
pytest tests/test_client_models.py

# Aumentar para 1000 iterações
pytest tests/test_client_models.py --hypothesis-iterations=1000
```

---

## 📈 MÉTRICAS DE SUCESSO

### Cobertura de Código
- **Mínimo Aceitável:** 70%
- **Alvo:** 80%
- **Ideal:** 90%+

### Property-Based Tests
- **Mínimo de Iterações:** 100 por teste
- **Recomendado:** 500 iterações
- **Stress Test:** 1000+ iterações

### Testes de Integração
- **Todos os fluxos CRUD:** 100% cobertos
- **Cenários de erro:** 100% cobertos
- **Autenticação:** 100% coberta

---

## 🚨 PRIORIZAÇÃO

### Prioridade CRÍTICA (Executar Primeiro)
1. **Task 13** - Testes Unitários de Validators
2. **Task 14** - Testes de Integração

### Prioridade ALTA
3. **Task 3.1** - Property Tests para Lead (validação de telefone)
4. **Task 5.1** - Property Tests para ClientService

### Prioridade MÉDIA
5. **Task 2.1** - Property Tests para Client Models
6. **Task 4.1** - Property Tests para Project Models
7. **Task 6.1** - Property Tests para LeadService

### Prioridade BAIXA
8. **Task 7.1** - Property Tests para ProjectService

---

## 📝 RELATÓRIO DE TESTES

Após execução, gerar relatório com:

1. **Resumo Executivo**
   - Total de testes executados
   - Testes passados/falhados
   - Cobertura de código

2. **Detalhes por Categoria**
   - Testes unitários
   - Property tests
   - Testes de integração

3. **Bugs Encontrados**
   - Descrição
   - Severidade
   - Steps to reproduce
   - Expected vs Actual

4. **Recomendações**
   - Melhorias sugeridas
   - Testes adicionais necessários

---

## 📞 CONTATO

**Dúvidas Técnicas:** Equipe de Desenvolvimento  
**Dúvidas de Negócio:** Product Owner  
**Bloqueios:** Reportar imediatamente

---

**Documento Criado:** 2025-11-25  
**Versão:** 1.0  
**Status:** Pronto para Execução ✅
