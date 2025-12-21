"""
Wizard Service - Sprint 06
Manages wizard sessions and progress
"""

from typing import Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime
from src.config.supabase import supabase_admin
from src.models.wizard import (
    WizardSession,
    WizardSessionCreate,
    WizardStep1Data,
    WizardStep2Data,
    WizardStep3Data,
    WizardStep4Data,
    WizardStep5Data,
)


class WizardService:
    """Service for managing wizard sessions"""
    
    def __init__(self):
        self.supabase = supabase_admin
    
    def start_wizard(self, client_id: Optional[UUID] = None, category: Optional[str] = None) -> WizardSession:
        """
        Create new wizard session
        
        Args:
            client_id: Client ID creating the agent (optional, None para templates)
            category: Category for template (b2b/b2c)
            
        Returns:
            Created wizard session
            
        Raises:
            ValueError: If B2C client has reached agent limit
        """
        # Check B2C agent limit only if client_id is provided
        if client_id:
            self._check_b2c_limit(client_id)
        
        # Se não tem client_id, está criando template
        is_template = client_id is None
        
        wizard_id = uuid4()
        now = datetime.utcnow()
        
        # Create wizard session record in agents table (Sprint 09 update)
        # Store wizard progress in config JSONB field
        
        wizard_data = {
            'id': str(wizard_id),
            'client_id': str(client_id) if client_id else None,
            'name': f'Draft {"Template" if is_template else "Agent"} {wizard_id.hex[:8]}',
            'description': 'Template in creation' if is_template else 'Agent in creation',
            # 'channel': 'web',  # Rely on DB default to avoid schema cache issues
            # 'system_prompt': 'Draft template' if is_template else 'Draft agent', # Rely on DB default
            'slug': f'draft-{"template" if is_template else "agent"}-{wizard_id.hex[:8]}',
            # 'model': 'gpt-4o-mini', # Rely on DB default
            # 'status': 'draft', # Rely on DB default
            # 'model': 'gpt-4o-mini', # Rely on DB default
            # 'status': 'draft', # Rely on DB default
            'template_type': 'custom',
            'is_public': False,
            'is_template': is_template,
            'category': category,
            'marketplace_visible': False,
            'config': {
                'wizard_session': True,
                'current_step': 1,
                'step_1_data': None,
                'step_2_data': None,
                'step_3_data': None,
                'step_4_data': None,
                'step_5_data': None,
            },
            'created_at': now.isoformat(),
            'updated_at': now.isoformat(),
        }
        
        result = self.supabase.table('agents').insert(wizard_data).execute()
        
        if not result.data:
            raise Exception("Failed to create wizard session")
        
        return self._parse_wizard_session(result.data[0])
    
    def save_step(
        self,
        wizard_id: UUID,
        step_number: int,
        data: Dict[str, Any]
    ) -> WizardSession:
        """
        Save progress for a specific step
        
        Args:
            wizard_id: Wizard session ID
            step_number: Step number (1-5)
            data: Step data
            
        Returns:
            Updated wizard session
        """
        # Get current wizard session
        result = self.supabase.table('agents')\
            .select('*')\
            .eq('id', str(wizard_id))\
            .eq('status', 'draft')\
            .single()\
            .execute()
        
        if not result.data:
            raise ValueError(f"Wizard session {wizard_id} not found")
        
        current_config = result.data.get('config', {})
        
        # Update step data
        step_key = f'step_{step_number}_data'
        current_config[step_key] = data
        current_config['current_step'] = step_number
        
        # Update wizard session
        update_data = {
            'config': current_config,
            'updated_at': datetime.utcnow().isoformat(),
        }
        
        # Sync specific fields to main columns for visibility
        if step_number == 1:
            if 'client_id' in data:
                update_data['client_id'] = data['client_id']
        
        if step_number == 2:
            if 'name' in data:
                update_data['name'] = data['name']
            if 'description' in data:
                update_data['description'] = data['description']
            if 'template_type' in data:
                update_data['template_type'] = data['template_type']

        if step_number == 3:
            if 'channels' in data and data['channels']:
                # For now take the first channel as primary or store as string
                update_data['channel'] = data['channels'][0] 
            if 'model' in data:
                update_data['model'] = data['model']
        
        result = self.supabase.table('agents')\
            .update(update_data)\
            .eq('id', str(wizard_id))\
            .execute()
        
        if not result.data:
            raise Exception("Failed to update wizard session")
        
        return self._parse_wizard_session(result.data[0])
    
    def get_wizard(self, wizard_id: UUID) -> Optional[WizardSession]:
        """
        Retrieve wizard session
        
        Args:
            wizard_id: Wizard session ID
            
        Returns:
            Wizard session or None if not found
        """
        result = self.supabase.table('agents')\
            .select('*')\
            .eq('id', str(wizard_id))\
            .eq('status', 'draft')\
            .single()\
            .execute()
        
        if not result.data:
            return None
        
        return self._parse_wizard_session(result.data)
    
    def delete_wizard(self, wizard_id: UUID, force: bool = False) -> bool:
        """
        Delete wizard session (abandon)
        
        Args:
            wizard_id: Wizard session ID
            force: If True, delete regardless of status (for testing)
            
        Returns:
            True if deleted successfully
        """
        query = self.supabase.table('agents').delete().eq('id', str(wizard_id))
        
        # Only filter by draft status if not forcing
        if not force:
            query = query.eq('status', 'draft')
        
        result = query.execute()
        
        return len(result.data) > 0 if result.data else False
    
    def list_drafts(self, client_id: UUID) -> list[WizardSession]:
        """
        List all draft wizard sessions for a client
        
        Args:
            client_id: Client ID
            
        Returns:
            List of wizard sessions
        """
        result = self.supabase.table('agents')\
            .select('*')\
            .eq('client_id', str(client_id))\
            .eq('status', 'draft')\
            .order('created_at', desc=True)\
            .execute()
        
        if not result.data:
            return []
        
        return [self._parse_wizard_session(item) for item in result.data]
    
    def _check_b2c_limit(self, client_id: UUID) -> None:
        """
        Check if B2C client has reached agent limit
        
        Args:
            client_id: Client ID
            
        Raises:
            ValueError: If B2C client has reached limit
        """
        # Get client info
        client_result = self.supabase.table('clients')\
            .select('*')\
            .eq('id', str(client_id))\
            .single()\
            .execute()
        
        if not client_result.data:
            raise ValueError(f"Client {client_id} not found")
        
        client = client_result.data
        
        # Check if client is B2C (we'll use a field or convention to identify)
        # For now, we'll check if there's a 'type' field or use segment
        client_type = client.get('type') or client.get('segment', '').lower()
        
        is_b2c = 'b2c' in client_type or 'distribuidor' in client_type or 'mmn' in client_type
        
        if is_b2c:
            # Count active agents for this client
            count_result = self.supabase.table('agents')\
                .select('id', count='exact')\
                .eq('client_id', str(client_id))\
                .in_('status', ['active', 'paused'])\
                .execute()
            
            active_count = count_result.count or 0
            
            if active_count >= 1:
                raise ValueError(
                    "B2C clients can only create 1 agent. "
                    "Please upgrade to B2B plan to create more agents. "
                    "Contact support or visit /pricing for upgrade options."
                )
    
    def _parse_wizard_session(self, data: Dict[str, Any]) -> WizardSession:
        """Parse database record to WizardSession model"""
        config = data.get('config', {})
        
        # Parse step data
        step_1_data = None
        if config.get('step_1_data'):
            try:
                step_1_data = WizardStep1Data(**config['step_1_data'])
            except Exception:
                pass
        
        step_2_data = None
        if config.get('step_2_data'):
            try:
                step_2_data = WizardStep2Data(**config['step_2_data'])
            except Exception:
                pass
        
        step_3_data = None
        if config.get('step_3_data'):
            try:
                step_3_data = WizardStep3Data(**config['step_3_data'])
            except Exception:
                pass
        
        step_4_data = None
        if config.get('step_4_data'):
            try:
                step_4_data = WizardStep4Data(**config['step_4_data'])
            except Exception:
                pass
        
        step_5_data = None
        if config.get('step_5_data'):
            try:
                step_5_data = WizardStep5Data(**config['step_5_data'])
            except Exception:
                pass
        
        return WizardSession(
            id=UUID(data['id']),
            client_id=UUID(data['client_id']) if data.get('client_id') else None,
            current_step=config.get('current_step', 1),
            step_1_data=step_1_data,
            step_2_data=step_2_data,
            step_3_data=step_3_data,
            step_4_data=step_4_data,
            step_5_data=step_5_data,
            created_at=datetime.fromisoformat(data['created_at'].replace('Z', '+00:00')),
            updated_at=datetime.fromisoformat(data['updated_at'].replace('Z', '+00:00')),
        )
    
    def validate_step(self, step_number: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate step data
        
        Args:
            step_number: Step number (1-5)
            data: Step data to validate
            
        Returns:
            Validation result with errors if any
        """
        errors = []
        
        try:
            if step_number == 1:
                WizardStep1Data(**data)
            elif step_number == 2:
                WizardStep2Data(**data)
            elif step_number == 3:
                WizardStep3Data(**data)
            elif step_number == 4:
                WizardStep4Data(**data)
            elif step_number == 5:
                WizardStep5Data(**data)
            elif step_number == 6:
                # Step 6 is review, no specific model but we allow it
                pass
            else:
                errors.append(f"Invalid step number: {step_number}")
        except Exception as e:
            errors.append(str(e))
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }


# Singleton instance
_wizard_service = None

def get_wizard_service() -> WizardService:
    """Get singleton instance of WizardService"""
    global _wizard_service
    if _wizard_service is None:
        _wizard_service = WizardService()
    return _wizard_service
