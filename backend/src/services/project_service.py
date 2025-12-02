"""
Serviço de negócio para Projetos
"""
from typing import Optional
from src.config.supabase import supabase_admin
from src.models.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectList
from src.utils.exceptions import NotFoundError, ValidationError
from src.utils.logger import logger


class ProjectService:
    """Serviço de Projetos"""
    
    async def get_all(
        self,
        page: int = 1,
        limit: int = 10,
        search: Optional[str] = None,
        status: Optional[str] = None,
        type: Optional[str] = None,
        client_id: Optional[str] = None
    ) -> ProjectList:
        """Lista Projetos com paginação e filtros"""
        try:
            query = supabase_admin.table("projects").select("*", count="exact")
            
            if status:
                query = query.eq("status", status)
            
            if type:
                query = query.eq("type", type)
            
            if client_id:
                query = query.eq("client_id", client_id)
            
            if search:
                query = query.or_(
                    f"name.ilike.%{search}%,description.ilike.%{search}%"
                )
            
            offset = (page - 1) * limit
            query = query.range(offset, offset + limit - 1)
            query = query.order("created_at", desc=True)
            
            response = query.execute()
            
            total = response.count or 0
            items = [ProjectResponse(**item) for item in response.data]
            has_next = total > (page * limit)
            
            logger.info(f"Listed {len(items)} projects")
            
            return ProjectList(
                items=items,
                total=total,
                page=page,
                limit=limit,
                has_next=has_next
            )
            
        except Exception as e:
            logger.error(f"Error listing projects: {str(e)}")
            raise
    
    async def get_by_id(self, project_id: str) -> ProjectResponse:
        """Busca Projeto por ID"""
        try:
            response = supabase_admin.table("projects").select("*").eq(
                "id", project_id
            ).single().execute()
            
            if not response.data:
                raise NotFoundError(f"Project {project_id} not found")
            
            return ProjectResponse(**response.data)
            
        except Exception as e:
            logger.error(f"Error retrieving project {project_id}: {str(e)}")
            if "not found" in str(e).lower() or "No rows found" in str(e):
                raise NotFoundError(f"Project {project_id} not found")
            raise
    
    async def create(self, data: ProjectCreate) -> ProjectResponse:
        """Cria novo Projeto"""
        try:
            project_data = data.model_dump()
            
            response = supabase_admin.table("projects").insert(
                project_data
            ).execute()
            
            if not response.data:
                raise ValidationError("Failed to create project")
            
            created = response.data[0]
            logger.info(f"Created project: {created['id']}")
            
            return ProjectResponse(**created)
            
        except Exception as e:
            logger.error(f"Error creating project: {str(e)}")
            raise ValidationError(f"Failed to create project: {str(e)}")
    
    async def update(self, project_id: str, data: ProjectUpdate) -> ProjectResponse:
        """Atualiza Projeto"""
        try:
            await self.get_by_id(project_id)
            
            update_data = data.model_dump(exclude_unset=True)
            
            if not update_data:
                raise ValidationError("No data to update")
            
            response = supabase_admin.table("projects").update(
                update_data
            ).eq("id", project_id).execute()
            
            if not response.data:
                raise NotFoundError(f"Project {project_id} not found")
            
            updated = response.data[0]
            logger.info(f"Updated project: {project_id}")
            
            return ProjectResponse(**updated)
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error updating project {project_id}: {str(e)}")
            raise ValidationError(f"Failed to update project: {str(e)}")
    
    async def delete(self, project_id: str) -> bool:
        """Deleta Projeto"""
        try:
            await self.get_by_id(project_id)
            
            response = supabase_admin.table("projects").delete().eq(
                "id", project_id
            ).execute()
            
            logger.info(f"Deleted project: {project_id}")
            
            return True
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error deleting project {project_id}: {str(e)}")
            raise


# Instância global
project_service = ProjectService()
