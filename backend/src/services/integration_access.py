"""
Integration Access Layer - Sub-agentes acessam integrações do agente pai
Controla permissões, rate limiting e logs de uso
"""

from typing import Dict, Any, Optional, List
from uuid import UUID
from datetime import datetime, timedelta
import asyncio
from src.config.supabase import supabase_admin
from src.utils.logger import logger
from src.utils.exceptions import PermissionError, ValidationError


class IntegrationAccess:
    """Gerencia acesso de sub-agentes às integrações do agente pai"""
    
    def __init__(self):
        self.supabase = supabase_admin
        self._rate_limits = {}  # Cache de rate limits
    
    async def send_whatsapp(
        self,
        sub_agent_id: UUID,
        phone: str,
        message: str,
        context: Optional[Dict] = None
    ) -> bool:
        """
        Envia mensagem WhatsApp via integração do agente pai
        
        Args:
            sub_agent_id: ID do sub-agente
            phone: Telefone de destino
            message: Mensagem a enviar
            context: Contexto adicional
            
        Returns:
            True se enviado com sucesso
        """
        try:
            # 1. Buscar sub-agente e agente pai
            sub_agent = await self._get_sub_agent(sub_agent_id)
            if not sub_agent:
                raise ValidationError(f"Sub-agente {sub_agent_id} não encontrado")
            
            parent_agent = await self._get_parent_agent(sub_agent['parent_agent_id'])
            if not parent_agent:
                raise ValidationError("Agente pai não encontrado")
            
            # 2. Verificar permissão
            if not await self._has_permission(sub_agent, 'whatsapp'):
                raise PermissionError(f"Sub-agente {sub_agent['name']} não tem permissão para WhatsApp")
            
            # 3. Verificar rate limit
            if not await self._check_rate_limit(sub_agent_id, 'whatsapp'):
                raise ValidationError("Rate limit excedido para WhatsApp")
            
            # 4. Buscar credenciais do agente pai
            integration = await self._get_integration(parent_agent['id'], 'whatsapp')
            if not integration:
                raise ValidationError("Integração WhatsApp não configurada no agente pai")
            
            # 5. Enviar mensagem (mock por enquanto)
            result = await self._send_whatsapp_message(
                credentials=integration.get('credentials', {}),
                phone=phone,
                message=message,
                context=context
            )
            
            # 6. Registrar uso
            await self._log_integration_usage(
                sub_agent_id=sub_agent_id,
                integration_type='whatsapp',
                action='send_message',
                success=result['success'],
                details={
                    'phone': phone,
                    'message_length': len(message),
                    'context': context
                }
            )
            
            return result['success']
            
        except Exception as e:
            logger.error(f"Error sending WhatsApp via sub-agent {sub_agent_id}: {e}")
            
            # Registrar erro
            await self._log_integration_usage(
                sub_agent_id=sub_agent_id,
                integration_type='whatsapp',
                action='send_message',
                success=False,
                error=str(e)
            )
            
            raise
    
    async def send_email(
        self,
        sub_agent_id: UUID,
        to_email: str,
        subject: str,
        body: str,
        context: Optional[Dict] = None
    ) -> bool:
        """Envia email via integração do agente pai"""
        try:
            # Lógica similar ao WhatsApp
            sub_agent = await self._get_sub_agent(sub_agent_id)
            parent_agent = await self._get_parent_agent(sub_agent['parent_agent_id'])
            
            if not await self._has_permission(sub_agent, 'email'):
                raise PermissionError(f"Sub-agente {sub_agent['name']} não tem permissão para Email")
            
            if not await self._check_rate_limit(sub_agent_id, 'email'):
                raise ValidationError("Rate limit excedido para Email")
            
            integration = await self._get_integration(parent_agent['id'], 'email')
            if not integration:
                raise ValidationError("Integração Email não configurada no agente pai")
            
            # Mock de envio de email
            result = await self._send_email_message(
                credentials=integration.get('credentials', {}),
                to_email=to_email,
                subject=subject,
                body=body,
                context=context
            )
            
            await self._log_integration_usage(
                sub_agent_id=sub_agent_id,
                integration_type='email',
                action='send_email',
                success=result['success'],
                details={
                    'to_email': to_email,
                    'subject': subject,
                    'body_length': len(body)
                }
            )
            
            return result['success']
            
        except Exception as e:
            logger.error(f"Error sending email via sub-agent {sub_agent_id}: {e}")
            await self._log_integration_usage(
                sub_agent_id=sub_agent_id,
                integration_type='email',
                action='send_email',
                success=False,
                error=str(e)
            )
            raise
    
    async def access_calendar(
        self,
        sub_agent_id: UUID,
        action: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Acessa calendar via integração do agente pai"""
        try:
            sub_agent = await self._get_sub_agent(sub_agent_id)
            parent_agent = await self._get_parent_agent(sub_agent['parent_agent_id'])
            
            if not await self._has_permission(sub_agent, 'calendar'):
                raise PermissionError(f"Sub-agente {sub_agent['name']} não tem permissão para Calendar")
            
            if not await self._check_rate_limit(sub_agent_id, 'calendar'):
                raise ValidationError("Rate limit excedido para Calendar")
            
            integration = await self._get_integration(parent_agent['id'], 'calendar')
            if not integration:
                raise ValidationError("Integração Calendar não configurada no agente pai")
            
            # Mock de acesso ao calendar
            result = await self._access_calendar_api(
                credentials=integration.get('credentials', {}),
                action=action,
                data=data
            )
            
            await self._log_integration_usage(
                sub_agent_id=sub_agent_id,
                integration_type='calendar',
                action=action,
                success=result['success'],
                details=data
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error accessing calendar via sub-agent {sub_agent_id}: {e}")
            await self._log_integration_usage(
                sub_agent_id=sub_agent_id,
                integration_type='calendar',
                action=action,
                success=False,
                error=str(e)
            )
            raise
    
    async def get_available_integrations(self, sub_agent_id: UUID) -> List[Dict[str, Any]]:
        """Lista integrações disponíveis para um sub-agente"""
        try:
            sub_agent = await self._get_sub_agent(sub_agent_id)
            parent_agent = await self._get_parent_agent(sub_agent['parent_agent_id'])
            
            # Buscar integrações do agente pai
            integrations = await self._get_all_integrations(parent_agent['id'])
            
            # Filtrar por permissões do sub-agente
            available = []
            for integration in integrations:
                if await self._has_permission(sub_agent, integration['type']):
                    available.append({
                        'type': integration['type'],
                        'name': integration['name'],
                        'status': integration['status'],
                        'permissions': sub_agent.get('config', {}).get('integrations', {}).get(integration['type'], {}),
                        'rate_limit': await self._get_rate_limit_status(sub_agent_id, integration['type'])
                    })
            
            return available
            
        except Exception as e:
            logger.error(f"Error getting available integrations for sub-agent {sub_agent_id}: {e}")
            return []
    
    # ============================================================================
    # Métodos Privados
    # ============================================================================
    
    async def _get_sub_agent(self, sub_agent_id: UUID) -> Optional[Dict]:
        """Busca sub-agente por ID"""
        try:
            response = self.supabase.table('sub_agents')\
                .select('*')\
                .eq('id', str(sub_agent_id))\
                .single()\
                .execute()
            
            return response.data if response.data else None
            
        except Exception as e:
            logger.error(f"Error getting sub-agent {sub_agent_id}: {e}")
            return None
    
    async def _get_parent_agent(self, agent_id: str) -> Optional[Dict]:
        """Busca agente pai por ID"""
        try:
            response = self.supabase.table('agents')\
                .select('*')\
                .eq('id', agent_id)\
                .single()\
                .execute()
            
            return response.data if response.data else None
            
        except Exception as e:
            logger.error(f"Error getting parent agent {agent_id}: {e}")
            return None
    
    async def _has_permission(self, sub_agent: Dict, integration_type: str) -> bool:
        """Verifica se sub-agente tem permissão para usar integração"""
        try:
            config = sub_agent.get('config', {})
            integrations_config = config.get('integrations', {})
            integration_config = integrations_config.get(integration_type, {})
            
            # Por padrão, sub-agentes herdam todas as integrações
            return integration_config.get('enabled', True)
            
        except Exception as e:
            logger.error(f"Error checking permission: {e}")
            return False
    
    async def _check_rate_limit(self, sub_agent_id: UUID, integration_type: str) -> bool:
        """Verifica rate limit para sub-agente e integração"""
        try:
            key = f"{sub_agent_id}:{integration_type}"
            now = datetime.now()
            
            # Buscar configuração de rate limit
            rate_config = await self._get_rate_limit_config(sub_agent_id, integration_type)
            
            if not rate_config:
                return True  # Sem rate limit configurado
            
            # Verificar cache
            if key in self._rate_limits:
                last_reset, count = self._rate_limits[key]
                
                # Reset se passou o período
                if now - last_reset > timedelta(seconds=rate_config['period_seconds']):
                    self._rate_limits[key] = (now, 0)
                    count = 0
                
                # Verificar limite
                if count >= rate_config['max_requests']:
                    return False
                
                # Incrementar contador
                self._rate_limits[key] = (last_reset, count + 1)
            else:
                # Primeira requisição
                self._rate_limits[key] = (now, 1)
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking rate limit: {e}")
            return True  # Em caso de erro, permitir
    
    async def _get_rate_limit_config(self, sub_agent_id: UUID, integration_type: str) -> Optional[Dict]:
        """Busca configuração de rate limit"""
        # Por enquanto, rate limits padrão
        defaults = {
            'whatsapp': {'max_requests': 100, 'period_seconds': 3600},  # 100/hora
            'email': {'max_requests': 50, 'period_seconds': 3600},      # 50/hora
            'calendar': {'max_requests': 200, 'period_seconds': 3600}   # 200/hora
        }
        
        return defaults.get(integration_type)
    
    async def _get_integration(self, agent_id: str, integration_type: str) -> Optional[Dict]:
        """Busca integração do agente pai"""
        try:
            # Mock de integrações - em produção, buscar da tabela de integrações
            mock_integrations = {
                'whatsapp': {
                    'type': 'whatsapp',
                    'name': 'WhatsApp Business',
                    'status': 'active',
                    'credentials': {
                        'api_url': 'https://api.whatsapp.com',
                        'token': 'mock_token'
                    }
                },
                'email': {
                    'type': 'email',
                    'name': 'SMTP Email',
                    'status': 'active',
                    'credentials': {
                        'smtp_host': 'smtp.gmail.com',
                        'smtp_port': 587,
                        'username': 'mock@example.com',
                        'password': 'mock_password'
                    }
                },
                'calendar': {
                    'type': 'calendar',
                    'name': 'Google Calendar',
                    'status': 'active',
                    'credentials': {
                        'api_key': 'mock_api_key',
                        'calendar_id': 'primary'
                    }
                }
            }
            
            return mock_integrations.get(integration_type)
            
        except Exception as e:
            logger.error(f"Error getting integration {integration_type} for agent {agent_id}: {e}")
            return None
    
    async def _get_all_integrations(self, agent_id: str) -> List[Dict]:
        """Busca todas as integrações do agente"""
        return [
            await self._get_integration(agent_id, 'whatsapp'),
            await self._get_integration(agent_id, 'email'),
            await self._get_integration(agent_id, 'calendar')
        ]
    
    async def _send_whatsapp_message(self, credentials: Dict, phone: str, message: str, context: Dict) -> Dict:
        """Mock de envio de WhatsApp"""
        # Em produção, usar API real do WhatsApp
        await asyncio.sleep(0.1)  # Simular latência
        
        return {
            'success': True,
            'message_id': f"whatsapp_msg_{datetime.now().timestamp()}",
            'status': 'sent'
        }
    
    async def _send_email_message(self, credentials: Dict, to_email: str, subject: str, body: str, context: Dict) -> Dict:
        """Mock de envio de email"""
        # Em produção, usar SMTP real
        await asyncio.sleep(0.2)  # Simular latência
        
        return {
            'success': True,
            'message_id': f"email_msg_{datetime.now().timestamp()}",
            'status': 'sent'
        }
    
    async def _access_calendar_api(self, credentials: Dict, action: str, data: Dict) -> Dict:
        """Mock de acesso ao calendar"""
        # Em produção, usar Google Calendar API
        await asyncio.sleep(0.1)  # Simular latência
        
        return {
            'success': True,
            'action': action,
            'result': f"calendar_action_{datetime.now().timestamp()}",
            'data': data
        }
    
    async def _log_integration_usage(
        self,
        sub_agent_id: UUID,
        integration_type: str,
        action: str,
        success: bool,
        details: Optional[Dict] = None,
        error: Optional[str] = None
    ):
        """Registra uso de integração"""
        try:
            log_data = {
                'sub_agent_id': str(sub_agent_id),
                'integration_type': integration_type,
                'action': action,
                'success': success,
                'details': details or {},
                'error': error,
                'timestamp': datetime.now().isoformat()
            }
            
            # Por enquanto, apenas log
            logger.info(f"Integration usage: {log_data}")
            
            # Em produção, salvar em tabela de auditoria
            # self.supabase.table('integration_usage_logs').insert(log_data).execute()
            
        except Exception as e:
            logger.error(f"Error logging integration usage: {e}")
    
    async def _get_rate_limit_status(self, sub_agent_id: UUID, integration_type: str) -> Dict:
        """Retorna status do rate limit"""
        key = f"{sub_agent_id}:{integration_type}"
        
        if key in self._rate_limits:
            last_reset, count = self._rate_limits[key]
            config = await self._get_rate_limit_config(sub_agent_id, integration_type)
            
            return {
                'current_count': count,
                'max_requests': config['max_requests'] if config else 0,
                'period_seconds': config['period_seconds'] if config else 0,
                'reset_at': (last_reset + timedelta(seconds=config['period_seconds'])).isoformat() if config else None
            }
        
        return {
            'current_count': 0,
            'max_requests': 0,
            'period_seconds': 0,
            'reset_at': None
        }


# Singleton instance
_integration_access = None

def get_integration_access() -> IntegrationAccess:
    """Retorna instância singleton do IntegrationAccess"""
    global _integration_access
    if _integration_access is None:
        _integration_access = IntegrationAccess()
    return _integration_access

# Global instance for direct import
integration_access = get_integration_access()