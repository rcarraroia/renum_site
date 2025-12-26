"""
SICC Niche Propagation Service
Gerencia propagação de conhecimento entre agentes do mesmo nicho
"""

import logging
from typing import List, Dict, Any, Optional, Set
from datetime import datetime, timedelta
import asyncio
from uuid import uuid4

from src.services.sicc.memory_service import MemoryService
from src.services.sicc.behavior_service import BehaviorService
from src.services.sicc.snapshot_service import SnapshotService
from src.services.sicc.embedding_service import EmbeddingService
from src.utils.supabase_client import get_client
from src.utils.logger import get_logger

logger = get_logger(__name__)

class NichePropagationService:
    """
    Serviço de propagação de conhecimento por nicho
    
    Features:
    - Propagação de memórias base para todos agentes do nicho
    - Versionamento de conhecimento base
    - Rollback de propagações
    - Isolamento por camadas (individual > empresa > base)
    - Sincronização automática
    """
    
    def __init__(self):
        self.supabase = get_client()
        self.memory_service = MemoryService()
        self.behavior_service = BehaviorService()
        self.snapshot_service = SnapshotService()
        self.embedding_service = EmbeddingService()
        
        # Configurações
        self.base_layer_priority = 1
        self.company_layer_priority = 2
        self.individual_layer_priority = 3
        
    async def get_agents_by_niche(self, niche_type: str) -> List[Dict[str, Any]]:
        """
        Obtém todos os agentes de um nicho específico
        
        Args:
            niche_type: Tipo do nicho (mmn, vereador, clinica, etc.)
            
        Returns:
            Lista de agentes do nicho
        """
        try:
            # Buscar agentes por tipo de nicho
            # Assumindo que existe uma coluna 'niche_type' na tabela agents
            response = self.supabase.table("agents").select("*").eq("niche_type", niche_type).execute()
            
            agents = response.data if response.data else []
            logger.info(f"Encontrados {len(agents)} agentes do nicho '{niche_type}'")
            
            return agents
            
        except Exception as e:
            logger.error(f"Erro ao buscar agentes do nicho: {str(e)}")
            raise
    
    async def create_base_knowledge_version(
        self, 
        niche_type: str,
        memories: List[Dict[str, Any]],
        patterns: List[Dict[str, Any]],
        version_name: Optional[str] = None
    ) -> str:
        """
        Cria nova versão do conhecimento base para um nicho
        
        Args:
            niche_type: Tipo do nicho
            memories: Lista de memórias base
            patterns: Lista de padrões comportamentais
            version_name: Nome da versão (opcional)
            
        Returns:
            ID da versão criada
        """
        try:
            version_id = str(uuid4())
            version_name = version_name or f"v{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Criar registro da versão
            version_data = {
                "id": version_id,
                "niche_type": niche_type,
                "version_name": version_name,
                "memories_count": len(memories),
                "patterns_count": len(patterns),
                "created_at": datetime.utcnow().isoformat(),
                "is_active": False,  # Não ativa automaticamente
                "metadata": {
                    "created_by": "system",
                    "description": f"Base knowledge for {niche_type} niche"
                }
            }
            
            # Salvar versão (assumindo tabela niche_knowledge_versions)
            self.supabase.table("niche_knowledge_versions").insert(version_data).execute()
            
            # Salvar memórias da versão
            for memory in memories:
                memory_version_data = {
                    "version_id": version_id,
                    "memory_data": memory,
                    "layer": "base",
                    "priority": self.base_layer_priority
                }
                self.supabase.table("niche_knowledge_memories").insert(memory_version_data).execute()
            
            # Salvar padrões da versão
            for pattern in patterns:
                pattern_version_data = {
                    "version_id": version_id,
                    "pattern_data": pattern,
                    "layer": "base",
                    "priority": self.base_layer_priority
                }
                self.supabase.table("niche_knowledge_patterns").insert(pattern_version_data).execute()
            
            logger.info(f"Versão de conhecimento criada: {version_id} ({version_name})")
            return version_id
            
        except Exception as e:
            logger.error(f"Erro ao criar versão de conhecimento: {str(e)}")
            raise
    
    async def propagate_knowledge_to_niche(
        self, 
        version_id: str,
        target_agents: Optional[List[str]] = None,
        create_snapshots: bool = True
    ) -> Dict[str, Any]:
        """
        Propaga conhecimento base para todos agentes do nicho
        
        Args:
            version_id: ID da versão de conhecimento
            target_agents: Lista específica de agentes (opcional)
            create_snapshots: Se deve criar snapshots antes da propagação
            
        Returns:
            Resultado da propagação
        """
        try:
            # Buscar dados da versão
            version_response = self.supabase.table("niche_knowledge_versions").select("*").eq("id", version_id).execute()
            
            if not version_response.data:
                raise ValueError(f"Versão não encontrada: {version_id}")
            
            version_data = version_response.data[0]
            niche_type = version_data["niche_type"]
            
            # Buscar agentes do nicho
            if target_agents:
                agents = []
                for agent_id in target_agents:
                    agent_response = self.supabase.table("agents").select("*").eq("id", agent_id).execute()
                    if agent_response.data:
                        agents.extend(agent_response.data)
            else:
                agents = await self.get_agents_by_niche(niche_type)
            
            if not agents:
                logger.warning(f"Nenhum agente encontrado para propagação do nicho '{niche_type}'")
                return {"status": "no_agents", "agents_updated": 0}
            
            # Buscar memórias e padrões da versão
            memories_response = self.supabase.table("niche_knowledge_memories").select("*").eq("version_id", version_id).execute()
            patterns_response = self.supabase.table("niche_knowledge_patterns").select("*").eq("version_id", version_id).execute()
            
            base_memories = memories_response.data if memories_response.data else []
            base_patterns = patterns_response.data if patterns_response.data else []
            
            # Propagar para cada agente
            propagation_results = []
            
            for agent in agents:
                agent_id = agent["id"]
                
                try:
                    # Criar snapshot antes da propagação (se solicitado)
                    snapshot_id = None
                    if create_snapshots:
                        snapshot_id = await self.snapshot_service.create_snapshot(
                            agent_id=agent_id,
                            name=f"pre_propagation_{version_data['version_name']}",
                            metadata={
                                "type": "pre_propagation",
                                "version_id": version_id,
                                "niche_type": niche_type
                            }
                        )
                    
                    # Propagar memórias base
                    memories_added = 0
                    for memory_item in base_memories:
                        memory_data = memory_item["memory_data"]
                        
                        # Verificar se memória já existe (evitar duplicatas)
                        existing = await self._check_existing_base_memory(agent_id, memory_data)
                        
                        if not existing:
                            # Criar memória com camada base
                            await self.memory_service.create_chunk(
                                agent_id=agent_id,
                                content=memory_data["content"],
                                chunk_type=memory_data.get("chunk_type", "base_knowledge"),
                                metadata={
                                    **memory_data.get("metadata", {}),
                                    "layer": "base",
                                    "priority": self.base_layer_priority,
                                    "version_id": version_id,
                                    "niche_type": niche_type,
                                    "propagated_at": datetime.utcnow().isoformat()
                                }
                            )
                            memories_added += 1
                    
                    # Propagar padrões comportamentais
                    patterns_added = 0
                    for pattern_item in base_patterns:
                        pattern_data = pattern_item["pattern_data"]
                        
                        # Verificar se padrão já existe
                        existing = await self._check_existing_base_pattern(agent_id, pattern_data)
                        
                        if not existing:
                            # Criar padrão com camada base
                            await self.behavior_service.create_pattern(
                                agent_id=agent_id,
                                pattern_name=pattern_data["pattern_name"],
                                trigger_conditions=pattern_data["trigger_conditions"],
                                response_template=pattern_data["response_template"],
                                metadata={
                                    **pattern_data.get("metadata", {}),
                                    "layer": "base",
                                    "priority": self.base_layer_priority,
                                    "version_id": version_id,
                                    "niche_type": niche_type,
                                    "propagated_at": datetime.utcnow().isoformat()
                                }
                            )
                            patterns_added += 1
                    
                    propagation_results.append({
                        "agent_id": agent_id,
                        "status": "success",
                        "memories_added": memories_added,
                        "patterns_added": patterns_added,
                        "snapshot_id": snapshot_id
                    })
                    
                    logger.info(f"Propagação concluída para agente {agent_id}: {memories_added} memórias, {patterns_added} padrões")
                    
                except Exception as e:
                    logger.error(f"Erro na propagação para agente {agent_id}: {str(e)}")
                    propagation_results.append({
                        "agent_id": agent_id,
                        "status": "error",
                        "error": str(e)
                    })
            
            # Marcar versão como ativa
            self.supabase.table("niche_knowledge_versions").update({"is_active": True}).eq("id", version_id).execute()
            
            # Resultado final
            successful_agents = [r for r in propagation_results if r["status"] == "success"]
            failed_agents = [r for r in propagation_results if r["status"] == "error"]
            
            result = {
                "version_id": version_id,
                "niche_type": niche_type,
                "total_agents": len(agents),
                "successful_propagations": len(successful_agents),
                "failed_propagations": len(failed_agents),
                "propagation_results": propagation_results,
                "propagated_at": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Propagação concluída: {len(successful_agents)}/{len(agents)} agentes atualizados")
            return result
            
        except Exception as e:
            logger.error(f"Erro na propagação de conhecimento: {str(e)}")
            raise
    
    async def rollback_propagation(
        self, 
        version_id: str,
        target_agents: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Faz rollback de uma propagação usando snapshots
        
        Args:
            version_id: ID da versão a ser revertida
            target_agents: Lista específica de agentes (opcional)
            
        Returns:
            Resultado do rollback
        """
        try:
            # Buscar dados da versão
            version_response = self.supabase.table("niche_knowledge_versions").select("*").eq("id", version_id).execute()
            
            if not version_response.data:
                raise ValueError(f"Versão não encontrada: {version_id}")
            
            version_data = version_response.data[0]
            niche_type = version_data["niche_type"]
            
            # Buscar agentes
            if target_agents:
                agents = target_agents
            else:
                agents_data = await self.get_agents_by_niche(niche_type)
                agents = [agent["id"] for agent in agents_data]
            
            rollback_results = []
            
            for agent_id in agents:
                try:
                    # Buscar snapshot pré-propagação
                    # CORRIGIDO: Usar agent_snapshots ao invés de agent_knowledge_snapshots
                    snapshots_response = self.supabase.table("agent_snapshots").select("*").eq("agent_id", agent_id).contains("metadata", {"version_id": version_id, "type": "pre_propagation"}).execute()
                    
                    if snapshots_response.data:
                        snapshot_id = snapshots_response.data[0]["id"]
                        
                        # Restaurar snapshot
                        await self.snapshot_service.restore_snapshot(snapshot_id)
                        
                        rollback_results.append({
                            "agent_id": agent_id,
                            "status": "success",
                            "snapshot_id": snapshot_id
                        })
                        
                        logger.info(f"Rollback concluído para agente {agent_id}")
                    else:
                        # Remover memórias e padrões da versão manualmente
                        await self._remove_propagated_knowledge(agent_id, version_id)
                        
                        rollback_results.append({
                            "agent_id": agent_id,
                            "status": "manual_cleanup",
                            "snapshot_id": None
                        })
                        
                        logger.info(f"Limpeza manual concluída para agente {agent_id}")
                    
                except Exception as e:
                    logger.error(f"Erro no rollback para agente {agent_id}: {str(e)}")
                    rollback_results.append({
                        "agent_id": agent_id,
                        "status": "error",
                        "error": str(e)
                    })
            
            # Marcar versão como inativa
            self.supabase.table("niche_knowledge_versions").update({"is_active": False}).eq("id", version_id).execute()
            
            successful_rollbacks = [r for r in rollback_results if r["status"] in ["success", "manual_cleanup"]]
            
            result = {
                "version_id": version_id,
                "niche_type": niche_type,
                "total_agents": len(agents),
                "successful_rollbacks": len(successful_rollbacks),
                "rollback_results": rollback_results,
                "rolled_back_at": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Rollback concluído: {len(successful_rollbacks)}/{len(agents)} agentes revertidos")
            return result
            
        except Exception as e:
            logger.error(f"Erro no rollback: {str(e)}")
            raise
    
    async def get_niche_knowledge_versions(self, niche_type: str) -> List[Dict[str, Any]]:
        """
        Lista versões de conhecimento de um nicho
        
        Args:
            niche_type: Tipo do nicho
            
        Returns:
            Lista de versões
        """
        try:
            response = self.supabase.table("niche_knowledge_versions").select("*").eq("niche_type", niche_type).order("created_at", desc=True).execute()
            
            versions = response.data if response.data else []
            logger.info(f"Encontradas {len(versions)} versões para nicho '{niche_type}'")
            
            return versions
            
        except Exception as e:
            logger.error(f"Erro ao buscar versões: {str(e)}")
            raise
    
    async def _check_existing_base_memory(self, agent_id: str, memory_data: Dict[str, Any]) -> bool:
        """Verifica se memória base já existe para o agente"""
        try:
            # Buscar por conteúdo similar ou metadata específica
            # CORRIGIDO: Usar memory_chunks ao invés de agent_memory_chunks
            response = self.supabase.table("memory_chunks").select("id").eq("agent_id", agent_id).contains("metadata", {"layer": "base"}).execute()
            
            if response.data:
                # Verificar conteúdo específico (implementar lógica de similaridade se necessário)
                for existing in response.data:
                    # Por simplicidade, assumir que não existe duplicata
                    pass
            
            return False  # Por enquanto, sempre permite adicionar
            
        except Exception as e:
            logger.error(f"Erro ao verificar memória existente: {str(e)}")
            return False
    
    async def _check_existing_base_pattern(self, agent_id: str, pattern_data: Dict[str, Any]) -> bool:
        """Verifica se padrão base já existe para o agente"""
        try:
            # Buscar por nome do padrão
            # CORRIGIDO: Usar behavior_patterns ao invés de agent_behavior_patterns
            response = self.supabase.table("behavior_patterns").select("id").eq("agent_id", agent_id).eq("pattern_name", pattern_data["pattern_name"]).contains("metadata", {"layer": "base"}).execute()
            
            return len(response.data) > 0 if response.data else False
            
        except Exception as e:
            logger.error(f"Erro ao verificar padrão existente: {str(e)}")
            return False
    
    async def _remove_propagated_knowledge(self, agent_id: str, version_id: str) -> None:
        """Remove conhecimento propagado de uma versão específica"""
        try:
            # Remover memórias da versão
            # CORRIGIDO: Usar memory_chunks ao invés de agent_memory_chunks
            self.supabase.table("memory_chunks").delete().eq("agent_id", agent_id).contains("metadata", {"version_id": version_id}).execute()
            
            # Remover padrões da versão
            # CORRIGIDO: Usar behavior_patterns ao invés de agent_behavior_patterns
            self.supabase.table("behavior_patterns").delete().eq("agent_id", agent_id).contains("metadata", {"version_id": version_id}).execute()
            
            logger.info(f"Conhecimento da versão {version_id} removido do agente {agent_id}")
            
        except Exception as e:
            logger.error(f"Erro ao remover conhecimento propagado: {str(e)}")
            raise