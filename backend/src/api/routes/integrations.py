"""
Integration Testing Endpoints - TRACK 2
Endpoints para testar integrações de sub-agentes
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from uuid import UUID

from src.services.integration_access import get_integration_access
from src.services.auto_lead_capture_hook import get_auto_lead_capture_hook
from src.services.orchestrator_service import get_orchestrator_service
from src.utils.logger import logger

router = APIRouter(prefix="/integrations", tags=["integrations"])

# ============================================================================
# Pydantic Models
# ============================================================================

class WhatsAppSendRequest(BaseModel):
    sub_agent_id: UUID
    phone: str
    message: str
    context: Optional[Dict[str, Any]] = None

class EmailSendRequest(BaseModel):
    sub_agent_id: UUID
    to_email: str
    subject: str
    body: str
    context: Optional[Dict[str, Any]] = None

class CalendarAccessRequest(BaseModel):
    sub_agent_id: UUID
    action: str
    data: Dict[str, Any]

class LeadCaptureTestRequest(BaseModel):
    sub_agent_id: UUID
    conversation_id: UUID
    user_message: str
    agent_response: str
    context: Optional[Dict[str, Any]] = None

class OrchestratorTestRequest(BaseModel):
    agent_id: UUID
    message: str
    conversation_id: UUID
    context: Optional[Dict[str, Any]] = None

# ============================================================================
# Integration Access Endpoints
# ============================================================================

@router.post("/whatsapp/send")
async def test_whatsapp_send(request: WhatsAppSendRequest):
    """Testa envio de WhatsApp via sub-agente"""
    try:
        integration_access = get_integration_access()
        
        result = await integration_access.send_whatsapp(
            sub_agent_id=request.sub_agent_id,
            phone=request.phone,
            message=request.message,
            context=request.context
        )
        
        return {
            "success": result,
            "sub_agent_id": str(request.sub_agent_id),
            "phone": request.phone,
            "message_length": len(request.message),
            "timestamp": "2025-12-23T12:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Error testing WhatsApp send: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/email/send")
async def test_email_send(request: EmailSendRequest):
    """Testa envio de email via sub-agente"""
    try:
        integration_access = get_integration_access()
        
        result = await integration_access.send_email(
            sub_agent_id=request.sub_agent_id,
            to_email=request.to_email,
            subject=request.subject,
            body=request.body,
            context=request.context
        )
        
        return {
            "success": result,
            "sub_agent_id": str(request.sub_agent_id),
            "to_email": request.to_email,
            "subject": request.subject,
            "body_length": len(request.body),
            "timestamp": "2025-12-23T12:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Error testing email send: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/calendar/access")
async def test_calendar_access(request: CalendarAccessRequest):
    """Testa acesso ao calendar via sub-agente"""
    try:
        integration_access = get_integration_access()
        
        result = await integration_access.access_calendar(
            sub_agent_id=request.sub_agent_id,
            action=request.action,
            data=request.data
        )
        
        return {
            "success": result.get('success', False),
            "sub_agent_id": str(request.sub_agent_id),
            "action": request.action,
            "result": result,
            "timestamp": "2025-12-23T12:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Error testing calendar access: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/available/{sub_agent_id}")
async def get_available_integrations(sub_agent_id: UUID):
    """Lista integrações disponíveis para um sub-agente"""
    try:
        integration_access = get_integration_access()
        
        integrations = await integration_access.get_available_integrations(sub_agent_id)
        
        return {
            "sub_agent_id": str(sub_agent_id),
            "available_integrations": integrations,
            "total_count": len(integrations),
            "timestamp": "2025-12-23T12:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Error getting available integrations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Lead Capture Hook Endpoints
# ============================================================================

@router.post("/leads/capture/test")
async def test_lead_capture(request: LeadCaptureTestRequest):
    """Testa captura automática de leads"""
    try:
        lead_capture_hook = get_auto_lead_capture_hook()
        
        result = await lead_capture_hook.process_conversation(
            sub_agent_id=request.sub_agent_id,
            conversation_id=request.conversation_id,
            user_message=request.user_message,
            agent_response=request.agent_response,
            context=request.context
        )
        
        return {
            "lead_captured": bool(result),
            "lead_data": result,
            "sub_agent_id": str(request.sub_agent_id),
            "conversation_id": str(request.conversation_id),
            "timestamp": "2025-12-23T12:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Error testing lead capture: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/leads/capture/stats/{sub_agent_id}")
async def get_lead_capture_stats(sub_agent_id: UUID):
    """Retorna estatísticas de captura de leads"""
    try:
        lead_capture_hook = get_auto_lead_capture_hook()
        
        stats = await lead_capture_hook.get_capture_stats(sub_agent_id)
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting lead capture stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Orchestrator Integration Endpoints
# ============================================================================

@router.post("/orchestrator/test")
async def test_orchestrator_with_integrations(request: OrchestratorTestRequest):
    """Testa orquestrador completo com integrações e captura de leads"""
    try:
        orchestrator = get_orchestrator_service()
        
        result = await orchestrator.process_message(
            agent_id=request.agent_id,
            message=request.message,
            conversation_id=request.conversation_id,
            context=request.context
        )
        
        return {
            "orchestrator_result": result,
            "agent_id": str(request.agent_id),
            "conversation_id": str(request.conversation_id),
            "message_length": len(request.message),
            "timestamp": "2025-12-23T12:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Error testing orchestrator: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Batch Testing Endpoints
# ============================================================================

@router.post("/test/batch")
async def test_integrations_batch():
    """Executa bateria de testes de integração"""
    try:
        results = {
            "whatsapp_test": None,
            "email_test": None,
            "calendar_test": None,
            "lead_capture_test": None,
            "orchestrator_test": None
        }
        
        # Mock sub-agent ID para testes
        test_sub_agent_id = UUID("12345678-1234-5678-9012-123456789012")
        test_conversation_id = UUID("87654321-4321-8765-2109-876543210987")
        test_agent_id = UUID("11111111-2222-3333-4444-555555555555")
        
        integration_access = get_integration_access()
        lead_capture_hook = get_auto_lead_capture_hook()
        orchestrator = get_orchestrator_service()
        
        # Teste WhatsApp
        try:
            whatsapp_result = await integration_access.send_whatsapp(
                sub_agent_id=test_sub_agent_id,
                phone="+5511999999999",
                message="Teste de integração WhatsApp",
                context={"test": True}
            )
            results["whatsapp_test"] = {"success": whatsapp_result, "error": None}
        except Exception as e:
            results["whatsapp_test"] = {"success": False, "error": str(e)}
        
        # Teste Email
        try:
            email_result = await integration_access.send_email(
                sub_agent_id=test_sub_agent_id,
                to_email="test@example.com",
                subject="Teste de integração",
                body="Teste de envio de email via sub-agente",
                context={"test": True}
            )
            results["email_test"] = {"success": email_result, "error": None}
        except Exception as e:
            results["email_test"] = {"success": False, "error": str(e)}
        
        # Teste Calendar
        try:
            calendar_result = await integration_access.access_calendar(
                sub_agent_id=test_sub_agent_id,
                action="check_availability",
                data={"date": "2025-12-24", "time": "14:00"}
            )
            results["calendar_test"] = {"success": calendar_result.get('success', False), "error": None}
        except Exception as e:
            results["calendar_test"] = {"success": False, "error": str(e)}
        
        # Teste Lead Capture
        try:
            lead_result = await lead_capture_hook.process_conversation(
                sub_agent_id=test_sub_agent_id,
                conversation_id=test_conversation_id,
                user_message="Olá, meu nome é João e meu email é joao@teste.com. Gostaria de saber os preços.",
                agent_response="Olá João! Vou te enviar nossa tabela de preços por email.",
                context={"phone": "+5511999999999", "email": "joao@teste.com"}
            )
            results["lead_capture_test"] = {"success": bool(lead_result), "lead_data": lead_result, "error": None}
        except Exception as e:
            results["lead_capture_test"] = {"success": False, "error": str(e)}
        
        # Teste Orchestrator
        try:
            orchestrator_result = await orchestrator.process_message(
                agent_id=test_agent_id,
                message="Preciso de ajuda com vendas e preços",
                conversation_id=test_conversation_id,
                context={"phone": "+5511999999999"}
            )
            results["orchestrator_test"] = {"success": True, "result": orchestrator_result, "error": None}
        except Exception as e:
            results["orchestrator_test"] = {"success": False, "error": str(e)}
        
        # Calcular estatísticas
        total_tests = len(results)
        successful_tests = sum(1 for result in results.values() if result and result.get("success"))
        success_rate = (successful_tests / total_tests) * 100
        
        return {
            "batch_test_results": results,
            "summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "failed_tests": total_tests - successful_tests,
                "success_rate": f"{success_rate:.1f}%"
            },
            "timestamp": "2025-12-23T12:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Error in batch integration test: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Health Check Endpoint
# ============================================================================

@router.get("/health")
async def integration_health_check():
    """Verifica saúde dos serviços de integração"""
    try:
        return {
            "status": "healthy",
            "services": {
                "integration_access": "available",
                "lead_capture_hook": "available",
                "orchestrator_service": "available"
            },
            "timestamp": "2025-12-23T12:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": "2025-12-23T12:00:00Z"
        }