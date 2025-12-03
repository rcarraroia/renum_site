"""
Interview Service - Gerencia entrevistas e integração com agentes
"""

from typing import Dict, Any, Optional, List
from uuid import UUID, uuid4
from datetime import datetime

from src.config.supabase import supabase_admin
from src.utils.logger import logger
from src.agents.mmn_agent_simple import MMNDiscoveryAgent


class InterviewService:
    """Serviço para gerenciar entrevistas"""
    
    def __init__(self):
        self.supabase = supabase_admin
    
    async def list_interviews(self, page: int = 1, limit: int = 10, offset: int = 0, status: Optional[str] = None) -> Dict[str, Any]:
        """
        Lista entrevistas com paginação
        
        Args:
            page: Número da página (usado se offset não for fornecido)
            limit: Itens por página
            offset: Offset direto (sobrescreve page se fornecido)
            status: Filtrar por status (opcional)
        
        Returns:
            Dict com interviews, total, page, page_size, total_pages
        """
        try:
            # Se offset não foi fornecido, calcular a partir de page
            if offset == 0 and page > 1:
                offset = (page - 1) * limit
            
            # Query base
            query = self.supabase.table('interviews').select('*', count='exact')
            
            # Filtrar por status se fornecido
            if status:
                query = query.eq('status', status)
            
            # Ordenar e paginar
            query = query.order('created_at', desc=True).range(offset, offset + limit - 1)
            
            response = query.execute()
            
            total = response.count or 0
            items = response.data or []
            
            # Calcular total de páginas
            import math
            total_pages = math.ceil(total / limit) if limit > 0 else 0
            
            return {
                "interviews": items,
                "total": total,
                "page": page,
                "page_size": limit,
                "total_pages": total_pages
            }
            
        except Exception as e:
            logger.error(f"Error listing interviews: {e}")
            raise
    
    def create_interview(self, subagent_id: str, lead_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Cria nova entrevista.
        
        Args:
            subagent_id: ID do sub-agente
            lead_id: ID do lead (opcional)
        
        Returns:
            Dados da entrevista criada
        """
        try:
            interview_data = {
                'id': str(uuid4()),
                'subagent_id': subagent_id,
                'lead_id': lead_id,
                'status': 'in_progress',
                'started_at': datetime.now().isoformat(),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
            }
            
            response = self.supabase.table('interviews').insert(interview_data).execute()
            
            if not response.data:
                raise Exception("Failed to create interview")
            
            logger.info(f"Interview created: {interview_data['id']}")
            return response.data[0]
            
        except Exception as e:
            logger.error(f"Error creating interview: {e}")
            raise
    
    def get_interview(self, interview_id: str) -> Optional[Dict[str, Any]]:
        """
        Busca entrevista por ID.
        
        Args:
            interview_id: ID da entrevista
        
        Returns:
            Dados da entrevista ou None
        """
        try:
            response = self.supabase.table('interviews')\
                .select('*')\
                .eq('id', interview_id)\
                .single()\
                .execute()
            
            return response.data if response.data else None
            
        except Exception as e:
            logger.error(f"Error getting interview {interview_id}: {e}")
            return None
    
    def add_message(
        self, 
        interview_id: str, 
        role: str, 
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Adiciona mensagem à entrevista.
        
        Args:
            interview_id: ID da entrevista
            role: 'user' ou 'assistant'
            content: Conteúdo da mensagem
            metadata: Metadados adicionais
        
        Returns:
            Dados da mensagem criada
        """
        try:
            message_data = {
                'id': str(uuid4()),
                'interview_id': interview_id,
                'role': role,
                'content': content,
                'metadata': metadata or {},
                'timestamp': datetime.now().isoformat(),
                'created_at': datetime.now().isoformat(),
            }
            
            response = self.supabase.table('interview_messages').insert(message_data).execute()
            
            if not response.data:
                raise Exception("Failed to add message")
            
            return response.data[0]
            
        except Exception as e:
            logger.error(f"Error adding message to interview {interview_id}: {e}")
            raise
    
    def get_messages(self, interview_id: str) -> List[Dict[str, Any]]:
        """
        Busca todas as mensagens de uma entrevista.
        
        Args:
            interview_id: ID da entrevista
        
        Returns:
            Lista de mensagens
        """
        try:
            response = self.supabase.table('interview_messages')\
                .select('*')\
                .eq('interview_id', interview_id)\
                .order('timestamp')\
                .execute()
            
            return response.data if response.data else []
            
        except Exception as e:
            logger.error(f"Error getting messages for interview {interview_id}: {e}")
            return []
    
    async def process_message_with_agent(
        self,
        interview_id: str,
        subagent_id: str,
        user_message: str
    ) -> Dict[str, Any]:
        """
        Processa mensagem do usuário com o agente apropriado.
        
        Args:
            interview_id: ID da entrevista
            subagent_id: ID do sub-agente
            user_message: Mensagem do usuário
        
        Returns:
            Resposta do agente com metadados
        """
        try:
            # Buscar entrevista
            interview = self.get_interview(interview_id)
            if not interview:
                raise Exception(f"Interview {interview_id} not found")
            
            # Buscar histórico de mensagens
            messages = self.get_messages(interview_id)
            
            # Buscar sub-agente
            from src.services.subagent_service import SubAgentService
            subagent_service = SubAgentService()
            subagent = subagent_service.get_subagent(subagent_id)
            
            if not subagent:
                raise Exception(f"SubAgent {subagent_id} not found")
            
            # Inicializar agente apropriado baseado no tipo
            from src.agents.discovery_agent import DiscoveryAgent
            from src.agents.mmn_discovery_agent import MMNDiscoveryAgent
            
            # Determinar qual agente usar
            agent_type = subagent.get('type', 'discovery')
            if agent_type == 'mmn' or 'mmn' in subagent.get('name', '').lower():
                agent = MMNDiscoveryAgent()
            else:
                agent = DiscoveryAgent()
            
            # Processar mensagem
            response = await agent.process_message(
                interview_id=interview_id,
                user_message=user_message,
                message_history=messages,
                interview_data=interview
            )
            
            # Salvar mensagem do usuário
            self.add_message(
                interview_id=interview_id,
                role='user',
                content=user_message
            )
            
            # Salvar resposta do agente
            self.add_message(
                interview_id=interview_id,
                role='assistant',
                content=response['message'],
                metadata=response.get('metadata', {})
            )
            
            # Atualizar entrevista se completa
            if response.get('is_complete'):
                self._complete_interview(interview_id, response.get('analysis'))
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message with agent: {e}")
            raise
    
    def _complete_interview(self, interview_id: str, analysis: Optional[Dict[str, Any]] = None):
        """
        Marca entrevista como completa e salva análise.
        
        Args:
            interview_id: ID da entrevista
            analysis: Análise gerada pelo agente
        """
        try:
            update_data = {
                'status': 'completed',
                'completed_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
            }
            
            if analysis:
                update_data['ai_analysis'] = analysis
            
            self.supabase.table('interviews')\
                .update(update_data)\
                .eq('id', interview_id)\
                .execute()
            
            logger.info(f"Interview {interview_id} marked as complete")
            
        except Exception as e:
            logger.error(f"Error completing interview {interview_id}: {e}")
