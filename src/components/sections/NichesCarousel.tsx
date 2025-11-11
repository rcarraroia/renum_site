import React, { useRef } from 'react';
import { motion } from 'framer-motion';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Autoplay, Navigation, Pagination, A11y } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowLeft, ArrowRight, Zap } from 'lucide-react';
import { cn } from '@/lib/utils';
import { NICHE_DATA, Niche } from '@/data/nicheData';
import { Button } from '@/components/ui/button';

// Componente de Card de Nicho
const NicheCard: React.FC<{ niche: Niche }> = ({ niche }) => {
    const { icon: Icon, title, description, color } = niche;

    return (
        <Card className="h-full flex flex-col transition-all duration-300 hover:shadow-xl hover:scale-[1.02] dark:border-gray-700 cursor-grab">
            <CardHeader className="flex flex-col items-start space-y-2 p-4 pb-2">
                <Icon className={cn("h-8 w-8 mb-1", color)} />
                <CardTitle className="text-lg font-bold" style={{ fontFamily: 'Montserrat, sans-serif' }}>{title}</CardTitle>
            </CardHeader>
            <CardContent className="flex-grow p-4 pt-0">
                <p className="text-sm text-muted-foreground line-clamp-2">{description}</p>
            </CardContent>
        </Card>
    );
};

const NichesCarousel: React.FC = () => {
    const swiperRef = useRef<any>(null);

    return (
        <div className="relative group">
            {/* Swiper Carousel */}
            <Swiper
                modules={[Autoplay, Navigation, A11y]}
                spaceBetween={24}
                slidesPerView={1.2}
                loop={true}
                autoplay={{
                    delay: 3000,
                    disableOnInteraction: false,
                    pauseOnMouseEnter: true,
                }}
                onSwiper={(swiper) => {
                    swiperRef.current = swiper;
                }}
                breakpoints={{
                    640: {
                        slidesPerView: 2.2,
                        spaceBetween: 20,
                    },
                    1024: {
                        slidesPerView: 4.2,
                        spaceBetween: 30,
                    },
                    1280: {
                        slidesPerView: 5,
                        spaceBetween: 30,
                    }
                }}
                className="w-full py-4"
            >
                {NICHE_DATA.map((niche) => (
                    <SwiperSlide key={niche.id} className="h-auto">
                        <NicheCard niche={niche} />
                    </SwiperSlide>
                ))}
            </Swiper>

            {/* Navigation Arrows (Desktop Only) */}
            <div className="hidden lg:block">
                <Button
                    variant="outline"
                    size="icon"
                    className="absolute top-1/2 left-0 transform -translate-x-1/2 -translate-y-1/2 z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-background/80 hover:bg-background"
                    onClick={() => swiperRef.current?.slidePrev()}
                    aria-label="Previous niche"
                >
                    <ArrowLeft className="h-5 w-5" />
                </Button>
                <Button
                    variant="outline"
                    size="icon"
                    className="absolute top-1/2 right-0 transform translate-x-1/2 -translate-y-1/2 z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-background/80 hover:bg-background"
                    onClick={() => swiperRef.current?.slideNext()}
                    aria-label="Next niche"
                >
                    <ArrowRight className="h-5 w-5" />
                </Button>
            </div>
            
            {/* Mobile Swipe Indicator */}
            <div className="lg:hidden text-center mt-4 text-sm text-muted-foreground flex items-center justify-center">
                <ArrowLeft className="h-4 w-4 mr-2" />
                Deslize para ver mais
                <ArrowRight className="h-4 w-4 ml-2" />
            </div>
        </div>
    );
};

export default NichesCarousel;