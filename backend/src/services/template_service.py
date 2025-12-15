"""
Template Service - Sprint 06
Manages agent templates and system prompt generation
"""

from typing import Dict, Any, Optional, List


class TemplateService:
    """Service for managing agent templates"""
    
    # Template definitions
    TEMPLATES: Dict[str, Dict[str, Any]] = {
        'customer_service': {
            'name': 'Customer Service',
            'description': 'Friendly agent for customer support and assistance',
            'personality': 'friendly',
            'tone_formal': 60,
            'tone_direct': 50,
            'system_prompt_base': """You are a friendly and helpful customer service agent. 
Your goal is to assist customers with their questions and concerns in a warm, empathetic manner.

Key behaviors:
- Always greet customers warmly
- Listen carefully to their concerns
- Provide clear, helpful solutions
- Show empathy and understanding
- Escalate to human support when needed
- End conversations positively

Remember: Customer satisfaction is your top priority.""",
            'default_fields': ['name', 'email', 'phone', 'issue'],
            'integrations': ['whatsapp', 'email'],
        },
        'sales': {
            'name': 'Sales',
            'description': 'Persuasive agent for lead qualification and sales',
            'personality': 'professional',
            'tone_formal': 70,
            'tone_direct': 80,
            'system_prompt_base': """You are a professional sales agent focused on qualifying leads and driving conversions.
Your goal is to understand customer needs and present solutions effectively.

Key behaviors:
- Ask qualifying questions to understand needs
- Present value propositions clearly
- Handle objections professionally
- Create urgency when appropriate
- Schedule follow-ups or demos
- Close conversations with clear next steps

Remember: Focus on value, not just features.""",
            'default_fields': ['name', 'phone', 'interest', 'budget'],
            'integrations': ['whatsapp', 'database'],
        },
        'support': {
            'name': 'Technical Support',
            'description': 'Technical agent for troubleshooting and problem-solving',
            'personality': 'technical',
            'tone_formal': 75,
            'tone_direct': 85,
            'system_prompt_base': """You are a technical support agent specialized in diagnosing and solving problems.
Your goal is to efficiently resolve technical issues with clear, step-by-step guidance.

Key behaviors:
- Gather detailed information about the issue
- Ask diagnostic questions systematically
- Provide clear, actionable solutions
- Use technical language when appropriate
- Document solutions for future reference
- Escalate complex issues when needed

Remember: Accuracy and clarity are essential.""",
            'default_fields': ['name', 'email', 'product', 'issue_description'],
            'integrations': ['email', 'database'],
        },
        'recruitment': {
            'name': 'Recruitment',
            'description': 'Professional agent for candidate screening and recruitment',
            'personality': 'professional',
            'tone_formal': 80,
            'tone_direct': 70,
            'system_prompt_base': """You are a professional recruitment agent focused on identifying and qualifying candidates.
Your goal is to assess candidate fit and guide them through the initial screening process.

Key behaviors:
- Ask about experience and qualifications
- Assess cultural fit and motivation
- Explain role requirements clearly
- Schedule interviews for qualified candidates
- Provide feedback professionally
- Maintain candidate engagement

Remember: Represent the company professionally while being approachable.""",
            'default_fields': ['name', 'email', 'phone', 'position_interest', 'experience'],
            'integrations': ['whatsapp', 'email'],
        },
        'custom': {
            'name': 'Custom',
            'description': 'Fully customizable agent - start from scratch',
            'personality': 'professional',
            'tone_formal': 50,
            'tone_direct': 50,
            'system_prompt_base': """You are an AI assistant designed to help users.
Your behavior and personality will be customized based on specific requirements.

Key behaviors:
- Be helpful and responsive
- Follow the guidelines provided
- Adapt to user needs
- Maintain professionalism

Remember: Your exact behavior will be defined by custom configuration.""",
            'default_fields': [],
            'integrations': [],
        },
    }
    
    # Personality modifiers
    PERSONALITY_MODIFIERS: Dict[str, str] = {
        'professional': """
Personality: Professional
- Use formal language and proper grammar
- Maintain a business-appropriate tone
- Be respectful and courteous
- Focus on efficiency and results""",
        'friendly': """
Personality: Friendly
- Use warm, conversational language
- Show empathy and understanding
- Be approachable and personable
- Create a comfortable atmosphere""",
        'technical': """
Personality: Technical
- Use precise, technical terminology
- Focus on accuracy and detail
- Provide systematic solutions
- Be methodical and thorough""",
        'casual': """
Personality: Casual
- Use relaxed, informal language
- Be conversational and natural
- Show personality and humor when appropriate
- Keep things light and easy""",
    }
    
    def get_template(self, template_type: str) -> Optional[Dict[str, Any]]:
        """
        Get template configuration by type
        
        Args:
            template_type: Type of template (customer_service, sales, support, recruitment, custom)
            
        Returns:
            Template configuration dict or None if not found
        """
        return self.TEMPLATES.get(template_type)
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """
        List all available templates
        
        Returns:
            List of template configurations with metadata
        """
        return [
            {
                'type': template_type,
                'name': config['name'],
                'description': config['description'],
                'default_personality': config['personality'],
                'default_fields': config['default_fields'],
                'recommended_integrations': config['integrations'],
            }
            for template_type, config in self.TEMPLATES.items()
        ]
    
    def generate_system_prompt(
        self,
        template_type: str,
        personality: str,
        tone_formal: int,
        tone_direct: int,
        custom_instructions: Optional[str] = None,
        niche: Optional[str] = None,
    ) -> str:
        """
        Generate system prompt based on template and customization
        
        Args:
            template_type: Base template to use
            personality: Personality type (professional, friendly, technical, casual)
            tone_formal: Formality level (0-100, where 100 is most formal)
            tone_direct: Directness level (0-100, where 100 is most direct)
            custom_instructions: Additional custom instructions
            niche: Business niche (mmn, clinicas, vereadores, ecommerce, generico)
            
        Returns:
            Generated system prompt
        """
        template = self.get_template(template_type)
        if not template:
            raise ValueError(f"Template '{template_type}' not found")
        
        # Start with base prompt
        prompt_parts = [template['system_prompt_base']]
        
        # Add personality modifier
        if personality in self.PERSONALITY_MODIFIERS:
            prompt_parts.append(self.PERSONALITY_MODIFIERS[personality])
        
        # Add tone adjustments
        tone_instructions = self._generate_tone_instructions(tone_formal, tone_direct)
        if tone_instructions:
            prompt_parts.append(tone_instructions)
        
        # Add niche-specific context
        if niche:
            niche_context = self._generate_niche_context(niche)
            if niche_context:
                prompt_parts.append(niche_context)
        
        # Add custom instructions
        if custom_instructions:
            prompt_parts.append(f"\nAdditional Instructions:\n{custom_instructions}")
        
        # Combine all parts
        return "\n\n".join(prompt_parts)
    
    def _generate_tone_instructions(self, tone_formal: int, tone_direct: int) -> str:
        """Generate tone-specific instructions"""
        instructions = []
        
        # Formality instructions
        if tone_formal >= 75:
            instructions.append("- Use very formal language and avoid contractions")
        elif tone_formal >= 50:
            instructions.append("- Use moderately formal language")
        elif tone_formal >= 25:
            instructions.append("- Use casual but professional language")
        else:
            instructions.append("- Use informal, conversational language")
        
        # Directness instructions
        if tone_direct >= 75:
            instructions.append("- Be direct and concise in responses")
        elif tone_direct >= 50:
            instructions.append("- Balance directness with explanation")
        elif tone_direct >= 25:
            instructions.append("- Provide detailed explanations")
        else:
            instructions.append("- Be descriptive and thorough in responses")
        
        if instructions:
            return "Communication Style:\n" + "\n".join(instructions)
        return ""
    
    def _generate_niche_context(self, niche: str) -> str:
        """Generate niche-specific context"""
        niche_contexts = {
            'mmn': """
Industry Context: Multi-Level Marketing (MMN)
- Understand network marketing terminology
- Focus on team building and recruitment
- Emphasize income opportunity and flexibility
- Be motivational and inspiring""",
            'clinicas': """
Industry Context: Healthcare/Clinics
- Use appropriate medical terminology
- Prioritize patient care and confidentiality
- Be empathetic and professional
- Follow healthcare communication standards""",
            'vereadores': """
Industry Context: Political/Electoral
- Understand political communication
- Be diplomatic and inclusive
- Focus on community needs and solutions
- Maintain neutrality on controversial topics""",
            'ecommerce': """
Industry Context: E-commerce
- Focus on product benefits and features
- Understand online shopping behavior
- Emphasize convenience and value
- Handle purchase-related questions efficiently""",
            'generico': """
Industry Context: General Business
- Adapt to various business contexts
- Be versatile in communication
- Focus on professional service delivery""",
        }
        
        return niche_contexts.get(niche, "")
    
    def validate_template_compatibility(
        self,
        template_type: str,
        selected_integrations: List[str]
    ) -> Dict[str, Any]:
        """
        Validate if selected integrations are compatible with template
        
        Args:
            template_type: Template type
            selected_integrations: List of integration types selected
            
        Returns:
            Dict with validation result and warnings
        """
        template = self.get_template(template_type)
        if not template:
            return {
                'valid': False,
                'error': f"Template '{template_type}' not found"
            }
        
        recommended = set(template['integrations'])
        selected = set(selected_integrations)
        
        missing_recommended = recommended - selected
        extra_integrations = selected - recommended
        
        warnings = []
        if missing_recommended:
            warnings.append(
                f"Recommended integrations not selected: {', '.join(missing_recommended)}"
            )
        
        return {
            'valid': True,
            'warnings': warnings,
            'recommended': list(recommended),
            'selected': list(selected),
            'missing_recommended': list(missing_recommended),
            'extra_integrations': list(extra_integrations),
        }


# Singleton instance
_template_service = None

def get_template_service() -> TemplateService:
    """Get singleton instance of TemplateService"""
    global _template_service
    if _template_service is None:
        _template_service = TemplateService()
    return _template_service
