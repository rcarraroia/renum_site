"""
Tools Routes
Sprint 04 - Sistema Multi-Agente

API endpoints for managing agent tools
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from src.models.tool import ToolCreate, ToolUpdate, ToolResponse
from src.services.tool_service import ToolService
from src.api.middleware.auth_middleware import get_current_user, require_admin

router = APIRouter(prefix="/tools", tags=["tools"])


@router.get("/", response_model=List[ToolResponse])
async def list_tools(
    current_user: dict = Depends(get_current_user)
) -> List[ToolResponse]:
    """
    List all available tools
    
    Returns all tools in the system. Admins see all tools,
    clients see only tools available to them.
    """
    service = ToolService()
    tools = await service.list_tools()
    return tools


@router.get("/enabled", response_model=List[ToolResponse])
async def list_enabled_tools(
    current_user: dict = Depends(get_current_user)
) -> List[ToolResponse]:
    """
    List tools enabled for current client
    
    Returns only tools that are active and available for the
    current client's agent configuration.
    """
    service = ToolService()
    client_id = getattr(current_user, "client_id", None)
    
    if not client_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Client ID not found in token"
        )
    
    tools = await service.get_enabled_tools(client_id)
    return tools


@router.get("/{tool_id}", response_model=ToolResponse)
async def get_tool(
    tool_id: UUID,
    current_user: dict = Depends(get_current_user)
) -> ToolResponse:
    """
    Get tool by ID
    
    Returns detailed information about a specific tool.
    """
    service = ToolService()
    tool = await service.get_tool(str(tool_id))
    
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tool {tool_id} not found"
        )
    
    return tool


@router.post("/", response_model=ToolResponse, status_code=status.HTTP_201_CREATED)
async def create_tool(
    data: ToolCreate,
    current_user: dict = Depends(require_admin)
) -> ToolResponse:
    """
    Create new tool (admin only)
    
    Creates a new tool that can be used by agents.
    Only administrators can create tools.
    """
    service = ToolService()
    
    try:
        tool = await service.create_tool(data.dict())
        return tool
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating tool: {str(e)}"
        )


@router.put("/{tool_id}", response_model=ToolResponse)
async def update_tool(
    tool_id: UUID,
    data: ToolUpdate,
    current_user: dict = Depends(require_admin)
) -> ToolResponse:
    """
    Update tool (admin only)
    
    Updates an existing tool's configuration.
    Only administrators can update tools.
    """
    service = ToolService()
    
    try:
        tool = await service.update_tool(str(tool_id), data.dict(exclude_unset=True))
        
        if not tool:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tool {tool_id} not found"
            )
        
        return tool
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating tool: {str(e)}"
        )


@router.delete("/{tool_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tool(
    tool_id: UUID,
    current_user: dict = Depends(require_admin)
):
    """
    Delete tool (admin only)
    
    Deletes a tool from the system.
    Only administrators can delete tools.
    Built-in tools cannot be deleted.
    """
    service = ToolService()
    
    try:
        success = await service.delete_tool(str(tool_id))
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tool {tool_id} not found or cannot be deleted"
            )
        
        return None
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting tool: {str(e)}"
        )


@router.patch("/{tool_id}/toggle", response_model=ToolResponse)
async def toggle_tool(
    tool_id: UUID,
    current_user: dict = Depends(require_admin)
) -> ToolResponse:
    """
    Toggle tool active status (admin only)
    
    Activates or deactivates a tool.
    Only administrators can toggle tools.
    """
    service = ToolService()
    
    try:
        tool = await service.toggle_active(str(tool_id))
        
        if not tool:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tool {tool_id} not found"
            )
        
        return tool
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error toggling tool: {str(e)}"
        )


@router.post("/{tool_id}/test")
async def test_tool(
    tool_id: UUID,
    parameters: dict,
    current_user: dict = Depends(get_current_user)
):
    """
    Test tool execution
    
    Executes a tool with provided parameters for testing purposes.
    Returns the tool's output or error message.
    """
    service = ToolService()
    
    try:
        result = await service.test_tool(str(tool_id), parameters)
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
