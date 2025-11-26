import React from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Zap } from 'lucide-react';
import { useRenusChat } from '@/context/RenusChatContext';
import { useInView } from 'react-intersection-observer';
import NichesCarousel from './NichesCarousel';

const NichesSection: React.FC = () => {
  const { openChat } = useRenusChat();
  const { ref, inView } = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  return (
    <section id="niches" className="py-20 md:py-32 bg-white dark:bg-gray-900 overflow-hidden">
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
                Soluções Para Seu Setor
            </h2>
            <p className="text-lg text-muted-foreground" style={{ fontFamily: 'Inter, sans-serif' }}>
                Nossa expertise é focada em nichos de alto impacto, onde a IA e a automação geram resultados exponenciais.
            </p>
        </motion.div>

        {/* Niche Carousel */}
        <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={inView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="mb-16"
        >
            <NichesCarousel />
        </motion.div>

        {/* Consolidated CTA */}
        <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={inView ? { opacity: 1, scale: 1 } : {}}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="text-center max-w-3xl mx-auto p-8 bg-gray-50 dark:bg-gray-800 rounded-xl shadow-lg"
        >
            <h3 className="text-2xl font-bold mb-4 text-primary dark:text-white">
                Não encontrou seu setor? Não tem problema!
            </h3>
            <p className="text-md text-muted-foreground mb-6">
                O Renus, nosso agente de descoberta, está treinado para mapear soluções personalizadas para *qualquer* tipo de negócio.
            </p>
            <Button 
                size="lg" 
                className="text-lg px-8 py-6 bg-[#0ca7d2] hover:bg-[#0987a8] text-white shadow-lg"
                onClick={openChat}
            >
                <Zap className="h-5 w-5 mr-2" /> Descubra soluções personalizadas para seu setor
            </Button>
        </motion.div>
      </div>
    </section>
  );
};

export default NichesSection;