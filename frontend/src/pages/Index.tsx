import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import RenusChatWidget from "@/components/RenusChatWidget";
import { MadeWithDyad } from "@/components/made-with-dyad";
import HeroSection from "@/components/sections/HeroSection";
import RenusShowcaseSection from "@/components/sections/RenusShowcaseSection";
import ServicesSection from "@/components/sections/ServicesSection";
import MethodologySection from "@/components/sections/MethodologySection";
import AboutSection from "@/components/sections/AboutSection";
import NichesSection from "@/components/sections/NichesSection";
import CTASection from "@/components/sections/CTASection";


const Index = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      <main className="flex-grow">
        <HeroSection />
        <RenusShowcaseSection />
        <ServicesSection />
        <MethodologySection />
        <AboutSection />
        <NichesSection />
        <CTASection />
      </main>
      
      <Footer />
      <RenusChatWidget />
      <MadeWithDyad />
    </div>
  );
};

export default Index;