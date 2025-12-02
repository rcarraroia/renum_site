"""
Endpoints REST para Projetos
"""
from fastapi import APIRouter, Depends, Query, status, HTTPException
from typing import Optional
from src.models.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectList
from src.models.user import UserProfile
from src.services.project_service import project_service
from src.api.middleware.auth_middleware import get_current_user
from src.utils.exceptions import NotFoundError, ValidationError
from src.utils.logger import logger


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("", response_model=ProjectList)
async def list_projects(
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(10, ge=1, le=100, description="Itens por página"),
    search: Optional[str] = Query(None, description="Busca por nome/descrição"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    type: Optional[str] = Query(None, description="Filtrar por tipo"),
    client_id: Optional[str] = Query(None, description="Filtrar por cliente"),
    current_user: UserProfile = Depends(get_current_user)
):
    """
    Lista Projetos com paginação
    
    Query params:
    - page: Página (padrão: 1)
    - limit: Itens por página (padrão: 10, máx: 100)
    - search: Busca por nome/descrição
    - status: Filtrar por status (planning, active, paused, completed, cancelled)
    - type: Filtrar por tipo
    - client_id: Filtrar por cliente
    """
    try:
        return await project_service.get_all(
            page=page,
            limit=limit,
            search=search,
            status=status,
            type=type,
            client_id=client_id
        )
    except Exception as e:
        logger.error(f"Error in list_projects: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    current_user: UserProfile = Depends(get_current_user)
):
    """Busca Projeto por ID"""
    try:
        return await project_service.get_by_id(project_id=project_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error in get_project: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreate,
    current_user: UserProfile = Depends(get_current_user)
):
    """Cria novo Projeto"""
    try:
        return await project_service.create(data=data)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in create_project: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    data: ProjectUpdate,
    current_user: UserProfile = Depends(get_current_user)
):
    """Atualiza Projeto"""
    try:
        return await project_service.update(
            project_id=project_id,
            data=data
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in update_project: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    current_user: UserProfile = Depends(get_current_user)
):
    """Deleta Projeto"""
    try:
        await project_service.delete(project_id=project_id)
        return None
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error in delete_project: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
