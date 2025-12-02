# Design Document - Sprint 04: Sistema Multi-Agente

## Overview

Este documento descreve a arquitetura e design do sistema multi-agente do RENUM, implementando três agentes principais (RENUS, ISA, Discovery) com infraestrutura LangGraph/LangChain, exposição via LangServe, e observabilidade completa via LangSmith.

O sistema utiliza uma arquitetura baseada em grafos de estados (LangGraph) para orquestração, com agentes especializados que podem ser dinamicamente configurados e gerenciados através de interface administrativa.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐ │
│  │ Admin Dashboard  │  │ Interview Form   │  │ Chat Widget   │ │
│  │  - ISA Chat      │  │  - Web Entry     │  │  - Lead Chat  │ │
│  │  - Sub-agents UI │  │  - Progress      │  │               │ │
│  └──────────────────┘  └──────────────────┘  └───────────────┘ │
└────────────┬────────────────────┬────────────────────┬──────────┘
             │                    │                    │
             │ HTTP/WebSocket     │ HTTP               │ WebSocket
             │                    │                    │
┌────────────▼────────────────────▼────────────────────▼──────────┐
│                    BACKEND (FastAPI + LangServe)                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    LangServe Routes                       │   │
│  │  /agents/renus/invoke  /agents/isa/invoke                │   │
│  │  /agents/discovery/invoke  /agents/{id}/stream           │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Agent Layer                            │   │
│  │  ┌──────────┐  ┌──────────┐  ┌────────────────────────┐ │   │
│  │  │  RENUS   │  │   ISA    │  │  Sub-Agents            │ │   │
│  │  │  (GPT-4) │  │ (Claude) │  │  - Discovery (GPT-4o)  │ │   │
│  │  │          │  │          │  │  - Future agents...    │ │   │
│  │  └────┬─────┘  └────┬─────┘  └──────────┬─────────────┘ │   │
│  │       │             │                   │               │   │
│  │       └─────────────┴───────────────────┘               │   │
│  │                     │                                    │   │
│  │              ┌──────▼──────┐                            │   │
│  │              │  LangGraph  │                            │   │
│  │              │  Orchestr.  │                            │   │
│  │              └──────┬──────┘                            │   │
│  └─────────────────────┼───────────────────────────────────┘   │
│  ┌─────────────────────▼───────────────────────────────────┐   │
│  │                    Tools Layer                           │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌─────────────────┐ │   │
│  │  │ Supabase     │ │ WhatsApp     │ │ Email           │ │   │
│  │  │ Tool         │ │ Tool (ABC)   │ │ Tool            │ │   │
│  │  └──────────────┘ └──────────────┘ └─────────────────┘ │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────┬─────────────────────────────────────────┬──────────┘
             │                                         │
             │                                         │
┌────────────▼──────────────┐              ┌──────────▼──────────┐
│   Supabase (PostgreSQL)   │              │   LangSmith         │
│   - interviews            │              │   - Traces          │
│   - interview_messages    │              │   - Metrics         │
│   - sub_agents            │              │   - Debugging       │
│   - isa_commands          │              │                     │
└───────────────────────────┘              └─────────────────────┘
```


### Agent Flow Diagrams

#### RENUS Orchestration Flow

```
User Message
     │
     ▼
┌─────────────────┐
│  RENUS Receives │
│     Message     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  Analyze Intent         │
│  - Extract context      │
│  - Identify topic       │
│  - Check history        │
└────────┬────────────────┘
         │
         ▼
    ┌────────┐
    │ Route? │
    └───┬────┘
        │
   ┌────┴────┐
   │         │
   ▼         ▼
[Sub-Agent] [Direct Response]
   │
   ▼
┌──────────────────┐
│ Sub-Agent        │
│ Processes        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Return to RENUS  │
│ - Result         │
│ - Next action    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ RENUS Decides    │
│ - Continue?      │
│ - Switch agent?  │
│ - End?           │
└────────┬─────────┘
         │
         ▼
    Response
```

#### ISA Command Flow

```
Admin Message
     │
     ▼
┌─────────────────┐
│  ISA Receives   │
│    Command      │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  Parse Command          │
│  - Identify action      │
│  - Extract parameters   │
│  - Validate permissions │
└────────┬────────────────┘
         │
         ▼
    ┌────────┐
    │ Valid? │
    └───┬────┘
        │
   ┌────┴────┐
   │         │
   ▼         ▼
[Execute]  [Error]
   │
   ▼
┌──────────────────┐
│ Invoke Tool      │
│ - Supabase query │
│ - Send messages  │
│ - Generate report│
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Log to           │
│ isa_commands     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Format Response  │
│ - Success msg    │
│ - Data summary   │
│ - Next steps     │
└────────┬─────────┘
         │
         ▼
    Response
```


#### Discovery Interview Flow

```
Start Interview
     │
     ▼
┌─────────────────┐
│ Create Interview│
│ Record (pending)│
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ Load Interview Script   │
│ - Required fields       │
│ - Question sequence     │
│ - Validation rules      │
└────────┬────────────────┘
         │
         ▼
┌──────────────────┐
│ Ask Question     │
│ (save as message)│
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Wait for Answer  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Validate Answer  │
│ (save as message)│
└────────┬─────────┘
         │
    ┌────┴────┐
    │ Valid?  │
    └───┬─────┘
        │
   ┌────┴────┐
   │         │
   ▼         ▼
[Next Q]  [Re-ask]
   │
   ▼
┌──────────────────┐
│ All Questions    │
│ Answered?        │
└────────┬─────────┘
         │
    ┌────┴────┐
    │  Yes    │
    ▼         
┌──────────────────┐
│ Generate AI      │
│ Analysis         │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Update Interview │
│ - status:        │
│   completed      │
│ - ai_analysis    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Notify Client    │
└────────┬─────────┘
         │
         ▼
      Done
```

## Components and Interfaces

### 1. Base Agent (Abstract)

```python
# backend/src/agents/base.py

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from langchain_core.messages import BaseMessage
from langchain_core.runnables import Runnable

class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(
        self,
        model: str,
        system_prompt: str,
        tools: Optional[List[Any]] = None,
        **kwargs
    ):
        self.model = model
        self.system_prompt = system_prompt
        self.tools = tools or []
        self.llm = self._initialize_llm()
        self.graph = self._build_graph()
    
    @abstractmethod
    def _initialize_llm(self) -> Any:
        """Initialize the LLM based on model name"""
        pass
    
    @abstractmethod
    def _build_graph(self) -> Runnable:
        """Build the LangGraph for this agent"""
        pass
    
    @abstractmethod
    async def invoke(
        self,
        messages: List[BaseMessage],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process messages and return response"""
        pass
```


### 2. RENUS Agent

```python
# backend/src/agents/renus.py

from typing import Any, Dict, List
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from .base import BaseAgent

class RenusAgent(BaseAgent):
    """Main orchestrator agent"""
    
    def __init__(self, **kwargs):
        super().__init__(
            model="gpt-4-turbo-preview",
            system_prompt=self._get_system_prompt(),
            **kwargs
        )
    
    def _get_system_prompt(self) -> str:
        return """You are RENUS, the main orchestrator agent for the RENUM system.
        
Your responsibilities:
1. Analyze incoming messages and determine intent
2. Route conversations to specialized sub-agents when appropriate
3. Handle general conversations directly when no sub-agent is needed
4. Maintain context across multiple turns
5. Implement fallback logic when sub-agents fail
6. Log all routing decisions with clear reasoning

Available sub-agents:
- Discovery: Conducts structured interviews for requirement gathering
- (More sub-agents will be added in future)

When routing, consider:
- Message topic and intent
- Conversation history
- Sub-agent capabilities
- User preferences

Always explain your routing decisions clearly."""
    
    def _initialize_llm(self) -> ChatOpenAI:
        return ChatOpenAI(
            model=self.model,
            temperature=0.7,
            streaming=True
        )
    
    def _build_graph(self) -> StateGraph:
        """Build LangGraph for RENUS orchestration"""
        
        workflow = StateGraph(dict)
        
        # Define nodes
        workflow.add_node("analyze", self._analyze_intent)
        workflow.add_node("route", self._route_to_subagent)
        workflow.add_node("respond", self._generate_response)
        
        # Define edges
        workflow.set_entry_point("analyze")
        workflow.add_conditional_edges(
            "analyze",
            self._should_route,
            {
                "route": "route",
                "respond": "respond"
            }
        )
        workflow.add_edge("route", "respond")
        workflow.add_edge("respond", END)
        
        return workflow.compile()
    
    async def _analyze_intent(self, state: Dict) -> Dict:
        """Analyze message intent and context"""
        # Implementation
        pass
    
    async def _route_to_subagent(self, state: Dict) -> Dict:
        """Route to appropriate sub-agent"""
        # Implementation
        pass
    
    async def _generate_response(self, state: Dict) -> Dict:
        """Generate final response"""
        # Implementation
        pass
    
    def _should_route(self, state: Dict) -> str:
        """Decide if routing is needed"""
        # Implementation
        pass
```


### 3. ISA Agent

```python
# backend/src/agents/isa.py

from typing import Any, Dict, List
from langchain_anthropic import ChatAnthropic
from .base import BaseAgent

class IsaAgent(BaseAgent):
    """Administrative assistant agent"""
    
    def __init__(self, **kwargs):
        super().__init__(
            model="claude-3-5-sonnet-20241022",
            system_prompt=self._get_system_prompt(),
            **kwargs
        )
    
    def _get_system_prompt(self) -> str:
        return """You are ISA (Intelligent System Assistant), an administrative assistant for the RENUM system.

Your capabilities:
1. Generate reports from database queries
2. Execute bulk operations (send messages, update records)
3. Query system data (leads, clients, projects, interviews)
4. Provide system insights and analytics
5. Execute administrative commands

Available commands:
- "generate report [type]" - Create various reports
- "send message to [target]" - Send bulk messages
- "query [entity] where [conditions]" - Database queries
- "analyze [data]" - Provide insights
- "list [entity]" - List records

Always:
- Confirm destructive operations before executing
- Provide clear summaries of results
- Log all commands to isa_commands table
- Respect admin permissions
- Format responses clearly with tables/lists when appropriate"""
    
    def _initialize_llm(self) -> ChatAnthropic:
        return ChatAnthropic(
            model=self.model,
            temperature=0.3,  # Lower temperature for precise commands
            max_tokens=4096
        )
```

### 4. Discovery Sub-Agent

```python
# backend/src/agents/subagents/discovery.py

from typing import Any, Dict, List
from langchain_openai import ChatOpenAI
from ..base import BaseAgent

class DiscoveryAgent(BaseAgent):
    """Sub-agent for conducting structured interviews"""
    
    def __init__(self, **kwargs):
        super().__init__(
            model="gpt-4o-mini",
            system_prompt=self._get_system_prompt(),
            **kwargs
        )
        self.required_fields = [
            "contact_name",
            "contact_phone",
            "email",
            "country",
            "company",
            "niche_experience",
            "current_rank",
            "operation_size"
        ]
    
    def _get_system_prompt(self) -> str:
        return """You are Discovery, a specialized interview agent for gathering structured information.

Your goal: Conduct natural, conversational interviews while collecting specific required information.

Required information to collect:
1. Contact Name - Full name of the person
2. Contact Phone - Phone number with country code
3. Email - Valid email address
4. Country - Country of residence/operation
5. Company - Company or organization name
6. Niche Experience - Experience in their field (time and level)
7. Current Rank/Position - Current role or rank
8. Operation Size - Size of their operation/team/network

Interview guidelines:
- Be conversational and friendly, not robotic
- Ask one question at a time
- Adapt follow-up questions based on answers
- Validate answers (e.g., email format, phone format)
- If answer is unclear, politely ask for clarification
- Acknowledge answers before moving to next question
- Maintain context throughout the conversation
- At the end, summarize collected information for confirmation

Remember: You're having a conversation, not filling a form. Make it natural!"""
    
    def _initialize_llm(self) -> ChatOpenAI:
        return ChatOpenAI(
            model=self.model,
            temperature=0.8,  # Higher for more natural conversation
            streaming=True
        )
```


### 5. Tools

#### Supabase Tool

```python
# backend/src/tools/supabase_tool.py

from typing import Any, Dict, Optional
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class SupabaseQueryInput(BaseModel):
    """Input schema for Supabase queries"""
    table: str = Field(description="Table name to query")
    operation: str = Field(description="Operation: select, insert, update, delete")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Filter conditions")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Data for insert/update")

class SupabaseTool(BaseTool):
    """Tool for querying Supabase database"""
    
    name = "supabase_query"
    description = """Query the Supabase database. 
    Supports select, insert, update, delete operations.
    Automatically enforces RLS based on user context."""
    args_schema = SupabaseQueryInput
    
    def __init__(self, client_id: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.client_id = client_id
    
    def _run(self, table: str, operation: str, filters: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute synchronous query"""
        from src.config.supabase import get_supabase_client
        
        supabase = get_supabase_client()
        
        # Add client_id filter if provided (multi-tenant)
        if self.client_id and filters:
            filters["client_id"] = self.client_id
        
        try:
            if operation == "select":
                query = supabase.table(table).select("*")
                if filters:
                    for key, value in filters.items():
                        query = query.eq(key, value)
                result = query.execute()
                return {"success": True, "data": result.data}
            
            elif operation == "insert":
                result = supabase.table(table).insert(data).execute()
                return {"success": True, "data": result.data}
            
            elif operation == "update":
                query = supabase.table(table).update(data)
                if filters:
                    for key, value in filters.items():
                        query = query.eq(key, value)
                result = query.execute()
                return {"success": True, "data": result.data}
            
            elif operation == "delete":
                query = supabase.table(table).delete()
                if filters:
                    for key, value in filters.items():
                        query = query.eq(key, value)
                result = query.execute()
                return {"success": True, "data": result.data}
            
            else:
                return {"success": False, "error": f"Unknown operation: {operation}"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _arun(self, *args, **kwargs) -> Dict[str, Any]:
        """Execute async query"""
        return self._run(*args, **kwargs)
```


#### WhatsApp Tool (Abstract)

```python
# backend/src/providers/whatsapp/base.py

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel

class WhatsAppMessage(BaseModel):
    """Standardized WhatsApp message"""
    phone: str
    content: str
    message_id: Optional[str] = None
    timestamp: Optional[str] = None
    status: Optional[str] = None

class WhatsAppProvider(ABC):
    """Abstract base class for WhatsApp providers"""
    
    @abstractmethod
    async def send_message(self, phone: str, message: str) -> Dict[str, Any]:
        """
        Send a text message
        
        Args:
            phone: Phone number in international format (+5511999999999)
            message: Message content
        
        Returns:
            Dict with success status and message_id
        """
        pass
    
    @abstractmethod
    async def send_media(self, phone: str, media_url: str, caption: str = "") -> Dict[str, Any]:
        """
        Send media (image, video, document)
        
        Args:
            phone: Phone number in international format
            media_url: URL of the media file
            caption: Optional caption
        
        Returns:
            Dict with success status and message_id
        """
        pass
    
    @abstractmethod
    async def handle_webhook(self, payload: Dict[str, Any]) -> WhatsAppMessage:
        """
        Parse webhook payload from provider
        
        Args:
            payload: Raw webhook payload from provider
        
        Returns:
            Standardized WhatsAppMessage object
        """
        pass
    
    @abstractmethod
    async def get_message_status(self, message_id: str) -> str:
        """
        Get delivery status of a message
        
        Args:
            message_id: ID of the message
        
        Returns:
            Status string: 'sent', 'delivered', 'read', 'failed'
        """
        pass

# backend/src/tools/whatsapp_tool.py

from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional

class WhatsAppMessageInput(BaseModel):
    """Input schema for WhatsApp messages"""
    phone: str = Field(description="Phone number in international format")
    message: str = Field(description="Message content to send")

class WhatsAppTool(BaseTool):
    """Tool for sending WhatsApp messages"""
    
    name = "send_whatsapp"
    description = """Send a WhatsApp message to a phone number.
    Phone must be in international format: +5511999999999"""
    args_schema = WhatsAppMessageInput
    
    def __init__(self, provider: WhatsAppProvider, **kwargs):
        super().__init__(**kwargs)
        self.provider = provider
    
    async def _arun(self, phone: str, message: str) -> Dict[str, Any]:
        """Send message asynchronously"""
        try:
            result = await self.provider.send_message(phone, message)
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _run(self, phone: str, message: str) -> Dict[str, Any]:
        """Sync version (not recommended)"""
        import asyncio
        return asyncio.run(self._arun(phone, message))
```


#### Email Tool

```python
# backend/src/tools/email_tool.py

from langchain.tools import BaseTool
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class EmailInput(BaseModel):
    """Input schema for emails"""
    to: List[EmailStr] = Field(description="List of recipient email addresses")
    subject: str = Field(description="Email subject")
    body: str = Field(description="Email body (HTML or plain text)")
    cc: Optional[List[EmailStr]] = Field(default=None, description="CC recipients")

class EmailTool(BaseTool):
    """Tool for sending emails"""
    
    name = "send_email"
    description = """Send an email to one or more recipients.
    Supports HTML and plain text bodies."""
    args_schema = EmailInput
    
    async def _arun(
        self,
        to: List[str],
        subject: str,
        body: str,
        cc: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Send email asynchronously"""
        # Implementation will depend on email provider chosen
        # (SendGrid, AWS SES, SMTP, etc.)
        try:
            # Placeholder for actual implementation
            return {
                "success": True,
                "message_id": "placeholder",
                "recipients": to
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
```

## Data Models

### Database Schema Updates

#### Migration: Add Fields to `interviews` Table

```sql
-- Migration: 004_add_interview_fields.sql

-- Add new fields to interviews table
ALTER TABLE interviews
ADD COLUMN IF NOT EXISTS email TEXT,
ADD COLUMN IF NOT EXISTS country TEXT,
ADD COLUMN IF NOT EXISTS company TEXT,
ADD COLUMN IF NOT EXISTS niche_experience TEXT,
ADD COLUMN IF NOT EXISTS current_rank TEXT,
ADD COLUMN IF NOT EXISTS operation_size TEXT;

-- Add comments for documentation
COMMENT ON COLUMN interviews.email IS 'Contact email address collected during interview';
COMMENT ON COLUMN interviews.country IS 'Country of residence or operation';
COMMENT ON COLUMN interviews.company IS 'Company or organization name';
COMMENT ON COLUMN interviews.niche_experience IS 'Experience in their field (time and level)';
COMMENT ON COLUMN interviews.current_rank IS 'Current role, rank, or position';
COMMENT ON COLUMN interviews.operation_size IS 'Size of operation/team/network (small/medium/large or number)';

-- Add indexes for common queries
CREATE INDEX IF NOT EXISTS idx_interviews_country ON interviews(country);
CREATE INDEX IF NOT EXISTS idx_interviews_company ON interviews(company);
CREATE INDEX IF NOT EXISTS idx_interviews_status_created ON interviews(status, created_at DESC);

-- Update RLS policies (already exist, just verify)
-- Admins should have full access
-- Clients should only see their own interviews (via lead_id -> client_id)
```


### Pydantic Models

```python
# backend/src/models/interview.py

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class InterviewBase(BaseModel):
    """Base interview model"""
    lead_id: Optional[UUID] = None
    subagent_id: Optional[UUID] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    email: Optional[EmailStr] = None
    country: Optional[str] = None
    company: Optional[str] = None
    niche_experience: Optional[str] = None
    current_rank: Optional[str] = None
    operation_size: Optional[str] = None
    status: str = "pending"
    topics_covered: Optional[List[str]] = None

class InterviewCreate(InterviewBase):
    """Model for creating interviews"""
    pass

class InterviewUpdate(BaseModel):
    """Model for updating interviews"""
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    email: Optional[EmailStr] = None
    country: Optional[str] = None
    company: Optional[str] = None
    niche_experience: Optional[str] = None
    current_rank: Optional[str] = None
    operation_size: Optional[str] = None
    status: Optional[str] = None
    completed_at: Optional[datetime] = None
    topics_covered: Optional[List[str]] = None
    ai_analysis: Optional[Dict[str, Any]] = None

class InterviewResponse(InterviewBase):
    """Model for interview responses"""
    id: UUID
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    ai_analysis: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class InterviewMessageCreate(BaseModel):
    """Model for creating interview messages"""
    interview_id: UUID
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str

class InterviewMessageResponse(BaseModel):
    """Model for interview message responses"""
    id: UUID
    interview_id: UUID
    role: str
    content: str
    timestamp: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

# backend/src/models/sub_agent.py

class SubAgentBase(BaseModel):
    """Base sub-agent model"""
    name: str
    description: Optional[str] = None
    channel: str = Field(..., pattern="^(whatsapp|web|sms|email)$")
    system_prompt: str
    topics: Optional[List[str]] = None
    model: str = "gpt-4o-mini"
    is_active: bool = True
    fine_tuning_config: Optional[Dict[str, Any]] = None

class SubAgentCreate(SubAgentBase):
    """Model for creating sub-agents"""
    config_id: Optional[int] = None

class SubAgentUpdate(BaseModel):
    """Model for updating sub-agents"""
    name: Optional[str] = None
    description: Optional[str] = None
    channel: Optional[str] = None
    system_prompt: Optional[str] = None
    topics: Optional[List[str]] = None
    model: Optional[str] = None
    is_active: Optional[bool] = None
    fine_tuning_config: Optional[Dict[str, Any]] = None

class SubAgentResponse(SubAgentBase):
    """Model for sub-agent responses"""
    id: UUID
    config_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# backend/src/models/isa_command.py

class IsaCommandCreate(BaseModel):
    """Model for creating ISA commands"""
    admin_id: UUID
    user_message: str
    assistant_response: str
    command_executed: bool = False

class IsaCommandResponse(BaseModel):
    """Model for ISA command responses"""
    id: UUID
    admin_id: UUID
    user_message: str
    assistant_response: str
    command_executed: bool
    executed_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: RENUS routing consistency
*For any* user message and conversation context, when RENUS analyzes the message multiple times with the same context, the routing decision should be consistent (same sub-agent or direct response).
**Validates: Requirements 1.1**

### Property 2: ISA command audit completeness
*For any* ISA command execution, there must exist exactly one corresponding record in the isa_commands table with matching admin_id, user_message, and execution timestamp.
**Validates: Requirements 2.3**

### Property 3: Discovery interview field completeness
*For any* interview with status 'completed', all mandatory fields (contact_name, contact_phone, email, country, company, niche_experience, current_rank, operation_size) must be non-null.
**Validates: Requirements 3.2**

### Property 4: Interview message ordering
*For any* interview, when retrieving interview_messages ordered by timestamp, the sequence should alternate between 'assistant' and 'user' roles (starting with 'assistant' asking the first question).
**Validates: Requirements 3.4**

### Property 5: LangSmith trace completeness
*For any* agent invocation that completes successfully, there must exist at least one trace in LangSmith with matching conversation_id and agent type.
**Validates: Requirements 10.1**

### Property 6: Multi-tenant data isolation
*For any* two different client_ids, querying interviews through the Supabase tool should return disjoint sets with no overlap in interview IDs.
**Validates: Requirements 12.1, 12.2**

### Property 7: Sub-agent model validation
*For any* sub-agent creation or update, if a model is specified, it must be one of the supported models: gpt-4, gpt-4-turbo-preview, gpt-4o-mini, claude-3-5-sonnet-20241022, claude-3-opus.
**Validates: Requirements 11.4**

### Property 8: WhatsApp provider interface compliance
*For any* WhatsApp provider implementation, all abstract methods (send_message, send_media, handle_webhook, get_message_status) must be implemented and return values matching the specified type signatures.
**Validates: Requirements 9.1, 9.2**

### Property 9: Interview AI analysis generation
*For any* interview that transitions to status 'completed', the ai_analysis field must be populated with a non-empty JSON object containing at least 'summary' and 'insights' keys.
**Validates: Requirements 3.6**

### Property 10: Tool invocation error handling
*For any* tool invocation that raises an exception, the tool must return a dictionary with 'success': False and 'error' key containing the error message, never propagating the exception to the agent.
**Validates: Requirements 5.5**

### Property 11: LangServe endpoint availability
*For any* registered agent (RENUS, ISA, Discovery), there must exist corresponding LangServe endpoints at /agents/{agent_name}/invoke and /agents/{agent_name}/stream that return 200 status for valid requests.
**Validates: Requirements 4.2**

### Property 12: Interview status transitions
*For any* interview, valid status transitions are: pending → in_progress → completed, or pending → in_progress → cancelled. No other transitions should be allowed.
**Validates: Requirements 3.1, 3.5**


## Error Handling

### Agent-Level Errors

1. **LLM API Failures**
   - Retry with exponential backoff (3 attempts)
   - Fall back to alternative model if available
   - Log error to LangSmith with full context
   - Return user-friendly error message

2. **Tool Execution Failures**
   - Catch all exceptions within tool
   - Return structured error response
   - Allow agent to decide next action
   - Never crash the agent

3. **State Management Errors**
   - Validate state at each graph node
   - Implement state recovery mechanisms
   - Log state transitions to LangSmith
   - Provide clear error messages

### System-Level Errors

1. **Database Connection Failures**
   - Implement connection pooling
   - Retry failed queries (3 attempts)
   - Circuit breaker pattern for sustained failures
   - Graceful degradation (read-only mode)

2. **Missing API Keys**
   - Fail fast at startup
   - Provide clear error messages with setup instructions
   - Validate all required keys on initialization

3. **WhatsApp Provider Errors**
   - Abstract provider errors into standard format
   - Implement fallback to SMS/Email
   - Queue failed messages for retry
   - Alert admins of sustained failures

### User-Facing Errors

1. **Invalid Input**
   - Validate input with Pydantic models
   - Return 400 with clear validation errors
   - Provide examples of correct format

2. **Permission Denied**
   - Return 403 with explanation
   - Log unauthorized access attempts
   - Never expose sensitive information in errors

3. **Resource Not Found**
   - Return 404 with helpful message
   - Suggest alternative actions
   - Log if pattern indicates bug

## Testing Strategy

### Unit Tests

**Agent Tests:**
- Test each agent's graph construction
- Test routing logic with various inputs
- Test system prompt effectiveness
- Mock LLM responses for deterministic tests

**Tool Tests:**
- Test each tool with valid inputs
- Test error handling with invalid inputs
- Test database operations with test database
- Mock external services (WhatsApp, Email)

**Model Tests:**
- Test Pydantic validation
- Test serialization/deserialization
- Test field constraints

### Integration Tests

**End-to-End Agent Flows:**
- Test complete RENUS routing flow
- Test ISA command execution
- Test Discovery interview completion
- Use test database with sample data

**LangServe API Tests:**
- Test all endpoints with various payloads
- Test streaming responses
- Test error responses
- Test authentication/authorization

**Database Integration:**
- Test RLS policies with different user roles
- Test multi-tenant isolation
- Test complex queries with joins

### Property-Based Tests

**Framework:** Use `hypothesis` library for Python

**Test Properties:**
- Property 1: RENUS routing consistency
- Property 3: Discovery field completeness
- Property 6: Multi-tenant isolation
- Property 8: WhatsApp interface compliance
- Property 12: Interview status transitions

**Configuration:**
- Minimum 100 iterations per property test
- Use custom generators for domain objects
- Tag each test with property number from design doc

### Manual Testing

**Agent Conversations:**
- Test RENUS with various conversation types
- Test ISA with all command types
- Test Discovery with complete interview flow
- Verify LangSmith traces are captured

**UI Testing:**
- Test sub-agent CRUD operations
- Test interview dashboard
- Test ISA chat interface
- Verify real-time updates

**Multi-Channel Testing:**
- Test WhatsApp webhook handling (when provider configured)
- Test web form submissions
- Verify message consistency across channels


## Configuration

### Environment Variables

```bash
# .env additions for Sprint 04

# AI Model APIs
OPENAI_API_KEY=sk-...                    # Required for GPT-4 models
ANTHROPIC_API_KEY=sk-ant-...             # Required for Claude models
GROQ_API_KEY=gsk_...                     # Optional for Llama/Mixtral
OPENROUTER_API_KEY=sk-or-...             # Optional fallback

# LangSmith (Observability) - REQUIRED
LANGSMITH_API_KEY=ls__...
LANGSMITH_PROJECT=renum-agents
LANGSMITH_ENVIRONMENT=development        # or 'production'
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com

# Agent Configuration
DEFAULT_RENUS_MODEL=gpt-4-turbo-preview
DEFAULT_ISA_MODEL=claude-3-5-sonnet-20241022
DEFAULT_DISCOVERY_MODEL=gpt-4o-mini

# WhatsApp Provider (to be configured later)
WHATSAPP_PROVIDER=none                   # none, uazapi, twilio, etc.
WHATSAPP_API_URL=
WHATSAPP_API_KEY=

# Email Provider (to be configured later)
EMAIL_PROVIDER=none                      # none, sendgrid, ses, smtp
EMAIL_API_KEY=
EMAIL_FROM_ADDRESS=

# LangServe
LANGSERVE_PORT=8001                      # Separate port from main API
LANGSERVE_HOST=0.0.0.0
```

### Settings Configuration

```python
# backend/src/config/settings.py (additions)

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # ... existing settings ...
    
    # AI Model APIs
    openai_api_key: str
    anthropic_api_key: str
    groq_api_key: Optional[str] = None
    openrouter_api_key: Optional[str] = None
    
    # LangSmith
    langsmith_api_key: str
    langsmith_project: str = "renum-agents"
    langsmith_environment: str = "development"
    langchain_tracing_v2: bool = True
    langchain_endpoint: str = "https://api.smith.langchain.com"
    
    # Agent Models
    default_renus_model: str = "gpt-4-turbo-preview"
    default_isa_model: str = "claude-3-5-sonnet-20241022"
    default_discovery_model: str = "gpt-4o-mini"
    
    # WhatsApp
    whatsapp_provider: str = "none"
    whatsapp_api_url: Optional[str] = None
    whatsapp_api_key: Optional[str] = None
    
    # Email
    email_provider: str = "none"
    email_api_key: Optional[str] = None
    email_from_address: Optional[str] = None
    
    # LangServe
    langserve_port: int = 8001
    langserve_host: str = "0.0.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def validate_ai_keys(self):
        """Validate required AI API keys are present"""
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required")
        if not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is required")
        if not self.langsmith_api_key:
            raise ValueError("LANGSMITH_API_KEY is required for observability")

settings = Settings()
settings.validate_ai_keys()
```

## Deployment Considerations

### Dependencies

```txt
# requirements.txt additions

# LangChain/LangGraph
langchain>=0.3.16
langchain-core>=0.3.63
langchain-community>=0.3.16
langchain-openai>=0.3.0
langchain-anthropic>=0.3.5
langchain-groq>=0.2.1
langgraph>=0.2.62
langgraph-checkpoint>=2.1.2
langserve[all]>=0.3.0

# LangSmith
langsmith>=0.1.0

# Additional
hypothesis>=6.100.0  # For property-based testing
```

### File Structure

```
backend/src/
├── agents/
│   ├── __init__.py
│   ├── base.py              # BaseAgent abstract class
│   ├── renus.py             # RENUS orchestrator
│   ├── isa.py               # ISA admin assistant
│   └── subagents/
│       ├── __init__.py
│       └── discovery.py     # Discovery interview agent
├── tools/
│   ├── __init__.py
│   ├── supabase_tool.py     # Database queries
│   ├── whatsapp_tool.py     # WhatsApp messaging
│   └── email_tool.py        # Email notifications
├── providers/
│   ├── __init__.py
│   └── whatsapp/
│       ├── __init__.py
│       ├── base.py          # WhatsAppProvider ABC
│       └── uazapi.py        # Future: Uazapi implementation
├── langserve/
│   ├── __init__.py
│   └── app.py               # LangServe FastAPI app
├── services/
│   ├── interview_service.py # Interview business logic
│   └── subagent_service.py  # Sub-agent management
└── api/routes/
    ├── agents.py            # Agent endpoints
    ├── interviews.py        # Interview endpoints
    └── subagents.py         # Sub-agent CRUD endpoints
```

### Performance Considerations

1. **LLM Response Streaming**
   - Use streaming for all user-facing responses
   - Implement proper error handling in streams
   - Buffer partial responses appropriately

2. **Database Query Optimization**
   - Use indexes on frequently queried fields
   - Implement pagination for large result sets
   - Cache frequently accessed data (Redis)

3. **Concurrent Request Handling**
   - Use async/await throughout
   - Implement request queuing for rate limits
   - Monitor and limit concurrent LLM calls

4. **LangSmith Overhead**
   - Tracing adds ~50-100ms per request
   - Acceptable for development
   - Consider sampling in production (e.g., 10%)

### Security Considerations

1. **API Key Management**
   - Never commit keys to git
   - Use environment variables
   - Rotate keys regularly
   - Monitor usage for anomalies

2. **RLS Enforcement**
   - Always use client_id filtering
   - Test multi-tenant isolation thoroughly
   - Audit admin access to bypass RLS

3. **Input Validation**
   - Validate all user inputs with Pydantic
   - Sanitize inputs before LLM calls
   - Prevent prompt injection attacks

4. **Rate Limiting**
   - Implement per-user rate limits
   - Protect against abuse
   - Monitor for unusual patterns

---

**Design Document Version:** 1.0  
**Last Updated:** 2025-11-29  
**Status:** Ready for Implementation
