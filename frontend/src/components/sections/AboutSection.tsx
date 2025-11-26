import React from 'react';
import { motion } from 'framer-motion';
import { Zap, Heart, Lightbulb, Award, Target } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useInView } from 'react-intersection-observer';

const coreValues = [
    { icon: Lightbulb, title: "Inovação", description: "Busca constante por soluções de ponta em IA e automação." },
    { icon: Heart, title: "Empatia", description: "Desenvolvimento focado no cuidado e na experiência humana." },
    { icon: Award, title: "Excelência", description: "Compromisso com a qualidade e resultados superiores." },
    { icon: Target, title: "Propósito", description: "Criar tecnologia que multiplica o impacto positivo." },
];

const AboutSection: React.FC = () => {
    const { ref, inView } = useInView({
        triggerOnce: true,
        threshold: 0.1,
    });

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: {
                staggerChildren: 0.3,
            },
        },
    };

    const itemVariants = {
        hidden: { opacity: 0, y: 50 },
        visible: { opacity: 1, y: 0, transition: { duration: 0.7 } },
    };

    return (
        <section id="about" className="py-20 md:py-32 bg-gray-50 dark:bg-gray-950 overflow-hidden">
            <div className="container mx-auto px-4">
                <motion.h2 
                    ref={ref}
                    initial={{ opacity: 0, y: 50 }}
                    animate={inView ? { opacity: 1, y: 0 } : {}}
                    transition={{ duration: 0.8 }}
                    className="text-4xl md:text-5xl font-bold text-center mb-16 text-primary dark:text-white"
                    style={{ fontFamily: 'Montserrat, sans-serif' }}
                >
                    Nossa História
                </motion.h2>

                <div className="grid md:grid-cols-2 gap-12 items-center">
                    
                    {/* Left Side: Founder Visuals */}
                    <motion.div
                        initial={{ opacity: 0, x: -50 }}
                        animate={inView ? { opacity: 1, x: 0 } : {}}
                        transition={{ duration: 0.8, delay: 0.2 }}
                        className="relative p-8 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700"
                    >
                        {/* Placeholder for Founder Photo */}
                        <div className="w-full h-64 bg-gray-200 dark:bg-gray-700 rounded-lg mb-6 flex items-center justify-center">
                            <span className="text-gray-500">Placeholder Foto Renato Carraro</span>
                        </div>
                        
                        <h3 className="text-2xl font-bold text-[#4e4ea8] dark:text-[#0ca7d2]">Renato Carraro, Fundador</h3>
                        <p className="text-lg font-medium text-muted-foreground">Unindo terapia integrativa e tecnologia</p>

                        {/* Visual element combining tech and human */}
                        <div className="absolute bottom-0 right-0 p-4 opacity-20">
                            <Heart className="h-16 w-16 text-[#FF6B35]" />
                        </div>
                    </motion.div>

                    {/* Right Side: Story and Mission */}
                    <motion.div
                        variants={containerVariants}
                        initial="hidden"
                        animate={inView ? "visible" : "hidden"}
                    >
                        <motion.div variants={itemVariants} className="mb-8">
                            <h4 className="text-xl font-semibold mb-3 text-[#FF6B35]">A Trajetória</h4>
                            <p className="text-lg text-muted-foreground mb-4">
                                Minha trajetória nasceu nas terapias integrativas e no desenvolvimento humano, áreas que moldaram minha visão sobre o cuidado e a transformação das pessoas.
                            </p>
                            <motion.blockquote 
                                className="p-4 border-l-4 border-[#0ca7d2] italic text-primary dark:text-white bg-gray-100 dark:bg-gray-800/50"
                                variants={itemVariants}
                            >
                                "Hoje, aplico essa mesma essência à tecnologia — criando agentes de IA, fluxos automatizados e sistemas que pensam, agem e aprendem com propósito."
                            </motion.blockquote>
                            <p className="text-lg text-muted-foreground mt-4">
                                As terapias me formaram como ser humano, mas a tecnologia é o canal através do qual multiplico o impacto que sempre busquei causar.
                            </p>
                        </motion.div>

                        <motion.div variants={itemVariants} className="mt-10 pt-6 border-t border-border dark:border-gray-700">
                            <h4 className="text-xl font-semibold mb-4 text-[#4e4ea8]">Nossa Missão</h4>
                            <p className="text-lg text-muted-foreground">
                                A missão da Renum é desenvolver tecnologia com sensibilidade humana, criando soluções de IA que não apenas automatizam, mas que também promovem crescimento ético e focado no bem-estar do cliente.
                            </p>
                        </motion.div>
                    </motion.div>
                </div>

                {/* Values Section */}
                <motion.div
                    variants={containerVariants}
                    initial="hidden"
                    animate={inView ? "visible" : "hidden"}
                    className="mt-20"
                >
                    <h3 className="text-3xl font-bold text-center mb-10 text-primary dark:text-white">Nossos Valores</h3>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                        {coreValues.map((value, index) => (
                            <motion.div 
                                key={index} 
                                variants={itemVariants}
                                className="text-center p-6 rounded-xl border border-border dark:border-gray-700 hover:shadow-md transition-shadow bg-white dark:bg-gray-800"
                            >
                                <value.icon className="h-10 w-10 mx-auto mb-3 text-[#0ca7d2] transition-transform hover:scale-110" />
                                <h4 className="font-semibold text-lg mb-1">{value.title}</h4>
                                <p className="text-sm text-muted-foreground">{value.description}</p>
                            </motion.div>
                        ))}
                    </div>
                </motion.div>
            </div>
        </section>
    );
};

export default AboutSection;