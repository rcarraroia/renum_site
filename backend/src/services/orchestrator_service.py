"""
Orchestrator Service - Sistema de Orquestração Multi-Agente
Responsável por analisar mensagens, identificar tópicos e rotear para sub-agentes.

CRÍTICO: Este é o coração do sistema multi-agente RENUM.
Será replicado para todos os agentes clientes.
"""

import json
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from uuid import UUID
from datetime import datetime

from src.config.supabase import supabase_admin
from src.utils.logger import logger
from src.services.sub_agent_inheritance_service import get_inheritance_service
from src.services.integration_access import get_integration_access
from src.services.auto_lead_capture_hook import get_auto_lead_capture_hook
from src.utils.openrouter_client import OpenRouterClient


class TopicAnalyzer:
    """Analisa tópicos e intenções de mensagens usando LLM"""
    
    def __init__(self):
        self.openrouter = OpenRouterClient()
    
    async def analyze_topics(self, message: str) -> List[Dict[str, Any]]:
        """
        Analisa mensagem e extrai tópicos/intenções relevantes
        
        Returns:
            Lista de tópicos com scores: [{"topic": "vendas", "score": 0.9, "keywords": [...]}]
        """
        try:
            prompt = f"""
Analise a seguinte mensagem e identifique os tópicos/intenções principais.
Retorne APENAS um JSON válido no formato:
[{{"topic": "nome_do_topico", "score": 0.0-1.0, "keywords": ["palavra1", "palavra2"]}}]

Tópicos possíveis: vendas, suporte, precos, planos, tecnico, agendamento, reclamacao, duvida, outros

Mensagem: "{message}"

JSON:"""

            response = await self.openrouter.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-4o-mini",
                max_tokens=500,
                temperature=0.1
            )
            
            content = response.choices[0].message.content.strip()
            
            # Tentar extrair JSON da resposta
            try:
                # Remover possíveis prefixos/sufixos
                if content.startswith('```json'):
                    content = content[7:]
                if content.endswith('```'):
                    content = content[:-3]
                
                topics = json.loads(content.strip())
                
                # Validar estrutura
                if isinstance(topics, list):
                    validated_topics = []
                    for topic in topics:
                        if isinstance(topic, dict) and 'topic' in topic and 'score' in topic:
                            validated_topics.append({
                                'topic': topic['topic'],
                                'score': float(topic.get('score', 0.5)),
                                'keywords': topic.get('keywords', [])
                            })
                    return validated_topics
                
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse topic analysis JSON: {content}")
            
            # Fallback: análise simples por keywords
            return self._fallback_analysis(message)
            
        except Exception as e:
            logger.error(f"Error in topic analysis: {e}")
            return self._fallback_analysis(message)
    
    def _fallback_analysis(self, message: str) -> List[Dict[str, Any]]:
        """Análise de fallback usando keywords simples"""
        message_lower = message.lower()
        
        keyword_map = {
            'vendas': ['preço', 'valor', 'custo', 'comprar', 'vender', 'plano', 'assinatura'],
            'suporte': ['problema', 'erro', 'bug', 'não funciona', 'ajuda', 'suporte'],
            'agendamento': ['agendar', 'marcar', 'reunião', 'horário', 'disponibilidade'],
            'tecnico': ['api', 'integração', 'webhook', 'código', 'desenvolvimento'],
            'duvida': ['como', 'o que', 'quando', 'onde', 'por que', 'dúvida']
        }
        
        topics = []
        for topic, keywords in keyword_map.items():
            matches = [kw for kw in keywords if kw in message_lower]
            if matches:
                score = min(len(matches) * 0.3, 1.0)
                topics.append({
                    'topic': topic,
                    'score': score,
                    'keywords': matches
                })
        
        # Se não encontrou nada, retorna "outros"
        if not topics:
            topics.append({
                'topic': 'outros',
                'score': 0.5,
                'keywords': []
            })
        
        return sorted(topics, key=lambda x: x['score'], reverse=True)


class SubAgentMatcher:
    """Escolhe o melhor sub-agente baseado nos tópicos identificados"""
    
    def __init__(self, supabase_client):
        self.supabase = supabase_client
    
    async def find_best_match(
        self, 
        agent_id: UUID, 
        topics: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Encontra o sub-agente mais adequado para os tópicos identificados
        
        Returns:
            Sub-agente com maior score ou None se nenhum match adequado
        """
        try:
            # Buscar sub-agentes ativos do agente pai
            result = self.supabase.table('sub_agents')\
                .select('*')\
                .eq('parent_agent_id', str(agent_id))\
                .eq('is_active', True)\
                .execute()
            
            if not result.data:
                return None
            
            sub_agents = result.data
            best_match = None
            best_score = 0.0
            
            for sub_agent in sub_agents:
                score = self._calculate_match_score(topics, sub_agent)
                
                if score > best_score and score >= 0.3:  # Threshold mínimo
                    best_score = score
                    best_match = sub_agent
            
            if best_match:
                logger.info(f"Selected sub-agent {best_match['name']} with score {best_score}")
            
            return best_match
            
        except Exception as e:
            logger.error(f"Error finding sub-agent match: {e}")
            return None
    
    def _calculate_match_score(
        self, 
        topics: List[Dict[str, Any]], 
        sub_agent: Dict[str, Any]
    ) -> float:
        """Calcula score de compatibilidade entre tópicos e sub-agente"""
        config = sub_agent.get('config', {})
        sub_agent_topics = config.get('topics', [])
        
        if not sub_agent_topics:
            return 0.0
        
        total_score = 0.0
        topic_weights = 0.0
        
        for topic_data in topics:
            topic = topic_data['topic']
            topic_score = topic_data['score']
            
            # Verificar match exato
            if topic in sub_agent_topics:
                total_score += topic_score * 1.0
                topic_weights += topic_score
            else:
                # Verificar match parcial (keywords)
                for sub_topic in sub_agent_topics:
                    if topic in sub_topic.lower() or sub_topic.lower() in topic:
                        total_score += topic_score * 0.7
                        topic_weights += topic_score * 0.7
                        break
        
        # Normalizar score
        if topic_weights > 0:
            return min(total_score / topic_weights, 1.0)
        
        return 0.0


class DelegationManager:
    """Gerencia delegação de conversas para sub-agentes"""
    
    def __init__(self, supabase_client):
        self.supabase = supabase_client
        self.openrouter = OpenRouterClient()
        self.inheritance_service = get_inheritance_service()
        self.integration_access = get_integration_access()
        self.lead_capture_hook = get_auto_lead_capture_hook()
    
    async def delegate_to_sub_agent(
        self,
        sub_agent: Dict[str, Any],
        message: str,
        conversation_id: UUID,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Delega conversa para sub-agente específico
        
        Returns:
            Resposta do sub-agente formatada
        """
        try:
            # 1. Carregar configuração efetiva do sub-agente
            effective_config = await self._get_effective_config(sub_agent)
            
            # 2. Preparar contexto da conversa
            conversation_context = await self._prepare_context(conversation_id, context)
            
            # 3. Gerar resposta usando sub-agente
            response = await self._generate_sub_agent_response(
                effective_config,
                message,
                conversation_context
            )
            
            # 4. Executar auto lead capture hook
            lead_data = await self.lead_capture_hook.process_conversation(
                sub_agent_id=UUID(sub_agent['id']),
                conversation_id=conversation_id,
                user_message=message,
                agent_response=response,
                context=context
            )
            
            # 5. Verificar se sub-agente precisa usar integrações
            integration_actions = await self._check_integration_needs(
                sub_agent, message, response, context
            )
            
            # 6. Executar ações de integração se necessário
            integration_results = []
            if integration_actions:
                integration_results = await self._execute_integrations(
                    sub_agent_id=UUID(sub_agent['id']),
                    actions=integration_actions,
                    context=context
                )
            
            # 7. Registrar delegação no histórico
            await self._log_delegation(
                sub_agent['id'], 
                conversation_id, 
                message, 
                response,
                lead_data,
                integration_results
            )
            
            return {
                'message': response,
                'sub_agent_id': sub_agent['id'],
                'sub_agent_name': sub_agent['name'],
                'delegated': True,
                'lead_captured': bool(lead_data),
                'lead_data': lead_data,
                'integrations_used': len(integration_results),
                'integration_results': integration_results,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error delegating to sub-agent: {e}")
            # Fallback: retornar erro para orquestrador lidar
            raise
    
    async def _get_effective_config(self, sub_agent: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula configuração efetiva com herança"""
        try:
            # Buscar agente pai
            parent_result = self.supabase.table('agents')\
                .select('config')\
                .eq('id', sub_agent['parent_agent_id'])\
                .single()\
                .execute()
            
            parent_config = parent_result.data.get('config', {})
            sub_agent_config = sub_agent.get('config', {})
            inheritance_config = sub_agent.get('inheritance_config', {})
            
            # Aplicar herança
            effective_config = self.inheritance_service.calculate_effective_config(
                parent_config,
                sub_agent_config,
                inheritance_config
            )
            
            return effective_config
            
        except Exception as e:
            logger.error(f"Error calculating effective config: {e}")
            return sub_agent.get('config', {})
    
    async def _prepare_context(
        self, 
        conversation_id: UUID, 
        additional_context: Dict[str, Any] = None
    ) -> str:
        """Prepara contexto da conversa para o sub-agente"""
        try:
            # Buscar mensagens recentes da conversa
            messages_result = self.supabase.table('interview_messages')\
                .select('role, content, timestamp')\
                .eq('interview_id', str(conversation_id))\
                .order('timestamp', desc=False)\
                .limit(10)\
                .execute()
            
            messages = messages_result.data or []
            
            # Formatar histórico
            context_parts = []
            if messages:
                context_parts.append("Histórico da conversa:")
                for msg in messages[-5:]:  # Últimas 5 mensagens
                    role = "Usuário" if msg['role'] == 'user' else "Assistente"
                    context_parts.append(f"{role}: {msg['content']}")
            
            # Adicionar contexto adicional
            if additional_context:
                context_parts.append(f"Contexto adicional: {json.dumps(additional_context, ensure_ascii=False)}")
            
            return "\n".join(context_parts)
            
        except Exception as e:
            logger.error(f"Error preparing context: {e}")
            return ""
    
    async def _generate_sub_agent_response(
        self,
        config: Dict[str, Any],
        message: str,
        context: str
    ) -> str:
        """Gera resposta usando configuração do sub-agente"""
        try:
            identity = config.get('identity', {})
            system_prompt = identity.get('system_prompt', 'Você é um assistente útil.')
            model = config.get('model', 'gpt-4o-mini')
            
            # Construir prompt completo
            full_prompt = system_prompt
            if context:
                full_prompt += f"\n\nContexto da conversa:\n{context}"
            
            messages = [
                {"role": "system", "content": full_prompt},
                {"role": "user", "content": message}
            ]
            
            response = await self.openrouter.chat_completion(
                messages=messages,
                model=model,
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating sub-agent response: {e}")
            return "Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente."
    
    async def _check_integration_needs(
        self,
        sub_agent: Dict[str, Any],
        user_message: str,
        agent_response: str,
        context: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Verifica se sub-agente precisa usar integrações baseado na resposta
        
        Returns:
            Lista de ações de integração necessárias
        """
        try:
            actions = []
            response_lower = agent_response.lower()
            
            # Detectar necessidade de envio de WhatsApp
            whatsapp_triggers = [
                'vou enviar por whatsapp', 'enviarei no whatsapp', 
                'te mando no zap', 'mando no whatsapp'
            ]
            
            if any(trigger in response_lower for trigger in whatsapp_triggers):
                if context and context.get('phone'):
                    actions.append({
                        'type': 'whatsapp',
                        'action': 'send_message',
                        'data': {
                            'phone': context['phone'],
                            'message': agent_response
                        }
                    })
            
            # Detectar necessidade de envio de email
            email_triggers = [
                'vou enviar por email', 'enviarei por email',
                'te mando por email', 'mando no email'
            ]
            
            if any(trigger in response_lower for trigger in email_triggers):
                if context and context.get('email'):
                    actions.append({
                        'type': 'email',
                        'action': 'send_email',
                        'data': {
                            'to_email': context['email'],
                            'subject': 'Informações solicitadas',
                            'body': agent_response
                        }
                    })
            
            # Detectar necessidade de agendamento
            calendar_triggers = [
                'vamos agendar', 'marcar reunião', 'agendar horário',
                'disponibilidade', 'marcar um horário'
            ]
            
            if any(trigger in response_lower for trigger in calendar_triggers):
                actions.append({
                    'type': 'calendar',
                    'action': 'check_availability',
                    'data': {
                        'requested_by': context.get('phone') or context.get('email'),
                        'context': user_message
                    }
                })
            
            return actions
            
        except Exception as e:
            logger.error(f"Error checking integration needs: {e}")
            return []
    
    async def _execute_integrations(
        self,
        sub_agent_id: UUID,
        actions: List[Dict[str, Any]],
        context: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Executa ações de integração para o sub-agente"""
        try:
            results = []
            
            for action in actions:
                try:
                    if action['type'] == 'whatsapp':
                        result = await self.integration_access.send_whatsapp(
                            sub_agent_id=sub_agent_id,
                            phone=action['data']['phone'],
                            message=action['data']['message'],
                            context=context
                        )
                        results.append({
                            'type': 'whatsapp',
                            'success': result,
                            'action': action['action']
                        })
                    
                    elif action['type'] == 'email':
                        result = await self.integration_access.send_email(
                            sub_agent_id=sub_agent_id,
                            to_email=action['data']['to_email'],
                            subject=action['data']['subject'],
                            body=action['data']['body'],
                            context=context
                        )
                        results.append({
                            'type': 'email',
                            'success': result,
                            'action': action['action']
                        })
                    
                    elif action['type'] == 'calendar':
                        result = await self.integration_access.access_calendar(
                            sub_agent_id=sub_agent_id,
                            action=action['action'],
                            data=action['data']
                        )
                        results.append({
                            'type': 'calendar',
                            'success': result.get('success', False),
                            'action': action['action'],
                            'data': result
                        })
                    
                except Exception as e:
                    logger.error(f"Error executing integration {action['type']}: {e}")
                    results.append({
                        'type': action['type'],
                        'success': False,
                        'error': str(e),
                        'action': action['action']
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"Error executing integrations: {e}")
            return []

    async def _log_delegation(
        self,
        sub_agent_id: str,
        conversation_id: UUID,
        user_message: str,
        agent_response: str,
        lead_data: Optional[Dict] = None,
        integration_results: Optional[List[Dict]] = None
    ):
        """Registra delegação no histórico"""
        try:
            log_data = {
                'sub_agent_id': sub_agent_id,
                'conversation_id': str(conversation_id),
                'user_message': user_message[:500],  # Truncar se muito longo
                'agent_response': agent_response[:1000],
                'lead_captured': bool(lead_data),
                'lead_id': lead_data.get('id') if lead_data else None,
                'integrations_used': len(integration_results) if integration_results else 0,
                'integration_results': integration_results or [],
                'timestamp': datetime.utcnow().isoformat(),
                'success': True
            }
            
            # Salvar em tabela de logs (criar se não existir)
            # Por enquanto, apenas log no sistema
            logger.info(f"Delegation logged: {json.dumps(log_data, ensure_ascii=False)}")
            
        except Exception as e:
            logger.error(f"Error logging delegation: {e}")


class OrchestratorService:
    """
    Serviço principal de orquestração multi-agente
    
    Responsável por:
    1. Analisar mensagens recebidas
    2. Identificar tópicos/intenções
    3. Escolher sub-agente apropriado
    4. Delegar conversa ou responder diretamente
    """
    
    def __init__(self):
        self.supabase = supabase_admin
        self.topic_analyzer = TopicAnalyzer()
        self.sub_agent_matcher = SubAgentMatcher(self.supabase)
        self.delegation_manager = DelegationManager(self.supabase)
        self.openrouter = OpenRouterClient()
    
    async def process_message(
        self,
        agent_id: UUID,
        message: str,
        conversation_id: UUID,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Processa mensagem através do sistema de orquestração
        
        Args:
            agent_id: ID do agente principal (RENUS ou cliente)
            message: Mensagem do usuário
            conversation_id: ID da conversa/interview
            context: Contexto adicional (perfil do usuário, etc)
            
        Returns:
            Resposta formatada com informações de roteamento
        """
        try:
            logger.info(f"Processing message for agent {agent_id}: {message[:100]}...")
            
            # 1. Analisar tópicos da mensagem
            topics = await self.topic_analyzer.analyze_topics(message)
            logger.info(f"Identified topics: {topics}")
            
            # 2. Buscar melhor sub-agente
            best_sub_agent = await self.sub_agent_matcher.find_best_match(agent_id, topics)
            
            # 3. Decidir roteamento
            if best_sub_agent:
                # Delegar para sub-agente
                logger.info(f"Delegating to sub-agent: {best_sub_agent['name']}")
                return await self.delegation_manager.delegate_to_sub_agent(
                    best_sub_agent,
                    message,
                    conversation_id,
                    context
                )
            else:
                # Responder com agente principal
                logger.info("No suitable sub-agent found, using main agent")
                return await self._main_agent_response(agent_id, message, conversation_id, context)
                
        except Exception as e:
            logger.error(f"Error in orchestrator: {e}")
            # Fallback para agente principal
            return await self._main_agent_response(agent_id, message, conversation_id, context)
    
    async def _main_agent_response(
        self,
        agent_id: UUID,
        message: str,
        conversation_id: UUID,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Gera resposta usando o agente principal (fallback)"""
        try:
            # Buscar configuração do agente principal
            agent_result = self.supabase.table('agents')\
                .select('name, config')\
                .eq('id', str(agent_id))\
                .single()\
                .execute()
            
            agent_data = agent_result.data
            config = agent_data.get('config', {})
            identity = config.get('identity', {})
            
            system_prompt = identity.get('system_prompt', 
                f"Você é {agent_data['name']}, um assistente inteligente e útil.")
            model = config.get('model', 'gpt-4o-mini')
            
            # Preparar contexto
            context_str = ""
            if context:
                context_str = f"Contexto: {json.dumps(context, ensure_ascii=False)}\n"
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{context_str}Mensagem: {message}"}
            ]
            
            response = await self.openrouter.chat_completion(
                messages=messages,
                model=model,
                max_tokens=1000,
                temperature=0.7
            )
            
            return {
                'message': response.choices[0].message.content.strip(),
                'sub_agent_id': None,
                'sub_agent_name': None,
                'delegated': False,
                'main_agent': agent_data['name'],
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in main agent response: {e}")
            return {
                'message': "Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente em alguns instantes.",
                'sub_agent_id': None,
                'sub_agent_name': None,
                'delegated': False,
                'error': True,
                'timestamp': datetime.utcnow().isoformat()
            }
    
    async def get_orchestration_stats(self, agent_id: UUID) -> Dict[str, Any]:
        """Retorna estatísticas de orquestração para o agente"""
        try:
            # Buscar sub-agentes
            sub_agents_result = self.supabase.table('sub_agents')\
                .select('id, name, is_active')\
                .eq('parent_agent_id', str(agent_id))\
                .execute()
            
            sub_agents = sub_agents_result.data or []
            
            return {
                'agent_id': str(agent_id),
                'total_sub_agents': len(sub_agents),
                'active_sub_agents': len([sa for sa in sub_agents if sa['is_active']]),
                'sub_agents': sub_agents,
                'orchestration_enabled': True,
                'last_updated': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting orchestration stats: {e}")
            return {
                'agent_id': str(agent_id),
                'error': str(e),
                'orchestration_enabled': False
            }


# Singleton instance
_orchestrator_service = None

def get_orchestrator_service() -> OrchestratorService:
    """Retorna instância singleton do OrchestratorService"""
    global _orchestrator_service
    if _orchestrator_service is None:
        _orchestrator_service = OrchestratorService()
    return _orchestrator_service

# Global instance for direct import
orchestrator_service = get_orchestrator_service()