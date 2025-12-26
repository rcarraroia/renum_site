"""
SICC Analyzer Service - Analyzes Interactions for Learning Opportunities
Sprint SICC Multi-Agente

Analisa cada interação e decide:
1. Se é uma oportunidade de aprendizado
2. Se deve criar uma memória
3. Se é um padrão de comportamento
"""

import json
from typing import Any, Dict, List, Optional
from uuid import uuid4
from datetime import datetime

from ...config.supabase import supabase_admin
from ...utils.logger import logger


class SiccAnalyzer:
    """
    Analisador de interações do SICC.
    
    Responsabilidades:
    1. Analisar interações de QUALQUER agente
    2. Detectar oportunidades de aprendizado
    3. Criar registros em learning_logs (pendentes de aprovação)
    4. Detectar padrões de comportamento
    5. Criar memórias quando apropriado
    
    Cada agente tem seus dados ISOLADOS por agent_id.
    """
    
    def __init__(self):
        self._learning_keywords = [
            # Português
            "aprenda", "lembre", "memorize", "guarde", "anote",
            "importante", "sempre", "nunca", "regra", "padrão",
            "quando eu disser", "toda vez que", "a partir de agora",
            # Inglês
            "learn", "remember", "memorize", "note", "important",
            "always", "never", "rule", "pattern", "from now on"
        ]
        
        self._feedback_keywords = [
            # Positivo
            "ótimo", "perfeito", "excelente", "correto", "isso mesmo",
            "great", "perfect", "excellent", "correct", "exactly",
            # Negativo
            "errado", "incorreto", "não é isso", "tente novamente",
            "wrong", "incorrect", "not that", "try again"
        ]
        
        self._pattern_threshold = 3  # Mínimo de ocorrências para detectar padrão
        
        logger.info("🧠 SICC Analyzer initialized")
    
    async def analyze_interaction(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa uma interação e decide o que fazer.
        
        Args:
            interaction: Dict com agent_id, messages, response, context, etc
            
        Returns:
            Dict com resultados da análise
        """
        agent_id = interaction.get("agent_id")
        agent_type = interaction.get("agent_type", "unknown")
        messages = interaction.get("messages", [])
        response = interaction.get("response", "")
        context = interaction.get("context", {})
        
        results = {
            "agent_id": agent_id,
            "agent_type": agent_type,
            "learning_created": False,
            "memory_created": False,
            "pattern_detected": False,
            "actions": []
        }
        
        try:
            # 1. Verificar se é oportunidade de aprendizado
            if self._is_learning_opportunity(messages, response):
                learning_id = await self._create_learning_log(
                    agent_id=agent_id,
                    interaction=interaction,
                    learning_type="explicit"
                )
                if learning_id:
                    results["learning_created"] = True
                    results["learning_id"] = learning_id
                    results["actions"].append("learning_log_created")
            
            # 2. Verificar se deve criar memória (feedback positivo)
            if self._should_memorize(messages, response):
                memory_id = await self._create_memory_chunk(
                    agent_id=agent_id,
                    interaction=interaction
                )
                if memory_id:
                    results["memory_created"] = True
                    results["memory_id"] = memory_id
                    results["actions"].append("memory_chunk_created")
            
            # 3. Verificar se é um padrão de comportamento
            pattern = await self._detect_pattern(agent_id, interaction)
            if pattern:
                results["pattern_detected"] = True
                results["pattern"] = pattern
                results["actions"].append("pattern_detected")
            
            # 4. Registrar métrica de interação
            await self._record_interaction_metric(agent_id, interaction)
            
            logger.debug(
                f"🧠 SICC Analysis complete | agent={agent_type} | "
                f"learning={results['learning_created']} | "
                f"memory={results['memory_created']} | "
                f"pattern={results['pattern_detected']}"
            )
            
        except Exception as e:
            logger.error(f"🧠 SICC Analysis error: {e}")
            results["error"] = str(e)
        
        return results
    
    def _is_learning_opportunity(
        self,
        messages: List[Dict],
        response: str
    ) -> bool:
        """
        Detecta se a interação contém uma oportunidade de aprendizado.
        
        Exemplos:
        - "Aprenda que meu nome é João"
        - "A partir de agora, sempre responda em português"
        - "Lembre-se: nunca mencione preços"
        """
        # Verificar última mensagem do usuário
        user_messages = [m for m in messages if m.get("role") in ["user", "human"]]
        if not user_messages:
            return False
        
        last_user_msg = user_messages[-1].get("content", "").lower()
        
        # Verificar keywords de aprendizado
        for keyword in self._learning_keywords:
            if keyword in last_user_msg:
                return True
        
        return False
    
    def _should_memorize(
        self,
        messages: List[Dict],
        response: str
    ) -> bool:
        """
        Detecta se deve criar uma memória baseado em feedback.
        
        Exemplos:
        - Usuário disse "perfeito!" após resposta
        - Usuário confirmou informação importante
        """
        user_messages = [m for m in messages if m.get("role") in ["user", "human"]]
        if len(user_messages) < 2:
            return False
        
        last_user_msg = user_messages[-1].get("content", "").lower()
        
        # Verificar feedback positivo
        positive_keywords = [
            "ótimo", "perfeito", "excelente", "correto", "isso mesmo",
            "great", "perfect", "excellent", "correct", "exactly",
            "obrigado", "thanks", "valeu"
        ]
        
        for keyword in positive_keywords:
            if keyword in last_user_msg:
                return True
        
        return False
    
    async def _create_learning_log(
        self,
        agent_id: str,
        interaction: Dict,
        learning_type: str = "explicit"
    ) -> Optional[str]:
        """
        Cria um registro de aprendizado pendente de aprovação.
        
        Args:
            agent_id: UUID do agente
            interaction: Dados da interação
            learning_type: Tipo (explicit, implicit, feedback)
            
        Returns:
            ID do learning_log criado ou None
        """
        try:
            messages = interaction.get("messages", [])
            user_messages = [m for m in messages if m.get("role") in ["user", "human"]]
            last_user_msg = user_messages[-1].get("content", "") if user_messages else ""
            
            # Extrair o que deve ser aprendido
            learning_content = self._extract_learning_content(last_user_msg)
            
            data = {
                "id": str(uuid4()),
                "agent_id": agent_id,
                "learning_type": learning_type,
                "source": "conversation",
                "content": learning_content,
                "context": json.dumps({
                    "messages": messages[-3:],  # Últimas 3 mensagens
                    "response": interaction.get("response", "")[:500],
                    "agent_type": interaction.get("agent_type")
                }),
                "status": "pending",  # Aguarda aprovação
                "confidence_score": 0.7,
                "created_at": datetime.utcnow().isoformat()
            }
            
            result = supabase_admin.table("learning_logs").insert(data).execute()
            
            if result.data:
                logger.info(
                    f"🧠 Learning log created | agent_id={agent_id[:8]}... | "
                    f"type={learning_type} | status=pending"
                )
                return result.data[0].get("id")
            
        except Exception as e:
            logger.error(f"🧠 Error creating learning_log: {e}")
        
        return None
    
    async def _create_memory_chunk(
        self,
        agent_id: str,
        interaction: Dict
    ) -> Optional[str]:
        """
        Cria um chunk de memória para o agente.
        
        Args:
            agent_id: UUID do agente
            interaction: Dados da interação
            
        Returns:
            ID do memory_chunk criado ou None
        """
        try:
            messages = interaction.get("messages", [])
            response = interaction.get("response", "")
            
            # Criar conteúdo da memória
            content = self._create_memory_content(messages, response)
            
            data = {
                "id": str(uuid4()),
                "agent_id": agent_id,
                "content": content,
                "chunk_type": "conversation",
                "source": "sicc_auto",
                "metadata": json.dumps({
                    "agent_type": interaction.get("agent_type"),
                    "context": interaction.get("context", {}),
                    "auto_created": True
                }),
                "confidence_score": 0.8,
                "created_at": datetime.utcnow().isoformat()
            }
            
            result = supabase_admin.table("memory_chunks").insert(data).execute()
            
            if result.data:
                logger.info(
                    f"🧠 Memory chunk created | agent_id={agent_id[:8]}... | "
                    f"type=conversation"
                )
                return result.data[0].get("id")
            
        except Exception as e:
            logger.error(f"🧠 Error creating memory_chunk: {e}")
        
        return None
    
    async def _detect_pattern(
        self,
        agent_id: str,
        interaction: Dict
    ) -> Optional[Dict]:
        """
        Detecta padrões de comportamento recorrentes.
        
        Args:
            agent_id: UUID do agente
            interaction: Dados da interação
            
        Returns:
            Dict com padrão detectado ou None
        """
        try:
            # Buscar interações recentes do mesmo agente
            # (simplificado - em produção usaria embedding similarity)
            
            messages = interaction.get("messages", [])
            if not messages:
                return None
            
            # Extrair intent/tópico da mensagem
            user_messages = [m for m in messages if m.get("role") in ["user", "human"]]
            if not user_messages:
                return None
            
            last_msg = user_messages[-1].get("content", "").lower()
            
            # Verificar se já existe padrão similar
            result = supabase_admin.table("behavior_patterns")\
                .select("*")\
                .eq("agent_id", agent_id)\
                .execute()
            
            existing_patterns = result.data or []
            
            # Verificar match com padrões existentes
            for pattern in existing_patterns:
                trigger = pattern.get("trigger_condition", "").lower()
                if trigger and trigger in last_msg:
                    # Incrementar contador
                    new_count = pattern.get("occurrence_count", 0) + 1
                    supabase_admin.table("behavior_patterns")\
                        .update({"occurrence_count": new_count})\
                        .eq("id", pattern["id"])\
                        .execute()
                    
                    if new_count >= self._pattern_threshold:
                        return {
                            "pattern_id": pattern["id"],
                            "pattern_name": pattern.get("pattern_name"),
                            "occurrences": new_count,
                            "status": "confirmed"
                        }
            
        except Exception as e:
            logger.error(f"🧠 Error detecting pattern: {e}")
        
        return None
    
    async def _record_interaction_metric(
        self,
        agent_id: str,
        interaction: Dict
    ) -> None:
        """
        Registra métrica de interação para analytics.
        
        Args:
            agent_id: UUID do agente
            interaction: Dados da interação
        """
        try:
            # Buscar ou criar registro de métricas
            result = supabase_admin.table("agent_metrics")\
                .select("*")\
                .eq("agent_id", agent_id)\
                .execute()
            
            if result.data:
                # Atualizar métricas existentes
                metrics = result.data[0]
                new_count = metrics.get("total_interactions", 0) + 1
                
                supabase_admin.table("agent_metrics")\
                    .update({
                        "total_interactions": new_count,
                        "last_interaction_at": datetime.utcnow().isoformat()
                    })\
                    .eq("id", metrics["id"])\
                    .execute()
            else:
                # Criar novo registro
                supabase_admin.table("agent_metrics").insert({
                    "id": str(uuid4()),
                    "agent_id": agent_id,
                    "total_interactions": 1,
                    "total_learnings": 0,
                    "total_memories": 0,
                    "last_interaction_at": datetime.utcnow().isoformat(),
                    "created_at": datetime.utcnow().isoformat()
                }).execute()
                
        except Exception as e:
            logger.error(f"🧠 Error recording metric: {e}")
    
    def _extract_learning_content(self, message: str) -> str:
        """Extrai o conteúdo de aprendizado da mensagem"""
        # Remove keywords de comando
        content = message
        for keyword in self._learning_keywords:
            content = content.replace(keyword, "")
        
        return content.strip()[:500]  # Limitar tamanho
    
    def _create_memory_content(
        self,
        messages: List[Dict],
        response: str
    ) -> str:
        """Cria conteúdo resumido para memória"""
        # Pegar últimas mensagens relevantes
        relevant = messages[-3:] if len(messages) > 3 else messages
        
        content_parts = []
        for msg in relevant:
            role = msg.get("role", "unknown")
            text = msg.get("content", "")[:200]
            content_parts.append(f"{role}: {text}")
        
        content_parts.append(f"assistant: {response[:200]}")
        
        return "\n".join(content_parts)
