"""
Serviço de negócio para Leads
"""
from typing import Optional
from src.config.supabase import supabase_admin
from src.models.lead import LeadCreate, LeadUpdate, LeadResponse, LeadList
from src.utils.exceptions import NotFoundError, ValidationError
from src.utils.logger import logger


class LeadService:
    """Serviço de Leads"""
    
    async def get_all(
        self,
        page: int = 1,
        limit: int = 10,
        search: Optional[str] = None,
        status: Optional[str] = None,
        source: Optional[str] = None
    ) -> LeadList:
        """
        Lista Leads com paginação e filtros
        
        Args:
            page: Página atual
            limit: Itens por página
            search: Busca por nome/email/telefone
            status: Filtrar por status
            source: Filtrar por origem
            
        Returns:
            Lista paginada de Leads
        """
        try:
            query = supabase_admin.table("leads").select("*", count="exact")
            
            # Filtros
            if status:
                query = query.eq("status", status)
            
            if source:
                query = query.eq("source", source)
            
            if search:
                query = query.or_(
                    f"name.ilike.%{search}%,email.ilike.%{search}%,phone.ilike.%{search}%"
                )
            
            # Paginação
            offset = (page - 1) * limit
            query = query.range(offset, offset + limit - 1)
            query = query.order("created_at", desc=True)
            
            response = query.execute()
            
            total = response.count or 0
            items = [LeadResponse(**item) for item in response.data]
            has_next = total > (page * limit)
            
            logger.info(f"Listed {len(items)} leads")
            
            return LeadList(
                items=items,
                total=total,
                page=page,
                limit=limit,
                has_next=has_next
            )
            
        except Exception as e:
            logger.error(f"Error listing leads: {str(e)}")
            raise
    
    async def get_by_id(self, lead_id: str) -> LeadResponse:
        """Busca Lead por ID"""
        try:
            response = supabase_admin.table("leads").select("*").eq(
                "id", lead_id
            ).single().execute()
            
            if not response.data:
                raise NotFoundError(f"Lead {lead_id} not found")
            
            return LeadResponse(**response.data)
            
        except Exception as e:
            logger.error(f"Error retrieving lead {lead_id}: {str(e)}")
            if "not found" in str(e).lower() or "No rows found" in str(e):
                raise NotFoundError(f"Lead {lead_id} not found")
            raise
    
    async def create(self, data: LeadCreate) -> LeadResponse:
        """Cria novo Lead"""
        try:
            lead_data = data.model_dump()
            
            response = supabase_admin.table("leads").insert(
                lead_data
            ).execute()
            
            if not response.data:
                raise ValidationError("Failed to create lead")
            
            created = response.data[0]
            logger.info(f"Created lead: {created['id']}")
            
            return LeadResponse(**created)
            
        except Exception as e:
            logger.error(f"Error creating lead: {str(e)}")
            raise ValidationError(f"Failed to create lead: {str(e)}")
    
    async def update(self, lead_id: str, data: LeadUpdate) -> LeadResponse:
        """Atualiza Lead"""
        try:
            await self.get_by_id(lead_id)
            
            update_data = data.model_dump(exclude_unset=True)
            
            if not update_data:
                raise ValidationError("No data to update")
            
            response = supabase_admin.table("leads").update(
                update_data
            ).eq("id", lead_id).execute()
            
            if not response.data:
                raise NotFoundError(f"Lead {lead_id} not found")
            
            updated = response.data[0]
            logger.info(f"Updated lead: {lead_id}")
            
            return LeadResponse(**updated)
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error updating lead {lead_id}: {str(e)}")
            raise ValidationError(f"Failed to update lead: {str(e)}")
    
    async def delete(self, lead_id: str) -> bool:
        """Deleta Lead"""
        try:
            await self.get_by_id(lead_id)
            
            response = supabase_admin.table("leads").delete().eq(
                "id", lead_id
            ).execute()
            
            logger.info(f"Deleted lead: {lead_id}")
            
            return True
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error deleting lead {lead_id}: {str(e)}")
            raise
    
    async def convert_to_client(self, lead_id: str, company_name: str, cnpj: str, segment: str, plan: str):
        """
        Converte Lead em Cliente
        
        Args:
            lead_id: ID do lead a ser convertido
            company_name: Nome da empresa
            cnpj: CNPJ da empresa
            segment: Segmento de atuação da empresa
            plan: Plano contratado (basic, pro, enterprise)
            
        Returns:
            Cliente criado
        """
        try:
            # Buscar lead
            lead = await self.get_by_id(lead_id)
            
            # Criar cliente
            from src.models.client import ClientCreate
            client_data = ClientCreate(
                company_name=company_name,
                document=cnpj,
                segment=segment,
                status="active"
            )
            
            client_dict = client_data.model_dump()
            
            # Inserir cliente no banco
            response = supabase_admin.table("clients").insert(
                client_dict
            ).execute()
            
            if not response.data:
                raise ValidationError("Failed to create client")
            
            created_client = response.data[0]
            
            # Atualizar lead com status "convertido" e vincular ao cliente
            await self.update(lead_id, LeadUpdate(status="qualificado"))
            
            logger.info(f"Converted lead {lead_id} to client {created_client['id']}")
            
            from src.models.client import ClientResponse
            return ClientResponse(**created_client)
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error converting lead {lead_id} to client: {str(e)}")
            raise ValidationError(f"Failed to convert lead: {str(e)}")


# Instância global
lead_service = LeadService()
