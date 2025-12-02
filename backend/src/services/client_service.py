"""
Serviço de negócio para Clientes
"""
from typing import Optional
from src.config.supabase import supabase_admin
from src.models.client import ClientCreate, ClientUpdate, ClientResponse, ClientList
from src.utils.exceptions import NotFoundError, ValidationError
from src.utils.logger import logger


class ClientService:
    """Serviço de Clientes"""
    
    async def get_all(
        self,
        page: int = 1,
        limit: int = 10,
        search: Optional[str] = None,
        status: Optional[str] = None
    ) -> ClientList:
        """
        Lista Clientes com paginação e filtros
        
        Args:
            page: Página atual
            limit: Itens por página
            search: Busca por nome da empresa
            status: Filtrar por status
            
        Returns:
            Lista paginada de Clientes
        """
        try:
            # Query base
            query = supabase_admin.table("clients").select("*", count="exact")
            
            # Aplicar filtro de status
            if status:
                query = query.eq("status", status)
            
            # Aplicar busca
            if search:
                query = query.ilike("company_name", f"%{search}%")
            
            # Paginação
            offset = (page - 1) * limit
            query = query.range(offset, offset + limit - 1)
            
            # Ordenar por criação (mais recente primeiro)
            query = query.order("created_at", desc=True)
            
            # Executar query
            response = query.execute()
            
            total = response.count or 0
            items = [ClientResponse(**item) for item in response.data]
            has_next = total > (page * limit)
            
            logger.info(f"Listed {len(items)} clients (page {page}/{limit})")
            
            return ClientList(
                items=items,
                total=total,
                page=page,
                limit=limit,
                has_next=has_next
            )
            
        except Exception as e:
            logger.error(f"Error listing clients: {str(e)}")
            raise
    
    async def get_by_id(self, client_id: str) -> ClientResponse:
        """
        Busca Cliente por ID
        
        Args:
            client_id: ID do cliente
            
        Returns:
            Dados do Cliente
            
        Raises:
            NotFoundError: Cliente não encontrado
        """
        try:
            response = supabase_admin.table("clients").select("*").eq(
                "id", client_id
            ).single().execute()
            
            if not response.data:
                raise NotFoundError(f"Client {client_id} not found")
            
            logger.info(f"Retrieved client: {client_id}")
            
            return ClientResponse(**response.data)
            
        except Exception as e:
            logger.error(f"Error retrieving client {client_id}: {str(e)}")
            if "not found" in str(e).lower() or "No rows found" in str(e):
                raise NotFoundError(f"Client {client_id} not found")
            raise
    
    async def create(self, data: ClientCreate) -> ClientResponse:
        """
        Cria novo Cliente
        
        Args:
            data: Dados do cliente
            
        Returns:
            Cliente criado
            
        Raises:
            ValidationError: Dados inválidos
        """
        try:
            # Preparar dados
            client_data = data.model_dump()
            
            # Inserir no banco
            response = supabase_admin.table("clients").insert(
                client_data
            ).execute()
            
            if not response.data:
                raise ValidationError("Failed to create client")
            
            created = response.data[0]
            logger.info(f"Created client: {created['id']}")
            
            return ClientResponse(**created)
            
        except Exception as e:
            logger.error(f"Error creating client: {str(e)}")
            raise ValidationError(f"Failed to create client: {str(e)}")
    
    async def update(
        self,
        client_id: str,
        data: ClientUpdate
    ) -> ClientResponse:
        """
        Atualiza Cliente
        
        Args:
            client_id: ID do cliente
            data: Dados a atualizar
            
        Returns:
            Cliente atualizado
            
        Raises:
            NotFoundError: Cliente não encontrado
        """
        try:
            # Verificar se existe
            await self.get_by_id(client_id)
            
            # Preparar dados (apenas campos não-None)
            update_data = data.model_dump(exclude_unset=True)
            
            if not update_data:
                raise ValidationError("No data to update")
            
            # Atualizar
            response = supabase_admin.table("clients").update(
                update_data
            ).eq("id", client_id).execute()
            
            if not response.data:
                raise NotFoundError(f"Client {client_id} not found")
            
            updated = response.data[0]
            logger.info(f"Updated client: {client_id}")
            
            return ClientResponse(**updated)
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error updating client {client_id}: {str(e)}")
            raise ValidationError(f"Failed to update client: {str(e)}")
    
    async def delete(self, client_id: str) -> bool:
        """
        Deleta Cliente
        
        Args:
            client_id: ID do cliente
            
        Returns:
            True se deletado com sucesso
            
        Raises:
            NotFoundError: Cliente não encontrado
        """
        try:
            # Verificar se existe
            await self.get_by_id(client_id)
            
            # Deletar
            response = supabase_admin.table("clients").delete().eq(
                "id", client_id
            ).execute()
            
            logger.info(f"Deleted client: {client_id}")
            
            return True
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error deleting client {client_id}: {str(e)}")
            raise


# Instância global
client_service = ClientService()
