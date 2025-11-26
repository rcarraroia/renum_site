import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Zap, Lightbulb, Layout, Clock, Server, Rocket, ArrowRight } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { useInView } from 'react-intersection-observer';
import { Badge } from '@/components/ui/badge';

const methodologySteps = [
  {
    id: 0,
    icon: Zap,
    title: "Discovery com Renus",
    description: "Nosso agente inteligente coleta requisitos e gera relatórios estruturados.",
    status: "Opcional/Fase 0",
    color: "text-[#0ca7d2]",
  },
  {
    id: 1,
    icon: Lightbulb,
    title: "Brainstorming",
    description: "Definimos objetivos, personas e escopo do projeto.",
    status: "Fase 1",
    color: "text-[#FF6B35]",
  },
  {
    id: 2,
    icon: Layout,
    title: "Design/Frontend",
    description: "Criamos toda a experiência visual para validação.",
    status: "Fase 2 (Ênfase)",
    color: "text-[#4e4ea8]",
    highlight: true,
  },
  {
    id: 3,
    icon: Clock,
    title: "Divisão em Sprints",
    description: "Organizamos o desenvolvimento em módulos priorizados.",
    status: "Fase 3",
    color: "text-green-500",
  },
  {
    id: 4,
    icon: Server,
    title: "Desenvolvimento Backend",
    description: "Implementamos a lógica conforme especificações aprovadas.",
    status: "Fase 4",
    color: "text-red-500",
  },
  {
    id: 5,
    icon: Rocket,
    title: "Testes e Lançamento",
    description: "Garantimos qualidade e implementamos em produção.",
    status: "Fase 5",
    color: "text-yellow-500",
  },
];

const benefits = [
    "Visualização rápida do produto",
    "Mudanças baratas no início do ciclo",
    "Aprovação contínua do cliente",
    "Experiência tangível antes do investimento completo",
];

const MethodologySection: React.FC = () => {
  // Start with the first step, not the highlighted one
  const [activeStep, setActiveStep] = useState(methodologySteps[0]); 
  
  const { ref, inView } = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  // Automatic Carousel Effect
  useEffect(() => {
    if (!inView) return;

    const interval = setInterval(() => {
      setActiveStep(prevStep => {
        const nextIndex = (prevStep.id + 1) % methodologySteps.length;
        return methodologySteps[nextIndex];
      });
    }, 5000); // Change every 5 seconds

    return () => clearInterval(interval);
  }, [inView]);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
  };

  return (
    <section id="methodology" className="py-20 md:py-32 bg-white dark:bg-gray-900 overflow-hidden">
      <div className="container mx-auto px-4">
        <motion.div
            ref={ref}
            initial={{ opacity: 0, y: 50 }}
            animate={inView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8 }}
            className="text-center max-w-4xl mx-auto mb-16"
        >
            <h2 
                className="text-4xl md:text-5xl font-bold mb-2 text-primary dark:text-white"
                style={{ fontFamily: 'Montserrat, sans-serif' }}
            >
                Nossa Metodologia Exclusiva
            </h2>
            <h3 className="text-2xl font-semibold mb-4 text-[#4e4ea8] dark:text-[#0ca7d2]">
                Frontend Primeiro, Resultados Visíveis
            </h3>
            <p className="text-lg text-muted-foreground" style={{ fontFamily: 'Inter, sans-serif' }}>
                Priorizamos a experiência do usuário e a validação visual antes do desenvolvimento pesado de backend, garantindo que o produto final atenda exatamente às suas expectativas.
            </p>
        </motion.div>

        {/* Methodology Timeline (Desktop/Tablet) */}
        <motion.div 
            className="hidden md:block relative pt-8 pb-16"
            variants={containerVariants}
            initial="hidden"
            animate={inView ? "visible" : "hidden"}
        >
            {/* Horizontal Line */}
            <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-border dark:bg-gray-700 transform -translate-y-1/2 mx-12"></div>
            
            <div className="flex justify-between relative z-10">
                {methodologySteps.map((step, index) => (
                    <motion.div 
                        key={step.id} 
                        variants={itemVariants}
                        className="flex flex-col items-center w-1/6 cursor-pointer group"
                        // Removed onMouseEnter/onMouseLeave to enable automatic cycling
                    >
                        <div className={cn(
                            "w-10 h-10 rounded-full flex items-center justify-center transition-all duration-300 border-4",
                            activeStep.id === step.id 
                                ? "bg-white dark:bg-gray-900 border-[#FF6B35] shadow-lg scale-110" 
                                : "bg-background border-border dark:border-gray-700 group-hover:border-[#FF6B35]"
                        )}>
                            <step.icon className={cn("h-5 w-5 transition-colors", step.color.replace('text-', ''))} />
                        </div>
                        <p className="mt-4 text-sm font-medium text-center group-hover:text-primary dark:group-hover:text-white transition-colors">
                            {step.title}
                        </p>
                    </motion.div>
                ))}
            </div>
        </motion.div>

        {/* Methodology Timeline (Mobile - Vertical) */}
        <div className="md:hidden space-y-8 relative border-l border-border dark:border-gray-700 pl-6">
            {methodologySteps.map((step, index) => (
                <motion.div 
                    key={step.id} 
                    initial={{ opacity: 0, x: -20 }}
                    animate={inView ? { opacity: 1, x: 0 } : {}}
                    transition={{ duration: 0.5, delay: index * 0.1 }}
                    className="relative"
                >
                    <div className={cn(
                        "absolute -left-5 top-0 w-10 h-10 rounded-full flex items-center justify-center transition-all duration-300 border-4",
                        activeStep.id === step.id 
                            ? "bg-white dark:bg-gray-900 border-[#FF6B35] shadow-lg" 
                            : "bg-background border-border dark:border-gray-700"
                    )}>
                        <step.icon className={cn("h-5 w-5", step.color.replace('text-', ''))} />
                    </div>
                    <Card className="p-4 ml-4">
                        <CardTitle className="text-lg">{step.title}</CardTitle>
                        <p className="text-sm text-muted-foreground mt-1">{step.description}</p>
                        <Badge variant="secondary" className="mt-2">{step.status}</Badge>
                    </Card>
                </motion.div>
            ))}
        </div>


        {/* Detail Card and Callout Box */}
        <div className="mt-16 grid md:grid-cols-3 gap-8">
            {/* Detail Card (Desktop) */}
            <motion.div 
                key={activeStep.id} // Key change forces re-render and animation
                className="md:col-span-2"
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5 }}
            >
                <Card className="p-6 h-full border-l-4 border-[#4e4ea8] dark:border-[#0ca7d2]">
                    <CardHeader className="p-0 mb-4">
                        <CardTitle className="text-3xl flex items-center">
                            <activeStep.icon className={cn("h-6 w-6 mr-3", activeStep.color.replace('text-', ''))} />
                            {activeStep.title}
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="p-0">
                        <p className="text-lg text-muted-foreground">{activeStep.description}</p>
                        <Badge variant="default" className="mt-4 bg-[#FF6B35]">{activeStep.status}</Badge>
                    </CardContent>
                </Card>
            </motion.div>

            {/* Frontend Primeiro Callout Box */}
            <motion.div
                initial={{ opacity: 0, x: 50 }}
                animate={inView ? { opacity: 1, x: 0 } : {}}
                transition={{ duration: 0.8, delay: 0.8 }}
            >
                <Card className="p-6 bg-[#4e4ea8] dark:bg-gray-800 text-white h-full">
                    <CardTitle className="text-xl mb-4 flex items-center text-[#0ca7d2]">
                        <Layout className="h-6 w-6 mr-2" />
                        Por que "Frontend Primeiro"?
                    </CardTitle>
                    <ul className="space-y-3">
                        {benefits.map((benefit, index) => (
                            <li key={index} className="flex items-start text-sm">
                                <ArrowRight className="h-4 w-4 mr-2 mt-1 flex-shrink-0 text-[#FF6B35]" />
                                {benefit}
                            </li>
                        ))}
                    </ul>
                </Card>
            </motion.div>
        </div>
      </div>
    </section>
  );
};

export default MethodologySection;