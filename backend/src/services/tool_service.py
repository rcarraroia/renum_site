"""
Tool Service - Gerenciamento de ferramentas disponíveis para agentes
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from ..utils.supabase_client import get_client
from ..models.tool import ToolCreate, ToolUpdate, ToolResponse


class ToolService:
    """Service para gerenciar tools disponíveis para agentes"""
    
    def __init__(self):
        self.supabase = get_client()
    
    def list_tools(
        self,
        active_only: bool = True,
        skip: int = 0,
        limit: int = 100
    ) -> List[ToolResponse]:
        """
        Lista todas as tools
        
        Args:
            active_only: Se True, retorna apenas tools ativas
            skip: Número de registros para pular (paginação)
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de tools
        """
        query = self.supabase.table('tools').select('*')
        
        if active_only:
            query = query.eq('active', True)
        
        query = query.range(skip, skip + limit - 1).order('name')
        
        result = query.execute()
        return [ToolResponse(**tool) for tool in result.data]
    
    def get_tool(self, tool_id: UUID) -> Optional[ToolResponse]:
        """
        Busca uma tool por ID
        
        Args:
            tool_id: ID da tool
            
        Returns:
            Tool encontrada ou None
        """
        result = self.supabase.table('tools').select('*').eq('id', str(tool_id)).execute()
        
        if not result.data:
            return None
        
        return ToolResponse(**result.data[0])
    
    def get_tool_by_name(self, name: str) -> Optional[ToolResponse]:
        """
        Busca uma tool por nome
        
        Args:
            name: Nome da tool
            
        Returns:
            Tool encontrada ou None
        """
        result = self.supabase.table('tools').select('*').eq('name', name).execute()
        
        if not result.data:
            return None
        
        return ToolResponse(**result.data[0])
    
    def create_tool(self, tool_data: ToolCreate) -> ToolResponse:
        """
        Cria uma nova tool
        
        Args:
            tool_data: Dados da tool a criar
            
        Returns:
            Tool criada
        """
        data = {
            'name': tool_data.name,
            'description': tool_data.description,
            'function_name': tool_data.function_name,
            'parameters_schema': tool_data.parameters_schema,
            'active': tool_data.active
        }
        
        result = self.supabase.table('tools').insert(data).execute()
        return ToolResponse(**result.data[0])
    
    def update_tool(self, tool_id: UUID, tool_data: ToolUpdate) -> Optional[ToolResponse]:
        """
        Atualiza uma tool existente
        
        Args:
            tool_id: ID da tool
            tool_data: Dados a atualizar
            
        Returns:
            Tool atualizada ou None se não encontrada
        """
        # Verificar se existe
        existing = self.get_tool(tool_id)
        if not existing:
            return None
        
        # Preparar dados para atualização (apenas campos fornecidos)
        update_data = tool_data.model_dump(exclude_unset=True)
        update_data['updated_at'] = datetime.utcnow().isoformat()
        
        result = self.supabase.table('tools').update(update_data).eq('id', str(tool_id)).execute()
        
        if not result.data:
            return None
        
        return ToolResponse(**result.data[0])
    
    def delete_tool(self, tool_id: UUID) -> bool:
        """
        Deleta uma tool (soft delete - marca como inativa)
        
        Args:
            tool_id: ID da tool
            
        Returns:
            True se deletada com sucesso, False caso contrário
        """
        result = self.supabase.table('tools').update({
            'active': False,
            'updated_at': datetime.utcnow().isoformat()
        }).eq('id', str(tool_id)).execute()
        
        return len(result.data) > 0
    
    def get_tools_by_ids(self, tool_ids: List[UUID]) -> List[ToolResponse]:
        """
        Busca múltiplas tools por IDs
        
        Args:
            tool_ids: Lista de IDs de tools
            
        Returns:
            Lista de tools encontradas
        """
        if not tool_ids:
            return []
        
        str_ids = [str(tid) for tid in tool_ids]
        result = self.supabase.table('tools').select('*').in_('id', str_ids).execute()
        
        return [ToolResponse(**tool) for tool in result.data]
