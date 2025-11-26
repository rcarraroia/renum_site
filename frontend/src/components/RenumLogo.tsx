import React from 'react';
import { Link } from 'react-router-dom';

const RenumLogo: React.FC = () => {
  return (
    <Link to="/" className="flex items-center space-x-2 text-lg font-bold tracking-tight">
      <img 
        src="/logo-renum.png" 
        alt="Renum Tech Agency Logo" 
        className="h-6 md:h-8 w-auto dark:invert"
      />
    </Link>
  );
};

export default RenumLogo;