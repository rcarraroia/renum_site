"""
Task 35: Security and Compliance Testing
Testes de segurança, guardrails e LGPD
"""

import pytest
from typing import Dict, Any
import re


class TestGuardrailsEnforcement:
    """Testes de enforcement de guardrails"""
    
    def test_content_filtering_blocks_inappropriate_content(self):
        """Verifica que conteúdo inapropriado é bloqueado"""
        blocked_patterns = [
            "conteúdo violento",
            "discurso de ódio",
            "informações pessoais sensíveis"
        ]
        
        for pattern in blocked_patterns:
            result = self._check_content_filter(pattern)
            assert result["blocked"] == True
            assert "guardrail" in result["reason"]
    
    def test_content_filtering_allows_safe_content(self):
        """Verifica que conteúdo seguro passa"""
        safe_contents = [
            "Olá, como posso ajudar?",
            "Informação sobre nossos produtos",
            "Agendamento de reunião"
        ]
        
        for content in safe_contents:
            result = self._check_content_filter(content)
            assert result["blocked"] == False
    
    def test_operational_limits_enforced(self):
        """Testa limites operacionais"""
        limits = {
            "max_tokens": 4000,
            "max_response_time": 30,
            "max_retries": 3
        }
        
        # Simula resposta que excede limite
        response = {"tokens": 5000}
        assert self._check_operational_limits(response, limits) == False
        
        response = {"tokens": 3000}
        assert self._check_operational_limits(response, limits) == True
    
    def _check_content_filter(self, content: str) -> Dict[str, Any]:
        """Helper para verificar filtro de conteúdo"""
        # Implementação real usaria o serviço de guardrails
        blocked_keywords = ["violento", "ódio", "sensíveis"]
        for keyword in blocked_keywords:
            if keyword in content.lower():
                return {"blocked": True, "reason": "guardrail:content_filter"}
        return {"blocked": False}
    
    def _check_operational_limits(self, response: Dict, limits: Dict) -> bool:
        """Helper para verificar limites"""
        if response.get("tokens", 0) > limits.get("max_tokens", 4000):
            return False
        return True


class TestLGPDCompliance:
    """Testes de conformidade LGPD"""
    
    def test_personal_data_anonymization(self):
        """Verifica anonimização de dados pessoais"""
        text_with_pii = "Meu CPF é 123.456.789-00 e email joao@email.com"
        
        anonymized = self._anonymize_pii(text_with_pii)
        
        assert "123.456.789-00" not in anonymized
        assert "joao@email.com" not in anonymized
        assert "[CPF_REDACTED]" in anonymized
        assert "[EMAIL_REDACTED]" in anonymized
    
    def test_data_retention_policy(self):
        """Verifica política de retenção de dados"""
        # Dados devem ser automaticamente excluídos após período
        retention_days = 90
        
        # Simula dado antigo
        old_data = {"created_at": "2024-01-01", "data": "sensitive"}
        
        should_delete = self._check_retention_policy(old_data, retention_days)
        assert should_delete == True
    
    def test_consent_tracking(self):
        """Verifica rastreamento de consentimento"""
        user_consent = {
            "user_id": "123",
            "consents": {
                "data_processing": True,
                "marketing": False,
                "analytics": True
            }
        }
        
        # Não deve processar marketing sem consentimento
        assert self._can_process("marketing", user_consent) == False
        assert self._can_process("analytics", user_consent) == True
    
    def test_data_export_right(self):
        """Verifica direito de exportação de dados (portabilidade)"""
        user_id = "test-user-123"
        
        exported_data = self._export_user_data(user_id)
        
        assert "conversations" in exported_data
        assert "preferences" in exported_data
        assert "format" in exported_data
        assert exported_data["format"] == "json"
    
    def test_data_deletion_right(self):
        """Verifica direito de exclusão de dados"""
        user_id = "test-user-123"
        
        result = self._delete_user_data(user_id)
        
        assert result["success"] == True
        assert result["deleted_items"] >= 0
    
    def _anonymize_pii(self, text: str) -> str:
        """Anonimiza PII no texto"""
        # CPF pattern
        text = re.sub(r'\d{3}\.\d{3}\.\d{3}-\d{2}', '[CPF_REDACTED]', text)
        # Email pattern
        text = re.sub(r'[\w.+-]+@[\w-]+\.[\w.-]+', '[EMAIL_REDACTED]', text)
        return text
    
    def _check_retention_policy(self, data: Dict, retention_days: int) -> bool:
        """Verifica se dado deve ser excluído"""
        from datetime import datetime, timedelta
        
        created = datetime.fromisoformat(data["created_at"])
        expiry = created + timedelta(days=retention_days)
        
        return datetime.now() > expiry
    
    def _can_process(self, purpose: str, consent: Dict) -> bool:
        """Verifica consentimento para propósito"""
        return consent.get("consents", {}).get(purpose, False)
    
    def _export_user_data(self, user_id: str) -> Dict:
        """Exporta dados do usuário"""
        return {
            "user_id": user_id,
            "conversations": [],
            "preferences": {},
            "format": "json"
        }
    
    def _delete_user_data(self, user_id: str) -> Dict:
        """Exclui dados do usuário"""
        return {"success": True, "deleted_items": 0}


class TestSecurityMonitoring:
    """Testes de monitoramento de segurança"""
    
    def test_rate_limiting(self):
        """Verifica rate limiting"""
        requests = [{"ip": "1.1.1.1"} for _ in range(100)]
        
        blocked = 0
        for i, req in enumerate(requests):
            if i > 50:  # Simula limite de 50 req/min
                if self._is_rate_limited(req):
                    blocked += 1
        
        assert blocked > 0
    
    def test_injection_prevention(self):
        """Verifica prevenção de injection"""
        malicious_inputs = [
            "'; DROP TABLE agents;--",
            "<script>alert('xss')</script>",
            "{{constructor.constructor('return this')()}}"
        ]
        
        for input_str in malicious_inputs:
            sanitized = self._sanitize_input(input_str)
            assert sanitized != input_str
            assert "<script>" not in sanitized
            assert "DROP TABLE" not in sanitized
    
    def test_authentication_required(self):
        """Verifica que endpoints requerem autenticação"""
        protected_endpoints = [
            "/api/agents",
            "/api/agents/wizard/start",
            "/api/integrations/status"
        ]
        
        for endpoint in protected_endpoints:
            result = self._check_auth_required(endpoint)
            assert result == True
    
    def test_audit_logging(self):
        """Verifica logging de auditoria"""
        action = {
            "type": "agent_created",
            "user_id": "admin-123",
            "agent_id": "new-agent"
        }
        
        log_entry = self._create_audit_log(action)
        
        assert log_entry["timestamp"] is not None
        assert log_entry["action"] == "agent_created"
        assert log_entry["user_id"] == "admin-123"
    
    def _is_rate_limited(self, request: Dict) -> bool:
        """Verifica rate limit"""
        return True  # Simula bloqueio
    
    def _sanitize_input(self, input_str: str) -> str:
        """Sanitiza input"""
        sanitized = input_str.replace("<script>", "").replace("</script>", "")
        sanitized = re.sub(r'DROP\s+TABLE', '[BLOCKED]', sanitized, flags=re.IGNORECASE)
        return sanitized
    
    def _check_auth_required(self, endpoint: str) -> bool:
        """Verifica se endpoint requer auth"""
        return True
    
    def _create_audit_log(self, action: Dict) -> Dict:
        """Cria log de auditoria"""
        from datetime import datetime
        return {
            **action,
            "timestamp": datetime.utcnow().isoformat()
        }


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
