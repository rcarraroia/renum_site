"""
n8n Converter Utility
Sprint 10 - Agent Wizard
Converts n8n workflow JSON to Renum agent configuration
"""

import json
from typing import Dict, Any, List

def convert_n8n_to_agent_config(n8n_json: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parses an n8n workflow and extracts matching agent fields.
    
    Args:
        n8n_json: The dictionary representing n8n workflow JSON
        
    Returns:
        A dictionary with extracted fields: name, description, system_prompt_hint
    """
    nodes = n8n_json.get('nodes', [])
    name = n8n_json.get('name', 'Agente Importado n8n')
    
    # Try to find a meaningful description or summary from nodes
    description_parts = []
    system_prompt_parts = []
    
    for node in nodes:
        node_type = node.get('type')
        node_name = node.get('name')
        
        # Extract keywords or purposes
        if 'chat' in node_type.lower() or 'ai' in node_type.lower():
            parameters = node.get('parameters', {})
            prompt = parameters.get('systemMessage', '') or parameters.get('prompt', '')
            if prompt:
                system_prompt_parts.append(f"Fluxo Original ({node_name}): {prompt}")
        
        description_parts.append(f"- {node_name} ({node_type})")

    full_description = f"Importado de n8n: {name}\nNós do workflow:\n" + "\n".join(description_parts[:10])
    if len(description_parts) > 10:
        full_description += f"\n... e mais {len(description_parts) - 10} nós."

    return {
        "name": name,
        "description": full_description,
        "system_prompt_hint": "\n\n".join(system_prompt_parts),
        "node_count": len(nodes)
    }
