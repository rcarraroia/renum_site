"""
SICC Hook - Universal Hook for All Agents
Sprint SICC Multi-Agente

Este hook intercepta TODAS as conversas de QUALQUER agente do sistema.
Cada agente tem suas memórias isoladas por agent_id.
"""

import asyncio
from typing import Any, Dict, List, Optional
from uuid import UUID
from datetime import datetime

from ...utils.logger import logger


class SiccHook:
    """
    Hook universal do SICC para interceptar conversas de todos os agentes.
    
    Responsabilidades:
    1. Interceptar mensagens APÓS o agente responder
    2. Enviar para análise assíncrona (não bloqueia resposta)
    3. Isolar dados por agent_id
    4. Funcionar para QUALQUER agente (RENUS, ISA, sub-agentes, futuros)
    
    Uso:
        # No BaseAgent.invoke():
        response = await self._generate_response(state)
        await sicc_hook.on_interaction(
            agent_id=self.agent_id,
            messages=messages,
            response=response,
            context=context
        )
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern - apenas uma instância do hook"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self._analyzer = None  # Lazy load
        self._enabled = True
        self._queue: List[Dict] = []  # Queue para processamento batch
        self._batch_size = 10
        self._processing = False
        
        logger.info("🧠 SICC Hook initialized - monitoring ALL agents")
    
    @property
    def analyzer(self):
        """Lazy load do analyzer para evitar imports circulares"""
        if self._analyzer is None:
            from .analyzer_service import SiccAnalyzer
            self._analyzer = SiccAnalyzer()
        return self._analyzer
    
    def enable(self):
        """Habilita o hook"""
        self._enabled = True
        logger.info("🧠 SICC Hook ENABLED")
    
    def disable(self):
        """Desabilita o hook (útil para testes)"""
        self._enabled = False
        logger.info("🧠 SICC Hook DISABLED")
    
    async def on_interaction(
        self,
        agent_id: str,
        agent_type: str,
        messages: List[Any],
        response: str,
        context: Dict[str, Any],
        metadata: Optional[Dict] = None
    ) -> None:
        """
        Chamado APÓS cada interação de qualquer agente.
        
        NÃO BLOQUEIA a resposta ao usuário - processa em background.
        
        Args:
            agent_id: UUID do agente (isolamento de dados)
            agent_type: Tipo do agente (renus, isa, discovery, etc)
            messages: Lista de mensagens da conversa
            response: Resposta gerada pelo agente
            context: Contexto da conversa (client_id, user_id, etc)
            metadata: Metadados adicionais (opcional)
        """
        if not self._enabled:
            return
        
        try:
            # Criar registro da interação
            interaction = {
                "agent_id": str(agent_id),
                "agent_type": agent_type,
                "messages": self._serialize_messages(messages),
                "response": response,
                "context": context,
                "metadata": metadata or {},
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Adicionar à queue
            self._queue.append(interaction)
            
            logger.debug(
                f"🧠 SICC Hook captured interaction | "
                f"agent={agent_type} | agent_id={agent_id[:8]}..."
            )
            
            # Processar em background se queue cheia ou forçar
            if len(self._queue) >= self._batch_size:
                asyncio.create_task(self._process_queue())
            
        except Exception as e:
            # NUNCA falhar a resposta do agente por causa do SICC
            logger.error(f"🧠 SICC Hook error (non-blocking): {e}")
    
    async def _process_queue(self) -> None:
        """Processa a queue de interações em background"""
        if self._processing or not self._queue:
            return
        
        self._processing = True
        
        try:
            # Pegar batch da queue
            batch = self._queue[:self._batch_size]
            self._queue = self._queue[self._batch_size:]
            
            logger.info(f"🧠 SICC processing batch of {len(batch)} interactions")
            
            # Analisar cada interação
            for interaction in batch:
                try:
                    await self.analyzer.analyze_interaction(interaction)
                except Exception as e:
                    logger.error(f"🧠 SICC analysis error: {e}")
            
        finally:
            self._processing = False
    
    async def flush(self) -> int:
        """
        Força processamento de todas as interações pendentes.
        Útil para shutdown graceful ou testes.
        
        Returns:
            Número de interações processadas
        """
        count = len(self._queue)
        
        while self._queue:
            await self._process_queue()
        
        logger.info(f"🧠 SICC Hook flushed {count} interactions")
        return count
    
    def _serialize_messages(self, messages: List[Any]) -> List[Dict]:
        """Serializa mensagens para armazenamento"""
        serialized = []
        
        for msg in messages:
            if hasattr(msg, 'content'):
                # LangChain message
                serialized.append({
                    "role": msg.__class__.__name__.replace("Message", "").lower(),
                    "content": msg.content
                })
            elif isinstance(msg, dict):
                serialized.append(msg)
            else:
                serialized.append({"role": "unknown", "content": str(msg)})
        
        return serialized
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do hook"""
        return {
            "enabled": self._enabled,
            "queue_size": len(self._queue),
            "processing": self._processing,
            "batch_size": self._batch_size
        }


# Singleton instance
_sicc_hook: Optional[SiccHook] = None


def get_sicc_hook() -> SiccHook:
    """
    Retorna a instância singleton do SICC Hook.
    
    Uso:
        from backend.src.services.sicc.sicc_hook import get_sicc_hook
        
        hook = get_sicc_hook()
        await hook.on_interaction(...)
    """
    global _sicc_hook
    if _sicc_hook is None:
        _sicc_hook = SiccHook()
    return _sicc_hook
