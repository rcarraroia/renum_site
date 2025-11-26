import React from 'react';
import { motion } from 'framer-motion';
import { Zap } from 'lucide-react';

const Star: React.FC<{ delay: number, size: number, color: string, x: string, y: string }> = ({ delay, size, color, x, y }) => (
  <motion.div
    className="absolute"
    style={{ top: y, left: x }}
    initial={{ opacity: 0, scale: 0.5 }}
    animate={{
      opacity: [0, 1, 0.5, 1, 0],
      scale: [0.5, 1, 0.8, 1.2, 0.5],
    }}
    transition={{
      duration: 8,
      repeat: Infinity,
      delay: delay,
      ease: "easeInOut",
    }}
  >
    <Zap className={color} style={{ width: size, height: size }} fill="currentColor" />
  </motion.div>
);

const AnimatedStars: React.FC = () => {
  const stars = Array.from({ length: 30 }).map((_, i) => ({
    id: i,
    delay: Math.random() * 8,
    size: Math.random() * 10 + 8, // 8px to 18px
    color: i % 3 === 0 ? 'text-[#0ca7d2]' : i % 2 === 0 ? 'text-[#4e4ea8]' : 'text-white',
    x: `${Math.random() * 100}%`,
    y: `${Math.random() * 100}%`,
  }));

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {stars.map(star => (
        <Star 
          key={star.id} 
          delay={star.delay} 
          size={star.size} 
          color={star.color} 
          x={star.x} 
          y={star.y} 
        />
      ))}
    </div>
  );
};

export default AnimatedStars;