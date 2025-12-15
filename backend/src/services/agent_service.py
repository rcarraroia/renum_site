"""
Agent Service - Lógica de Negócios para Agentes
Fase 2 - Modelo de Agente Unificado
"""

from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
import json

from ..config.supabase import supabase_admin
from ..models.agent import (
    AgentCreate,
    AgentUpdate,
    AgentResponse,
    AgentListItem,
    AgentStats,
    AgentRole
)
from ..utils.logger import logger


class AgentService:
    """Serviço para gerenciamento unificado de agentes"""
    
    def __init__(self):
        """Inicializa serviço com cliente Supabase admin"""
        self.supabase = supabase_admin
    
    async def create_agent(self, data: AgentCreate) -> AgentResponse:
        """Cria um novo agente"""
        try:
            logger.info(f"Criando agente: {data.name} (Papel: {data.role})")
            
            # Prepara payload para inserção
            # Nota: config é um dict, será convertido automaticamente para JSONB pelo driver/Supabase sdk? 
            # Geralmente sim, ou precisamos de json.dumps se for raw SQL. Usando lib supabase-py.
            
            agent_payload = {
                "role": data.role.value,
                "name": data.name,
                "description": data.description,
                "client_id": str(data.client_id) if data.client_id else None,
                "parent_id": str(data.parent_id) if data.parent_id else None,
                "sicc_enabled": data.sicc_enabled,
                "fine_tuning_config": data.fine_tuning_config,
                "is_active": data.is_active,
                "is_public": data.is_public,
                "public_url": data.public_url,
                "config": data.config, # Assumindo que supabase-py serializa dict -> jsonb
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            # Gerar slug se não fornecido
            if data.slug:
                agent_payload["slug"] = data.slug
            else:
                agent_payload["slug"] = self._generate_slug(data.name)

            response = self.supabase.table('agents').insert(agent_payload).execute()
            
            if not response.data:
                raise Exception("Falha ao criar agente: Retorno vazio do banco.")
            
            return AgentResponse(**response.data[0])
            
        except Exception as e:
            logger.error(f"Erro ao criar agente: {e}")
            raise

    async def get_agent(self, agent_id: UUID) -> Optional[AgentResponse]:
        """Busca agente por ID"""
        try:
            response = self.supabase.table('agents').select('*').eq('id', str(agent_id)).execute()
            
            if not response.data:
                return None
            
            return AgentResponse(**response.data[0])
            
        except Exception as e:
            logger.error(f"Erro ao buscar agente {agent_id}: {e}")
            raise

    async def get_system_agent(self, role: AgentRole) -> Optional[AgentResponse]:
        """Busca agente de sistema (Renus ou ISA) pelo papel"""
        try:
            response = self.supabase.table('agents').select('*').eq('role', role.value).limit(1).execute()
            
            if not response.data:
                return None
            
            return AgentResponse(**response.data[0])
            
        except Exception as e:
            logger.error(f"Erro ao buscar agente de sistema {role}: {e}")
            raise

    async def get_by_slug(self, slug: str) -> Optional[AgentResponse]:
        """Busca agente por slug"""
        try:
            response = self.supabase.table('agents').select('*').eq('slug', slug).limit(1).execute()
            
            if not response.data:
                return None
            
            return AgentResponse(**response.data[0])
            
        except Exception as e:
            logger.error(f"Erro ao buscar agente por slug {slug}: {e}")
            raise

    async def list_agents(
        self,
        client_id: Optional[UUID] = None,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[AgentListItem]:
        """Lista agentes com filtros"""
        try:
            query = self.supabase.table('agents').select('*')
            
            if client_id:
                query = query.eq('client_id', str(client_id))
            
            if role:
                query = query.eq('role', role)
            
            if is_active is not None:
                query = query.eq('is_active', is_active)
                
            query = query.order('created_at', desc=True).range(offset, offset + limit - 1)
            response = query.execute()
            
            return [AgentListItem(**agent) for agent in response.data]
            
        except Exception as e:
            logger.error(f"Erro ao listar agentes: {e}")
            raise

    async def update_agent(self, agent_id: UUID, data: AgentUpdate) -> AgentResponse:
        """Atualiza agente"""
        try:
            # Verifica existência
            existing = await self.get_agent(agent_id)
            if not existing:
                raise Exception(f"Agente {agent_id} não encontrado")
            
            # Prepara dados (apenas campos setados)
            update_data = data.model_dump(exclude_unset=True)
            update_data['updated_at'] = datetime.now().isoformat()
            
            # Se status legado for passado, mapear para is_active
            if 'status' in update_data:
                status_val = update_data.pop('status')
                if status_val == 'active':
                    update_data['is_active'] = True
                elif status_val in ['paused', 'archived', 'draft']:
                    update_data['is_active'] = False
            
            response = self.supabase.table('agents').update(update_data).eq('id', str(agent_id)).execute()
            
            if not response.data:
                raise Exception("Falha ao atualizar agente")
                
            return AgentResponse(**response.data[0])
            
        except Exception as e:
            logger.error(f"Erro ao atualizar agente {agent_id}: {e}")
            raise

    async def delete_agent(self, agent_id: UUID) -> bool:
        """Deleta agente (Verifica se tem filhos antes)"""
        try:
            # Verifica filhos (sub-agentes)
            children = self.supabase.table('agents').select('id').eq('parent_id', str(agent_id)).execute()
            if children.data and len(children.data) > 0:
                raise Exception(f"Não é possível deletar agente {agent_id}: Possui {len(children.data)} sub-agentes ativos.")
            
            self.supabase.table('agents').delete().eq('id', str(agent_id)).execute()
            logger.info(f"Agente deletado: {agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao deletar agente {agent_id}: {e}")
            raise

    async def get_stats(self, agent_id: UUID) -> AgentStats:
        """Obtém estatísticas do agente"""
        try:
            agent = await self.get_agent(agent_id)
            if not agent:
                raise Exception("Agente não encontrado")
                
            # Conta filhos direto na tabela agents
            children_resp = self.supabase.table('agents').select('id', count='exact').eq('parent_id', str(agent_id)).execute()
            sub_agents_count = children_resp.count or 0
            
            # TODO: Ajustar lógica de contagem de conversas conforme nova arquitetura
            # Por enquanto retorna 0 ou conta da tabela de conversas se existir
            total_conv = 0
            active_conv = 0
            total_msgs = 0
            
            # Tenta buscar se tabela conversations existir
            try:
                # Exemplo genérico, ajustar conforme tabela real
                # conversations_resp = self.supabase.table('conversations').select('id', count='exact').eq('agent_id', str(agent_id)).execute()
                # total_conv = conversations_resp.count or 0
                pass
            except:
                pass
            
            return AgentStats(
                agent_id=agent_id,
                sub_agents_count=sub_agents_count,
                total_conversations=total_conv,
                active_conversations=active_conv,
                total_messages=total_msgs,
                # Usa .get('config', {}) se necessário, mas AgentResponse deve ter access_count se estiver no DB
                # Se não tiver coluna access_count no DB novo (a migration não criou?), retorne 0
                # A migration antiga tinha. A nova unificada TEM access_count?
                # Verificando SQL migration... Não vi access_count no CREATE TABLE.
                # Se não tiver, isso vai quebrar. Vamos assumir 0 por segurança.
                access_count=0 
            )
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {e}")
            raise

    def _generate_slug(self, name: str) -> str:
        """Gera slug amigável para URL"""
        import re, unicodedata
        slug = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii').lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
        return slug

# Singleton
_agent_service = None

def get_agent_service() -> AgentService:
    """Retorna instância singleton do AgentService"""
    global _agent_service
    if _agent_service is None:
        _agent_service = AgentService()
    return _agent_service
