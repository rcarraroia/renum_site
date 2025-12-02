# 🛠️ RENUM - Tecnologias e Padrões

## Stack Detalhada

### Backend
- **Python:** 3.11+
- **Framework Web:** FastAPI 0.104+
- **Validação:** Pydantic 2.0+
- **Cliente Supabase:** supabase-py
- **Filas:** Celery 5.3+
- **Message Broker:** Redis 7+
- **IA Framework:** LangChain 0.1+, LangGraph 0.0.20+
- **HTTP Client:** httpx (async)

### Integrações
- **WhatsApp:** API a ser definida por projeto
- **SMS:** Provedor a ser definido por projeto
- **Email:** Provedor a ser definido por projeto
- **LLMs:** OpenRouter (acesso a múltiplos modelos)

### Ferramentas de Desenvolvimento
- **Formatação:** Black, Ruff
- **Type Checking:** mypy
- **Testes:** pytest, pytest-asyncio, pytest-cov
- **Linting:** ruff
- **Pre-commit:** hooks para qualidade de código

---

## 📏 Padrões de Código

### Type Hints Obrigatórios
```python
# ✅ CORRETO
def process_interview(interview_id: str, lead_id: str) -> dict[str, Any]:
    """Processa uma entrevista e retorna o resultado."""
    pass

# ❌ ERRADO
def process_interview(interview_id, lead_id):
    pass
```

### Pydantic Models para Validação
```python
from pydantic import BaseModel, Field, validator
from datetime import datetime
from uuid import UUID

class InterviewCreate(BaseModel):
    lead_id: UUID
    project_id: UUID
    metadata: dict[str, Any] = Field(default_factory=dict)
    
    @validator('metadata')
    def validate_metadata(cls, v):
        # Validações customizadas
        return v

class InterviewResponse(BaseModel):
    id: UUID
    lead_id: UUID
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True  # Pydantic v2
```

### Docstrings em Funções Públicas
```python
def send_whatsapp_message(phone: str, message: str) -> bool:
    """
    Envia mensagem via WhatsApp.
    
    Args:
        phone: Número de telefone no formato internacional (+5511999999999)
        message: Conteúdo da mensagem a ser enviada
        
    Returns:
        True se mensagem foi enviada com sucesso, False caso contrário
        
    Raises:
        WhatsAppAPIError: Se houver erro na comunicação com a API
        ValidationError: Se o número de telefone for inválido
    """
    pass
```

### Formatação com Black + Ruff
```python
# Configuração em pyproject.toml
[tool.black]
line-length = 100
target-version = ['py311']

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W"]
ignore = ["E501"]  # line too long (Black cuida disso)
```

---

## 🗃️ Padrões de Banco de Dados

### Nomenclatura (snake_case)
```sql
-- ✅ CORRETO
CREATE TABLE interview_messages (
    id UUID PRIMARY KEY,
    interview_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ❌ ERRADO
CREATE TABLE InterviewMessages (
    Id UUID PRIMARY KEY,
    InterviewId UUID NOT NULL,
    CreatedAt TIMESTAMP
);
```

### Timestamps Obrigatórios
```sql
-- Todas as tabelas devem ter:
created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
```

### Trigger para updated_at
```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_interviews_updated_at
    BEFORE UPDATE ON interviews
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### RLS Habilitado em Todas Tabelas
```sql
-- Habilitar RLS
ALTER TABLE clients ENABLE ROW LEVEL SECURITY;

-- Política para admins (acesso total)
CREATE POLICY "Admins have full access"
    ON clients
    FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );

-- Política para clientes (apenas seus dados)
CREATE POLICY "Clients can view own data"
    ON clients
    FOR SELECT
    TO authenticated
    USING (profile_id = auth.uid());
```

### Migrations Versionadas
```
migrations/
├── 001_create_profiles.sql
├── 002_create_clients.sql
├── 003_create_leads.sql
├── 004_create_interviews.sql
├── 005_create_interview_messages.sql
└── ...
```

---

## 🔒 Segurança

### Variáveis de Ambiente
```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Supabase
    supabase_url: str
    supabase_anon_key: str
    supabase_service_key: str  # NUNCA expor ao frontend
    
    # OpenRouter
    openrouter_api_key: str
    
    # WhatsApp (configurar conforme API escolhida)
    whatsapp_api_url: str | None = None
    whatsapp_api_key: str | None = None
    
    # SMS (configurar conforme provedor escolhido)
    sms_api_key: str | None = None
    sms_phone_number: str | None = None
    
    # Email (configurar conforme provedor escolhido)
    email_api_key: str | None = None
    email_from_address: str | None = None
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # App
    python_env: str = "development"
    port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

### .env NUNCA Commitado
```bash
# .gitignore
.env
.env.local
.env.*.local
docs/SUPABASE_CREDENTIALS.md
docs/*_CREDENTIALS.md
```

### Validação com Pydantic
```python
from pydantic import BaseModel, validator
import re

class LeadCreate(BaseModel):
    phone: str
    name: str
    email: str | None = None
    
    @validator('phone')
    def validate_phone(cls, v):
        # Formato: +5511999999999
        pattern = r'^\+\d{13}$'
        if not re.match(pattern, v):
            raise ValueError('Telefone deve estar no formato +5511999999999')
        return v
    
    @validator('email')
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('Email inválido')
        return v
```

### Rate Limiting
```python
from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/webhooks/whatsapp")
@limiter.limit("100/minute")
async def whatsapp_webhook(request: Request):
    pass
```

---

## 🧪 Testes

### Pytest
```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_supabase(mocker):
    return mocker.patch('src.utils.supabase_client.get_client')

# tests/unit/test_interview_service.py
import pytest
from src.services.interview_service import InterviewService

def test_create_interview(mock_supabase):
    service = InterviewService()
    result = service.create_interview(
        lead_id="123",
        project_id="456"
    )
    assert result['status'] == 'pending'

@pytest.mark.asyncio
async def test_process_interview_message():
    service = InterviewService()
    result = await service.process_message(
        interview_id="123",
        message="Minha resposta"
    )
    assert result is not None
```

### Coverage > 70%
```bash
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=70
```

---

## 🚀 Estrutura de Código

### Services (Lógica de Negócio)
```python
# src/services/interview_service.py
from uuid import UUID
from src.utils.supabase_client import get_client
from src.models.interview import InterviewCreate, InterviewResponse

class InterviewService:
    def __init__(self):
        self.supabase = get_client()
    
    def create_interview(
        self, 
        lead_id: UUID, 
        project_id: UUID
    ) -> InterviewResponse:
        """Cria nova entrevista."""
        data = {
            'lead_id': str(lead_id),
            'project_id': str(project_id),
            'status': 'pending'
        }
        result = self.supabase.table('interviews').insert(data).execute()
        return InterviewResponse(**result.data[0])
    
    async def process_message(
        self, 
        interview_id: UUID, 
        message: str
    ) -> dict:
        """Processa mensagem de entrevista com LangGraph."""
        # Lógica de processamento
        pass
```

### API Routes
```python
# src/api/routes/interviews.py
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from src.services.interview_service import InterviewService
from src.models.interview import InterviewCreate, InterviewResponse

router = APIRouter(prefix="/interviews", tags=["interviews"])

@router.post("/", response_model=InterviewResponse)
async def create_interview(
    data: InterviewCreate,
    service: InterviewService = Depends()
):
    """Cria nova entrevista."""
    try:
        return service.create_interview(
            lead_id=data.lead_id,
            project_id=data.project_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Celery Tasks
```python
# src/workers/message_tasks.py
from celery import Task
from src.workers.celery_app import celery_app
from src.services.whatsapp_service import WhatsAppService

class CallbackTask(Task):
    """Task base com retry automático."""
    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 3}
    retry_backoff = True
    retry_backoff_max = 600
    retry_jitter = True

@celery_app.task(base=CallbackTask, bind=True)
def send_whatsapp_message(self, phone: str, message: str):
    """Envia mensagem via WhatsApp."""
    service = WhatsAppService()
    return service.send_message(phone, message)
```

---

## 📦 Dependências

### requirements.txt
```txt
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Database
supabase==2.0.3
psycopg2-binary==2.9.9

# Async
httpx==0.25.2
aiofiles==23.2.1

# Celery + Redis
celery==5.3.4
redis==5.0.1

# AI
langchain==0.1.0
langgraph==0.0.20
openai==1.6.1

# Integrações (adicionar conforme necessidade do projeto)
# Exemplos:
# twilio==8.11.0  # Para SMS
# sendgrid==6.11.0  # Para Email
# requests==2.31.0  # Para APIs REST genéricas

# Utils
python-dotenv==1.0.0
python-multipart==0.0.6

# Dev
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
pytest-mock==3.12.0
black==23.12.0
ruff==0.1.8
mypy==1.7.1
```

---

## 🔧 Configuração do Projeto

### pyproject.toml
```toml
[tool.black]
line-length = 100
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W", "UP"]
ignore = ["E501"]
target-version = "py311"

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "--cov=src --cov-report=html --cov-report=term-missing"
```

---

**Última atualização:** 2025-11-25  
**Versão:** 1.0  
**Responsável:** Equipe RENUM
