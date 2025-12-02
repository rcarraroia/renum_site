# Design - Sprint 05: Completar Menus Sidebar + Correções Críticas

## Overview

Este documento detalha a arquitetura e implementação do Sprint 05, focando em correções críticas e integração dos menus sidebar com backend real.

---

## 🏗️ Arquitetura Geral

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Sidebar Menus (10 itens)                            │  │
│  │  - Overview Dashboard                                 │  │
│  │  - Conversas                                          │  │
│  │  - Pesquisas/Entrevistas                             │  │
│  │  - Clientes (✅ já funciona)                         │  │
│  │  - Leads (✅ já funciona)                            │  │
│  │  - Projetos (✅ já funciona)                         │  │
│  │  - Config. RENUS                                      │  │
│  │  - Sub-Agentes (✅ já funciona)                      │  │
│  │  - Relatórios                                         │  │
│  │  - Configurações                                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                           ↕ HTTP + JWT                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Routes (15 routers)                             │  │
│  │  - /api/dashboard/stats (NOVO)                       │  │
│  │  - /api/conversations (✅ existe)                    │  │
│  │  - /api/interviews (✅ existe)                       │  │
│  │  - /api/isa/chat (🔧 corrigir)                      │  │
│  │  - /chat/{slug}/message (🔧 implementar)            │  │
│  │  - /api/renus-config (🔧 completar)                 │  │
│  │  - /api/reports/* (NOVO)                             │  │
│  │  - /api/settings (NOVO)                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                           ↕                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Services (11 services)                              │  │
│  │  - DashboardService (NOVO)                           │  │
│  │  - ConversationService (✅ existe)                   │  │
│  │  - InterviewService (✅ existe)                      │  │
│  │  - RenusConfigService (✅ existe)                    │  │
│  │  - ReportService (NOVO)                              │  │
│  │  - SettingsService (NOVO)                            │  │
│  └──────────────────────────────────────────────────────┘  │
│                           ↕                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Agents (LangChain/LangGraph)                        │  │
│  │  - IsaAgent (🔧 conectar à rota)                    │  │
│  │  - RenusAgent (✅ existe)                            │  │
│  │  - DiscoveryAgent (✅ existe)                        │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              SUPABASE (PostgreSQL)                           │
│  - profiles, clients, leads, projects (✅)                  │
│  - conversations, messages (✅)                              │
│  - interviews, interview_messages (✅)                       │
│  - renus_config, tools, sub_agents (✅)                     │
│  - isa_commands (✅)                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔴 PARTE 1: Correções Críticas

### 1.1 Bug de Import - interviews.py

**Problema:**
```python
# backend/src/api/routes/interviews.py:226
update_data: Dict[str, Any],  # ❌ Dict não importado
```

**Solução:**
```python
# backend/src/api/routes/interviews.py
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
# ... resto dos imports
```

**Correctness Property 1:** Import Completeness
- GIVEN any Python file in the project
- WHEN the file uses type hints (Dict, List, Optional, etc)
- THEN all types must be imported from typing module
- AND file must pass `python -m py_compile` without errors

---

### 1.2 Bug JWT_SECRET - ws_handler.py

**Problema:**
```python
# backend/src/api/websocket/ws_handler.py:162
payload = jwt.decode(
    token,
    settings.JWT_SECRET,  # ❌ Atributo não existe
    algorithms=["HS256"]
)
```

**Solução:**
```python
# backend/src/api/websocket/ws_handler.py:162
payload = jwt.decode(
    token,
    settings.SECRET_KEY,  # ✅ Atributo correto
    algorithms=["HS256"]
)
```

**Correctness Property 2:** Configuration Consistency
- GIVEN settings.py defines SECRET_KEY
- WHEN any module needs JWT secret
- THEN it must use settings.SECRET_KEY (not JWT_SECRET)
- AND JWT validation must succeed with valid tokens

---

### 1.3 API Key - ANTHROPIC_API_KEY

**Problema:**
```bash
⚠️ WARNING: Missing required API keys: ANTHROPIC_API_KEY
```

**Solução:**
```bash
# backend/.env
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
```

**Correctness Property 3:** Required API Keys
- GIVEN settings.py validates API keys on startup
- WHEN ANTHROPIC_API_KEY is missing
- THEN system should start with warning (not fail)
- AND ISA Agent should gracefully handle missing key
- WHEN ANTHROPIC_API_KEY is present
- THEN no warning should appear

---

## 🟠 PARTE 2: Integrações Importantes

### 2.1 Conectar ISA à Rota Real

**Arquitetura:**
```
User (Admin) → POST /api/isa/chat
                    ↓
            isa.py (route)
                    ↓
            IsaAgent.process_message()
                    ↓
            LangChain (Claude 3.5 Sonnet)
                    ↓
            SupabaseTool (execute query)
                    ↓
            IsaCommandService.save_command()
                    ↓
            Response com dados reais
```

**Implementação:**
```python
# backend/src/api/routes/isa.py
from src.agents.isa import IsaAgent
from src.services.isa_command_service import IsaCommandService

# Inicializar agente (singleton ou por request)
isa_agent = IsaAgent()
command_service = IsaCommandService()

@router.post("/chat", response_model=IsaChatResponse)
async def chat_with_isa(
    request: IsaChatRequest,
    current_user: dict = Depends(get_current_user)
):
    # Verificar admin
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only admins can use ISA")
    
    try:
        # Processar com agente real
        result = await isa_agent.invoke({
            "messages": [{"role": "user", "content": request.message}],
            "user_id": current_user["id"]
        })
        
        # Salvar comando para auditoria
        await command_service.create({
            "admin_id": current_user["id"],
            "user_message": request.message,
            "assistant_response": result["response"],
            "command_executed": result.get("executed", False),
            "result": result.get("data", {})
        })
        
        return IsaChatResponse(
            message=result["response"],
            command_executed=result.get("executed", False),
            result=result.get("data", {})
        )
    except Exception as e:
        logger.error(f"ISA error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

**Correctness Property 4:** ISA Command Execution
- GIVEN admin sends command "list interviews"
- WHEN IsaAgent processes the command
- THEN it must query Supabase and return real data
- AND command must be saved in isa_commands table
- AND response.command_executed must be true

---

### 2.2 Implementar send_message - public_chat.py

**Implementação:**
```python
# backend/src/api/routes/public_chat.py
from src.services.subagent_service import SubAgentService
from src.services.interview_service import InterviewService
from src.agents.discovery_agent import DiscoveryAgent

@router.post("/chat/{agent_slug}/message")
async def send_message(agent_slug: str, request: ChatMessageRequest):
    try:
        subagent_service = SubAgentService()
        interview_service = InterviewService()
        
        # Buscar agente por slug
        agent = subagent_service.get_by_slug(agent_slug)
        if not agent or not agent.get("is_public"):
            raise HTTPException(status_code=404, detail="Agent not found")
        
        # Criar ou recuperar entrevista
        interview_id = request.interview_id
        if not interview_id:
            interview = interview_service.create({
                "sub_agent_id": agent["id"],
                "status": "in_progress"
            })
            interview_id = interview["id"]
        
        # Salvar mensagem do usuário
        await interview_service.add_message(interview_id, {
            "role": "user",
            "content": request.message
        })
        
        # Processar com agente
        discovery_agent = DiscoveryAgent()
        result = await discovery_agent.process_message(
            interview_id=interview_id,
            message=request.message,
            context=request.context
        )
        
        # Salvar resposta do agente
        await interview_service.add_message(interview_id, {
            "role": "assistant",
            "content": result["response"]
        })
        
        # Atualizar progresso
        progress = result.get("progress", {})
        is_complete = result.get("is_complete", False)
        
        if is_complete:
            await interview_service.complete_interview(
                interview_id,
                ai_analysis=result.get("analysis")
            )
        
        return ChatMessageResponse(
            message=result["response"],
            interview_id=interview_id,
            is_complete=is_complete,
            progress=progress
        )
    except Exception as e:
        logger.error(f"Error in public chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

**Correctness Property 5:** Message Persistence
- GIVEN user sends message via public chat
- WHEN message is processed
- THEN user message must be saved with role="user"
- AND agent response must be saved with role="assistant"
- AND both must have same interview_id
- AND messages must be retrievable via get_interview_history

---

## 📊 PARTE 3: Dashboard Overview

**Novo Endpoint:**
```python
# backend/src/api/routes/dashboard.py
from fastapi import APIRouter, Depends
from src.api.middleware.auth_middleware import get_current_user
from src.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats")
async def get_dashboard_stats(current_user = Depends(get_current_user)):
    service = DashboardService()
    
    stats = await service.get_stats(client_id=current_user.get("client_id"))
    
    return {
        "total_clients": stats["clients"],
        "total_leads": stats["leads"],
        "total_conversations": stats["conversations"],
        "active_interviews": stats["active_interviews"],
        "completed_interviews": stats["completed_interviews"],
        "completion_rate": stats["completion_rate"],
        "recent_activities": stats["recent_activities"]
    }
```

**Novo Service:**
```python
# backend/src/services/dashboard_service.py
from src.utils.supabase_client import get_client

class DashboardService:
    def __init__(self):
        self.client = get_client()
    
    async def get_stats(self, client_id: str = None):
        # Queries agregadas
        clients_count = self.client.table('clients').select('*', count='exact').execute().count
        leads_count = self.client.table('leads').select('*', count='exact').execute().count
        
        conversations_count = self.client.table('conversations')\
            .select('*', count='exact')\
            .eq('status', 'active')\
            .execute().count
        
        active_interviews = self.client.table('interviews')\
            .select('*', count='exact')\
            .eq('status', 'in_progress')\
            .execute().count
        
        completed_interviews = self.client.table('interviews')\
            .select('*', count='exact')\
            .eq('status', 'completed')\
            .execute().count
        
        total_interviews = active_interviews + completed_interviews
        completion_rate = (completed_interviews / total_interviews * 100) if total_interviews > 0 else 0
        
        # Atividades recentes (últimas 10)
        recent_activities = self._get_recent_activities()
        
        return {
            "clients": clients_count,
            "leads": leads_count,
            "conversations": conversations_count,
            "active_interviews": active_interviews,
            "completed_interviews": completed_interviews,
            "completion_rate": round(completion_rate, 2),
            "recent_activities": recent_activities
        }
    
    def _get_recent_activities(self):
        # Combinar últimas ações de várias tabelas
        activities = []
        
        # Últimas conversas
        conversations = self.client.table('conversations')\
            .select('id, created_at, status')\
            .order('created_at', desc=True)\
            .limit(5)\
            .execute().data
        
        for conv in conversations:
            activities.append({
                "type": "conversation",
                "action": "created",
                "timestamp": conv["created_at"],
                "details": f"Conversa {conv['status']}"
            })
        
        # Últimas entrevistas
        interviews = self.client.table('interviews')\
            .select('id, created_at, status')\
            .order('created_at', desc=True)\
            .limit(5)\
            .execute().data
        
        for interview in interviews:
            activities.append({
                "type": "interview",
                "action": "created",
                "timestamp": interview["created_at"],
                "details": f"Entrevista {interview['status']}"
            })
        
        # Ordenar por timestamp e retornar top 10
        activities.sort(key=lambda x: x["timestamp"], reverse=True)
        return activities[:10]
```

**Correctness Property 6:** Dashboard Metrics Accuracy
- GIVEN database has N clients, M leads, K conversations
- WHEN admin requests /api/dashboard/stats
- THEN response.total_clients must equal N
- AND response.total_leads must equal M
- AND response.total_conversations must equal K
- AND completion_rate must be (completed / total * 100)

---

## 🔧 PARTE 4: Configuração RENUS

**Endpoints Faltantes:**
```python
# backend/src/api/routes/renus_config.py

@router.post("/publish")
async def publish_config(current_user = Depends(get_current_user)):
    """Marca configuração como publicada e aplica imediatamente"""
    service = RenusConfigService()
    
    config = await service.get_config(current_user["client_id"])
    config["is_published"] = True
    config["published_at"] = datetime.now()
    
    await service.update_config(current_user["client_id"], config)
    
    # Recarregar agentes com nova configuração
    await reload_agents()
    
    return {"message": "Configuration published successfully"}
```

**Correctness Property 7:** Configuration Persistence
- GIVEN admin edits system_prompt in UI
- WHEN admin clicks "Salvar e Publicar"
- THEN new system_prompt must be saved in renus_config table
- AND Discovery Agent must use new prompt in next conversation
- AND old prompt must not be used anymore

---

## 📈 PARTE 5: Relatórios

**Estrutura:**
```python
# backend/src/services/report_service.py
class ReportService:
    async def generate_conversations_report(self, start_date, end_date):
        # Agregações de conversas
        pass
    
    async def generate_interviews_report(self, start_date, end_date):
        # Agregações de entrevistas
        pass
    
    async def generate_agents_report(self, start_date, end_date):
        # Estatísticas de uso de agentes
        pass
    
    async def export_to_csv(self, data, filename):
        # Exportação CSV
        pass
```

---

## ⚙️ PARTE 6: Configurações

**Estrutura:**
```python
# backend/src/models/settings.py
class UserSettings(BaseModel):
    user_id: str
    language: str = "pt-BR"
    timezone: str = "America/Sao_Paulo"
    theme: str = "light"
    email_notifications: bool = True
    push_notifications: bool = True
    sound_notifications: bool = True

# backend/src/services/settings_service.py
class SettingsService:
    async def get_settings(self, user_id: str):
        pass
    
    async def update_settings(self, user_id: str, settings: dict):
        pass
```

---

## 🧹 PARTE 7: Limpeza

**Código Duplicado:**
```python
# backend/src/services/subagent_service.py
# REMOVER: Linhas 357-600 (métodos síncronos duplicados)
# MANTER: Linhas 28-350 (métodos async)
```

**Rotas Duplicadas:**
```bash
# DELETAR: backend/src/api/routes/subagents.py
# MANTER: backend/src/api/routes/sub_agents.py
```

---

## 📊 Correctness Properties Summary

1. **Import Completeness** - All type hints must be imported
2. **Configuration Consistency** - JWT secret must use SECRET_KEY
3. **Required API Keys** - System handles missing keys gracefully
4. **ISA Command Execution** - Commands execute and audit
5. **Message Persistence** - All messages saved correctly
6. **Dashboard Metrics Accuracy** - Metrics match database counts
7. **Configuration Persistence** - Config changes apply immediately

---

## 🎯 Success Criteria

- ✅ Backend inicia sem erros
- ✅ ISA executa comandos reais
- ✅ Public chat processa com agentes
- ✅ Todos 10 menus sidebar funcionam
- ✅ Dados vêm do backend (não mock)
- ✅ Configuração RENUS salva e aplica
- ✅ Relatórios geram com dados reais
- ✅ Código limpo sem duplicações

---

**Design Version:** 1.0  
**Last Updated:** 2025-11-30  
**Status:** Ready for Implementation
