-- Enable pgvector if not enabled
create extension if not exists vector;

-- Table to store uploaded document metadata
create table if not exists agent_documents (
  id uuid primary key default gen_random_uuid(),
  agent_id uuid not null, -- references agents(id) on delete cascade
  title text not null,
  file_type text not null, -- 'pdf', 'txt', 'md'
  status text not null default 'indexing', -- 'indexing', 'ready', 'error'
  chunk_count int default 0,
  metadata jsonb default '{}',
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Table to store vector embeddings for RAG
create table if not exists agent_knowledge (
  id uuid primary key default gen_random_uuid(),
  agent_id uuid not null,
  document_id uuid references agent_documents(id) on delete cascade,
  content text not null,
  metadata jsonb default '{}',
  embedding vector(1536), -- OpenAI Small Embedding size
  created_at timestamptz default now()
);

-- Index for fast vector search
create index if not exists agent_knowledge_embedding_idx 
on agent_knowledge 
using ivfflat (embedding vector_cosine_ops)
with (lists = 100);

-- RPC function for similarity search
create or replace function match_agent_knowledge (
  query_embedding vector(1536),
  match_threshold float,
  match_count int,
  filter jsonb
)
returns table (
  id uuid,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    agent_knowledge.id,
    agent_knowledge.content,
    agent_knowledge.metadata,
    1 - (agent_knowledge.embedding <=> query_embedding) as similarity
  from agent_knowledge
  where 1 - (agent_knowledge.embedding <=> query_embedding) > match_threshold
  and (filter ->> 'agent_id')::uuid = agent_knowledge.agent_id
  order by agent_knowledge.embedding <=> query_embedding
  limit match_count;
end;
$$;
