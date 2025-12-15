from typing import List, Dict, Any, Optional
import re
from src.utils.logger import logger

class GuardrailService:
    """Service to enforce security and quality input/output policies"""

    def validate_input(self, text: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Layer 1: Input Validation
        Checks user message BEFORE it reaches the agent.
        Returns: {'valid': bool, 'modified_text': str, 'violation': str}
        """
        guardrails = config.get('guardrails', {})
        if not guardrails or not guardrails.get('enabled', False):
             return {'valid': True, 'modified_text': text, 'violation': None}

        # 1. PII Redaction (Mock - Simple Regex for Email/CPF)
        if guardrails.get('pii', {}).get('enabled', False):
            text = self._redact_pii(text, guardrails['pii'].get('types', []))

        # 2. Blocked Words (Keywords)
        blocked_words = guardrails.get('keywords', [])
        for word in blocked_words:
            if word.lower() in text.lower():
                return {'valid': False, 'modified_text': text, 'violation': f"Keyword blocked: {word}"}

        # 3. Jailbreak Heuristic (Simple)
        # N8N style: Check if prompt tries to override system instructions
        jailbreak_phrases = ["ignore previous instructions", "você agora é", "you are now"]
        if guardrails.get('jailbreak', {}).get('enabled', False):
             for phrase in jailbreak_phrases:
                 if phrase in text.lower():
                     return {'valid': False, 'modified_text': text, 'violation': "Jailbreak attempt detected"}

        return {'valid': True, 'modified_text': text, 'violation': None}

    def validate_output(self, text: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Layer 2: Output Validation
        Checks agent response BEFORE it reaches the user.
        Returns: {'valid': bool, 'violation': str}
        """
        guardrails = config.get('guardrails', {})
        if not guardrails or not guardrails.get('enabled', False):
             return {'valid': True, 'violation': None}

        # 1. Secret Leakage (Regex for common keys)
        if guardrails.get('secrets', {}).get('enabled', False):
            if self._contains_secrets(text):
                return {'valid': False, 'violation': "Secret leakage detected"}

        # 2. Topic/Hallucination Check (Mock)
        # N8N style: Ensure response is related to business scope or doesn't match forbidden patterns
        # For MVP: We check if agent generated forbidden keywords in output too
        blocked_words = guardrails.get('keywords', [])
        for word in blocked_words:
            if word.lower() in text.lower():
                return {'valid': False, 'violation': f"Output contained forbidden word: {word}"}

        return {'valid': True, 'violation': None}

    def _redact_pii(self, text: str, types: List[str]) -> str:
        # Simple Redaction Logic
        # Email
        text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[EMAIL REDACTED]', text)
        return text

    def _contains_secrets(self, text: str) -> bool:
        # Simple Heuristic for API Keys (sk-...)
        if "sk-" in text and len(text) > 20: 
            return True
        return False

guardrail_service = GuardrailService()
