"""
Serviço de negócio para Leads
"""
from typing import Optional
from datetime import datetime
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
    
    async def capture_from_conversation(
        self,
        conversation_id: str,
        agent_id: str,
        messages: Optional[list] = None
    ) -> Optional[LeadResponse]:
        """
        Captura lead automaticamente de uma conversa
        
        Args:
            conversation_id: ID da conversa
            agent_id: ID do agente (RENUS ou sub-agente)
            messages: Lista de mensagens (opcional, busca se não fornecido)
            
        Returns:
            Lead criado ou None se dados insuficientes
        """
        try:
            # 1. Buscar mensagens se não fornecidas
            if not messages:
                messages = await self._get_conversation_messages(conversation_id)
            
            if not messages:
                logger.info(f"No messages found for conversation {conversation_id}")
                return None
            
            # 2. Extrair dados de contato usando IA
            contact_data = await self._extract_contact_info(messages)
            
            # 3. Validar dados mínimos (pelo menos email ou telefone)
            if not (contact_data.get('email') or contact_data.get('phone')):
                logger.info(f"Insufficient contact data in conversation {conversation_id}")
                return None
            
            # 4. Verificar se lead já existe
            existing_lead = None
            if contact_data.get('phone'):
                existing = supabase_admin.table("leads").select("*").eq(
                    "phone", contact_data['phone']
                ).execute()
                if existing.data:
                    existing_lead = existing.data[0]
            
            if existing_lead:
                # Atualizar lead existente com novos dados
                update_data = {}
                if contact_data.get('name') and not existing_lead.get('name'):
                    update_data['name'] = contact_data['name']
                if contact_data.get('email') and not existing_lead.get('email'):
                    update_data['email'] = contact_data['email']
                
                # Adicionar notas sobre a conversa (usando campo 'notes' ao invés de 'metadata')
                existing_notes = existing_lead.get('notes', '')
                conversation_note = f"Conversa {conversation_id} com agente {agent_id} em {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                if existing_notes:
                    update_data['notes'] = f"{existing_notes}\n{conversation_note}"
                else:
                    update_data['notes'] = conversation_note
                
                update_data['last_interaction_at'] = datetime.now().isoformat()
                
                if update_data:
                    response = supabase_admin.table("leads").update(
                        update_data
                    ).eq("id", existing_lead['id']).execute()
                    
                    logger.info(f"Updated existing lead: {existing_lead['id']}")
                    return LeadResponse(**response.data[0])
                else:
                    logger.info(f"Lead already up to date: {existing_lead['id']}")
                    return LeadResponse(**existing_lead)
            
            # 5. Criar novo lead
            lead_data = {
                'name': contact_data.get('name', f"Lead {contact_data.get('phone', contact_data.get('email'))}"),
                'email': contact_data.get('email'),
                'phone': contact_data.get('phone'),
                'source': 'pesquisa',  # Usar valor válido do constraint
                'status': 'qualificado',  # Usar valor válido do constraint
                'subagent_id': agent_id,
                'notes': f"Capturado automaticamente da conversa {conversation_id} com agente {agent_id}",
                'first_contact_at': datetime.now().isoformat(),
                'last_interaction_at': datetime.now().isoformat(),
                'score': 50  # Score padrão
            }
            
            response = supabase_admin.table("leads").insert(
                lead_data
            ).execute()
            
            if not response.data:
                raise ValidationError("Failed to create lead from conversation")
            
            created = response.data[0]
            logger.info(f"Created lead from conversation: {created['id']}")
            
            # 6. Registrar no histórico
            await self._log_lead_creation(created['id'], agent_id, conversation_id)
            
            return LeadResponse(**created)
            
        except Exception as e:
            logger.error(f"Error capturing lead from conversation: {str(e)}")
            return None
    
    async def _get_conversation_messages(self, conversation_id: str) -> list:
        """Busca mensagens de uma conversa"""
        try:
            # Tentar buscar em interview_messages primeiro (tem coluna 'role')
            response = supabase_admin.table("interview_messages").select("*").eq(
                "interview_id", conversation_id
            ).order("created_at").execute()
            
            if response.data:
                return [
                    {
                        'role': msg.get('role', 'user'),
                        'content': msg.get('content', ''),
                        'timestamp': msg.get('created_at', '')
                    }
                    for msg in response.data
                ]
            
            # Se não encontrar, tentar em messages (usar 'sender' ao invés de 'role')
            response = supabase_admin.table("messages").select("*").eq(
                "conversation_id", conversation_id
            ).order("created_at").execute()
            
            if response.data:
                return [
                    {
                        'role': 'user' if msg.get('sender') == 'user' else 'assistant',
                        'content': msg.get('content', ''),
                        'timestamp': msg.get('created_at', '')
                    }
                    for msg in response.data
                ]
            
            return []
            
        except Exception as e:
            logger.error(f"Error getting conversation messages: {e}")
            return []
    
    async def _extract_contact_info(self, messages: list) -> dict:
        """
        Extrai informações de contato das mensagens usando IA
        """
        try:
            # Concatenar mensagens do usuário
            user_messages = [
                msg['content'] for msg in messages 
                if msg.get('role') == 'user' and msg.get('content')
            ]
            
            if not user_messages:
                return {}
            
            conversation_text = " ".join(user_messages)
            
            # Usar regex simples primeiro (mais rápido)
            contact_data = {}
            
            # Extrair email
            import re
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, conversation_text)
            if emails:
                contact_data['email'] = emails[0]
            
            # Extrair telefone (formato brasileiro)
            phone_patterns = [
                r'\+55\s*\(?(\d{2})\)?\s*\d{4,5}[-\s]?\d{4}',  # +55 (11) 99999-9999
                r'\(?(\d{2})\)?\s*\d{4,5}[-\s]?\d{4}',         # (11) 99999-9999
                r'\d{10,11}',                                   # 11999999999
            ]
            
            for pattern in phone_patterns:
                phones = re.findall(pattern, conversation_text)
                if phones:
                    # Normalizar telefone
                    phone = re.sub(r'[^\d]', '', phones[0] if isinstance(phones[0], str) else conversation_text)
                    if len(phone) >= 10:
                        if not phone.startswith('55'):
                            phone = '55' + phone
                        contact_data['phone'] = '+' + phone
                        break
            
            # Extrair nome (heurística simples)
            # Procurar por "meu nome é", "me chamo", etc.
            name_patterns = [
                r'(?:meu nome é|me chamo|sou (?:a|o)?)\s+([A-Za-zÀ-ÿ\s]{2,30})',
                r'(?:nome:?)\s+([A-Za-zÀ-ÿ\s]{2,30})',
            ]
            
            for pattern in name_patterns:
                names = re.findall(pattern, conversation_text, re.IGNORECASE)
                if names:
                    name = names[0].strip().title()
                    # Validar se parece um nome real
                    if len(name.split()) <= 4 and all(len(word) >= 2 for word in name.split()):
                        contact_data['name'] = name
                        break
            
            logger.info(f"Extracted contact data: {contact_data}")
            return contact_data
            
        except Exception as e:
            logger.error(f"Error extracting contact info: {e}")
            return {}
    
    async def _log_lead_creation(self, lead_id: str, agent_id: str, conversation_id: str):
        """Registra criação de lead no histórico"""
        try:
            # Registrar em uma tabela de auditoria (se existir)
            # Por enquanto, apenas log
            logger.info(f"Lead created - ID: {lead_id}, Agent: {agent_id}, Conversation: {conversation_id}")
            
        except Exception as e:
            logger.error(f"Error logging lead creation: {e}")

    async def create_from_conversation(
        self, 
        phone: str, 
        name: Optional[str] = None, 
        email: Optional[str] = None,
        source: str = "chat",
        subagent_id: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> LeadResponse:
        """
        Cria lead a partir de conversa com sub-agente
        
        Args:
            phone: Telefone do lead (obrigatório)
            name: Nome do lead (opcional)
            email: Email do lead (opcional)
            source: Origem do lead (default: "chat")
            subagent_id: ID do sub-agente que gerou o lead
            metadata: Dados adicionais da conversa
            
        Returns:
            Lead criado
        """
        try:
            # Verificar se já existe lead com este telefone
            existing = supabase_admin.table("leads").select("*").eq(
                "phone", phone
            ).execute()
            
            if existing.data:
                # Atualizar lead existente
                lead_id = existing.data[0]["id"]
                update_data = {}
                
                if name and not existing.data[0].get("name"):
                    update_data["name"] = name
                if email and not existing.data[0].get("email"):
                    update_data["email"] = email
                if subagent_id:
                    update_data["subagent_id"] = subagent_id
                if metadata:
                    existing_metadata = existing.data[0].get("metadata", {})
                    existing_metadata.update(metadata)
                    update_data["metadata"] = existing_metadata
                
                if update_data:
                    response = supabase_admin.table("leads").update(
                        update_data
                    ).eq("id", lead_id).execute()
                    
                    logger.info(f"Updated existing lead: {lead_id}")
                    return LeadResponse(**response.data[0])
                else:
                    logger.info(f"Lead already exists: {lead_id}")
                    return LeadResponse(**existing.data[0])
            
            # Criar novo lead
            lead_data = {
                "phone": phone,
                "name": name or f"Lead {phone}",
                "email": email,
                "source": "pesquisa",  # Usar valor válido do constraint
                "status": "qualificado",  # Usar valor válido do constraint
                "subagent_id": subagent_id,
                "metadata": metadata or {}
            }
            
            response = supabase_admin.table("leads").insert(
                lead_data
            ).execute()
            
            if not response.data:
                raise ValidationError("Failed to create lead from conversation")
            
            created = response.data[0]
            logger.info(f"Created lead from conversation: {created['id']}")
            
            return LeadResponse(**created)
            
        except Exception as e:
            logger.error(f"Error creating lead from conversation: {str(e)}")
            raise ValidationError(f"Failed to create lead: {str(e)}")

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
