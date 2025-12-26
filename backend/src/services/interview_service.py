"""
Interview Service - Gerencia entrevistas e integração com agentes
"""

from typing import Dict, Any, Optional, List
from uuid import UUID, uuid4
from datetime import datetime

from src.config.supabase import supabase_admin
from src.utils.logger import logger
# from src.agents.mmn_agent_simple import MMNDiscoveryAgent  # Comentado temporariamente para testes


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
            
            # Converter items para InterviewListItem format
            interview_items = []
            for item in items:
                interview_items.append({
                    "id": item.get("id"),
                    "contact_name": item.get("contact_name"),
                    "email": item.get("email"),
                    "status": item.get("status"),
                    "started_at": item.get("started_at"),
                    "completed_at": item.get("completed_at"),
                    "created_at": item.get("created_at"),
                    "duration_minutes": None  # TODO: Calculate if needed
                })
            
            return {
                "interviews": interview_items,
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
            
            # Buscar sub-agente (Agora usando AgentService para compatibilidade unificada)
            # from src.services.subagent_service import SubAgentService
            from src.services.agent_service import get_agent_service
            
            agent_service = get_agent_service()
            # O nome do parametro ainda é subagent_id por compatibilidade com a tabela interviews
            agent = await agent_service.get_agent(subagent_id)
            
            if not agent:
                raise Exception(f"Agent {subagent_id} not found")
            
            # Inicializar agente apropriado baseado no tipo
            from src.agents.discovery_agent import DiscoveryAgent
            from src.agents.mmn_discovery_agent import MMNDiscoveryAgent
            
            # Determinar qual agente usar
            is_mmn = False
            is_orchestrator = False
            
            # Checar se é o Renus (Orchestrator)
            if agent.slug == 'renus' or (agent.role and agent.role == 'system_orchestrator'):
                 is_orchestrator = True
            elif agent.slug and 'mmn' in agent.slug:
                is_mmn = True
            elif agent.name and 'mmn' in agent.name.lower():
                is_mmn = True
            
            # Determinar ferramentas
            config = agent.config or {}
            config_tools = config.get("tools", [])
            
            # IMPORTER: Importar get_tools_by_names aqui para evitar ciclo no topo
            from src.tools.registry import get_tools_by_names
            
            # RESOLVE TOOLS: Injeção de Dependência
            # Passamos 'self' (InterviewService) para que o registry possa criar sub-agentes sem importar o Service
            loaded_tools = get_tools_by_names(
                config_tools, 
                client_id=agent.client_id, 
                agent_id=agent.id,
                interview_service=self
            )
            
            if is_orchestrator:
                # Usa DiscoveryAgent como base pro Renus por enquanto
                # Passamos todo o config para que o DiscoveryAgent possa ler identity.system_prompt
                config['agent_id'] = str(agent.id)  # Inject agent ID for tools
                
                # Garantir model no config se não existir
                model_name = config.get("model", "gpt-4o-mini")
                
                # Remover chaves conflitantes de config antes de passar como kwargs
                safe_config = config.copy()
                safe_config.pop('model', None)
                safe_config.pop('tools', None)
                safe_config.pop('system_prompt', None)

                agent_instance = DiscoveryAgent(
                    model=model_name,
                    tools=loaded_tools, # Tools já carregadas!
                    client_id=agent.client_id,
                    **safe_config
                )
            elif is_mmn:
                model_name = config.get("model", "gpt-4o-mini")
                
                safe_config = config.copy()
                safe_config.pop('model', None)
                safe_config.pop('tools', None)
                safe_config.pop('system_prompt', None)
                
                agent_instance = MMNDiscoveryAgent(
                    model=model_name,
                    tools=loaded_tools,
                    client_id=agent.client_id,
                    **safe_config
                )
            else:
                model_name = config.get("model", "gpt-4o-mini")
                
                safe_config = config.copy()
                safe_config.pop('model', None)
                safe_config.pop('tools', None)
                safe_config.pop('system_prompt', None)
                
                agent_instance = DiscoveryAgent(
                    model=model_name,
                    tools=loaded_tools,
                    client_id=agent.client_id,
                    **safe_config
                )
            
            # --- GUARDRAILS LAYER 1: INPUT ---
            from src.services.guardrail_service import guardrail_service
            input_validation = guardrail_service.validate_input(user_message, agent.config or {})
            if not input_validation['valid']:
                logger.warning(f"Guardrail Input Violation: {input_validation['violation']}")
                
                # Salvar mensagem bloqueada mas com resposta de erro
                self.add_message(interview_id, 'user', user_message)
                error_msg = "Desculpe, não posso processar essa mensagem devido às políticas de segurança."
                self.add_message(interview_id, 'assistant', error_msg, metadata={"violation": input_validation['violation']})
                return {
                   "message": error_msg,
                   "metadata": {"violation": input_validation['violation']},
                   "is_complete": False
                }
            # Use sanitized text if modified
            processed_user_message = input_validation['modified_text']
            # ---------------------------------

            # Processar mensagem (com texto sanitizado)
            response = await agent_instance.process_message(
                interview_id=interview_id,
                user_message=processed_user_message,
                message_history=messages,
                interview_data=interview
            )
            
            # --- GUARDRAILS LAYER 2: OUTPUT ---
            output_validation = guardrail_service.validate_output(response['message'], agent.config or {})
            if not output_validation['valid']:
                logger.warning(f"Guardrail Output Violation: {output_validation['violation']}")
                response['message'] = "Desculpe, a resposta gerada foi bloqueada pelas políticas de segurança."
                if 'metadata' not in response: response['metadata'] = {}
                response['metadata']['violation'] = output_validation['violation']
            # ----------------------------------
            
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
            
            # --- TRIGGER CHECK ---
            try:
                from src.services.trigger_service import trigger_service
                trigger_context = {
                    'interview_id': interview_id,
                    'message': user_message, # User's last message content
                    'agent_response': response['message'],
                    'collected_data': response.get('metadata', {}).get('collected_data', {})
                }
                # Run triggers (fire and forget / await)
                await trigger_service.evaluate_triggers(agent, trigger_context, event_type="on_message_received")
            except Exception as trigger_error:
                logger.error(f"Error evaluating triggers: {trigger_error}")
            # ---------------------
            
            # CRITICAL FIX: Persist collected fields to DB so agent remembers them next turn
            collected_data = response.get('metadata', {}).get('collected_data', {})
            if collected_data:
                valid_fields = ['contact_name', 'email', 'contact_phone', 'country', 'company', 'experience_level', 'operation_size']
                updates = {k: v for k, v in collected_data.items() if k in valid_fields and v is not None}
                
                if updates:
                    try:
                        self.supabase.table('interviews').update(updates).eq('id', interview_id).execute()
                    except Exception as db_err:
                        logger.error(f"Failed to update interview fields: {db_err}")

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
    
    async def get_interview_details(self, interview_id: str) -> Optional[Dict[str, Any]]:
        """
        Busca detalhes completos da entrevista com mensagens e progresso.
        
        Args:
            interview_id: ID da entrevista
        
        Returns:
            Dict com interview, messages e progress
        """
        try:
            # Buscar entrevista
            interview = self.get_interview(interview_id)
            if not interview:
                return None
            
            # Buscar mensagens
            messages = self.get_messages(interview_id)
            
            # Calcular progresso
            required_fields = ['contact_name', 'email', 'contact_phone', 'country', 'company', 'experience_level', 'operation_size']
            collected = sum(1 for field in required_fields if interview.get(field))
            total = len(required_fields)
            percentage = int((collected / total) * 100) if total > 0 else 0
            missing_fields = [field for field in required_fields if not interview.get(field)]
            
            progress = {
                'collected': collected,
                'total': total,
                'percentage': percentage,
                'missing_fields': missing_fields
            }
            
            return {
                'interview': interview,
                'messages': messages,
                'progress': progress
            }
            
        except Exception as e:
            logger.error(f"Error getting interview details {interview_id}: {e}")
            raise
    
    async def process_user_message(self, interview_id: str, user_message: str) -> Dict[str, Any]:
        """
        Processa mensagem do usuário (versão simplificada sem agente).
        
        Args:
            interview_id: ID da entrevista
            user_message: Mensagem do usuário
        
        Returns:
            Dict com user_message, agent_response, progress, is_complete
        """
        try:
            # Buscar entrevista
            interview = self.get_interview(interview_id)
            if not interview:
                raise Exception(f"Interview {interview_id} not found")
            
            if interview['status'] == 'completed':
                raise Exception(f"Interview {interview_id} is already completed")
            
            # Salvar mensagem do usuário
            user_msg = self.add_message(
                interview_id=interview_id,
                role='user',
                content=user_message
            )
            
            # Resposta simples do agente (sem IA real por enquanto)
            agent_response_text = "Obrigado pela sua mensagem. Estou processando suas informações."
            
            agent_msg = self.add_message(
                interview_id=interview_id,
                role='assistant',
                content=agent_response_text
            )
            
            # Calcular progresso
            required_fields = ['contact_name', 'email', 'contact_phone', 'country', 'company', 'experience_level', 'operation_size']
            collected = sum(1 for field in required_fields if interview.get(field))
            total = len(required_fields)
            percentage = int((collected / total) * 100) if total > 0 else 0
            missing_fields = [field for field in required_fields if not interview.get(field)]
            
            progress = {
                'collected': collected,
                'total': total,
                'percentage': percentage,
                'missing_fields': missing_fields
            }
            
            is_complete = collected == total
            
            return {
                'user_message': user_msg,
                'agent_response': agent_msg,
                'fields_updated': [],
                'is_complete': is_complete,
                'progress': progress
            }
            
        except Exception as e:
            logger.error(f"Error processing message for interview {interview_id}: {e}")
            raise
