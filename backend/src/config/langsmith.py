"""
LangSmith Configuration - Observability for Agents
Sprint 04 - Sistema Multi-Agente

Configures LangSmith tracing for all LLM calls, agent decisions, and tool invocations.
"""

import os
from typing import Optional, Dict, Any
from .settings import settings


def configure_langsmith(
    project: Optional[str] = None,
    environment: Optional[str] = None,
    tags: Optional[list[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """
    Configure LangSmith tracing for observability.
    
    Args:
        project: Project name (defaults to settings.LANGSMITH_PROJECT)
        environment: Environment name (defaults to settings.LANGSMITH_ENVIRONMENT)
        tags: Default tags to add to all traces
        metadata: Default metadata to add to all traces
    
    Raises:
        ValueError: If LANGSMITH_API_KEY is not set
    """
    # Validate API key
    if not settings.LANGSMITH_API_KEY or settings.LANGSMITH_API_KEY == "your-langsmith-api-key-here":
        raise ValueError(
            "LANGSMITH_API_KEY is required for observability.\n"
            "Please set it in your .env file.\n"
            "Get your API key from: https://smith.langchain.com/settings"
        )
    
    # Set environment variables for LangSmith
    os.environ["LANGSMITH_API_KEY"] = settings.LANGSMITH_API_KEY
    os.environ["LANGCHAIN_TRACING_V2"] = str(settings.LANGCHAIN_TRACING_V2).lower()
    os.environ["LANGCHAIN_ENDPOINT"] = settings.LANGCHAIN_ENDPOINT
    os.environ["LANGCHAIN_PROJECT"] = project or settings.LANGSMITH_PROJECT
    
    # Set environment tag
    env_tag = environment or settings.LANGSMITH_ENVIRONMENT
    os.environ["LANGCHAIN_TAGS"] = f"environment:{env_tag}"
    
    # Add custom tags if provided
    if tags:
        existing_tags = os.environ.get("LANGCHAIN_TAGS", "")
        all_tags = f"{existing_tags},{','.join(tags)}" if existing_tags else ','.join(tags)
        os.environ["LANGCHAIN_TAGS"] = all_tags
    
    # Add metadata if provided
    if metadata:
        # LangSmith metadata is set per-trace, not globally
        # Store in module-level variable for use in traces
        global _default_metadata
        _default_metadata = metadata
    
    print(f"LangSmith configured:")
    print(f"   Project: {os.environ['LANGCHAIN_PROJECT']}")
    print(f"   Environment: {env_tag}")
    print(f"   Tracing: {os.environ['LANGCHAIN_TRACING_V2']}")
    if tags:
        print(f"   Tags: {tags}")


def get_trace_metadata(client_id: Optional[str] = None, **kwargs) -> Dict[str, Any]:
    """
    Get metadata for a trace.
    
    Args:
        client_id: Client ID for multi-tenant isolation
        **kwargs: Additional metadata fields
    
    Returns:
        Dictionary of metadata for the trace
    """
    metadata = _default_metadata.copy() if _default_metadata else {}
    
    # Add client_id for multi-tenant filtering
    if client_id:
        metadata["client_id"] = client_id
    
    # Add environment
    metadata["environment"] = settings.LANGSMITH_ENVIRONMENT
    
    # Add custom fields
    metadata.update(kwargs)
    
    return metadata


def test_langsmith_connection() -> bool:
    """
    Test connection to LangSmith.
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        from langsmith import Client
        
        client = Client(
            api_key=settings.LANGSMITH_API_KEY,
            api_url=settings.LANGCHAIN_ENDPOINT
        )
        
        # Try to get current project
        project = client.read_project(project_name=settings.LANGSMITH_PROJECT)
        print(f"LangSmith connection successful!")
        print(f"   Project: {project.name}")
        return True
        
    except Exception as e:
        print(f"LangSmith connection failed: {e}")
        return False


# Module-level variable for default metadata
_default_metadata: Dict[str, Any] = {}


# Auto-configure on import if in production
if not settings.DEBUG:
    try:
        configure_langsmith()
    except ValueError as e:
        print(f"WARNING: {e}")
        print("LangSmith tracing will be disabled.")
