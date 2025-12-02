import { Agent, CategoryMock } from "@/types/agent";

export const mockProjects = [
  { id: "1", name: "Pacote Enterprise Slim", client_id: "1", agents_limit: 10 },
  { id: "2", name: "Pacote MMN Discovery", client_id: "2", agents_limit: 5 },
  { id: "3", name: "Pacote Básico COMADEMIG", client_id: "3", agents_limit: 3 }
]

export const mockClients = [
  { id: "1", name: "Slim Quality Ltda", type: "b2b_empresa", slug: "slim" },
  { id: "2", name: "MMN Marketplace", type: "b2c_marketplace", slug: "mmn" },
  { id: "3", name: "COMADEMIG", type: "b2b_empresa", slug: "comademig" }
]

export const mockAgents: Agent[] = [
  {
    id: "1",
    name: "Agente de Vendas Slim",
    description: "Agente especializado em vendas de colchões",
    client_id: "1",
    project_id: "1",
    type: "b2b_empresa",
    category: "vendas",
    slug: "slim",
    domain: "slim.renum.com.br",
    channel: ["whatsapp"],
    model: "gpt-4o-mini",
    status: "ativo",
    instances_count: 47,
    conversations_today: 123,
    created_at: "2025-11-15",
    version: "V1.2"
  },
  {
    id: "2",
    name: "Discovery MMN",
    description: "Agente de descoberta para distribuidores",
    client_id: "2",
    project_id: "2",
    type: "b2c_individual",
    category: "discovery",
    slug: "mmn",
    domain: "mmn.renum.com.br",
    channel: ["whatsapp", "web"],
    model: "gpt-4o-mini",
    status: "ativo",
    instances_count: 0,
    conversations_today: 8,
    created_at: "2025-11-20",
    version: "V1.0"
  }
]

export const mockChannels = [
  { id: "whatsapp", name: "WhatsApp Business", icon: "📱" },
  { id: "web", name: "Widget Web (Site)", icon: "🌐" },
  { id: "telegram", name: "Telegram", icon: "✈️" },
  { id: "sms", name: "SMS", icon: "💬" }
]

export const mockModels = [
  { id: "gpt-4o", name: "GPT-4o", provider: "OpenAI", cost: "$$$", description: "Mais inteligente" },
  { id: "gpt-4o-mini", name: "GPT-4o-mini", provider: "OpenAI", cost: "$$", description: "Balanceado (Recomendado)" },
  { id: "claude-3-5-sonnet", name: "Claude 3.5 Sonnet", provider: "Anthropic", cost: "$$$", description: "Excelente para textos" },
  { id: "claude-3-haiku", name: "Claude 3 Haiku", provider: "Anthropic", cost: "$$", description: "Rápido e econômico" }
]

export const mockCategories: CategoryMock[] = [
  { id: "discovery", name: "Discovery (Entrevistas)", icon: "🔍" },
  { id: "vendas", name: "Vendas", icon: "💼" },
  { id: "suporte", name: "Suporte", icon: "🎧" },
  { id: "mmn", name: "MMN (Marketing Multinível)", icon: "🔗" },
  { id: "clinica", name: "Clínica (Saúde)", icon: "🏥" },
  { id: "vereador", name: "Vereador (Político)", icon: "🏛️" },
  { id: "custom", name: "Personalizado", icon: "⚙️" }
]