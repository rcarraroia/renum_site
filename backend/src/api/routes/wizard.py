"""
Task 4: Create wizard API endpoints
POST /api/agents/wizard/start - Initialize wizard session
POST /api/agents/wizard/step/{step} - Process wizard step
POST /api/agents/wizard/complete - Finalize agent creation
GET /api/agents/wizard/templates - Get available templates
Requirements: 1.1, 1.2, 1.3, 1.4, 1.5
"""

from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from typing import Optional
from src.models.wizard import (
    WizardSessionCreate,
    WizardSession,
    WizardStepData,
    PublicationResult
)
from src.services.wizard_service import get_wizard_service
from src.services.publication_service import get_publication_service

router = APIRouter(prefix="/agents/wizard", tags=["wizard"])

@router.post("/start", response_model=WizardSession)
async def start_wizard(
    data: WizardSessionCreate,
    wizard_service = Depends(get_wizard_service)
):
    """
    Initialize new wizard session with type selection
    """
    try:
        print(f"DEBUG: Starting wizard with data: {data}")
        wizard = wizard_service.start_wizard(
            client_id=data.client_id,
            category=data.category
        )
        print(f"DEBUG: Wizard started successfully: {wizard.id}")
        return wizard
    except ValueError as e:
        print(f"DEBUG: ValueError in start_wizard: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        print(f"DEBUG: Unexpected error in start_wizard: {e}")
        traceback.print_exc()
        # Return the error in detail for debugging (remove in production)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.put("/{wizard_id}/step/{step_number}", response_model=WizardSession)
async def save_wizard_step(
    wizard_id: UUID,
    step_number: int,
    data: WizardStepData,
    wizard_service = Depends(get_wizard_service)
):
    """
    Save progress for a specific wizard step
    """
    try:
        wizard = wizard_service.save_step(
            wizard_id=wizard_id,
            step_number=step_number,
            data=data.data
        )
        return wizard
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{wizard_id}/publish", response_model=PublicationResult)
async def publish_wizard(
    wizard_id: UUID,
    wizard_service = Depends(get_wizard_service),
    publication_service = Depends(get_publication_service)
):
    """
    Finalize agent creation and publish
    """
    try:
        # Get wizard session
        wizard = wizard_service.get_wizard(wizard_id)
        if not wizard:
            raise HTTPException(status_code=404, detail="Wizard session not found")
        
        # Publish agent
        result = publication_service.publish_from_wizard(wizard)
        
        # Clean up wizard session
        wizard_service.delete_wizard(wizard_id)
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates")
async def get_templates(
    category: Optional[str] = None,
    niche: Optional[str] = None,
    wizard_service = Depends(get_wizard_service)
):
    """
    Get available marketplace templates
    
    Filters:
    - category: b2b or b2c
    - niche: industry/vertical
    """
    try:
        # Get templates from agent_service
        from src.services.agent_service import get_agent_service
        agent_service = get_agent_service()
        
        templates = agent_service.list_agents(
            is_template=True,
            limit=100
        )
        
        # Filter by category and niche if provided
        if category:
            templates = [t for t in templates if t.category == category]
        if niche:
            templates = [t for t in templates if t.niche == niche]
        
        # Filter only marketplace visible
        templates = [t for t in templates if t.marketplace_visible]
        
        return templates
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{wizard_id}", response_model=WizardSession)
async def get_wizard(
    wizard_id: UUID,
    wizard_service = Depends(get_wizard_service)
):
    """Get wizard session by ID"""
    wizard = wizard_service.get_wizard(wizard_id)
    if not wizard:
        raise HTTPException(status_code=404, detail="Wizard session not found")
    return wizard

@router.delete("/{wizard_id}")
async def delete_wizard(
    wizard_id: UUID,
    wizard_service = Depends(get_wizard_service)
):
    """Delete/abandon wizard session"""
    success = wizard_service.delete_wizard(wizard_id)
    if not success:
        raise HTTPException(status_code=404, detail="Wizard session not found")
    return {"message": "Wizard session deleted"}
