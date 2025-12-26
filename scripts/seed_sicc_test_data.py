#!/usr/bin/env python3
"""
Script para criar dados de teste nas tabelas SICC
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import uuid

# Carrega .env do backend
backend_env = Path(__file__).parent.parent / 'backend' / '.env'
if backend_env.exists():
    from dotenv import load_dotenv
    load_dotenv(backend_env)

from supabase import create_client

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_ANON_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ ERRO: Variáveis SUPABASE_URL e SUPABASE_KEY não configuradas")
    sys.exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_agent_id(slug: str) -> str:
    """Busca ID do agente pelo slug"""
    result = supabase.table("agents").select("id").eq("slug", slug).limit(1).execute()
    if result.data:
        return result.data[0]["id"]
    return None

def seed_memory_chunks(agent_id: str):
    """Cria memórias de teste"""
    # Precisa de um client_id - vamos buscar ou usar um padrão
    client_result = supabase.table("clients").select("id").limit(1).execute()
    client_id = client_result.data[0]["id"] if client_result.data else agent_id
    
    memories = [
        {
            "agent_id": agent_id,
            "client_id": client_id,
            "content": "Cliente interessado em automação de WhatsApp para vendas. Demonstrou interesse em plano Pro.",
            "chunk_type": "insight",
            "confidence_score": 0.85,
            "is_active": True,
            "metadata": {"source": "conversation", "client_type": "lead"}
        },
        {
            "agent_id": agent_id,
            "client_id": client_id,
            "content": "FAQ: Como funciona o sistema de agentes? R: O sistema permite criar agentes de IA personalizados para diferentes nichos.",
            "chunk_type": "faq",
            "confidence_score": 0.92,
            "is_active": True,
            "metadata": {"category": "produto", "frequency": "alta"}
        },
        {
            "agent_id": agent_id,
            "client_id": client_id,
            "content": "Estratégia: Quando cliente pergunta sobre preço, primeiro qualificar necessidades antes de apresentar valores.",
            "chunk_type": "process",
            "confidence_score": 0.78,
            "is_active": True,
            "metadata": {"type": "sales", "effectiveness": 0.82}
        },
        {
            "agent_id": agent_id,
            "client_id": client_id,
            "content": "Termo de negócio: MLM = Marketing Multinível. Modelo de vendas diretas com rede de distribuidores.",
            "chunk_type": "business_term",
            "confidence_score": 0.65,
            "is_active": True,
            "metadata": {"domain": "mlm"}
        }
    ]
    
    for memory in memories:
        try:
            supabase.table("memory_chunks").insert(memory).execute()
            print(f"   ✅ Memória criada: {memory['chunk_type']}")
        except Exception as e:
            print(f"   ❌ Erro ao criar memória: {e}")

def seed_learning_logs(agent_id: str):
    """Cria aprendizados de teste"""
    # Precisa de um client_id
    client_result = supabase.table("clients").select("id").limit(1).execute()
    client_id = client_result.data[0]["id"] if client_result.data else agent_id
    
    learnings = [
        {
            "agent_id": agent_id,
            "client_id": client_id,
            "learning_type": "pattern_detection",
            "source_data": {"detected_from": "10 conversas", "keywords": ["preço", "plano"]},
            "analysis": {"suggestion": "Enviar tabela de planos com comparativo", "success_rate": 0.85},
            "confidence": 0.92,
            "status": "pending"
        },
        {
            "agent_id": agent_id,
            "client_id": client_id,
            "learning_type": "faq_detection",
            "source_data": {"question": "Vocês têm integração com WhatsApp?", "occurrences": 15},
            "analysis": {"suggested_answer": "Sim, temos integração nativa com WhatsApp Business API"},
            "confidence": 0.88,
            "status": "pending"
        },
        {
            "agent_id": agent_id,
            "client_id": client_id,
            "learning_type": "behavior_correction",
            "source_data": {"issue": "Mencionou preços sem qualificar"},
            "analysis": {"correction": "Não mencionar preços específicos sem antes qualificar o lead"},
            "action_taken": "Regra adicionada ao comportamento",
            "confidence": 0.75,
            "status": "approved"
        }
    ]
    
    for learning in learnings:
        try:
            supabase.table("learning_logs").insert(learning).execute()
            print(f"   ✅ Aprendizado criado: {learning['learning_type']} ({learning['status']})")
        except Exception as e:
            print(f"   ❌ Erro ao criar aprendizado: {e}")

def seed_behavior_patterns(agent_id: str):
    """Cria padrões de comportamento de teste"""
    # Precisa de um client_id
    client_result = supabase.table("clients").select("id").limit(1).execute()
    client_id = client_result.data[0]["id"] if client_result.data else agent_id
    
    patterns = [
        {
            "agent_id": agent_id,
            "client_id": client_id,
            "pattern_type": "response_strategy",
            "trigger_context": {"keywords": ["orçamento", "preço", "quanto custa", "valores"]},
            "action_config": {"action": "qualify_first", "template": "Antes de falar sobre valores, me conta um pouco mais sobre sua necessidade..."},
            "confidence": 0.85,
            "application_count": 47,
            "success_rate": 0.78,
            "is_active": True
        },
        {
            "agent_id": agent_id,
            "client_id": client_id,
            "pattern_type": "objection_handling",
            "trigger_context": {"keywords": ["atendente", "humano", "pessoa real", "reclamação"]},
            "action_config": {"action": "escalate", "template": "Entendo sua necessidade. Vou transferir você para um de nossos especialistas."},
            "confidence": 0.95,
            "application_count": 12,
            "success_rate": 0.92,
            "is_active": True
        }
    ]
    
    for pattern in patterns:
        try:
            supabase.table("behavior_patterns").insert(pattern).execute()
            print(f"   ✅ Padrão criado: {pattern['pattern_type']}")
        except Exception as e:
            print(f"   ❌ Erro ao criar padrão: {e}")

def seed_agent_metrics(agent_id: str):
    """Cria métricas de teste"""
    from datetime import date
    
    metrics = {
        "agent_id": agent_id,
        "metric_date": date.today().isoformat(),
        "total_memories": 4,
        "active_memories": 4,
        "total_patterns": 2,
        "active_patterns": 2,
        "learning_velocity": 0.65,
        "avg_confidence": 0.82,
        "success_rate": 0.78,
        "interactions_count": 156,
        "auto_approved_learnings": 5,
        "manual_approved_learnings": 3,
        "rejected_learnings": 1
    }
    
    try:
        # Verifica se já existe métrica para este agente e data
        existing = supabase.table("agent_metrics").select("id").eq("agent_id", agent_id).eq("metric_date", metrics["metric_date"]).execute()
        if existing.data:
            supabase.table("agent_metrics").update(metrics).eq("agent_id", agent_id).eq("metric_date", metrics["metric_date"]).execute()
            print(f"   ✅ Métricas atualizadas")
        else:
            supabase.table("agent_metrics").insert(metrics).execute()
            print(f"   ✅ Métricas criadas")
    except Exception as e:
        print(f"   ❌ Erro ao criar métricas: {e}")

def main():
    print("=" * 60)
    print("🌱 SEED DADOS DE TESTE SICC")
    print("=" * 60)
    
    # Busca agente RENUS
    renus_id = get_agent_id("renus")
    if not renus_id:
        print("❌ Agente RENUS não encontrado!")
        sys.exit(1)
    
    print(f"📍 Agente RENUS: {renus_id[:8]}...")
    print()
    
    print("📝 Criando memórias...")
    seed_memory_chunks(renus_id)
    print()
    
    print("📚 Criando aprendizados...")
    seed_learning_logs(renus_id)
    print()
    
    print("🎯 Criando padrões de comportamento...")
    seed_behavior_patterns(renus_id)
    print()
    
    print("📊 Criando métricas...")
    seed_agent_metrics(renus_id)
    print()
    
    print("=" * 60)
    print("✅ SEED CONCLUÍDO!")
    print("=" * 60)
    print()
    print("Agora você pode testar:")
    print(f"  → /dashboard/admin/agents/renus/intelligence/evolution")
    print(f"  → /dashboard/admin/agents/renus/intelligence/memories")
    print(f"  → /dashboard/admin/agents/renus/intelligence/queue")

if __name__ == "__main__":
    main()
