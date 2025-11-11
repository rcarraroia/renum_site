import { Network, HeartPulse, Landmark, Wrench, ShoppingCart, GraduationCap, Scale, Home, Utensils, Calculator, TrendingUp, Dumbbell, Sparkles, Briefcase, Tag } from 'lucide-react';
import { LucideIcon } from 'lucide-react';

export interface Niche {
    id: number;
    title: string;
    description: string;
    icon: LucideIcon;
    color: string;
}

export const NICHE_DATA: Niche[] = [
    {
        id: 1,
        title: "Distribuidores MMN",
        description: "Ferramentas que potencializam seu negócio e equipe de distribuidores.",
        icon: Network,
        color: "text-[#FF6B35]",
    },
    {
        id: 2,
        title: "Profissionais de Saúde",
        description: "Soluções para clínicas médicas, odontológicas, terapeutas e psicólogos.",
        icon: HeartPulse,
        color: "text-green-500",
    },
    {
        id: 3,
        title: "Assessores Parlamentares",
        description: "Sistemas para organização de demandas e comunicação eficiente.",
        icon: Landmark,
        color: "text-[#4e4ea8]",
    },
    {
        id: 4,
        title: "Prestadores de Serviços",
        description: "Ferramentas para melhorar atendimento e gestão de serviços.",
        icon: Wrench,
        color: "text-[#0ca7d2]",
    },
    {
        id: 5,
        title: "E-commerce",
        description: "Automação de funis de vendas, suporte e gestão de estoque.",
        icon: ShoppingCart,
        color: "text-purple-500",
    },
    {
        id: 6,
        title: "Educação Online",
        description: "Plataformas de aprendizado e agentes de suporte para alunos.",
        icon: GraduationCap,
        color: "text-yellow-500",
    },
    {
        id: 7,
        title: "Advocacia",
        description: "Gestão de processos, documentos e atendimento jurídico inicial.",
        icon: Scale,
        color: "text-blue-600",
    },
    {
        id: 8,
        title: "Imobiliárias",
        description: "Qualificação de leads, agendamento de visitas e gestão de corretores.",
        icon: Home,
        color: "text-indigo-500",
    },
    {
        id: 9,
        title: "Restaurantes",
        description: "Automação de pedidos, reservas e comunicação com clientes.",
        icon: Utensils,
        color: "text-red-500",
    },
    {
        id: 10,
        title: "Contabilidade",
        description: "Organização de documentos fiscais e comunicação com clientes.",
        icon: Calculator,
        color: "text-gray-600",
    },
    {
        id: 11,
        title: "Marketing Digital",
        description: "Criação de conteúdo, análise de dados e gestão de campanhas.",
        icon: TrendingUp,
        color: "text-pink-500",
    },
    {
        id: 12,
        title: "Academias/Fitness",
        description: "Gestão de matrículas, agendamentos e retenção de alunos.",
        icon: Dumbbell,
        color: "text-lime-500",
    },
    {
        id: 13,
        title: "Beleza e Estética",
        description: "Agendamento, lembretes e gestão de clientes para clínicas e salões.",
        icon: Sparkles,
        color: "text-fuchsia-500",
    },
    {
        id: 14,
        title: "Consultoria Empresarial",
        description: "Mapeamento de processos e geração de relatórios de diagnóstico.",
        icon: Briefcase,
        color: "text-cyan-500",
    },
    {
        id: 15,
        title: "Outros Setores",
        description: "Soluções personalizadas para qualquer nicho de mercado.",
        icon: Tag,
        color: "text-muted-foreground",
    },
];