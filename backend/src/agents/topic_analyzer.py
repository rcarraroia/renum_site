"""
Topic Analyzer - Sprint 09
Analyzes message topics and routes to appropriate sub-agents using LLM
"""

from typing import Optional, List
import json

from src.utils.logger import logger


class TopicAnalyzer:
    """
    Analyzes message topics and finds matching sub-agents
    
    Uses LLM to understand message intent and match with sub-agent topics
    """
    
    def __init__(self):
        """Initialize topic analyzer"""
        self.llm_client = None  # TODO: Initialize LLM client (OpenRouter)
    
    async def analyze_topic(self, message: str, available_topics: List[str]) -> Optional[str]:
        """
        Analyze message and determine which topic it belongs to (Sprint 09 - E.3)
        
        Uses LLM to understand message intent and match with available topics
        
        Args:
            message: User message
            available_topics: List of available topics from sub-agents
            
        Returns:
            Matched topic or None if no match
        """
        try:
            if not available_topics:
                logger.info("No topics available for matching")
                return None
            
            # Try LLM-based analysis first
            if self.llm_client:
                topic = await self.analyze_topic_with_llm(message, available_topics)
                if topic and topic != "none":
                    return topic
            
            # Fallback to keyword matching
            message_lower = message.lower()
            
            for topic in available_topics:
                topic_lower = topic.lower()
                # Check if topic is in message (exact or partial match)
                if topic_lower in message_lower or any(
                    word in message_lower for word in topic_lower.split()
                ):
                    logger.info(f"Matched topic '{topic}' in message (keyword match)")
                    return topic
            
            logger.info("No topic match found")
            return None
            
        except Exception as e:
            logger.error(f"Error analyzing topic: {e}")
            return None
    
    async def analyze_topic_with_llm(
        self, 
        message: str, 
        available_topics: List[str]
    ) -> Optional[str]:
        """
        Analyze message using LLM to determine topic (Sprint 09 - E.3)
        
        Uses OpenRouter/OpenAI to intelligently match message to topics
        
        Args:
            message: User message
            available_topics: List of available topics
            
        Returns:
            Matched topic or None
        """
        try:
            if not available_topics:
                return None
            
            # Prepare prompt for LLM
            prompt = f"""Analyze the following user message and determine which topic it belongs to.

Available topics:
{json.dumps(available_topics, indent=2)}

User message: "{message}"

Instructions:
- Return ONLY the matching topic name from the list above
- If no topic matches, return "none"
- Be precise and consider context
- Consider synonyms and related terms

Topic:"""
            
            # Initialize LLM client if not done
            if not self.llm_client:
                from langchain_openai import ChatOpenAI
                from src.config.settings import settings
                
                self.llm_client = ChatOpenAI(
                    model="gpt-4o-mini",  # Fast and cheap for topic analysis
                    temperature=0.0,  # Deterministic
                    api_key=settings.OPENAI_API_KEY
                )
            
            # Call LLM
            from langchain_core.messages import HumanMessage
            
            response = await self.llm_client.ainvoke([HumanMessage(content=prompt)])
            topic = response.content.strip().lower()
            
            # Validate response
            if topic == "none":
                logger.info("LLM returned 'none' - no topic match")
                return None
            
            # Check if returned topic is in available topics (case-insensitive)
            for available_topic in available_topics:
                if available_topic.lower() == topic:
                    logger.info(f"LLM matched topic: '{available_topic}'")
                    return available_topic
            
            logger.warning(f"LLM returned invalid topic: '{topic}'")
            return None
            
        except Exception as e:
            logger.error(f"Error analyzing topic with LLM: {e}")
            return None
    
    def find_subagent_by_topic(
        self, 
        topic: str, 
        sub_agents: List[dict]
    ) -> Optional[dict]:
        """
        Find sub-agent that handles a specific topic
        
        Args:
            topic: Topic to match
            sub_agents: List of sub-agent data
            
        Returns:
            Matching sub-agent or None
        """
        try:
            for sub_agent in sub_agents:
                topics = sub_agent.get('topics', [])
                if topics and topic in topics:
                    logger.info(
                        f"Found sub-agent '{sub_agent['name']}' for topic '{topic}'"
                    )
                    return sub_agent
            
            logger.info(f"No sub-agent found for topic '{topic}'")
            return None
            
        except Exception as e:
            logger.error(f"Error finding sub-agent by topic: {e}")
            return None
    
    async def route_message(
        self, 
        message: str, 
        agent_data: dict, 
        sub_agents: List[dict]
    ) -> dict:
        """
        Route message to appropriate agent or sub-agent
        
        Args:
            message: User message
            agent_data: Main agent data
            sub_agents: List of sub-agents
            
        Returns:
            Dict with routing decision
        """
        try:
            # Extract topics from sub-agents
            all_topics = []
            for sub_agent in sub_agents:
                topics = sub_agent.get('topics', [])
                if topics:
                    all_topics.extend(topics)
            
            # Remove duplicates
            all_topics = list(set(all_topics))
            
            if not all_topics:
                # No topics available, use main agent
                logger.info("No topics available, routing to main agent")
                return {
                    'type': 'agent',
                    'agent_id': agent_data['id'],
                    'agent_name': agent_data['name'],
                    'system_prompt': agent_data['system_prompt'],
                    'model': agent_data['model']
                }
            
            # Analyze topic
            matched_topic = await self.analyze_topic(message, all_topics)
            
            if not matched_topic:
                # No topic match, use main agent
                logger.info("No topic match, routing to main agent")
                return {
                    'type': 'agent',
                    'agent_id': agent_data['id'],
                    'agent_name': agent_data['name'],
                    'system_prompt': agent_data['system_prompt'],
                    'model': agent_data['model']
                }
            
            # Find sub-agent for topic
            sub_agent = self.find_subagent_by_topic(matched_topic, sub_agents)
            
            if not sub_agent:
                # Topic matched but no sub-agent, use main agent
                logger.info(f"Topic '{matched_topic}' matched but no sub-agent, routing to main agent")
                return {
                    'type': 'agent',
                    'agent_id': agent_data['id'],
                    'agent_name': agent_data['name'],
                    'system_prompt': agent_data['system_prompt'],
                    'model': agent_data['model']
                }
            
            # Route to sub-agent
            logger.info(f"Routing to sub-agent '{sub_agent['name']}' for topic '{matched_topic}'")
            return {
                'type': 'sub_agent',
                'sub_agent_id': sub_agent['id'],
                'sub_agent_name': sub_agent['name'],
                'agent_id': agent_data['id'],
                'agent_name': agent_data['name'],
                'topic': matched_topic,
                'system_prompt': sub_agent['system_prompt'],
                'model': sub_agent['model']
            }
            
        except Exception as e:
            logger.error(f"Error routing message: {e}")
            # Fallback to main agent on error
            return {
                'type': 'agent',
                'agent_id': agent_data['id'],
                'agent_name': agent_data['name'],
                'system_prompt': agent_data['system_prompt'],
                'model': agent_data['model'],
                'error': str(e)
            }


# Singleton instance
_topic_analyzer = None

def get_topic_analyzer() -> TopicAnalyzer:
    """Get singleton instance of TopicAnalyzer"""
    global _topic_analyzer
    if _topic_analyzer is None:
        _topic_analyzer = TopicAnalyzer()
    return _topic_analyzer
