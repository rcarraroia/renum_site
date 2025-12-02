"""
Endpoints REST para Clientes
"""
from fastapi import APIRouter, Depends, Query, status, HTTPException
from typing import Optional
from src.models.client import ClientCreate, ClientUpdate, ClientResponse, ClientList
from src.models.user import UserProfile
from src.services.client_service import client_service
from src.api.middleware.auth_middleware import get_current_user
from src.utils.exceptions import NotFoundError, ValidationError
from src.utils.logger import logger


router = APIRouter(prefix="/clients", tags=["Clients"])


@router.get("", response_model=ClientList)
async def list_clients(
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(10, ge=1, le=100, description="Itens por página"),
    search: Optional[str] = Query(None, description="Busca por nome da empresa"),
    status: Optional[str] = Query(None, description="Filtrar por status (active, inactive, suspended)"),
    current_user: UserProfile = Depends(get_current_user)
):
    """
    Lista Clientes com paginação
    
    Query params:
    - page: Página (padrão: 1)
    - limit: Itens por página (padrão: 10, máx: 100)
    - search: Busca por nome da empresa
    - status: Filtrar por status (active, inactive, suspended)
    """
    try:
        return await client_service.get_all(
            page=page,
            limit=limit,
            search=search,
            status=status
        )
    except Exception as e:
        logger.error(f"Error in list_clients: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: str,
    current_user: UserProfile = Depends(get_current_user)
):
    """Busca Cliente por ID"""
    try:
        return await client_service.get_by_id(client_id=client_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error in get_client: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
async def create_client(
    data: ClientCreate,
    current_user: UserProfile = Depends(get_current_user)
):
    """Cria novo Cliente"""
    try:
        return await client_service.create(data=data)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in create_client: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: str,
    data: ClientUpdate,
    current_user: UserProfile = Depends(get_current_user)
):
    """Atualiza Cliente"""
    try:
        return await client_service.update(
            client_id=client_id,
            data=data
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in update_client: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: str,
    current_user: UserProfile = Depends(get_current_user)
):
    """Deleta Cliente"""
    try:
        await client_service.delete(client_id=client_id)
        return None
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error in delete_client: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
