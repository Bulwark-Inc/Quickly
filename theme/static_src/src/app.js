import { createIcons, icons } from 'lucide';
import Alpine from 'alpinejs'
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
});