"""
Orchestrator API Routes - Endpoints para gerenciar orquestração
Permite testar e monitorar o sistema de roteamento de sub-agentes
"""

from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from typing import Dict, Any, Optional
from pydantic import BaseModel

from src.services.orchestrator_service import get_orchestrator_service
from src.services.agent_service import get_agent_service
from src.utils.logger import logger


router = APIRouter(prefix="/api/orchestrator", tags=["Orchestrator"])


# ============================================================================
# Request/Response Models
# ============================================================================

class TestMessageRequest(BaseModel):
    """Request para testar orquestração"""
    message: str
    context: Optional[Dict[str, Any]] = {}


class AnalyzeRequest(BaseModel):
    """Request para análise de mensagem"""
    message: str
    context: Optional[Dict[str, Any]] = {}


class RouteRequest(BaseModel):
    """Request para roteamento"""
    message: str
    agent_id: str
    context: Optional[Dict[str, Any]] = {}


class AnalyzeResponse(BaseModel):
    """Response da análise"""
    topics: list
    confidence: float
    processing_time_ms: float


class RouteResponse(BaseModel):
    """Response do roteamento"""
    should_route: bool
    selected_subagent: Optional[str] = None
    routing_reason: str
    confidence: float


class OrchestrationResponse(BaseModel):
    """Response da orquestração"""
    message: str
    delegated: bool
    sub_agent_id: Optional[str] = None
    sub_agent_name: Optional[str] = None
    main_agent: Optional[str] = None
    topics_identified: Optional[list] = []
    processing_time_ms: Optional[float] = None
    timestamp: str


class OrchestrationStatsResponse(BaseModel):
    """Estatísticas de orquestração"""
    agent_id: str
    total_sub_agents: int
    active_sub_agents: int
    orchestration_enabled: bool
    sub_agents: list
    last_updated: str


# ============================================================================
# Routes
# ============================================================================

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_message(request: AnalyzeRequest):
    """
    Analisa uma mensagem e identifica tópicos
    Endpoint usado pelos scripts de validação
    """
    try:
        orchestrator = get_orchestrator_service()
        
        import time
        start_time = time.time()
        
        # Analisar tópicos
        topics = await orchestrator.topic_analyzer.analyze_topics(request.message)
        
        processing_time = (time.time() - start_time) * 1000
        
        # Calcular confidence baseado no número de tópicos encontrados
        confidence = min(len(topics) * 0.3, 1.0) if topics else 0.1
        
        return AnalyzeResponse(
            topics=topics,
            confidence=confidence,
            processing_time_ms=round(processing_time, 2)
        )
        
    except Exception as e:
        logger.error(f"Error analyzing message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/route", response_model=RouteResponse)
async def route_message(request: RouteRequest):
    """
    Determina se uma mensagem deve ser roteada para sub-agente
    Endpoint usado pelos scripts de validação
    """
    try:
        orchestrator = get_orchestrator_service()
        
        # Converter agent_id para UUID
        try:
            agent_uuid = UUID(request.agent_id)
        except ValueError:
            # Se não for UUID válido, usar um UUID de teste
            from uuid import uuid4
            agent_uuid = uuid4()
        
        # Analisar tópicos
        topics = await orchestrator.topic_analyzer.analyze_topics(request.message)
        
        # Buscar melhor match
        best_match = await orchestrator.sub_agent_matcher.find_best_match(agent_uuid, topics)
        
        should_route = best_match is not None
        selected_subagent = best_match['name'] if best_match else None
        
        # Determinar razão do roteamento
        if should_route:
            routing_reason = f"Matched topics: {topics} with sub-agent: {selected_subagent}"
            confidence = 0.8
        else:
            routing_reason = f"No sub-agent found for topics: {topics}"
            confidence = 0.2
        
        return RouteResponse(
            should_route=should_route,
            selected_subagent=selected_subagent,
            routing_reason=routing_reason,
            confidence=confidence
        )
        
    except Exception as e:
        logger.error(f"Error routing message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agents/{agent_id}/test")
async def test_orchestration(
    agent_id: UUID,
    request: TestMessageRequest
):
    """
    Testa orquestração para um agente específico
    Útil para debug e validação do roteamento
    """
    try:
        orchestrator = get_orchestrator_service()
        
        # Verificar se agente existe
        agent_service = get_agent_service()
        agent = await agent_service.get_agent(agent_id)
        
        if not agent:
            raise HTTPException(status_code=404, detail="Agente não encontrado")
        
        # Simular conversation_id para teste
        from uuid import uuid4
        test_conversation_id = uuid4()
        
        # Processar mensagem
        import time
        start_time = time.time()
        
        result = await orchestrator.process_message(
            agent_id=agent_id,
            message=request.message,
            conversation_id=test_conversation_id,
            context=request.context
        )
        
        processing_time = (time.time() - start_time) * 1000
        
        # Analisar tópicos separadamente para debug
        topics = await orchestrator.topic_analyzer.analyze_topics(request.message)
        
        return OrchestrationResponse(
            message=result['message'],
            delegated=result.get('delegated', False),
            sub_agent_id=result.get('sub_agent_id'),
            sub_agent_name=result.get('sub_agent_name'),
            main_agent=result.get('main_agent'),
            topics_identified=topics,
            processing_time_ms=round(processing_time, 2),
            timestamp=result['timestamp']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error testing orchestration: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/{agent_id}/stats")
async def get_orchestration_stats(agent_id: UUID):
    """
    Retorna estatísticas de orquestração para um agente
    """
    try:
        orchestrator = get_orchestrator_service()
        stats = await orchestrator.get_orchestration_stats(agent_id)
        
        return OrchestrationStatsResponse(**stats)
        
    except Exception as e:
        logger.error(f"Error getting orchestration stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agents/{agent_id}/enable")
async def enable_orchestration(agent_id: UUID):
    """
    Habilita orquestração para um agente
    Adiciona orchestrator_enabled: true na configuração
    """
    try:
        agent_service = get_agent_service()
        
        # Buscar agente atual
        agent = await agent_service.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agente não encontrado")
        
        # Atualizar configuração
        config = agent.config or {}
        config['orchestrator_enabled'] = True
        
        # Salvar
        await agent_service.update_agent(agent_id, {'config': config})
        
        return {
            "message": f"Orquestração habilitada para {agent.name}",
            "agent_id": str(agent_id),
            "orchestrator_enabled": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enabling orchestration: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agents/{agent_id}/disable")
async def disable_orchestration(agent_id: UUID):
    """
    Desabilita orquestração para um agente
    Remove orchestrator_enabled da configuração
    """
    try:
        agent_service = get_agent_service()
        
        # Buscar agente atual
        agent = await agent_service.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agente não encontrado")
        
        # Atualizar configuração
        config = agent.config or {}
        config['orchestrator_enabled'] = False
        
        # Salvar
        await agent_service.update_agent(agent_id, {'config': config})
        
        return {
            "message": f"Orquestração desabilitada para {agent.name}",
            "agent_id": str(agent_id),
            "orchestrator_enabled": False
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error disabling orchestration: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/{agent_id}/sub-agents/matches")
async def test_sub_agent_matching(
    agent_id: UUID,
    message: str
):
    """
    Testa matching de sub-agentes para uma mensagem específica
    Útil para debug do algoritmo de seleção
    """
    try:
        orchestrator = get_orchestrator_service()
        
        # Analisar tópicos
        topics = await orchestrator.topic_analyzer.analyze_topics(message)
        
        # Buscar matches
        best_match = await orchestrator.sub_agent_matcher.find_best_match(agent_id, topics)
        
        # Buscar todos os sub-agentes para comparação
        all_sub_agents = orchestrator.supabase.table('sub_agents')\
            .select('*')\
            .eq('parent_agent_id', str(agent_id))\
            .eq('is_active', True)\
            .execute()
        
        # Calcular scores para todos
        scores = []
        for sub_agent in all_sub_agents.data:
            score = orchestrator.sub_agent_matcher._calculate_match_score(topics, sub_agent)
            scores.append({
                'sub_agent_id': sub_agent['id'],
                'sub_agent_name': sub_agent['name'],
                'score': round(score, 3),
                'topics': sub_agent.get('config', {}).get('topics', []),
                'selected': sub_agent['id'] == (best_match['id'] if best_match else None)
            })
        
        # Ordenar por score
        scores.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'message': message,
            'topics_identified': topics,
            'best_match': {
                'sub_agent_id': best_match['id'] if best_match else None,
                'sub_agent_name': best_match['name'] if best_match else None,
                'score': scores[0]['score'] if scores else 0.0
            },
            'all_scores': scores,
            'threshold': 0.3,
            'would_delegate': best_match is not None
        }
        
    except Exception as e:
        logger.error(f"Error testing sub-agent matching: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def orchestrator_health():
    """
    Health check do sistema de orquestração
    """
    try:
        orchestrator = get_orchestrator_service()
        
        # Testar componentes básicos
        health_status = {
            'orchestrator_service': True,
            'topic_analyzer': True,
            'sub_agent_matcher': True,
            'delegation_manager': True,
            'supabase_connection': False,
            'openrouter_connection': False
        }
        
        # Testar Supabase
        try:
            result = orchestrator.supabase.table('agents').select('id').limit(1).execute()
            health_status['supabase_connection'] = True
        except:
            health_status['supabase_connection'] = False
        
        # Testar OpenRouter (mock sempre funciona)
        try:
            test_response = await orchestrator.topic_analyzer.openrouter.chat_completion(
                messages=[{"role": "user", "content": "test"}],
                model="gpt-4o-mini",
                max_tokens=10
            )
            health_status['openrouter_connection'] = True
        except:
            health_status['openrouter_connection'] = False
        
        all_healthy = all(health_status.values())
        
        return {
            'status': 'healthy' if all_healthy else 'degraded',
            'components': health_status,
            'timestamp': orchestrator.supabase.table('agents').select('created_at').limit(1).execute().data[0]['created_at'] if health_status['supabase_connection'] else None
        }
        
    except Exception as e:
        logger.error(f"Error in orchestrator health check: {e}")
        return {
            'status': 'unhealthy',
            'error': str(e),
            'components': {k: False for k in ['orchestrator_service', 'topic_analyzer', 'sub_agent_matcher', 'delegation_manager', 'supabase_connection', 'openrouter_connection']}
        }