import React from 'react';
import RenumLogo from '@/components/RenumLogo';
import { Mail, Phone, Facebook, Twitter, Linkedin } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { useRenusChat } from '@/context/RenusChatContext';

const Footer: React.FC = () => {
  const { openChat } = useRenusChat();

  const navigationLinks = [
    { name: 'Home', href: '#home' },
    { name: 'About', href: '#about' },
    { name: 'Methodology', href: '#methodology' },
    { name: 'Niches', href: '#niches' },
    { name: 'Renus Demo', href: '/renus' },
  ];

  const serviceLinks = [
    { name: 'Sistemas AI Native', href: '#services' },
    { name: 'Workflows em Background', href: '#services' },
    { name: 'Agentes Solo', href: '#services' },
  ];

  const handleScroll = (e: React.MouseEvent, href: string) => {
    if (href.startsWith('#')) {
      e.preventDefault();
      const targetId = href.substring(1);
      const targetElement = document.getElementById(targetId);
      if (targetElement) {
        targetElement.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };

  return (
    <footer className="bg-neutral text-white dark:bg-gray-900 border-t border-gray-700 mt-12">
      <div className="container mx-auto px-4 py-12 md:py-16">
        <div className="grid grid-cols-2 gap-8 md:grid-cols-4 lg:grid-cols-4">
          
          {/* Column 1: Company Info */}
          <div className="col-span-2 md:col-span-1">
            <RenumLogo />
            <p className="mt-4 text-sm text-gray-300">
              Desenvolvemos soluções inteligentes que unem automação, IA e sensibilidade humana.
            </p>
            <div className="flex space-x-4 mt-6">
              <a href="#" aria-label="Facebook" className="text-gray-400 hover:text-[#4e4ea8] transition-colors"><Facebook size={20} /></a>
              <a href="#" aria-label="Twitter" className="text-gray-400 hover:text-[#4e4ea8] transition-colors"><Twitter size={20} /></a>
              <a href="#" aria-label="LinkedIn" className="text-gray-400 hover:text-[#4e4ea8] transition-colors"><Linkedin size={20} /></a>
            </div>
          </div>

          {/* Column 2: Navigation Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-[#0ca7d2]">Navegação</h3>
            <ul className="space-y-2">
              {navigationLinks.map((item) => (
                <li key={item.name}>
                  {item.href.startsWith('/') ? (
                    <Link to={item.href} className="text-sm text-gray-300 hover:text-[#FF6B35] transition-colors">
                      {item.name}
                    </Link>
                  ) : (
                    <a 
                      href={item.href} 
                      onClick={(e) => handleScroll(e, item.href)}
                      className="text-sm text-gray-300 hover:text-[#FF6B35] transition-colors"
                    >
                      {item.name}
                    </a>
                  )}
                </li>
              ))}
            </ul>
          </div>

          {/* Column 3: Services Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-[#0ca7d2]">Serviços</h3>
            <ul className="space-y-2">
              {serviceLinks.map((item) => (
                <li key={item.name}>
                  <a 
                    href={item.href} 
                    onClick={(e) => handleScroll(e, item.href)}
                    className="text-sm text-gray-300 hover:text-[#FF6B35] transition-colors"
                  >
                    {item.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Column 4: Contact Information */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-[#0ca7d2]">Contato</h3>
            <ul className="space-y-2">
              <li className="flex items-center space-x-2">
                <Mail size={16} className="text-[#FF6B35]" />
                <a href="mailto:contato@renum.tech" className="text-sm text-gray-300 hover:text-[#FF6B35] transition-colors">
                  contato@renum.tech
                </a>
              </li>
              <li className="flex items-center space-x-2">
                <Phone size={16} className="text-[#FF6B35]" />
                <span className="text-sm text-gray-300">(XX) XXXX-XXXX</span>
              </li>
            </ul>
            <div className="mt-6 space-y-2">
              <Button 
                onClick={openChat} 
                className="w-full bg-[#4e4ea8] hover:bg-[#3a3a80] text-white"
              >
                Fale com Renus
              </Button>
              <Button variant="secondary" className="w-full bg-gray-700 hover:bg-gray-600 text-white">
                Agendar Call
              </Button>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-12 pt-8 border-t border-gray-700 flex flex-col md:flex-row justify-between items-center text-sm text-gray-400">
          <p>&copy; {new Date().getFullYear()} Renum Tech Agency. Todos os direitos reservados.</p>
          <div className="flex space-x-4 mt-4 md:mt-0">
            <a href="#" className="hover:text-[#FF6B35] transition-colors">Política de Privacidade</a>
            <a href="#" className="hover:text-[#FF6B35] transition-colors">Termos de Serviço</a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;