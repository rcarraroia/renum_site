"""
Publication Service - Sprint 06
Manages agent publication and asset generation
"""

import re
import io
from typing import Optional
from uuid import UUID
from datetime import datetime
from src.config.supabase import supabase_admin
from src.models.wizard import PublicationResult
from src.services.template_service import get_template_service


class PublicationService:
    """Service for managing agent publication"""
    
    def __init__(self):
        self.supabase = supabase_admin
        self.template_service = get_template_service()
        self.base_url = "https://renum.com.br"  # TODO: Get from settings
    
    def generate_slug(self, name: str, client_id: UUID) -> str:
        """
        Generate unique URL-friendly slug
        
        Args:
            name: Agent name
            client_id: Client ID
            
        Returns:
            Unique slug
        """
        # Convert to lowercase and replace spaces with hyphens
        slug = name.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)  # Remove special characters
        slug = re.sub(r'[-\s]+', '-', slug)  # Replace spaces/multiple hyphens with single hyphen
        slug = slug.strip('-')  # Remove leading/trailing hyphens
        
        # Ensure slug is not empty
        if not slug:
            slug = 'agent'
        
        # Check uniqueness
        base_slug = slug
        counter = 1
        
        while True:
            # Check if slug exists for this client
            result = self.supabase.table('agents')\
                .select('id')\
                .eq('client_id', str(client_id))\
                .eq('slug', slug)\
                .execute()
            
            if not result.data or len(result.data) == 0:
                break
            
            # Slug exists, try with counter
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        return slug
    
    def generate_public_url(self, slug: str) -> str:
        """
        Generate public URL
        
        Args:
            slug: Agent slug
            
        Returns:
            Public chat URL
        """
        return f"{self.base_url}/chat/{slug}"
    
    def generate_embed_code(self, agent_id: UUID, slug: str) -> str:
        """
        Generate HTML embed code
        
        Args:
            agent_id: Agent ID
            slug: Agent slug
            
        Returns:
            HTML embed code
        """
        public_url = self.generate_public_url(slug)
        
        embed_code = f"""<!-- RENUM Agent Chat Widget -->
<div id="renum-chat-widget" data-agent-id="{agent_id}" data-slug="{slug}"></div>
<script>
  (function() {{
    var script = document.createElement('script');
    script.src = '{self.base_url}/widget.js';
    script.async = true;
    script.onload = function() {{
      RenumChat.init({{
        agentId: '{agent_id}',
        slug: '{slug}',
        publicUrl: '{public_url}',
        position: 'bottom-right',
        theme: 'light'
      }});
    }};
    document.head.appendChild(script);
  }})();
</script>
<!-- End RENUM Agent Chat Widget -->"""
        
        return embed_code
    
    def generate_qr_code(self, public_url: str) -> str:
        """
        Generate QR code for public URL
        
        Args:
            public_url: Public URL to encode
            
        Returns:
            QR code data URL (base64 encoded PNG)
        """
        try:
            import qrcode
            from base64 import b64encode
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(public_url)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            img_base64 = b64encode(buffer.read()).decode()
            
            return f"data:image/png;base64,{img_base64}"
            
        except ImportError:
            # qrcode library not installed, return placeholder
            return f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={public_url}"
    
    def publish_agent(self, wizard_id: UUID) -> PublicationResult:
        """
        Publish agent and generate all assets
        
        Args:
            wizard_id: Wizard session ID
            
        Returns:
            Publication result with all assets
        """
        # Get wizard session
        wizard_result = self.supabase.table('agents')\
            .select('*')\
            .eq('id', str(wizard_id))\
            .eq('status', 'draft')\
            .single()\
            .execute()
        
        if not wizard_result.data:
            raise ValueError(f"Wizard session {wizard_id} not found")
        
        wizard_data = wizard_result.data
        wizard_config = wizard_data.get('config', {})
        
        # Validate wizard completion
        if not all([
            wizard_config.get('step_1_data'),
            wizard_config.get('step_2_data'),
            wizard_config.get('step_3_data'),
            wizard_config.get('step_4_data'),
        ]):
            raise ValueError("Wizard not completed. Please complete all steps before publishing.")
        
        # Extract wizard data
        step_1 = wizard_config['step_1_data']
        step_2 = wizard_config['step_2_data']
        step_3 = wizard_config['step_3_data']
        step_4 = wizard_config['step_4_data']
        
        # Generate slug
        slug = self.generate_slug(step_1['name'], UUID(wizard_data['client_id']))
        
        # Generate public URL
        public_url = self.generate_public_url(slug)
        
        # Generate system prompt
        system_prompt = self.template_service.generate_system_prompt(
            template_type=step_1['template_type'],
            personality=step_2['personality'],
            tone_formal=step_2['tone_formal'],
            tone_direct=step_2['tone_direct'],
            custom_instructions=step_2.get('custom_instructions'),
            niche=step_1.get('niche'),
        )
        
        # Update agent to active status
        update_data = {
            'name': step_1['name'],
            'description': step_1.get('description'),
            'template_type': step_1['template_type'],
            'system_prompt': system_prompt,
            'slug': slug,
            'public_url': public_url,
            'status': 'active',
            'is_public': True,
            'config': wizard_config,  # Keep wizard config for reference
            'updated_at': datetime.utcnow().isoformat(),
        }
        
        result = self.supabase.table('agents')\
            .update(update_data)\
            .eq('id', str(wizard_id))\
            .execute()
        
        if not result.data:
            raise Exception("Failed to publish agent")
        
        # Generate embed code
        embed_code = self.generate_embed_code(wizard_id, slug)
        
        # Generate QR code
        qr_code_url = self.generate_qr_code(public_url)
        
        return PublicationResult(
            agent_id=wizard_id,
            slug=slug,
            public_url=public_url,
            embed_code=embed_code,
            qr_code_url=qr_code_url,
            status='active',
        )


# Singleton instance
_publication_service = None

def get_publication_service() -> PublicationService:
    """Get singleton instance of PublicationService"""
    global _publication_service
    if _publication_service is None:
        _publication_service = PublicationService()
    return _publication_service
