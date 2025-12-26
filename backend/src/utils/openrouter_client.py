"""
OpenRouter Client - Cliente para API do OpenRouter
Usado pelo OrchestratorService para análise de tópicos e geração de respostas
"""

import httpx
import json
from typing import Dict, Any, List
from src.config.settings import settings
from src.utils.logger import logger


class OpenRouterClient:
    """Cliente para comunicação com OpenRouter API"""
    
    def __init__(self):
        self.base_url = "https://openrouter.ai/api/v1"
        self.openrouter_key = getattr(settings, 'OPENROUTER_API_KEY', None)
        self.openai_key = getattr(settings, 'OPENAI_API_KEY', None)
        
        # Usar OpenAI diretamente se OpenRouter não estiver configurado
        if not self.openrouter_key and self.openai_key:
            self.api_key = self.openai_key
            self.base_url = "https://api.openai.com/v1"
            self.use_openai = True
            logger.info("Using OpenAI API directly")
        elif self.openrouter_key:
            self.api_key = self.openrouter_key
            self.base_url = "https://openrouter.ai/api/v1"
            self.use_openai = False
            logger.info("Using OpenRouter API")
        else:
            self.api_key = None
            self.use_openai = False
            logger.warning("Neither OPENROUTER_API_KEY nor OPENAI_API_KEY configured")
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini",
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> Any:
        """
        Faz chamada para chat completion
        
        Args:
            messages: Lista de mensagens no formato OpenAI
            model: Modelo a usar (gpt-4o-mini, gpt-4o, claude-3-5-sonnet, etc)
            max_tokens: Máximo de tokens na resposta
            temperature: Criatividade (0.0 - 1.0)
            
        Returns:
            Resposta da API no formato OpenAI
        """
        if not self.api_key:
            # Fallback para resposta mock em desenvolvimento
            return self._mock_response(messages[-1]['content'])
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Adicionar headers específicos do OpenRouter se não for OpenAI direto
            if not self.use_openai:
                headers.update({
                    "HTTP-Referer": "https://renum.com.br",
                    "X-Title": "RENUM Multi-Agent System"
                })
            
            # Mapear modelo para OpenAI se necessário
            if self.use_openai:
                model = self._map_model_to_openai(model)
            
            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                **kwargs
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPError as e:
            logger.error(f"API HTTP error: {e}")
            return self._mock_response(messages[-1]['content'])
        except Exception as e:
            logger.error(f"API error: {e}")
            return self._mock_response(messages[-1]['content'])
    
    def _mock_response(self, user_message: str) -> Dict[str, Any]:
        """Resposta mock para desenvolvimento/fallback"""
        
        # Análise simples para mock
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ['preço', 'valor', 'custo', 'plano']):
            mock_content = "Entendo que você tem interesse em nossos planos. Posso ajudar com informações sobre preços e funcionalidades."
        elif any(word in message_lower for word in ['problema', 'erro', 'não funciona']):
            mock_content = "Vejo que você está enfrentando um problema técnico. Vou ajudar você a resolver isso."
        elif any(word in message_lower for word in ['agendar', 'reunião', 'horário']):
            mock_content = "Posso ajudar você a agendar uma reunião. Qual seria o melhor horário para você?"
        else:
            mock_content = "Obrigado por sua mensagem. Como posso ajudar você hoje?"
        
        return {
            "choices": [{
                "message": {
                    "content": mock_content,
                    "role": "assistant"
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": len(user_message.split()),
                "completion_tokens": len(mock_content.split()),
                "total_tokens": len(user_message.split()) + len(mock_content.split())
            },
            "model": "mock-model"
        }
    
    async def analyze_intent(self, message: str) -> Dict[str, Any]:
        """
        Analisa intenção específica de uma mensagem
        Método especializado para análise de tópicos
        """
        prompt = f"""
Analise a intenção da seguinte mensagem e classifique em uma das categorias:
- vendas (interesse em comprar, preços, planos)
- suporte (problemas técnicos, bugs, ajuda)
- agendamento (marcar reunião, horários)
- informacao (dúvidas gerais, como funciona)
- outros (não se encaixa nas anteriores)

Mensagem: "{message}"

Responda apenas com o nome da categoria.
"""
        
        try:
            response = await self.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-4o-mini",
                max_tokens=50,
                temperature=0.1
            )
            
            intent = response['choices'][0]['message']['content'].strip().lower()
            
            # Validar resposta
            valid_intents = ['vendas', 'suporte', 'agendamento', 'informacao', 'outros']
            if intent in valid_intents:
                return {"intent": intent, "confidence": 0.8}
            else:
                return {"intent": "outros", "confidence": 0.3}
                
        except Exception as e:
            logger.error(f"Error analyzing intent: {e}")
            return {"intent": "outros", "confidence": 0.1}
    
    def _map_model_to_openai(self, model: str) -> str:
        """Mapeia modelos para nomes corretos da OpenAI"""
        model_mapping = {
            "gpt-4o-mini": "gpt-4o-mini",
            "gpt-4o": "gpt-4o",
            "gpt-4": "gpt-4",
            "gpt-3.5-turbo": "gpt-3.5-turbo",
            "claude-3-5-sonnet": "gpt-4o-mini",  # Fallback para OpenAI
        }
        
        return model_mapping.get(model, "gpt-4o-mini")