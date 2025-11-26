import React from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Server, Workflow, MessageSquare, ArrowRight } from 'lucide-react';
import { useRenusChat } from '@/context/RenusChatContext';
import { useInView } from 'react-intersection-observer';
import { Badge } from '@/components/ui/badge';

const serviceData = [
  {
    icon: Server,
    title: "Sistemas AI Native",
    description: "Plataformas completas, SaaS e sistemas integrados com IA avançada",
    tag: "Mais lucrativo",
    uses: ["Portais corporativos", "Ferramentas de análise", "Plataformas personalizadas"],
    color: "bg-[#4e4ea8]", // Primary
  },
  {
    icon: Workflow,
    title: "Workflows em Background",
    description: "Processos empresariais automatizados end-to-end funcionando nos bastidores",
    tag: "Mais eficiente",
    uses: ["Processamento de dados", "Integrações entre sistemas", "Automação de tarefas"],
    color: "bg-[#0ca7d2]", // Accent
  },
  {
    icon: MessageSquare,
    title: "Agentes Solo",
    description: "Assistentes virtuais para atendimento e suporte via WhatsApp e chat",
    tag: "Mais rápido",
    uses: ["Atendimento ao cliente", "Qualificação de leads", "Suporte técnico"],
    color: "bg-[#FF6B35]", // Secondary
  },
];

interface ServiceCardProps {
    data: typeof serviceData[0];
    index: number;
}

const ServiceCard: React.FC<ServiceCardProps> = ({ data, index }) => {
    const { icon: Icon, title, description, tag, uses, color } = data;
    
    const { ref, inView } = useInView({
        triggerOnce: true,
        threshold: 0.2,
    });

    return (
        <motion.div
            ref={ref}
            initial={{ opacity: 0, y: 50 }}
            animate={inView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.6, delay: index * 0.1 }}
            className="h-full"
        >
            <Card className="h-full flex flex-col transition-all duration-300 hover:shadow-xl hover:scale-[1.02] dark:border-gray-700">
                <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-2">
                    <div className="p-3 rounded-full text-white" style={{ backgroundColor: color.replace('bg-', '') }}>
                        <Icon className="h-6 w-6" />
                    </div>
                    <Badge className="bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-200">{tag}</Badge>
                </CardHeader>
                <CardContent className="flex-grow pt-6">
                    <CardTitle className="text-2xl mb-3" style={{ fontFamily: 'Montserrat, sans-serif' }}>{title}</CardTitle>
                    <CardDescription className="mb-4">{description}</CardDescription>
                    
                    <h4 className="text-sm font-semibold mt-4 mb-2 text-muted-foreground">Exemplos de Uso:</h4>
                    <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400 list-disc pl-5">
                        {uses.map((use, i) => (
                            <li key={i}>{use}</li>
                        ))}
                    </ul>
                </CardContent>
                <div className="p-6 pt-0">
                    <Button variant="link" className="p-0 h-auto text-[#FF6B35] hover:text-[#e55f30]">
                        Saiba Mais <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                </div>
            </Card>
        </motion.div>
    );
};

const ServicesSection: React.FC = () => {
  const { openChat } = useRenusChat();
  const { ref, inView } = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  return (
    <section id="services" className="py-20 md:py-32 bg-gray-50 dark:bg-gray-950 overflow-hidden">
      <div className="container mx-auto px-4">
        <motion.div
            ref={ref}
            initial={{ opacity: 0, y: 50 }}
            animate={inView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8 }}
            className="text-center max-w-3xl mx-auto mb-16"
        >
            <h2 
                className="text-4xl md:text-5xl font-bold mb-4 text-primary dark:text-white"
                style={{ fontFamily: 'Montserrat, sans-serif' }}
            >
                Nossas Soluções
            </h2>
            <p className="text-lg text-muted-foreground" style={{ fontFamily: 'Inter, sans-serif' }}>
                Transformamos complexidade em sistemas inteligentes. Nossa abordagem foca em entregar valor rápido, utilizando IA para otimizar cada aspecto do seu negócio.
            </p>
        </motion.div>

        {/* Service Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          {serviceData.map((service, index) => (
            <ServiceCard key={index} data={service} index={index} />
          ))}
        </div>

        {/* CTA */}
        <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={inView ? { opacity: 1, scale: 1 } : {}}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="text-center"
        >
            <Button 
                size="lg" 
                className="text-lg px-8 py-6 bg-[#FF6B35] hover:bg-[#e55f30] text-white shadow-lg"
                onClick={openChat}
            >
                Descubra Sua Solução Ideal (Fale com Renus)
            </Button>
        </motion.div>
      </div>
    </section>
  );
};

export default ServicesSection;