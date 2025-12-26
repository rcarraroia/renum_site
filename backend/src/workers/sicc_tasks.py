"""
SICC Tasks - Celery Tasks for SICC Processing
Sprint SICC Multi-Agente

Tasks para processamento assíncrono do SICC:
1. Consolidação de aprendizados
2. Análise de padrões
3. Geração de snapshots
4. Limpeza de dados antigos
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any
from uuid import uuid4

from celery import shared_task
from celery.utils.log import get_task_logger

from .celery_app import celery_app

logger = get_task_logger(__name__)


@celery_app.task(
    name='src.workers.sicc_tasks.consolidate_learnings',
    bind=True,
    max_retries=3,
    default_retry_delay=60
)
def consolidate_learnings(self, agent_id: str = None) -> Dict[str, Any]:
    """
    Consolida aprendizados pendentes em memórias aprovadas.
    
    Executa periodicamente (a cada 5 minutos) ou sob demanda.
    
    Args:
        agent_id: Se fornecido, consolida apenas para este agente.
                  Se None, consolida para TODOS os agentes.
    
    Returns:
        Dict com estatísticas de consolidação
    """
    logger.info(f"🧠 SICC: Starting learning consolidation | agent_id={agent_id or 'ALL'}")
    
    try:
        from ..config.supabase import supabase_admin
        
        # Buscar aprendizados aprovados não consolidados
        query = supabase_admin.table("learning_logs")\
            .select("*")\
            .eq("status", "approved")\
            .is_("consolidated_at", "null")
        
        if agent_id:
            query = query.eq("agent_id", agent_id)
        
        result = query.limit(50).execute()
        learnings = result.data or []
        
        if not learnings:
            logger.info("🧠 SICC: No learnings to consolidate")
            return {"consolidated": 0, "errors": 0}
        
        consolidated = 0
        errors = 0
        
        for learning in learnings:
            try:
                # Criar memory_chunk a partir do learning
                memory_data = {
                    "id": str(uuid4()),
                    "agent_id": learning["agent_id"],
                    "content": learning.get("content", ""),
                    "chunk_type": "learning",
                    "source": f"learning_log:{learning['id']}",
                    "metadata": {
                        "learning_type": learning.get("learning_type"),
                        "original_context": learning.get("context"),
                        "consolidated_at": datetime.utcnow().isoformat()
                    },
                    "confidence_score": learning.get("confidence_score", 0.8),
                    "created_at": datetime.utcnow().isoformat()
                }
                
                # Inserir memória
                supabase_admin.table("memory_chunks").insert(memory_data).execute()
                
                # Marcar learning como consolidado
                supabase_admin.table("learning_logs")\
                    .update({"consolidated_at": datetime.utcnow().isoformat()})\
                    .eq("id", learning["id"])\
                    .execute()
                
                consolidated += 1
                
            except Exception as e:
                logger.error(f"🧠 SICC: Error consolidating learning {learning['id']}: {e}")
                errors += 1
        
        logger.info(f"🧠 SICC: Consolidation complete | consolidated={consolidated} | errors={errors}")
        
        return {
            "consolidated": consolidated,
            "errors": errors,
            "agent_id": agent_id
        }
        
    except Exception as e:
        logger.error(f"🧠 SICC: Consolidation failed: {e}")
        raise self.retry(exc=e)


@celery_app.task(
    name='src.workers.sicc_tasks.analyze_patterns',
    bind=True,
    max_retries=3
)
def analyze_patterns(self, agent_id: str = None) -> Dict[str, Any]:
    """
    Analisa padrões de comportamento nos dados do SICC.
    
    Executa periodicamente (a cada 15 minutos).
    
    Args:
        agent_id: Se fornecido, analisa apenas para este agente.
    
    Returns:
        Dict com padrões detectados
    """
    logger.info(f"🧠 SICC: Starting pattern analysis | agent_id={agent_id or 'ALL'}")
    
    try:
        from ..config.supabase import supabase_admin
        
        # Buscar memórias recentes para análise
        query = supabase_admin.table("memory_chunks")\
            .select("*")\
            .gte("created_at", (datetime.utcnow() - timedelta(hours=24)).isoformat())
        
        if agent_id:
            query = query.eq("agent_id", agent_id)
        
        result = query.limit(100).execute()
        memories = result.data or []
        
        if not memories:
            logger.info("🧠 SICC: No recent memories to analyze")
            return {"patterns_found": 0}
        
        # Agrupar por agent_id
        by_agent = {}
        for mem in memories:
            aid = mem.get("agent_id")
            if aid not in by_agent:
                by_agent[aid] = []
            by_agent[aid].append(mem)
        
        patterns_found = 0
        
        for aid, agent_memories in by_agent.items():
            # Análise simples: detectar tópicos frequentes
            # (Em produção, usaria embeddings e clustering)
            
            if len(agent_memories) >= 3:
                # Criar padrão se não existir
                pattern_data = {
                    "id": str(uuid4()),
                    "agent_id": aid,
                    "pattern_name": f"frequent_topic_{datetime.utcnow().strftime('%Y%m%d')}",
                    "pattern_type": "topic_frequency",
                    "trigger_condition": "auto_detected",
                    "response_template": None,
                    "occurrence_count": len(agent_memories),
                    "confidence_score": 0.6,
                    "metadata": {
                        "memory_ids": [m["id"] for m in agent_memories[:5]],
                        "detected_at": datetime.utcnow().isoformat()
                    },
                    "created_at": datetime.utcnow().isoformat()
                }
                
                try:
                    supabase_admin.table("behavior_patterns").insert(pattern_data).execute()
                    patterns_found += 1
                except Exception as e:
                    logger.warning(f"🧠 SICC: Could not create pattern: {e}")
        
        logger.info(f"🧠 SICC: Pattern analysis complete | patterns_found={patterns_found}")
        
        return {
            "patterns_found": patterns_found,
            "agents_analyzed": len(by_agent)
        }
        
    except Exception as e:
        logger.error(f"🧠 SICC: Pattern analysis failed: {e}")
        raise self.retry(exc=e)


@celery_app.task(
    name='src.workers.sicc_tasks.create_snapshot',
    bind=True,
    max_retries=3
)
def create_snapshot(self, agent_id: str) -> Dict[str, Any]:
    """
    Cria um snapshot do estado atual do agente.
    
    Chamado quando há mudanças significativas ou periodicamente.
    
    Args:
        agent_id: UUID do agente
    
    Returns:
        Dict com ID do snapshot criado
    """
    logger.info(f"🧠 SICC: Creating snapshot for agent {agent_id}")
    
    try:
        from ..config.supabase import supabase_admin
        import json
        
        # Buscar dados atuais do agente
        memories = supabase_admin.table("memory_chunks")\
            .select("*")\
            .eq("agent_id", agent_id)\
            .execute().data or []
        
        patterns = supabase_admin.table("behavior_patterns")\
            .select("*")\
            .eq("agent_id", agent_id)\
            .execute().data or []
        
        metrics = supabase_admin.table("agent_metrics")\
            .select("*")\
            .eq("agent_id", agent_id)\
            .execute().data or []
        
        # Criar snapshot
        snapshot_data = {
            "id": str(uuid4()),
            "agent_id": agent_id,
            "snapshot_type": "full",
            "data": json.dumps({
                "memories_count": len(memories),
                "patterns_count": len(patterns),
                "metrics": metrics[0] if metrics else {},
                "created_at": datetime.utcnow().isoformat()
            }),
            "version": 1,
            "created_at": datetime.utcnow().isoformat()
        }
        
        result = supabase_admin.table("agent_snapshots").insert(snapshot_data).execute()
        
        snapshot_id = result.data[0]["id"] if result.data else None
        
        logger.info(f"🧠 SICC: Snapshot created | id={snapshot_id}")
        
        return {
            "snapshot_id": snapshot_id,
            "agent_id": agent_id,
            "memories_count": len(memories),
            "patterns_count": len(patterns)
        }
        
    except Exception as e:
        logger.error(f"🧠 SICC: Snapshot creation failed: {e}")
        raise self.retry(exc=e)


@celery_app.task(
    name='src.workers.sicc_tasks.flush_sicc_queue',
    bind=True
)
def flush_sicc_queue(self) -> Dict[str, Any]:
    """
    Força processamento de todas as interações pendentes no hook SICC.
    
    Chamado periodicamente ou antes de shutdown.
    
    Returns:
        Dict com número de interações processadas
    """
    logger.info("🧠 SICC: Flushing interaction queue")
    
    try:
        from ..services.sicc.sicc_hook import get_sicc_hook
        
        hook = get_sicc_hook()
        
        # Executar flush de forma síncrona
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            count = loop.run_until_complete(hook.flush())
        finally:
            loop.close()
        
        logger.info(f"🧠 SICC: Queue flushed | processed={count}")
        
        return {"processed": count}
        
    except Exception as e:
        logger.error(f"🧠 SICC: Queue flush failed: {e}")
        return {"processed": 0, "error": str(e)}


@celery_app.task(
    name='src.workers.sicc_tasks.cleanup_old_data',
    bind=True
)
def cleanup_old_data(self, days: int = 90) -> Dict[str, Any]:
    """
    Remove dados antigos do SICC para manter performance.
    
    Executa semanalmente.
    
    Args:
        days: Dados mais antigos que X dias serão removidos
    
    Returns:
        Dict com contagem de registros removidos
    """
    logger.info(f"🧠 SICC: Starting cleanup of data older than {days} days")
    
    try:
        from ..config.supabase import supabase_admin
        
        cutoff_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
        
        deleted = {
            "learning_logs": 0,
            "agent_snapshots": 0
        }
        
        # Remover learning_logs antigos já consolidados
        result = supabase_admin.table("learning_logs")\
            .delete()\
            .lt("created_at", cutoff_date)\
            .not_.is_("consolidated_at", "null")\
            .execute()
        deleted["learning_logs"] = len(result.data) if result.data else 0
        
        # Remover snapshots antigos (manter apenas últimos 10 por agente)
        # Simplificado: remove snapshots muito antigos
        result = supabase_admin.table("agent_snapshots")\
            .delete()\
            .lt("created_at", cutoff_date)\
            .execute()
        deleted["agent_snapshots"] = len(result.data) if result.data else 0
        
        logger.info(f"🧠 SICC: Cleanup complete | deleted={deleted}")
        
        return deleted
        
    except Exception as e:
        logger.error(f"🧠 SICC: Cleanup failed: {e}")
        return {"error": str(e)}
