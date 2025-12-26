"""
SICC Layer Management Service
Gerencia camadas de conhecimento (individual > empresa > base)
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from enum import Enum

from src.services.sicc.memory_service import MemoryService
from src.services.sicc.behavior_service import BehaviorService
from src.utils.supabase_client import get_client
from src.utils.logger import get_logger

logger = get_logger(__name__)

class KnowledgeLayer(Enum):
    """Camadas de conhecimento por prioridade"""
    BASE = ("base", 1)           # Conhecimento base do nicho
    COMPANY = ("company", 2)     # Conhecimento específico da empresa
    INDIVIDUAL = ("individual", 3) # Conhecimento específico do agente
    
    def __init__(self, layer_name: str, priority: int):
        self.layer_name = layer_name
        self.priority = priority

class LayerManagementService:
    """
    Serviço de gerenciamento de camadas de conhecimento
    
    Features:
    - Priorização de camadas (individual > empresa > base)
    - Isolamento de planos de negócio (camada empresa)
    - Gestão de conhecimento por camada
    - Resolução de conflitos entre camadas
    - Queries otimizadas por prioridade
    """
    
    def __init__(self):
        self.supabase = get_client()
        self.memory_service = MemoryService()
        self.behavior_service = BehaviorService()
        
        # Mapeamento de prioridades
        self.layer_priorities = {
            layer.layer_name: layer.priority 
            for layer in KnowledgeLayer
        }
    
    async def add_knowledge_to_layer(
        self,
        agent_id: str,
        layer: str,
        knowledge_type: str,  # "memory" ou "pattern"
        knowledge_data: Dict[str, Any],
        company_id: Optional[str] = None
    ) -> str:
        """
        Adiciona conhecimento a uma camada específica
        
        Args:
            agent_id: ID do agente
            layer: Camada (base, company, individual)
            knowledge_type: Tipo (memory ou pattern)
            knowledge_data: Dados do conhecimento
            company_id: ID da empresa (obrigatório para camada company)
            
        Returns:
            ID do conhecimento criado
        """
        try:
            # Validar camada
            if layer not in self.layer_priorities:
                raise ValueError(f"Camada inválida: {layer}. Camadas válidas: {list(self.layer_priorities.keys())}")
            
            # Validar company_id para camada empresa
            if layer == "company" and not company_id:
                raise ValueError("company_id é obrigatório para camada 'company'")
            
            # Preparar metadados da camada
            layer_metadata = {
                "layer": layer,
                "priority": self.layer_priorities[layer],
                "created_at": datetime.utcnow().isoformat(),
                "company_id": company_id if layer == "company" else None
            }
            
            # Adicionar conhecimento baseado no tipo
            if knowledge_type == "memory":
                knowledge_id = await self._add_memory_to_layer(
                    agent_id, knowledge_data, layer_metadata
                )
            elif knowledge_type == "pattern":
                knowledge_id = await self._add_pattern_to_layer(
                    agent_id, knowledge_data, layer_metadata
                )
            else:
                raise ValueError(f"Tipo de conhecimento inválido: {knowledge_type}")
            
            logger.info(f"Conhecimento {knowledge_type} adicionado à camada {layer}: {knowledge_id}")
            return knowledge_id
            
        except Exception as e:
            logger.error(f"Erro ao adicionar conhecimento à camada: {str(e)}")
            raise
    
    async def get_layered_memories(
        self,
        agent_id: str,
        query: Optional[str] = None,
        limit: int = 10,
        company_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Busca memórias respeitando prioridade das camadas
        
        Args:
            agent_id: ID do agente
            query: Query de busca (opcional)
            limit: Limite de resultados
            company_id: ID da empresa (para filtrar camada company)
            
        Returns:
            Lista de memórias ordenadas por prioridade de camada
        """
        try:
            memories = []
            
            # Buscar memórias de todas as camadas
            all_memories = await self.memory_service.list_memories(
                agent_id=agent_id,
                limit=limit * 3,  # Buscar mais para depois filtrar
                filters={"is_active": True}
            )
            
            # Filtrar e organizar por camadas
            individual_memories = []
            company_memories = []
            base_memories = []
            
            for memory in all_memories:
                metadata = memory.get("metadata", {})
                layer = metadata.get("layer", "individual")  # Default individual
                memory_company_id = metadata.get("company_id")
                
                # Aplicar filtro de query se fornecido
                if query and query.lower() not in memory.get("content", "").lower():
                    continue
                
                # Organizar por camada
                if layer == "individual":
                    individual_memories.append(memory)
                elif layer == "company":
                    # Filtrar por company_id se fornecido
                    if not company_id or memory_company_id == company_id:
                        company_memories.append(memory)
                elif layer == "base":
                    base_memories.append(memory)
            
            # Combinar respeitando prioridades (individual > company > base)
            memories.extend(individual_memories)
            memories.extend(company_memories)
            memories.extend(base_memories)
            
            # Limitar resultado final
            memories = memories[:limit]
            
            logger.info(f"Memórias por camada - Individual: {len(individual_memories)}, Company: {len(company_memories)}, Base: {len(base_memories)}")
            return memories
            
        except Exception as e:
            logger.error(f"Erro ao buscar memórias por camada: {str(e)}")
            raise
    
    async def get_layered_patterns(
        self,
        agent_id: str,
        trigger_context: Optional[str] = None,
        company_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Busca padrões comportamentais respeitando prioridade das camadas
        
        Args:
            agent_id: ID do agente
            trigger_context: Contexto do trigger (opcional)
            company_id: ID da empresa
            
        Returns:
            Lista de padrões ordenados por prioridade de camada
        """
        try:
            # Buscar todos os padrões ativos
            all_patterns = await self.behavior_service.get_applicable_patterns(
                agent_id=agent_id,
                context=trigger_context or {}
            )
            
            # Organizar por camadas
            individual_patterns = []
            company_patterns = []
            base_patterns = []
            
            for pattern in all_patterns:
                metadata = pattern.get("metadata", {})
                layer = metadata.get("layer", "individual")
                pattern_company_id = metadata.get("company_id")
                
                if layer == "individual":
                    individual_patterns.append(pattern)
                elif layer == "company":
                    if not company_id or pattern_company_id == company_id:
                        company_patterns.append(pattern)
                elif layer == "base":
                    base_patterns.append(pattern)
            
            # Combinar respeitando prioridades
            layered_patterns = []
            layered_patterns.extend(individual_patterns)
            layered_patterns.extend(company_patterns)
            layered_patterns.extend(base_patterns)
            
            logger.info(f"Padrões por camada - Individual: {len(individual_patterns)}, Company: {len(company_patterns)}, Base: {len(base_patterns)}")
            return layered_patterns
            
        except Exception as e:
            logger.error(f"Erro ao buscar padrões por camada: {str(e)}")
            raise
    
    async def resolve_knowledge_conflicts(
        self,
        agent_id: str,
        knowledge_type: str,
        conflict_key: str,
        company_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Resolve conflitos entre conhecimentos de diferentes camadas
        
        Args:
            agent_id: ID do agente
            knowledge_type: Tipo (memory ou pattern)
            conflict_key: Chave para identificar conflito (ex: pattern_name)
            company_id: ID da empresa
            
        Returns:
            Conhecimento com maior prioridade
        """
        try:
            if knowledge_type == "memory":
                # Para memórias, buscar por similaridade de conteúdo
                memories = await self.get_layered_memories(
                    agent_id=agent_id,
                    query=conflict_key,
                    company_id=company_id
                )
                
                if memories:
                    # Retornar a primeira (maior prioridade)
                    winner = memories[0]
                    logger.info(f"Conflito de memória resolvido - Camada vencedora: {winner.get('metadata', {}).get('layer', 'individual')}")
                    return winner
                    
            elif knowledge_type == "pattern":
                # Para padrões, buscar por nome específico
                patterns = await self.get_layered_patterns(
                    agent_id=agent_id,
                    company_id=company_id
                )
                
                # Filtrar por nome do padrão
                matching_patterns = [
                    p for p in patterns 
                    if p.get("pattern_name") == conflict_key
                ]
                
                if matching_patterns:
                    # Retornar o primeiro (maior prioridade)
                    winner = matching_patterns[0]
                    logger.info(f"Conflito de padrão resolvido - Camada vencedora: {winner.get('metadata', {}).get('layer', 'individual')}")
                    return winner
            
            logger.warning(f"Nenhum conhecimento encontrado para resolver conflito: {conflict_key}")
            return {}
            
        except Exception as e:
            logger.error(f"Erro ao resolver conflito: {str(e)}")
            raise
    
    async def get_layer_statistics(
        self,
        agent_id: str,
        company_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Obtém estatísticas de conhecimento por camada
        
        Args:
            agent_id: ID do agente
            company_id: ID da empresa
            
        Returns:
            Estatísticas por camada
        """
        try:
            stats = {
                "individual": {"memories": 0, "patterns": 0},
                "company": {"memories": 0, "patterns": 0},
                "base": {"memories": 0, "patterns": 0},
                "total": {"memories": 0, "patterns": 0}
            }
            
            # Contar memórias por camada
            memories = await self.memory_service.list_memories(
                agent_id=agent_id,
                limit=1000,  # Limite alto para contar tudo
                filters={"is_active": True}
            )
            
            for memory in memories:
                layer = memory.get("metadata", {}).get("layer", "individual")
                if layer in stats:
                    stats[layer]["memories"] += 1
                    stats["total"]["memories"] += 1
            
            # Contar padrões por camada
            patterns = await self.behavior_service.get_applicable_patterns(
                agent_id=agent_id,
                context={}
            )
            
            for pattern in patterns:
                layer = pattern.get("metadata", {}).get("layer", "individual")
                if layer in stats:
                    stats[layer]["patterns"] += 1
                    stats["total"]["patterns"] += 1
            
            logger.info(f"Estatísticas de camadas calculadas para agente {agent_id}")
            return stats
            
        except Exception as e:
            logger.error(f"Erro ao calcular estatísticas: {str(e)}")
            raise
    
    async def migrate_knowledge_to_layer(
        self,
        agent_id: str,
        knowledge_ids: List[str],
        target_layer: str,
        company_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Migra conhecimento existente para uma camada específica
        
        Args:
            agent_id: ID do agente
            knowledge_ids: Lista de IDs de conhecimento
            target_layer: Camada de destino
            company_id: ID da empresa (se target_layer for company)
            
        Returns:
            Resultado da migração
        """
        try:
            if target_layer not in self.layer_priorities:
                raise ValueError(f"Camada inválida: {target_layer}")
            
            if target_layer == "company" and not company_id:
                raise ValueError("company_id é obrigatório para camada 'company'")
            
            migration_results = []
            
            for knowledge_id in knowledge_ids:
                try:
                    # Tentar atualizar como memória
                    memory_updated = await self._update_memory_layer(
                        knowledge_id, target_layer, company_id
                    )
                    
                    if memory_updated:
                        migration_results.append({
                            "id": knowledge_id,
                            "type": "memory",
                            "status": "success"
                        })
                        continue
                    
                    # Tentar atualizar como padrão
                    pattern_updated = await self._update_pattern_layer(
                        knowledge_id, target_layer, company_id
                    )
                    
                    if pattern_updated:
                        migration_results.append({
                            "id": knowledge_id,
                            "type": "pattern",
                            "status": "success"
                        })
                    else:
                        migration_results.append({
                            "id": knowledge_id,
                            "type": "unknown",
                            "status": "not_found"
                        })
                        
                except Exception as e:
                    migration_results.append({
                        "id": knowledge_id,
                        "type": "unknown",
                        "status": "error",
                        "error": str(e)
                    })
            
            successful_migrations = [r for r in migration_results if r["status"] == "success"]
            
            result = {
                "target_layer": target_layer,
                "total_items": len(knowledge_ids),
                "successful_migrations": len(successful_migrations),
                "migration_results": migration_results,
                "migrated_at": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Migração concluída: {len(successful_migrations)}/{len(knowledge_ids)} itens migrados para camada {target_layer}")
            return result
            
        except Exception as e:
            logger.error(f"Erro na migração de conhecimento: {str(e)}")
            raise
    
    async def _add_memory_to_layer(
        self,
        agent_id: str,
        memory_data: Dict[str, Any],
        layer_metadata: Dict[str, Any]
    ) -> str:
        """Adiciona memória com metadados de camada"""
        # Combinar metadados
        combined_metadata = {
            **memory_data.get("metadata", {}),
            **layer_metadata
        }
        
        # Criar memória
        memory = await self.memory_service.create_chunk(
            agent_id=agent_id,
            content=memory_data["content"],
            chunk_type=memory_data.get("chunk_type", "layered_knowledge"),
            metadata=combined_metadata
        )
        
        return memory["id"]
    
    async def _add_pattern_to_layer(
        self,
        agent_id: str,
        pattern_data: Dict[str, Any],
        layer_metadata: Dict[str, Any]
    ) -> str:
        """Adiciona padrão com metadados de camada"""
        # Combinar metadados
        combined_metadata = {
            **pattern_data.get("metadata", {}),
            **layer_metadata
        }
        
        # Criar padrão
        pattern = await self.behavior_service.create_pattern(
            agent_id=agent_id,
            pattern_name=pattern_data["pattern_name"],
            trigger_conditions=pattern_data["trigger_conditions"],
            response_template=pattern_data["response_template"],
            metadata=combined_metadata
        )
        
        return pattern["id"]
    
    async def _update_memory_layer(
        self,
        memory_id: str,
        target_layer: str,
        company_id: Optional[str]
    ) -> bool:
        """Atualiza camada de uma memória"""
        try:
            update_data = {
                "metadata": {
                    "layer": target_layer,
                    "priority": self.layer_priorities[target_layer],
                    "company_id": company_id if target_layer == "company" else None,
                    "migrated_at": datetime.utcnow().isoformat()
                }
            }
            
            response = self.supabase.table("memory_chunks").update(update_data).eq("id", memory_id).execute()
            
            return len(response.data) > 0 if response.data else False
            
        except Exception:
            return False
    
    async def _update_pattern_layer(
        self,
        pattern_id: str,
        target_layer: str,
        company_id: Optional[str]
    ) -> bool:
        """Atualiza camada de um padrão"""
        try:
            update_data = {
                "metadata": {
                    "layer": target_layer,
                    "priority": self.layer_priorities[target_layer],
                    "company_id": company_id if target_layer == "company" else None,
                    "migrated_at": datetime.utcnow().isoformat()
                }
            }
            
            # CORRIGIDO: Usar behavior_patterns ao invés de agent_behavior_patterns
            response = self.supabase.table("behavior_patterns").update(update_data).eq("id", pattern_id).execute()
            
            return len(response.data) > 0 if response.data else False
            
        except Exception:
            return False