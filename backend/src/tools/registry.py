from typing import List, Any, Dict
from langchain.tools import BaseTool
from langchain_core.tools import tool
from .email_tool import get_email_tool
from .whatsapp_tool import get_whatsapp_tools
from .supabase_tool import create_supabase_tool
from .knowledge_tool import KnowledgeBaseTool
from .google_tool import get_google_tools
from .chatwoot_tool import get_chatwoot_tools

# Maps tool key to a factory function that returns one or more tools
TOOL_FACTORIES = {
    "email_sender": lambda client_id=None, agent_id=None: [get_email_tool(client_id)],
    "whatsapp_suite": lambda client_id=None, agent_id=None: get_whatsapp_tools(client_id=client_id),
    "database_tools": lambda client_id=None, agent_id=None: [create_supabase_tool(client_id)],
    "knowledge_base": lambda client_id=None, agent_id=None: [KnowledgeBaseTool(agent_id=agent_id)] if agent_id else [],
    "google_suite": lambda client_id=None, agent_id=None: get_google_tools(client_id=client_id, agent_id=agent_id),
    "chatwoot_handoff": lambda client_id=None, agent_id=None: get_chatwoot_tools(client_id=client_id, agent_id=agent_id)
}

AVAILABLE_TOOLS_METADATA = [
    {
        "key": "email_sender",
        "name": "Envio de Email (Legacy)",
        "description": "Permite ao agente enviar emails via SMTP/SendGrid.",
        "icon": "Mail" 
    },
    {
        "key": "whatsapp_suite",
        "name": "WhatsApp (Mensagens e Mídia)",
        "description": "Permite enviar mensagens de texto e mídia pelo WhatsApp.",
        "icon": "MessageCircle"
    },
    {
        "key": "google_suite",
        "name": "Google Workspace (Gmail, Calendar, Drive)",
        "description": "Permite enviar emails pelo Gmail, listar eventos na Agenda e buscar arquivos no Drive.",
        "icon": "Mail"
    },
    {
        "key": "chatwoot_handoff",
        "name": "Transbordo Humano (Chatwoot)",
        "description": "Permite transferir o atendimento para um humano no Chatwoot.",
        "icon": "MessageCircle"
    },
    {
        "key": "database_tools",
        "name": "Consultas Banco de Dados (Supabase)",
        "description": "Permite consultar dados de clientes e projetos no banco de dados do cliente.",
        "icon": "Database"
    },
    {
        "key": "knowledge_base",
        "name": "Base de Conhecimento (RAG)",
        "description": "Permite ao agente consultar documentos e manuais enviados.",
        "icon": "BookOpen"
    }
]

from .subagent_tool import create_subagent_tool
from src.config.supabase import supabase_admin
# We need to import InterviewService lazily or handle it to avoid circular deps if any
# But here we can pass it instance or class.
# For simplicity, we'll instantiate a service wrapper or use the Import inside function
 
def _fetch_subagents(client_id: str) -> List[Dict]:
    """Fetch active sub-agents for the client."""
    if not client_id:
        return []
    try:
        response = supabase_admin.table('agents')\
            .select('id, name, description, role')\
            .eq('client_id', client_id)\
            .eq('role', 'sub_agent')\
            .execute()
        return response.data or []
    except Exception as e:
        print(f"Error fetching subagents: {e}")
        return []

def get_tools_by_names(names: List[str], client_id: Any = None, agent_id: Any = None, interview_service: Any = None) -> List[BaseTool]:
    """
    Returns a flattened list of tools based on the requested names (keys).
    
    Args:
        names: List of tool keys
        client_id: Client ID (UUID)
        agent_id: Agent ID (UUID) for agent-specific tools (like RAG)
        interview_service: Optional instance of InterviewService (for subagents)
        
    Returns:
        List of initialized LangChain tools
    """
    tools = []
    
    # 1. Standard Factory Tools
    for name in names:
        factory = TOOL_FACTORIES.get(name)
        if factory:
            try:
                result = factory(client_id=client_id, agent_id=agent_id)
                if isinstance(result, list):
                    tools.extend(result)
                else:
                    tools.append(result)
            except Exception as e:
                # ENHANCED LOGGING: Show exactly which tool failed and why
                print(f"[REGISTRY ERROR] Failed to load tool '{name}': {type(e).__name__}: {e}")
                # Continue to next tool (graceful degradation)
                continue
    
    # 2. Dynamic Sub-Agent Tools (Automatically added if client_id is present)
    # Only if interview_service is provided to avoid circular imports
    if client_id and interview_service:
        subagents = _fetch_subagents(str(client_id))
        
        current_interview_id = "UNKNOWN_INTERVIEW_ID" 
        
        for sub in subagents:
            # Create tool for each sub-agent
            try:
                tool = create_subagent_tool(
                    subagent_id=str(sub['id']),
                    subagent_name=sub['name'],
                    subagent_description=sub.get('description', ''),
                    interview_service=interview_service,
                    interview_id=current_interview_id 
                )
                tools.append(tool)
            except Exception as e:
                print(f"Error creating tool for subagent {sub['name']}: {e}")
    
    return tools
