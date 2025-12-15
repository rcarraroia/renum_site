# Design Document - Sprint 05B

## Overview

Sprint 05B valida funcionalmente todos os componentes implementados nos Sprints 01-07A através de 4 fases sequenciais:

1. **Fase 1 (1.5h):** Validação Funcional (WebSocket, Frontend, Wizard, Integrações, E2E)
2. **Fase 2 (1h):** Análise de Gaps (Bugs pendentes, Funcionalidades faltantes, Docs)
3. **Fase 3 (1h):** Priorização e Roadmap (MVP, Sprint 07B, 08+)
4. **Fase 4 (0.5h):** Relatório Executivo

**Tempo total:** 4 horas

**Objetivo:** Garantir que o sistema está pronto para deploy em produção (Sprint 07B) com todas as funcionalidades MVP validadas e bugs críticos identificados.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SPRINT 05B WORKFLOW                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  FASE 1: VALIDAÇÃO FUNCIONAL (1.5h)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  WebSocket   │  │   Frontend   │  │    Wizard    │      │
│  │   Testing    │  │   Testing    │  │   Testing    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Integrações  │  │   Triggers   │  │     E2E      │      │
│  │   Testing    │  │   Testing    │  │   Complete   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                           │                                  │
│                  Resultados de Testes                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  FASE 2: ANÁLISE DE GAPS (1h)                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Bugs Sprint │  │  Bugs Sprint │  │ Funcional.   │      │
│  │     05A      │  │   06 + 07A   │  │  Faltantes   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                           │                                  │
│                  Lista de Gaps e Bugs                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  FASE 3: PRIORIZAÇÃO E ROADMAP (1h)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Definir    │  │    Sprint    │  │   Sprints    │      │
│  │  MVP (novo)  │  │  07B (deploy)│  │   08, 09+    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                           │                                  │
│                  Roadmap Priorizado                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  FASE 4: RELATÓRIO EXECUTIVO (0.5h)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Consolidar  │  │  Apresentar  │  │    Obter     │      │
│  │  Resultados  │  │ Recomendações│  │  Aprovação   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                           │                                  │
│             Decisão: Iniciar Sprint 07B (Deploy)            │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. WebSocket Validator

**Responsabilidade:** Testar conexão WebSocket em cenários reais

**Interface:**
```python
from dataclasses import dataclass
from typing import Optional
import asyncio
import websockets
import json

@dataclass
class TestResult:
    test_name: str
    passed: bool
    message: str
    duration_ms: float
    details: Optional[dict] = None

class WebSocketValidator:
    def __init__(self, ws_url: str, token: str):
        self.ws_url = ws_url
        self.token = token
        self.results: list[TestResult] = []
    
    async def test_connection_with_token(self) -> TestResult:
        """Testa conexão com token válido"""
        pass
    
    async def test_connection_without_token(self) -> TestResult:
        """Testa rejeição sem token"""
        pass
    
    async def test_message_exchange(self) -> TestResult:
        """Testa envio e recebimento de mensagens"""
        pass
    
    async def test_multiple_clients(self) -> TestResult:
        """Testa múltiplos clientes simultâneos"""
        pass
    
    async def test_connection_cleanup(self) -> TestResult:
        """Testa limpeza de recursos ao fechar"""
        pass
    
    async def run_all_tests(self) -> list[TestResult]:
        """Executa todos os testes"""
        pass
```

### 2. Frontend Validator

**Responsabilidade:** Testar frontend no navegador real

**Interface:**
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FrontendValidator:
    def __init__(self, base_url: str, credentials: dict):
        self.base_url = base_url
        self.credentials = credentials
        self.driver: Optional[webdriver.Chrome] = None
        self.results: list[TestResult] = []
    
    def setup_browser(self):
        """Inicializa navegador"""
        pass
    
    def test_page_load(self) -> TestResult:
        """Testa carregamento sem erros"""
        pass
    
    def test_login_flow(self) -> TestResult:
        """Testa autenticação e redirect"""
        pass
    
    def test_navigation(self) -> TestResult:
        """Testa navegação entre páginas"""
        pass
    
    def test_data_loading(self) -> TestResult:
        """Testa carregamento de dados do backend"""
        pass
    
    def test_crud_operations(self) -> TestResult:
        """Testa operações CRUD"""
        pass
    
    def run_all_tests(self) -> list[TestResult]:
        """Executa todos os testes"""
        pass
    
    def teardown_browser(self):
        """Fecha navegador"""
        pass
```

### 3. Wizard Validator

**Responsabilidade:** Testar Wizard 5 etapas + Sandbox + Publicação

**Interface:**
```python
class WizardValidator:
    def __init__(self, driver: webdriver.Chrome, base_url: str):
        self.driver = driver
        self.base_url = base_url
        self.results: list[TestResult] = []
    
    def test_step1_objective(self) -> TestResult:
        """Testa Step 1: Seleção template e preview slug"""
        pass
    
    def test_step2_personality(self) -> TestResult:
        """Testa Step 2: Personalidade e sliders tom"""
        pass
    
    def test_step3_fields(self) -> TestResult:
        """Testa Step 3: Campos customizados e drag-drop"""
        pass
    
    def test_step4_integrations(self) -> TestResult:
        """Testa Step 4: Status integrações"""
        pass
    
    def test_step5_test_publish(self) -> TestResult:
        """Testa Step 5: Sandbox e publicação"""
        pass
    
    def test_sandbox_langgraph(self) -> TestResult:
        """Testa WizardAgent com LangGraph"""
        pass
    
    def test_auto_save(self) -> TestResult:
        """Testa salvamento automático"""
        pass
    
    def test_agent_dashboard(self) -> TestResult:
        """Testa dashboard de agentes"""
        pass
    
    def run_all_tests(self) -> list[TestResult]:
        """Executa todos os testes"""
        pass
```

### 4. Integrations Validator

**Responsabilidade:** Testar Integrações + Triggers + Celery

**Interface:**
```python
class IntegrationsValidator:
    def __init__(self, api_client, db_client):
        self.api = api_client
        self.db = db_client
        self.results: list[TestResult] = []
    
    def test_uazapi_config(self) -> TestResult:
        """Testa configuração Uazapi"""
        pass
    
    def test_smtp_config(self) -> TestResult:
        """Testa configuração SMTP"""
        pass
    
    def test_supabase_client_config(self) -> TestResult:
        """Testa configuração Supabase Cliente"""
        pass
    
    def test_trigger_create_execute(self) -> TestResult:
        """Testa criação e execução de trigger"""
        pass
    
    def test_celery_redis(self) -> TestResult:
        """Testa Celery + Redis"""
        pass
    
    def run_all_tests(self) -> list[TestResult]:
        """Executa todos os testes"""
        pass
```

### 5. Bug Analyzer

**Responsabilidade:** Analisar bugs pendentes de todos os sprints

**Interface:**
```python
from enum import Enum
from dataclasses import dataclass

class BugSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class BugStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    FIXED = "fixed"
    WONT_FIX = "wont_fix"

@dataclass
class Bug:
    id: str
    sprint: str
    title: str
    description: str
    severity: BugSeverity
    status: BugStatus
    effort_hours: float
    dependencies: list[str]
    must_fix: bool

class BugAnalyzer:
    def __init__(self):
        self.bugs: list[Bug] = []
    
    def load_bugs_from_sprint(self, sprint_id: str) -> list[Bug]:
        """Carrega bugs de um sprint específico"""
        pass
    
    def classify_severity(self, bug: Bug) -> BugSeverity:
        """Classifica severidade do bug"""
        pass
    
    def identify_dependencies(self, bug: Bug) -> list[str]:
        """Identifica dependências do bug"""
        pass
    
    def estimate_effort(self, bug: Bug) -> float:
        """Estima esforço de correção em horas"""
        pass
    
    def mark_must_fix(self, bug: Bug) -> bool:
        """Marca se bug é bloqueador"""
        pass
    
    def generate_prioritized_list(self) -> list[Bug]:
        """Gera lista priorizada de bugs"""
        pass
```

### 6. Gap Identifier

**Responsabilidade:** Identificar funcionalidades faltantes

**Interface:**
```python
from enum import Enum

class GapPriority(Enum):
    ESSENTIAL = "essential"
    IMPORTANT = "important"
    NICE_TO_HAVE = "nice_to_have"

@dataclass
class Gap:
    id: str
    component: str
    title: str
    description: str
    priority: GapPriority
    effort_hours: float
    dependencies: list[str]
    mvp_required: bool

class GapIdentifier:
    def __init__(self):
        self.gaps: list[Gap] = []
    
    def audit_component(self, component_name: str) -> list[Gap]:
        """Audita componente e identifica gaps"""
        pass
    
    def classify_priority(self, gap: Gap) -> GapPriority:
        """Classifica prioridade do gap"""
        pass
    
    def identify_missing_dependencies(self, gap: Gap) -> list[str]:
        """Identifica dependências faltantes"""
        pass
    
    def estimate_implementation_effort(self, gap: Gap) -> float:
        """Estima esforço de implementação"""
        pass
    
    def check_documentation_gaps(self) -> list[Gap]:
        """Identifica documentação faltante"""
        pass
    
    def generate_gap_report(self) -> dict:
        """Gera relatório de gaps"""
        pass
```

### 7. MVP Definer

**Responsabilidade:** Definir MVP incluindo Wizard e Integrações

**Interface:**
```python
@dataclass
class Feature:
    name: str
    sprint: str
    status: str  # "complete", "partial", "missing"
    bugs_critical: int
    in_mvp: bool

class MVPDefiner:
    def __init__(self):
        self.features: list[Feature] = []
        self.mvp_features: list[Feature] = []
        self.post_mvp_features: list[Feature] = []
    
    def define_mvp_scope(self) -> dict:
        """Define escopo do MVP"""
        mvp = {
            "included": [
                "Auth + CRUD (Sprints 01-02)",
                "WebSocket + Conversas (Sprint 03)",
                "Multi-Agent System (Sprint 04)",
                "Wizard Criação Agentes (Sprint 06)",
                "Integrações Core (Sprint 07A)"
            ],
            "excluded": [
                "Google Workspace",
                "Chatwoot",
                "Sub-agentes especializados",
                "Analytics avançado"
            ]
        }
        return mvp
    
    def validate_mvp_features(self) -> list[Feature]:
        """Valida funcionalidades MVP sem bugs críticos"""
        pass
    
    def document_mvp(self) -> str:
        """Documenta escopo MVP"""
        pass
    
    def check_critical_bugs(self) -> list[Bug]:
        """Verifica bugs críticos no MVP"""
        pass
```

### 8. Roadmap Creator

**Responsabilidade:** Criar roadmap priorizado

**Interface:**
```python
@dataclass
class Sprint:
    id: str
    name: str
    duration_hours: float
    tasks: list[str]
    dependencies: list[str]
    priority: int

class RoadmapCreator:
    def __init__(self):
        self.sprints: list[Sprint] = []
    
    def create_sprint_07b(self) -> Sprint:
        """Cria roadmap Sprint 07B (Deploy)"""
        return Sprint(
            id="07B",
            name="Deploy VPS + Produção",
            duration_hours=6,
            tasks=[
                "Deploy backend VPS",
                "Configurar Celery produção",
                "Configurar Nginx + SSL",
                "Setup monitoring",
                "Testes produção"
            ],
            dependencies=["Sprint 05B completo"],
            priority=1
        )
    
    def create_sprint_08(self) -> Sprint:
        """Cria roadmap Sprint 08 (Bugs + Performance)"""
        pass
    
    def create_sprint_09_plus(self) -> list[Sprint]:
        """Cria roadmap Sprints 09+ (Features)"""
        pass
    
    def prioritize_tasks(self, tasks: list) -> list:
        """Prioriza tarefas por valor e esforço"""
        pass
    
    def validate_dependencies(self) -> bool:
        """Valida ordenação respeitando dependências"""
        pass
    
    def generate_roadmap(self) -> dict:
        """Gera roadmap completo"""
        pass
```

### 9. Executive Reporter

**Responsabilidade:** Gerar relatório executivo

**Interface:**
```python
@dataclass
class ExecutiveReport:
    functional_percentage: float
    achievements: list[str]
    bugs_fixed: list[str]
    roadmap_summary: dict
    recommendations: list[str]
    next_steps: list[str]

class ExecutiveReporter:
    def __init__(self, validation_results, bugs, gaps, mvp, roadmap):
        self.validation = validation_results
        self.bugs = bugs
        self.gaps = gaps
        self.mvp = mvp
        self.roadmap = roadmap
    
    def calculate_functional_percentage(self) -> float:
        """Calcula % funcional do sistema"""
        pass
    
    def list_achievements(self) -> list[str]:
        """Lista conquistas Sprints 01-07A"""
        pass
    
    def highlight_bugs_fixed(self) -> list[str]:
        """Destaca bugs críticos corrigidos"""
        pass
    
    def summarize_roadmap(self) -> dict:
        """Resume roadmap"""
        pass
    
    def create_recommendations(self) -> list[str]:
        """Cria recomendações Sprint 07B"""
        pass
    
    def generate_report(self) -> ExecutiveReport:
        """Gera relatório executivo completo"""
        pass
    
    def export_markdown(self, report: ExecutiveReport) -> str:
        """Exporta relatório em Markdown"""
        pass
```

## Data Models

### TestResult
```python
@dataclass
class TestResult:
    test_name: str
    component: str
    passed: bool
    message: str
    duration_ms: float
    timestamp: datetime
    details: Optional[dict] = None
    screenshot_path: Optional[str] = None
```

### Bug
```python
@dataclass
class Bug:
    id: str
    sprint: str
    title: str
    description: str
    severity: BugSeverity  # CRITICAL, HIGH, MEDIUM, LOW
    status: BugStatus  # PENDING, IN_PROGRESS, FIXED, WONT_FIX
    effort_hours: float
    dependencies: list[str]
    must_fix: bool
    created_at: datetime
    updated_at: datetime
```

### Gap
```python
@dataclass
class Gap:
    id: str
    component: str
    title: str
    description: str
    priority: GapPriority  # ESSENTIAL, IMPORTANT, NICE_TO_HAVE
    effort_hours: float
    dependencies: list[str]
    mvp_required: bool
    documentation_missing: bool
```

### Feature
```python
@dataclass
class Feature:
    name: str
    sprint: str
    status: str  # "complete", "partial", "missing"
    bugs_critical: int
    bugs_high: int
    bugs_medium: int
    bugs_low: int
    in_mvp: bool
    completion_percentage: float
```

### Sprint (Roadmap)
```python
@dataclass
class Sprint:
    id: str
    name: str
    duration_hours: float
    tasks: list[str]
    dependencies: list[str]
    priority: int
    estimated_start: Optional[datetime] = None
    estimated_end: Optional[datetime] = None
```

## Error Handling

### Validation Errors
```python
class ValidationError(Exception):
    """Erro durante validação funcional"""
    pass

class TestTimeoutError(ValidationError):
    """Timeout durante teste"""
    pass

class ConnectionError(ValidationError):
    """Erro de conexão (WebSocket, API, DB)"""
    pass
```

### Analysis Errors
```python
class AnalysisError(Exception):
    """Erro durante análise de bugs/gaps"""
    pass

class DataIncompleteError(AnalysisError):
    """Dados incompletos para análise"""
    pass
```

### Reporting Errors
```python
class ReportingError(Exception):
    """Erro durante geração de relatório"""
    pass
```

## Testing Strategy

### Unit Tests
- Testar cada validator isoladamente
- Mockar conexões externas (WebSocket, API, DB)
- Validar lógica de classificação (bugs, gaps)
- Testar geração de relatórios

### Integration Tests
- Testar validadores com sistema real
- Validar fluxo completo E2E
- Testar persistência de resultados

### Manual Tests
- Executar validação funcional no navegador
- Verificar visualmente Wizard e Integrações
- Validar relatório executivo gerado

## Implementation Notes

**Tempo estimado:** 4h (antes 2h)

**Motivo:** Validação Sprint 06 (Wizard) + Sprint 07A (Integrações) adicionadas

**Ferramentas necessárias:**
- Selenium WebDriver (testes frontend)
- websockets library (testes WebSocket)
- pytest (framework testes)
- Supabase client (validação DB)

**Dependências:**
- Backend rodando (localhost:8000)
- Frontend rodando (localhost:5173)
- Supabase acessível
- Redis rodando (para Celery)

**Outputs esperados:**
1. Relatório validação funcional (JSON + Markdown)
2. Lista bugs priorizados (CSV + Markdown)
3. Lista gaps identificados (CSV + Markdown)
4. Definição MVP atualizado (Markdown)
5. Roadmap priorizado (Markdown)
6. Relatório executivo final (Markdown + PDF)
