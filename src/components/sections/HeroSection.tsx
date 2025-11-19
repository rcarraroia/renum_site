import React from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { useRenusChat } from '@/context/RenusChatContext';
import AnimatedStars from '@/components/AnimatedStars';
import { Zap, Shield, Users, TrendingUp } from 'lucide-react';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.2,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: [0, 0, 0.2, 1] } },
};

const HeroSection: React.FC = () => {
  const { openChat } = useRenusChat();
  const { scrollY } = useScroll();
  
  // Parallax effect for the content
  const yContent = useTransform(scrollY, [0, 500], [0, -100]);

  const handleScrollToMethodology = (e: React.MouseEvent) => {
    e.preventDefault();
    const targetElement = document.getElementById('methodology');
    if (targetElement) {
      targetElement.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const TrustedByIcons = [Shield, Users, TrendingUp, Zap];

  return (
    <section 
      id="home" 
      className="relative min-h-screen flex flex-col justify-center items-center overflow-hidden pt-16 pb-12 md:pt-24"
    >
      {/* Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-[#4e4ea8] to-[#0ca7d2] opacity-90 dark:opacity-70"></div>
      
      {/* Animated Stars */}
      <AnimatedStars />

      {/* Content */}
      <motion.div 
        className="container mx-auto px-4 text-center relative z-10"
        style={{ y: yContent }}
      >
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="max-w-4xl mx-auto"
        >
          <motion.h1 
            className="text-4xl md:text-6xl lg:text-7xl font-extrabold text-white mb-4 leading-tight"
            variants={itemVariants}
            style={{ fontFamily: 'Montserrat, sans-serif' }}
          >
            Inteligência Artificial a serviço do seu negócio
          </motion.h1>
          
          <motion.p 
            className="text-xl md:text-2xl text-gray-200 mb-8 max-w-3xl mx-auto"
            variants={itemVariants}
            style={{ fontFamily: 'Inter, sans-serif' }}
          >
            Desenvolvemos soluções inteligentes que unem automação, IA e sensibilidade humana
          </motion.p>

          <motion.div 
            className="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-4 mb-12"
            variants={itemVariants}
          >
            <Button 
              size="lg" 
              className="text-lg px-8 py-6 bg-[#FF6B35] hover:bg-[#e55f30] text-white shadow-lg transition-transform hover:scale-[1.02]"
              onClick={openChat}
            >
              Converse com Renus
            </Button>
            <Button 
              size="lg" 
              variant="outline" 
              className="text-lg px-8 py-6 border-2 border-white text-white bg-transparent hover:bg-white/10 transition-transform hover:scale-[1.02]"
              onClick={handleScrollToMethodology}
            >
              Nossa Abordagem
            </Button>
          </motion.div>
          
          {/* Visual Element: Abstract AI/Automation */}
          <motion.div 
            className="mt-16 mb-12 flex justify-center"
            variants={itemVariants}
          >
            <Zap className="h-20 w-20 text-[#FF6B35] opacity-80 animate-pulse" />
          </motion.div>

          {/* Trusted By Section */}
          <motion.div 
            className="mt-12 pt-8 border-t border-white/20"
            variants={itemVariants}
          >
            <p className="text-sm uppercase tracking-widest text-gray-300 mb-4">Trusted by industries worldwide</p>
            <div className="flex justify-center space-x-6 opacity-70">
              {TrustedByIcons.map((Icon, index) => (
                <Icon key={index} className="h-8 w-8 text-white hover:text-[#FF6B35] transition-colors" />
              ))}
            </div>
          </motion.div>

        </motion.div>
      </motion.div>
    </section>
  );
};

export default HeroSection;