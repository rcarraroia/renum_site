"""
Endpoints REST para Leads
"""
from fastapi import APIRouter, Depends, Query, status, HTTPException
from typing import Optional
from src.models.lead import LeadCreate, LeadUpdate, LeadResponse, LeadList, LeadConvertRequest
from src.models.user import UserProfile
from src.services.lead_service import lead_service
from src.api.middleware.auth_middleware import get_current_user
from src.utils.exceptions import NotFoundError, ValidationError
from src.utils.logger import logger


router = APIRouter(prefix="/leads", tags=["Leads"])


@router.get("", response_model=LeadList)
async def list_leads(
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(10, ge=1, le=100, description="Itens por página"),
    search: Optional[str] = Query(None, description="Busca por nome/email/telefone"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    source: Optional[str] = Query(None, description="Filtrar por origem"),
    current_user: UserProfile = Depends(get_current_user)
):
    """
    Lista Leads com paginação
    
    Query params:
    - page: Página (padrão: 1)
    - limit: Itens por página (padrão: 10, máx: 100)
    - search: Busca por nome/email/telefone
    - status: Filtrar por status (new, contacted, qualified, converted, lost)
    - source: Filtrar por origem
    """
    try:
        return await lead_service.get_all(
            page=page,
            limit=limit,
            search=search,
            status=status,
            source=source
        )
    except Exception as e:
        logger.error(f"Error in list_leads: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: str,
    current_user: UserProfile = Depends(get_current_user)
):
    """Busca Lead por ID"""
    try:
        return await lead_service.get_by_id(lead_id=lead_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error in get_lead: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
async def create_lead(
    data: LeadCreate,
    current_user: UserProfile = Depends(get_current_user)
):
    """Cria novo Lead"""
    try:
        return await lead_service.create(data=data)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in create_lead: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: str,
    data: LeadUpdate,
    current_user: UserProfile = Depends(get_current_user)
):
    """Atualiza Lead"""
    try:
        return await lead_service.update(
            lead_id=lead_id,
            data=data
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in update_lead: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lead(
    lead_id: str,
    current_user: UserProfile = Depends(get_current_user)
):
    """Deleta Lead"""
    try:
        await lead_service.delete(lead_id=lead_id)
        return None
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error in delete_lead: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{lead_id}/convert")
async def convert_lead_to_client(
    lead_id: str,
    data: LeadConvertRequest,
    current_user: UserProfile = Depends(get_current_user)
):
    """Converte Lead em Cliente"""
    try:
        return await lead_service.convert_to_client(
            lead_id=lead_id,
            company_name=data.company_name,
            cnpj=data.cnpj,
            segment=data.segment,
            plan=data.plan
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in convert_lead_to_client: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
