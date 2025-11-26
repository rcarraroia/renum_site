import React from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Zap, Calendar } from 'lucide-react';
import { useRenusChat } from '@/context/RenusChatContext';
import { useInView } from 'react-intersection-observer';

const CTASection: React.FC = () => {
  const { openChat } = useRenusChat();
  const { ref, inView } = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  return (
    <section id="cta" className="relative py-20 md:py-28 overflow-hidden">
      {/* Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-r from-[#4e4ea8] to-[#0ca7d2] opacity-90 dark:opacity-80"></div>
      
      <div className="container mx-auto px-4 text-center relative z-10">
        <motion.div
            ref={ref}
            initial={{ opacity: 0, y: 50 }}
            animate={inView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8 }}
            className="max-w-4xl mx-auto"
        >
            <Zap className="h-12 w-12 text-[#FF6B35] mx-auto mb-4 animate-pulse" />
            
            <h2 
                className="text-4xl md:text-5xl font-extrabold text-white mb-4 leading-tight"
                style={{ fontFamily: 'Montserrat, sans-serif' }}
            >
                Transforme seu negócio com IA
            </h2>
            
            <p 
                className="text-xl text-gray-200 mb-10 max-w-3xl mx-auto"
                style={{ fontFamily: 'Inter, sans-serif' }}
            >
                Dê o primeiro passo para a automação inteligente e descubra o potencial da Renum Tech Agency.
            </p>

            <div className="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-4">
                <Button 
                    size="lg" 
                    className="text-lg px-8 py-6 bg-[#FF6B35] hover:bg-[#e55f30] text-white shadow-xl transition-transform hover:scale-[1.02]"
                    onClick={openChat}
                >
                    Falar com Renus
                </Button>
                <Button 
                    size="lg" 
                    variant="outline" 
                    className="text-lg px-8 py-6 border-2 border-white text-white bg-transparent hover:bg-white/10 transition-transform hover:scale-[1.02]"
                >
                    <Calendar className="h-5 w-5 mr-2" />
                    Agendar Demonstração
                </Button>
            </div>
        </motion.div>
      </div>
    </section>
  );
};

export default CTASection;