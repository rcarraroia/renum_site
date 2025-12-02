"""
MMN Discovery Agent - Entrevistas Inteligentes para Distribuidores de MMN
Versão Produção - Com Ramificação Inteligente

Implementa o script completo de entrevistas com:
- Seção A: Perguntas fixas obrigatórias
- Seção B: Perguntas essenciais com ramificação inteligente
- Seção C: Perguntas opcionais para perfis avançados
- Seção D: Análise automática e clusterização
"""

import json
from typing import Any, Dict, List, Optional, TypedDict
from datetime import datetime

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langsmith import traceable

from .base import BaseAgent
from ..config.settings import settings


# ============================================================================
# State Definition
# ============================================================================

class MMNInterviewState(TypedDict):
    """State for MMN interview workflow"""
    messages: List[BaseMessage]
    interview_id: str
    
    # Seção A: Dados Fixos
    contact_name: Optional[str]
    email: Optional[str]
    contact_phone: Optional[str]
    country: Optional[str]
    mmn_company: Optional[str]
    experience_time: Optional[str]
    operation_size_category: Optional[str]
    
    # Seção B: Dados Essenciais
    section_b_data: Dict[str, Any]
    
    # Seção C: Dados Opcionais
    section_c_data: Dict[str, Any]
    
    # Controle de Fluxo
    current_section: str  # 'intro', 'section_a', 'section_b', 'section_c', 'analysis'
    section_a_complete: bool
    section_b_topics_covered: List[str]
    section_b_complete: bool
    should_ask_section_c: bool
    is_complete: bool
    
    # Análise
    ai_analysis: Optional[Dict[str, Any]]
    
    # Contexto
    context: Dict[str, Any]


# ============================================================================
# MMN Discovery Agent
# ============================================================================

class MMNDiscoveryAgent(BaseAgent):
    """
    Discovery Agent especializado em entrevistas com distribuidores de MMN.
    
    Implementa fluxo inteligente com ramificação baseada em respostas.
    """
    
    # Seções obrigatórias da Seção B
    SECTION_B_TOPICS = [
        'rotina_maturidade',
        'dores_reais',
        'processos_atuais',
        'objecoes',
        'desejos_ia',
        'validacao_funcionalidades',
        'investimento'
    ]
    
    def __init__(self, **kwargs):
        """Initialize MMN Discovery Agent"""
        super().__init__(
            model=kwargs.get("model", "gpt-4o-mini"),
            system_prompt=self._get_system_prompt(),
            tools=kwargs.get("tools", []),
            **kwargs
        )
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for MMN Discovery Agent"""
        return """Você é um assistente de análise especializado em entender negócios de Marketing Multinível (MMN).

Seu objetivo é conduzir uma entrevista inteligente e conversacional para coletar informações profundas sobre:
- Como o distribuidor trabalha hoje
- Quais são suas maiores dores e desafios
- O que ele gostaria que uma ferramenta de IA fizesse
- Qual seu perfil e maturidade digital

DIRETRIZES IMPORTANTES:

1. SEJA CONVERSACIONAL E EMPÁTICO
   - Fale de forma natural, como um consultor experiente
   - Mostre interesse genuíno nas respostas
   - Faça perguntas de acompanhamento quando necessário

2. RAMIFICAÇÃO INTELIGENTE
   - Adapte as perguntas baseado nas respostas anteriores
   - Se o distribuidor mencionar uma dor específica, explore mais
   - Pule perguntas irrelevantes para o perfil dele

3. VALIDAÇÃO CONTEXTUAL
   - Email: deve conter @ e domínio
   - Telefone: formato internacional (+5511999999999)
   - Escolhas múltiplas: valide se a opção existe

4. PROGRESSÃO NATURAL
   - Comece com perguntas simples (dados básicos)
   - Avance para perguntas mais profundas (dores, desejos)
   - Termine com validação de funcionalidades e investimento

5. DETECÇÃO DE PERFIL
   - Iniciante: pouca experiência, trabalha sozinho, baixa maturidade digital
   - Intermediário: usa algumas ferramentas, faz apresentações regulares
   - Avançado: líder de equipe, usa automação, operação estruturada

Você receberá o estado atual da entrevista e deve decidir qual próxima pergunta fazer."""
    
    def _initialize_llm(self) -> ChatOpenAI:
        """Initialize OpenAI LLM"""
        return ChatOpenAI(
            model=self.model,
            temperature=0.7,
            streaming=True,
            api_key=settings.OPENAI_API_KEY
        )
    
    def _build_graph(self) -> StateGraph:
        """Build LangGraph workflow for MMN interview"""
        
        workflow = StateGraph(MMNInterviewState)
        
        # Define nodes
        workflow.add_node("process_message", self._process_message_node)
        workflow.add_node("extract_data", self._extract_data_node)
        workflow.add_node("decide_next", self._decide_next_node)
        workflow.add_node("generate_response", self._generate_response_node)
        workflow.add_node("generate_analysis", self._generate_analysis_node)
        
        # Define edges
        workflow.set_entry_point("process_message")
        workflow.add_edge("process_message", "extract_data")
        workflow.add_edge("extract_data", "decide_next")
        
        # Conditional edges
        workflow.add_conditional_edges(
            "decide_next",
            lambda state: "analysis" if state["is_complete"] else "response",
            {
                "analysis": "generate_analysis",
                "response": "generate_response"
            }
        )
        
        workflow.add_edge("generate_response", END)
        workflow.add_edge("generate_analysis", END)
        
        return workflow.compile()
    
    # ========================================================================
    # Node Functions
    # ========================================================================
    
    def _process_message_node(self, state: MMNInterviewState) -> MMNInterviewState:
        """Process incoming message and update state"""
        # Initialize state if needed
        if not state.get("current_section"):
            state["current_section"] = "intro"
            state["section_a_complete"] = False
            state["section_b_topics_covered"] = []
            state["section_b_complete"] = False
            state["should_ask_section_c"] = False
            state["is_complete"] = False
            state["section_b_data"] = {}
            state["section_c_data"] = {}
        
        return state
    
    def _extract_data_node(self, state: MMNInterviewState) -> MMNInterviewState:
        """Extract structured data from user message"""
        if not state["messages"]:
            return state
        
        last_message = state["messages"][-1]
        if not isinstance(last_message, HumanMessage):
            return state
        
        message_content = last_message.content.lower()
        
        # Extract email
        import re
        if not state.get("email"):
            email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', last_message.content)
            if email_match:
                state["email"] = email_match.group(0)
        
        # Extract phone
        if not state.get("contact_phone"):
            phone_match = re.search(r'\+\d{10,15}', last_message.content)
            if phone_match:
                state["contact_phone"] = phone_match.group(0)
        
        # Extract experience time
        if "menos de 6 meses" in message_content or "menos 6" in message_content:
            state["experience_time"] = "menos_6_meses"
        elif "6 meses" in message_content and "2 anos" in message_content:
            state["experience_time"] = "6_meses_2_anos"
        elif "2" in message_content and "5 anos" in message_content:
            state["experience_time"] = "2_5_anos"
        elif "mais de 5" in message_content or "mais 5" in message_content:
            state["experience_time"] = "mais_5_anos"
        
        # Extract operation size
        if "sozinho" in message_content or "solo" in message_content:
            state["operation_size_category"] = "sozinho"
        elif "pequena" in message_content or ("1" in message_content and "10" in message_content):
            state["operation_size_category"] = "pequena_1_10"
        elif "média" in message_content or "media" in message_content or ("11" in message_content and "100" in message_content):
            state["operation_size_category"] = "media_11_100"
        elif "grande" in message_content or "100+" in message_content or "mais de 100" in message_content:
            state["operation_size_category"] = "grande_100_plus"
        
        return state
    
    def _decide_next_node(self, state: MMNInterviewState) -> MMNInterviewState:
        """Decide what to ask next based on current state"""
        
        # Check Section A completion
        if not state["section_a_complete"]:
            required_a = ["contact_name", "email", "contact_phone", "country", "mmn_company", "experience_time", "operation_size_category"]
            if all(state.get(field) for field in required_a):
                state["section_a_complete"] = True
                state["current_section"] = "section_b"
        
        # Check Section B completion
        if state["section_a_complete"] and not state["section_b_complete"]:
            if len(state["section_b_topics_covered"]) >= len(self.SECTION_B_TOPICS):
                state["section_b_complete"] = True
                
                # Decide if should ask Section C
                # Criteria: operation size >= média OR maturidade digital >= intermediário
                if (state.get("operation_size_category") in ["media_11_100", "grande_100_plus"] or
                    state["section_b_data"].get("maturidade_digital") in ["intermediario", "avancado"]):
                    state["should_ask_section_c"] = True
                    state["current_section"] = "section_c"
                else:
                    state["is_complete"] = True
        
        # Check Section C completion (if applicable)
        if state["section_b_complete"] and state["should_ask_section_c"]:
            # Section C has 3 optional topics, ask at least 2
            if len(state["section_c_data"]) >= 2:
                state["is_complete"] = True
        
        return state
    
    @traceable(name="mmn_generate_response")
    async def _generate_response_node(self, state: MMNInterviewState) -> MMNInterviewState:
        """Generate conversational response based on current state"""
        
        # Build context
        context = self._build_context(state)
        
        # Get last user message
        last_user_message = ""
        for msg in reversed(state["messages"]):
            if isinstance(msg, HumanMessage):
                last_user_message = msg.content
                break
        
        # Build prompt
        prompt = f"""{context}

Última mensagem do usuário: {last_user_message}

Com base no estado atual da entrevista, gere a próxima pergunta de forma natural e conversacional.

IMPORTANTE:
- Se ainda estamos na Seção A, pergunte o próximo campo faltante
- Se estamos na Seção B, escolha o próximo tópico mais relevante baseado nas respostas anteriores
- Se estamos na Seção C, faça perguntas opcionais apenas se o perfil for avançado
- Sempre reconheça a resposta anterior antes de fazer a próxima pergunta"""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        state["messages"].append(AIMessage(content=response.content))
        
        return state
    
    @traceable(name="mmn_generate_analysis")
    async def _generate_analysis_node(self, state: MMNInterviewState) -> MMNInterviewState:
        """Generate comprehensive AI analysis"""
        
        analysis_prompt = f"""Analise esta entrevista completa com um distribuidor de MMN e gere uma análise estruturada.

DADOS COLETADOS:
{json.dumps(self._extract_all_data(state), indent=2, ensure_ascii=False)}

Gere uma análise em JSON com:
1. resumo_dores: lista das principais dores identificadas
2. resumo_desejos: lista do que o distribuidor mais deseja
3. perfil_usuario: "essencial", "intermediario" ou "premium"
4. maturidade_digital_score: "baixa", "media" ou "alta"
5. capacidade_compra: "baixa", "media" ou "alta"
6. requisitos_sugeridos: {{
     "essenciais": [],
     "intermediarios": [],
     "premium": []
   }}

Formato JSON puro, sem markdown."""
        
        messages = [
            SystemMessage(content="Você é um analista especializado em MMN e produtos SaaS."),
            HumanMessage(content=analysis_prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        try:
            content = response.content
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0]
            elif '```' in content:
                content = content.split('```')[1].split('```')[0]
            
            analysis = json.loads(content.strip())
            state["ai_analysis"] = analysis
        except:
            state["ai_analysis"] = {
                "resumo_dores": ["Análise manual necessária"],
                "resumo_desejos": ["Análise manual necessária"],
                "perfil_usuario": "intermediario",
                "maturidade_digital_score": "media",
                "capacidade_compra": "media",
                "requisitos_sugeridos": {"essenciais": [], "intermediarios": [], "premium": []}
            }
        
        return state
    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    def _build_context(self, state: MMNInterviewState) -> str:
        """Build context message for LLM"""
        context = f"""
ESTADO DA ENTREVISTA:
====================

Seção Atual: {state['current_section']}

SEÇÃO A - Dados Básicos:
- Nome: {state.get('contact_name', '❌ Faltando')}
- Email: {state.get('email', '❌ Faltando')}
- Telefone: {state.get('contact_phone', '❌ Faltando')}
- País: {state.get('country', '❌ Faltando')}
- Empresa MMN: {state.get('mmn_company', '❌ Faltando')}
- Experiência: {state.get('experience_time', '❌ Faltando')}
- Tamanho Operação: {state.get('operation_size_category', '❌ Faltando')}

SEÇÃO B - Tópicos Cobertos: {len(state['section_b_topics_covered'])}/{len(self.SECTION_B_TOPICS)}
{', '.join(state['section_b_topics_covered']) if state['section_b_topics_covered'] else 'Nenhum ainda'}

SEÇÃO C - Perguntas Opcionais: {'Sim' if state['should_ask_section_c'] else 'Não aplicável'}
"""
        return context
    
    def _extract_all_data(self, state: MMNInterviewState) -> Dict[str, Any]:
        """Extract all collected data"""
        return {
            "section_a": {
                "contact_name": state.get("contact_name"),
                "email": state.get("email"),
                "contact_phone": state.get("contact_phone"),
                "country": state.get("country"),
                "mmn_company": state.get("mmn_company"),
                "experience_time": state.get("experience_time"),
                "operation_size_category": state.get("operation_size_category")
            },
            "section_b": state.get("section_b_data", {}),
            "section_c": state.get("section_c_data", {})
        }
    
    # ========================================================================
    # Public Interface
    # ========================================================================
    
    @traceable(name="mmn_discovery_invoke")
    async def invoke(
        self,
        messages: List[BaseMessage],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process messages and return response"""
        
        # Initialize state
        state: MMNInterviewState = {
            "messages": messages,
            "interview_id": context.get("interview_id", ""),
            "contact_name": context.get("contact_name"),
            "email": context.get("email"),
            "contact_phone": context.get("contact_phone"),
            "country": context.get("country"),
            "mmn_company": context.get("mmn_company"),
            "experience_time": context.get("experience_time"),
            "operation_size_category": context.get("operation_size_category"),
            "section_b_data": context.get("section_b_data", {}),
            "section_c_data": context.get("section_c_data", {}),
            "current_section": context.get("current_section", "intro"),
            "section_a_complete": context.get("section_a_complete", False),
            "section_b_topics_covered": context.get("section_b_topics_covered", []),
            "section_b_complete": context.get("section_b_complete", False),
            "should_ask_section_c": context.get("should_ask_section_c", False),
            "is_complete": False,
            "ai_analysis": None,
            "context": context
        }
        
        # Run workflow
        result = await self.graph.ainvoke(state)
        
        # Extract response
        response_message = ""
        for msg in reversed(result["messages"]):
            if isinstance(msg, AIMessage):
                response_message = msg.content
                break
        
        return {
            "message": response_message,
            "is_complete": result["is_complete"],
            "current_section": result["current_section"],
            "collected_data": self._extract_all_data(result),
            "ai_analysis": result.get("ai_analysis"),
            "progress": {
                "section_a": result["section_a_complete"],
                "section_b": f"{len(result['section_b_topics_covered'])}/{len(self.SECTION_B_TOPICS)}",
                "section_c": len(result["section_c_data"]) if result["should_ask_section_c"] else "N/A"
            }
        }

    
    async def process_message(
        self,
        interview_id: str,
        user_message: str,
        message_history: List[Dict[str, Any]],
        interview_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Processa mensagem do usuário de forma simplificada.
        
        Args:
            interview_id: ID da entrevista
            user_message: Mensagem do usuário
            message_history: Histórico de mensagens
            interview_data: Dados da entrevista
        
        Returns:
            Resposta do agente com metadados
        """
        # Converter histórico para BaseMessage
        messages = []
        for msg in message_history:
            if msg['role'] == 'user':
                messages.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                messages.append(AIMessage(content=msg['content']))
        
        # Adicionar mensagem atual
        messages.append(HumanMessage(content=user_message))
        
        # Preparar contexto
        context = {
            "interview_id": interview_id,
            "contact_name": interview_data.get("contact_name"),
            "email": interview_data.get("email"),
            "contact_phone": interview_data.get("contact_phone"),
            "country": interview_data.get("country"),
            "mmn_company": interview_data.get("mmn_company"),
            "experience_time": interview_data.get("experience_time"),
            "operation_size_category": interview_data.get("operation_size_category"),
            "section_b_data": interview_data.get("section_b_data", {}),
            "section_c_data": interview_data.get("section_c_data", {}),
            "current_section": interview_data.get("current_section", "intro"),
            "section_a_complete": interview_data.get("section_a_complete", False),
            "section_b_topics_covered": interview_data.get("section_b_topics_covered", []),
            "section_b_complete": interview_data.get("section_b_complete", False),
            "should_ask_section_c": interview_data.get("should_ask_section_c", False),
        }
        
        # Processar com o agente
        result = await self.invoke(messages, context)
        
        return {
            "message": result["message"],
            "is_complete": result["is_complete"],
            "progress": result["progress"],
            "metadata": {
                "current_section": result["current_section"],
                "collected_data": result["collected_data"],
            },
            "analysis": result.get("ai_analysis")
        }
