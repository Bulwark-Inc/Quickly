import Alpine from 'alpinejs'
import { createIcons, icons } from 'lucide';
import Splide from '@splidejs/splide';
// Optional: import default CSS
import '@splidejs/splide/dist/css/splide.min.css';
import AOS from 'aos';
import 'aos/dist/aos.css';

window.Alpine = Alpine

Alpine.start()

document.addEventListener('DOMContentLoaded', () => {
    AOS.init({
        duration: 1000,
        once: true
    });

    createIcons({ icons });
    
    new Splide('#testimonial-carousel', {
        type: 'loop',
        perPage: 1,
        autoplay: true,
        interval: 5000,
        arrows: true,
        pagination: true,
        pauseOnHover: true,
        breakpoints: {
        768: {
            perPage: 1,
        },
        },
    }).mount();
});