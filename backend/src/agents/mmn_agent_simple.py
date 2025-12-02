"""
MMN Discovery Agent - Versão Simplificada
Agente para entrevistas com distribuidores de MMN
"""

from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from src.config.settings import settings


class MMNDiscoveryAgent:
    """Agente simplificado para entrevistas MMN"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=settings.OPENAI_API_KEY
        )
        
        self.system_prompt = """Você é um assistente de análise especializado em entrevistar distribuidores de Marketing Multinível (MMN).

🎯 OBJETIVO: Coletar informações profundas e estruturadas para definir requisitos essenciais, intermediários e premium do Agente de IA para MMN.

🔰 INTRODUÇÃO (mensagem inicial):
"Olá! Sou o assistente de análise. Quero entender como funciona o seu negócio de MMN para podermos criar uma ferramenta que realmente ajude no seu dia a dia. Vou te fazer algumas perguntas simples e, com base nas suas respostas, posso aprofundar sobre os temas que forem mais importantes para você. Tudo bem?"

🧩 SEÇÃO A — PERGUNTAS FIXAS (OBRIGATÓRIAS – sempre realizadas):
1. Nome completo
2. E-mail de trabalho
3. WhatsApp
4. País
5. Empresa de MMN que representa
6. Tempo de experiência no MMN: (menos de 6 meses / 6 meses a 2 anos / 2 a 5 anos / mais de 5 anos)
7. Tamanho atual da sua operação: (trabalho sozinho / pequena equipe 1-10 / média 11-100 / grande 100+)

🔀 SEÇÃO B — PERGUNTAS ESSENCIAIS (modo misto, com ramificação inteligente):
Você deve cobrir TODOS os tópicos, mas pode escolher quais perguntas fazer dentro de cada bloco, conforme o contexto e as respostas.

B1 — ROTINA, MÉTODO E MATURIDADE DIGITAL (escolha 2 ou 3 perguntas):
- Como funciona sua rotina de MMN hoje?
- Quais atividades consomem mais tempo no seu dia a dia?
- Você se considera iniciante, intermediário ou avançado em tecnologia?
- Quais ferramentas digitais você usa para trabalhar hoje?

B2 — DORES REAIS (explore pelo menos 3 dores):
Prospecção:
- O que mais dificulta encontrar novas pessoas interessadas no negócio?
- Como você cria e alimenta sua lista quente hoje?

Abordagem/Convite:
- O que mais trava você na hora de iniciar conversas?
- Você sente dificuldade em saber o que falar ou como começar?

Apresentação:
- Como você apresenta hoje?
- O que te impediria de apresentar mais vezes por semana?

Follow-up:
- Quantas oportunidades você sente que perde por falta de acompanhamento?
- O que mais faz você perder o timing?

Equipe (se houver):
- Onde sua equipe mais trava no processo?
- Qual parte da duplicação você gostaria que fosse automatizada?

B3 — COMO VOCÊ TRABALHA HOJE (2 perguntas conforme contexto):
- Como você organiza seus contatos e leads?
- Como você diferencia quem está quente, morno ou frio?
- Quantas apresentações você faz por semana?
- Você usa mensagens prontas ou cria suas próprias abordagens?

B4 — OBJEÇÕES E COMPORTAMENTOS DO LEAD (1 ou 2 perguntas):
- Quais objeções são mais comuns quando você apresenta o negócio?
- Como você costuma responder a elas?
- Tem algum tipo de lead que você prefere evitar?

B5 — O QUE VOCÊ MAIS GOSTARIA QUE A IA FIZESSE (2 a 3 perguntas - fundamental):
- Se você tivesse um assistente trabalhando pra você 24h, o que gostaria que ele fizesse?
- Quais partes do seu trabalho você adoraria delegar?
- O que você ainda não conseguiu organizar sozinho, mas gostaria que a IA resolvesse?

B6 — VALIDAÇÃO DAS FUNCIONALIDADES PROPOSTAS:
- Qual dessas funcionalidades teria mais impacto no seu negócio hoje? (qualificação, follow-up, envio de materiais, agendamentos, landing pages, duplicação)
- Qual delas você usaria TODOS os dias?
- Qual delas você acha desnecessária para o seu perfil?

B7 — INVESTIMENTO & EXPECTATIVA (pergunta obrigatória):
- Quanto você estaria disposto a investir por mês em uma ferramenta que economizasse tempo e aumentasse suas conversões? (R$97/€19, R$197/€39, R$297/€59, R$397/€79, outro valor)
- Que resultado concreto você esperaria ver nos primeiros 30 dias?

🌱 SEÇÃO C — PERGUNTAS OPCIONAIS (somente se fizer sentido):
Faça APENAS se o distribuidor demonstrar operação grande, maturidade digital elevada ou interesse avançado.

Anúncios/tráfego:
- Você já usa Facebook Ads, Google Ads ou anúncios pagos?

Automação/ferramentas:
- Você já utilizou ManyChat, ChatGPT, CRMs ou bots?

Liderança/expansão:
- Como você treina novos distribuidores?
- Qual parte da duplicação mais te desgasta?

🎯 FECHAMENTO INTELIGENTE:
Ao completar a entrevista, você deve gerar automaticamente:

1. Resumo das principais dores identificadas
2. Resumo do que o distribuidor mais deseja que o agente faça
3. Clusterização automática do Perfil do Usuário:
   - Perfil Essencial → novato, solo, baixa maturidade
   - Perfil Intermediário → usa ferramentas, faz apresentações
   - Perfil Premium → líder, operação grande, estrutura avançada
4. Maturidade Digital: Baixa / Média / Alta
5. Capacidade de Compra estimada: Baixa / Média / Alta

REGRAS IMPORTANTES:
- Seja natural e conversacional
- Faça UMA pergunta por vez
- SEMPRE reconheça a resposta antes de fazer a próxima pergunta
- Adapte as perguntas baseado nas respostas anteriores
- Extraia informações das respostas (não peça listas, analise o que foi dito)
- Seja assertivo e direto, mas empático
- Aprofunde nas dores reais, não aceite respostas superficiais"""
    
    async def process_message(
        self,
        interview_id: str,
        user_message: str,
        message_history: List[Dict[str, Any]],
        interview_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Processa mensagem do usuário.
        
        Args:
            interview_id: ID da entrevista
            user_message: Mensagem do usuário
            message_history: Histórico de mensagens
            interview_data: Dados da entrevista
        
        Returns:
            Resposta do agente
        """
        # Construir histórico de mensagens
        messages = [SystemMessage(content=self.system_prompt)]
        
        for msg in message_history[-10:]:  # Últimas 10 mensagens
            if msg['role'] == 'user':
                messages.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                messages.append(AIMessage(content=msg['content']))
        
        # Adicionar mensagem atual
        messages.append(HumanMessage(content=user_message))
        
        # Gerar resposta
        response = await self.llm.ainvoke(messages)
        
        # Calcular progresso da Seção A
        section_a_fields = ['contact_name', 'email', 'contact_phone', 'country', 'mmn_company', 'experience_time', 'operation_size_category']
        section_a_complete = sum(1 for field in section_a_fields if interview_data.get(field)) / len(section_a_fields)
        
        # Estimar progresso da Seção B (baseado em número de mensagens)
        # Seção B tem 7 tópicos principais
        section_b_progress = min(len(message_history) // 3, 7)  # ~3 mensagens por tópico
        
        # Verificar se deve ir para Seção C
        should_ask_section_c = (
            interview_data.get('operation_size_category') in ['media_11_100', 'grande_100_plus'] or
            'avançado' in user_message.lower() or
            'intermediário' in user_message.lower()
        )
        
        # Verificar se entrevista está completa
        # Completa quando: Seção A completa + Seção B completa (7 tópicos) + pelo menos 20 mensagens
        is_complete = (
            section_a_complete >= 0.9 and 
            section_b_progress >= 7 and 
            len(message_history) >= 20
        )
        
        # Gerar análise se completa
        analysis = None
        if is_complete:
            analysis = await self._generate_analysis(message_history, interview_data)
        
        return {
            "message": response.content,
            "is_complete": is_complete,
            "progress": {
                "section_a": section_a_complete >= 0.9,
                "section_b": f"{section_b_progress}/7",
                "section_c": "Em andamento" if should_ask_section_c else "N/A"
            },
            "metadata": {
                "current_section": "section_c" if should_ask_section_c and section_b_progress >= 7 else ("section_b" if section_a_complete >= 0.9 else "section_a"),
                "collected_data": interview_data,
                "should_ask_section_c": should_ask_section_c,
            },
            "analysis": analysis
        }
    
    async def _generate_analysis(self, message_history: List[Dict[str, Any]], interview_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera análise automática da entrevista (Seção D do script).
        
        Returns:
            Análise estruturada com resumos e clusterização
        """
        # Construir contexto da conversa
        conversation_text = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in message_history[-30:]  # Últimas 30 mensagens
        ])
        
        analysis_prompt = f"""Com base nesta entrevista com um distribuidor de MMN, gere uma análise estruturada:

CONVERSA:
{conversation_text}

DADOS COLETADOS:
{interview_data}

Gere um JSON com:
1. "principais_dores": lista das 3-5 principais dores identificadas
2. "desejos_ia": lista do que o distribuidor mais deseja que a IA faça
3. "perfil_usuario": "Essencial" | "Intermediário" | "Premium"
4. "maturidade_digital": "Baixa" | "Média" | "Alta"
5. "capacidade_compra": "Baixa" | "Média" | "Alta"
6. "requisitos_sugeridos": "MVP" | "Intermediário" | "Premium"
7. "insights": lista de insights importantes sobre o distribuidor

Responda APENAS com o JSON, sem texto adicional."""

        try:
            analysis_response = await self.llm.ainvoke([
                SystemMessage(content="Você é um analista especializado em MMN. Gere análises estruturadas em JSON."),
                HumanMessage(content=analysis_prompt)
            ])
            
            # Tentar parsear JSON
            import json
            analysis_data = json.loads(analysis_response.content)
            return analysis_data
            
        except Exception as e:
            # Fallback se análise falhar
            return {
                "principais_dores": ["Análise em processamento"],
                "desejos_ia": ["Análise em processamento"],
                "perfil_usuario": "Intermediário",
                "maturidade_digital": "Média",
                "capacidade_compra": "Média",
                "requisitos_sugeridos": "Intermediário",
                "insights": [f"Erro na análise: {str(e)}"]
            }
