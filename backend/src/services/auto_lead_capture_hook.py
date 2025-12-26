"""
Auto Lead Capture Hook - TRACK 2
Event handler que captura leads automaticamente após mensagens de sub-agentes

CRÍTICO: Este hook é executado após cada resposta de sub-agente
para identificar e capturar leads automaticamente.
"""

import asyncio
from typing import Dict, Any, Optional, List
from uuid import UUID
from datetime import datetime

from src.config.supabase import supabase_admin
from src.services.lead_service import lead_service
from src.utils.logger import logger


class AutoLeadCaptureHook:
    """
    Hook que monitora conversas de sub-agentes e captura leads automaticamente
    
    Triggers:
    - Após resposta de sub-agente
    - Quando detecta informações de contato
    - Quando identifica interesse comercial
    """
    
    def __init__(self):
        self.supabase = supabase_admin
        self.lead_service = lead_service
        
        # Padrões que indicam interesse comercial
        self.commercial_intent_patterns = [
            'preço', 'valor', 'custo', 'quanto custa', 'plano', 'assinatura',
            'contratar', 'comprar', 'adquirir', 'orçamento', 'proposta',
            'demonstração', 'demo', 'teste grátis', 'trial',
            'falar com vendedor', 'contato comercial', 'mais informações'
        ]
        
        # Padrões que indicam dados de contato
        self.contact_patterns = [
            'meu email', 'meu telefone', 'meu whatsapp', 'meu contato',
            'me chamo', 'meu nome é', 'sou', 'trabalho na', 'empresa'
        ]
    
    async def process_conversation(
        self,
        sub_agent_id: UUID,
        conversation_id: UUID,
        user_message: str,
        agent_response: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Processa conversa e captura lead se necessário
        
        Args:
            sub_agent_id: ID do sub-agente que respondeu
            conversation_id: ID da conversa
            user_message: Mensagem do usuário
            agent_response: Resposta do agente
            context: Contexto adicional (phone, email, etc)
            
        Returns:
            Dados do lead capturado ou None
        """
        try:
            logger.info(f"Processing conversation for lead capture: {conversation_id}")
            
            # 1. Verificar se já existe lead para esta conversa
            existing_lead = await self._check_existing_lead(conversation_id)
            
            # 2. Analisar se há interesse comercial
            has_commercial_intent = self._detect_commercial_intent(user_message, agent_response)
            
            # 3. Analisar se há dados de contato
            has_contact_data = self._detect_contact_data(user_message) or bool(context)
            
            # 4. Decidir se deve capturar lead
            should_capture = self._should_capture_lead(
                existing_lead, has_commercial_intent, has_contact_data
            )
            
            if not should_capture:
                logger.info(f"Lead capture not needed for conversation {conversation_id}")
                return None
            
            # 5. Capturar lead
            lead_data = await self._capture_lead(
                sub_agent_id=sub_agent_id,
                conversation_id=conversation_id,
                user_message=user_message,
                agent_response=agent_response,
                context=context,
                existing_lead=existing_lead
            )
            
            # 6. Registrar evento de captura
            await self._log_capture_event(
                sub_agent_id=sub_agent_id,
                conversation_id=conversation_id,
                lead_id=lead_data['id'] if lead_data else None,
                trigger_type='auto_capture',
                success=bool(lead_data)
            )
            
            return lead_data
            
        except Exception as e:
            logger.error(f"Error in auto lead capture: {e}")
            
            # Registrar erro
            await self._log_capture_event(
                sub_agent_id=sub_agent_id,
                conversation_id=conversation_id,
                lead_id=None,
                trigger_type='auto_capture',
                success=False,
                error=str(e)
            )
            
            return None
    
    async def process_batch_conversations(
        self,
        conversations: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Processa múltiplas conversas em lote para captura de leads
        
        Args:
            conversations: Lista de conversas para processar
            
        Returns:
            Lista de leads capturados
        """
        try:
            tasks = []
            
            for conv in conversations:
                task = self.process_conversation(
                    sub_agent_id=UUID(conv['sub_agent_id']),
                    conversation_id=UUID(conv['conversation_id']),
                    user_message=conv['user_message'],
                    agent_response=conv['agent_response'],
                    context=conv.get('context')
                )
                tasks.append(task)
            
            # Executar em paralelo
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filtrar sucessos
            captured_leads = [
                result for result in results 
                if result and not isinstance(result, Exception)
            ]
            
            logger.info(f"Batch processed {len(conversations)} conversations, captured {len(captured_leads)} leads")
            
            return captured_leads
            
        except Exception as e:
            logger.error(f"Error in batch lead capture: {e}")
            return []
    
    def _detect_commercial_intent(self, user_message: str, agent_response: str) -> bool:
        """Detecta se há interesse comercial na conversa"""
        try:
            combined_text = f"{user_message} {agent_response}".lower()
            
            # Verificar padrões de interesse comercial
            for pattern in self.commercial_intent_patterns:
                if pattern in combined_text:
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error detecting commercial intent: {e}")
            return False
    
    def _detect_contact_data(self, user_message: str) -> bool:
        """Detecta se usuário forneceu dados de contato"""
        try:
            message_lower = user_message.lower()
            
            # Verificar padrões de dados de contato
            for pattern in self.contact_patterns:
                if pattern in message_lower:
                    return True
            
            # Verificar padrões de email e telefone
            import re
            
            # Email pattern
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if re.search(email_pattern, user_message):
                return True
            
            # Phone pattern (brasileiro)
            phone_patterns = [
                r'\+55\s*\(?(\d{2})\)?\s*\d{4,5}[-\s]?\d{4}',
                r'\(?(\d{2})\)?\s*\d{4,5}[-\s]?\d{4}',
                r'\d{10,11}'
            ]
            
            for pattern in phone_patterns:
                if re.search(pattern, user_message):
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error detecting contact data: {e}")
            return False
    
    def _should_capture_lead(
        self,
        existing_lead: Optional[Dict],
        has_commercial_intent: bool,
        has_contact_data: bool
    ) -> bool:
        """Decide se deve capturar lead baseado nas condições"""
        
        # Se já existe lead, apenas atualizar se houver novos dados
        if existing_lead:
            return has_contact_data  # Atualizar com novos dados de contato
        
        # Para novo lead, precisa de interesse comercial OU dados de contato
        return has_commercial_intent or has_contact_data
    
    async def _check_existing_lead(self, conversation_id: UUID) -> Optional[Dict]:
        """Verifica se já existe lead para esta conversa"""
        try:
            # Buscar em notes ao invés de metadata
            result = self.supabase.table('leads')\
                .select('*')\
                .ilike('notes', f'%{str(conversation_id)}%')\
                .execute()
            
            if result.data:
                return result.data[0]
            
            return None
            
        except Exception as e:
            logger.error(f"Error checking existing lead: {e}")
            return None
    
    async def _capture_lead(
        self,
        sub_agent_id: UUID,
        conversation_id: UUID,
        user_message: str,
        agent_response: str,
        context: Optional[Dict[str, Any]],
        existing_lead: Optional[Dict]
    ) -> Optional[Dict[str, Any]]:
        """Executa a captura do lead"""
        try:
            # Buscar mensagens da conversa para análise completa
            messages = await self._get_conversation_messages(conversation_id)
            
            # Usar o lead_service para capturar
            if existing_lead:
                # Atualizar lead existente
                lead_response = await self.lead_service.capture_from_conversation(
                    conversation_id=str(conversation_id),
                    agent_id=str(sub_agent_id),
                    messages=messages
                )
            else:
                # Criar novo lead
                lead_response = await self.lead_service.capture_from_conversation(
                    conversation_id=str(conversation_id),
                    agent_id=str(sub_agent_id),
                    messages=messages
                )
            
            if lead_response:
                logger.info(f"Lead captured successfully: {lead_response.id}")
                return lead_response.model_dump()
            
            return None
            
        except Exception as e:
            logger.error(f"Error capturing lead: {e}")
            return None
    
    async def _get_conversation_messages(self, conversation_id: UUID) -> List[Dict]:
        """Busca mensagens da conversa"""
        try:
            # Tentar buscar em interview_messages primeiro (tem coluna 'role')
            result = self.supabase.table('interview_messages')\
                .select('role, content, created_at')\
                .eq('interview_id', str(conversation_id))\
                .order('created_at')\
                .execute()
            
            if result.data:
                return [
                    {
                        'role': msg.get('role', 'user'),
                        'content': msg.get('content', ''),
                        'timestamp': msg.get('created_at', '')
                    }
                    for msg in result.data
                ]
            
            # Fallback para messages (usar 'sender' ao invés de 'role')
            result = self.supabase.table('messages')\
                .select('sender, content, created_at')\
                .eq('conversation_id', str(conversation_id))\
                .order('created_at')\
                .execute()
            
            if result.data:
                # Converter 'sender' para 'role'
                return [
                    {
                        'role': 'user' if msg.get('sender') == 'user' else 'assistant',
                        'content': msg.get('content', ''),
                        'timestamp': msg.get('created_at', '')
                    }
                    for msg in result.data
                ]
            
            return []
            
        except Exception as e:
            logger.error(f"Error getting conversation messages: {e}")
            return []
    
    async def _log_capture_event(
        self,
        sub_agent_id: UUID,
        conversation_id: UUID,
        lead_id: Optional[str],
        trigger_type: str,
        success: bool,
        error: Optional[str] = None
    ):
        """Registra evento de captura de lead"""
        try:
            event_data = {
                'sub_agent_id': str(sub_agent_id),
                'conversation_id': str(conversation_id),
                'lead_id': lead_id,
                'trigger_type': trigger_type,
                'success': success,
                'error': error,
                'timestamp': datetime.utcnow().isoformat(),
                'event_type': 'auto_lead_capture'
            }
            
            # Por enquanto, apenas log
            logger.info(f"Lead capture event: {event_data}")
            
            # Em produção, salvar em tabela de eventos
            # self.supabase.table('lead_capture_events').insert(event_data).execute()
            
        except Exception as e:
            logger.error(f"Error logging capture event: {e}")
    
    async def get_capture_stats(self, sub_agent_id: UUID) -> Dict[str, Any]:
        """Retorna estatísticas de captura de leads para um sub-agente"""
        try:
            # Por enquanto, mock de estatísticas
            # Em produção, buscar de tabela de eventos
            
            return {
                'sub_agent_id': str(sub_agent_id),
                'total_conversations': 0,
                'leads_captured': 0,
                'capture_rate': 0.0,
                'last_capture': None,
                'commercial_intent_detected': 0,
                'contact_data_detected': 0
            }
            
        except Exception as e:
            logger.error(f"Error getting capture stats: {e}")
            return {
                'sub_agent_id': str(sub_agent_id),
                'error': str(e)
            }


# Singleton instance
_auto_lead_capture_hook = None

def get_auto_lead_capture_hook() -> AutoLeadCaptureHook:
    """Retorna instância singleton do AutoLeadCaptureHook"""
    global _auto_lead_capture_hook
    if _auto_lead_capture_hook is None:
        _auto_lead_capture_hook = AutoLeadCaptureHook()
    return _auto_lead_capture_hook

# Global instance for direct import
auto_lead_capture_hook = get_auto_lead_capture_hook()