"""
Wizard API Routes - Sprint 06
API endpoints for agent creation wizard
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from src.models.wizard import (
    WizardSession,
    WizardSessionCreate,
    WizardSessionUpdate,
    WizardStepData,
    TemplateInfo,
)
from src.services.wizard_service import get_wizard_service
from src.services.template_service import get_template_service
from src.api.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/agents/wizard", tags=["wizard"])


@router.post("/start", response_model=WizardSession, status_code=status.HTTP_201_CREATED)
async def start_wizard(
    data: WizardSessionCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Start new wizard session
    
    Creates a draft agent/template and returns wizard session ID
    """
    wizard_service = get_wizard_service()
    
    try:
        # Extrair category se fornecida (para templates)
        category = getattr(data, 'category', None)
        
        session = wizard_service.start_wizard(
            client_id=data.client_id,
            category=category
        )
        return session
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start wizard: {str(e)}"
        )


@router.get("/{wizard_id}", response_model=WizardSession)
async def get_wizard(
    wizard_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Get wizard session by ID
    
    Retrieves current wizard progress
    """
    wizard_service = get_wizard_service()
    
    session = wizard_service.get_wizard(wizard_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wizard session not found"
        )
    
    return session


@router.put("/{wizard_id}/step/{step_number}", response_model=WizardSession)
async def save_wizard_step(
    wizard_id: UUID,
    step_number: int,
    step_data: WizardStepData,
    current_user: dict = Depends(get_current_user)
):
    """
    Save wizard step progress
    
    Updates wizard session with step data
    """
    if step_number < 1 or step_number > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Step number must be between 1 and 5"
        )
    
    wizard_service = get_wizard_service()
    
    # Validate step data
    validation = wizard_service.validate_step(step_number, step_data.data)
    if not validation['valid']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Validation failed",
                "errors": validation['errors']
            }
        )
    
    try:
        session = wizard_service.save_step(wizard_id, step_number, step_data.data)
        return session
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save step: {str(e)}"
        )


@router.delete("/{wizard_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wizard(
    wizard_id: UUID,
    force: bool = False,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete wizard session (abandon)
    
    Removes draft agent and wizard progress.
    Use force=true to delete published agents (for testing).
    """
    wizard_service = get_wizard_service()
    
    success = wizard_service.delete_wizard(wizard_id, force=force)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wizard session not found"
        )


@router.get("/templates/list", response_model=List[TemplateInfo])
async def list_templates(
    current_user: dict = Depends(get_current_user)
):
    """
    List available agent templates
    
    Returns all predefined templates with metadata
    """
    template_service = get_template_service()
    return template_service.list_templates()


@router.get("/templates/{template_type}", response_model=dict)
async def get_template(
    template_type: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get template details by type
    
    Returns template configuration
    """
    template_service = get_template_service()
    
    template = template_service.get_template(template_type)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template '{template_type}' not found"
        )
    
    return template


# Sandbox endpoints

@router.post("/{wizard_id}/sandbox/start", response_model=dict, status_code=status.HTTP_201_CREATED)
async def start_sandbox(
    wizard_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Start sandbox testing session
    
    Creates temporary conversation for testing agent
    """
    from src.services.sandbox_service import get_sandbox_service
    
    sandbox_service = get_sandbox_service()
    
    try:
        session = sandbox_service.create_sandbox(wizard_id)
        return {
            "sandbox_id": str(session.id),
            "conversation_id": str(session.conversation_id),
            "expires_at": session.expires_at.isoformat(),
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start sandbox: {str(e)}"
        )


@router.post("/{wizard_id}/sandbox/message", response_model=dict)
async def send_sandbox_message(
    wizard_id: UUID,
    message: dict,
    current_user: dict = Depends(get_current_user)
):
    """
    Send message in sandbox
    
    Processes message and returns agent response
    """
    from src.services.sandbox_service import get_sandbox_service
    from src.models.wizard import SandboxMessageRequest
    
    sandbox_service = get_sandbox_service()
    
    try:
        msg_request = SandboxMessageRequest(**message)
        response = await sandbox_service.process_message(wizard_id, msg_request.message)
        
        return {
            "role": response.role,
            "content": response.content,
            "timestamp": response.timestamp.isoformat(),
            "collected_data": response.collected_data,
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process message: {str(e)}"
        )


@router.get("/{wizard_id}/sandbox/history", response_model=List[dict])
async def get_sandbox_history(
    wizard_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Get sandbox conversation history
    
    Returns all messages from sandbox session
    """
    from src.services.sandbox_service import get_sandbox_service
    
    sandbox_service = get_sandbox_service()
    
    try:
        history = sandbox_service.get_sandbox_history(wizard_id)
        return history
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/{wizard_id}/sandbox/data", response_model=dict)
async def get_sandbox_collected_data(
    wizard_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Get data collected during sandbox
    
    Returns structured data collected from conversation
    """
    from src.services.sandbox_service import get_sandbox_service
    
    sandbox_service = get_sandbox_service()
    
    try:
        data = sandbox_service.get_collected_data(wizard_id)
        return {"collected_data": data}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{wizard_id}/sandbox", status_code=status.HTTP_204_NO_CONTENT)
async def cleanup_sandbox(
    wizard_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Clean up sandbox session
    
    Deletes temporary conversation and messages
    """
    from src.services.sandbox_service import get_sandbox_service
    
    sandbox_service = get_sandbox_service()
    
    success = sandbox_service.cleanup_sandbox(wizard_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sandbox session not found"
        )


# Publication endpoint

@router.post("/{wizard_id}/publish", response_model=dict, status_code=status.HTTP_200_OK)
async def publish_agent(
    wizard_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Publish agent
    
    Activates agent and generates public URL, embed code, and QR code
    """
    from src.services.publication_service import get_publication_service
    
    publication_service = get_publication_service()
    
    try:
        result = publication_service.publish_agent(wizard_id)
        
        return {
            "agent_id": str(result.agent_id),
            "slug": result.slug,
            "public_url": result.public_url,
            "embed_code": result.embed_code,
            "qr_code_url": result.qr_code_url,
            "status": result.status,
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to publish agent: {str(e)}"
        )


@router.post("/n8n-convert", response_model=dict)
async def convert_n8n_workflow(
    workflow: dict,
    current_user: dict = Depends(get_current_user)
):
    """
    Convert n8n workflow to agent config
    
    Parses n8n JSON and returns suggested name, description and prompt
    """
    from src.utils.n8n_converter import convert_n8n_to_agent_config
    
    try:
        config = convert_n8n_to_agent_config(workflow)
        return config
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to convert n8n workflow: {str(e)}"
        )
