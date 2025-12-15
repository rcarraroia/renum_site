import io
from typing import List, Dict, Any, Optional
from uuid import uuid4
from datetime import datetime
from fastapi import UploadFile

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document as LangChainDocument

from src.config.settings import settings
from src.config.supabase import supabase_admin
from src.utils.logger import logger
from src.models.knowledge import KnowledgeDocumentResponse, KnowledgeSearchResult

class KnowledgeService:
    def __init__(self):
        self.supabase = supabase_admin
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=settings.OPENAI_API_KEY
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True
        )

    async def list_documents(self, agent_id: str) -> List[KnowledgeDocumentResponse]:
        """List distinct documents for an agent based on metadata source"""
        try:
            # This is a bit inefficient (fetching all to group), but for MVP it works without a separate documents table
            # Ideally we should have a 'agent_documents' table.
            # Using RPC or distinct query if possible. 
            # For now, let's assume we maintain a strictly distinct list of files in a separate table 'agent_documents'
            
            response = self.supabase.table('agent_documents').select('*').eq('agent_id', agent_id).execute()
            if not response.data:
                return []
                
            return [KnowledgeDocumentResponse(**doc) for doc in response.data]
        except Exception as e:
            logger.error(f"Error listing documents: {e}")
            return []

    async def upload_document(self, agent_id: str, file: UploadFile) -> KnowledgeDocumentResponse:
        """Process and index a document"""
        try:
            content = await file.read()
            filename = file.filename
            file_ext = filename.split('.')[-1].lower()
            
            # 1. Extract Text
            text = ""
            if file_ext == 'pdf':
                import pypdf
                pdf_file = io.BytesIO(content)
                reader = pypdf.PdfReader(pdf_file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            elif file_ext in ['txt', 'md', 'csv']:
                text = content.decode('utf-8')
            else:
                raise ValueError(f"Unsupported file type: {file_ext}")
                
            # 2. Create Document Entry
            doc_id = str(uuid4())
            doc_entry = {
                "id": doc_id,
                "agent_id": agent_id,
                "title": filename,
                "file_type": file_ext,
                "status": "indexing",
                "chunk_count": 0,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "metadata": {"size": len(content)}
            }
            
            self.supabase.table('agent_documents').insert(doc_entry).execute()
            
            # 3. Chunk Text
            docs = [LangChainDocument(page_content=text, metadata={"source": filename, "doc_id": doc_id})]
            splits = self.text_splitter.split_documents(docs)
            
            # 4. Generate Embeddings & Store
            chunks_data = []
            
            # Batch processing could be better, but doing simple loop for now
            texts = [doc.page_content for doc in splits]
            embeddings_vectors = await self.embeddings.aembed_documents(texts)
            
            for i, (split, vector) in enumerate(zip(splits, embeddings_vectors)):
                chunks_data.append({
                    "id": str(uuid4()),
                    "agent_id": agent_id,
                    "document_id": doc_id,
                    "content": split.page_content,
                    "metadata": split.metadata,
                    "embedding": vector
                })
            
            if chunks_data:
                # Insert in batches of 100
                batch_size = 100
                for i in range(0, len(chunks_data), batch_size):
                    batch = chunks_data[i:i+batch_size]
                    self.supabase.table('agent_knowledge').insert(batch).execute()
            
            # 5. Update Status
            self.supabase.table('agent_documents').update({
                "status": "ready",
                "chunk_count": len(chunks_data),
                "updated_at": datetime.now().isoformat()
            }).eq("id", doc_id).execute()
            
            doc_entry["status"] = "ready"
            doc_entry["chunk_count"] = len(chunks_data)
            return KnowledgeDocumentResponse(**doc_entry)

        except Exception as e:
            logger.error(f"Error uploading document: {e}")
            if 'doc_id' in locals():
                 self.supabase.table('agent_documents').update({
                    "status": "error",
                    "metadata": {"error": str(e)}
                }).eq("id", doc_id).execute()
            raise

    async def delete_document(self, agent_id: str, document_id: str):
        """Delete a document and its vectors"""
        try:
            # Delete vectors
            self.supabase.table('agent_knowledge').delete().eq('document_id', document_id).eq('agent_id', agent_id).execute()
            # Delete document metadata
            self.supabase.table('agent_documents').delete().eq('id', document_id).eq('agent_id', agent_id).execute()
            return True
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            raise

    async def query_knowledge(self, agent_id: str, query: str, limit: int = 5, threshold: float = 0.5) -> List[KnowledgeSearchResult]:
        """Query knowledge base using vector similarity"""
        try:
            # Generate query embedding
            query_vector = await self.embeddings.aembed_query(query)
            
            # Call Supabase RPC 'match_documents'
            params = {
                "query_embedding": query_vector,
                "match_threshold": threshold,
                "match_count": limit,
                "filter": {"agent_id": agent_id}
            }
            
            # Note: You must ensure an RPC function exist in supabase:
            # create or replace function match_knowledge (
            #   query_embedding vector(1536),
            #   match_threshold float,
            #   match_count int,
            #   filter jsonb
            # )
            # ...
            
            # Using RPC call
            response = self.supabase.rpc('match_agent_knowledge', params).execute()
            
            if not response.data:
                return []
                
            results = []
            for item in response.data:
                results.append(KnowledgeSearchResult(
                    content=item['content'],
                    metadata=item['metadata'],
                    similarity=item['similarity']
                ))
            
            return results
            
        except Exception as e:
            logger.error(f"Error querying knowledge: {e}")
            # Fallback (empty)
            return []
