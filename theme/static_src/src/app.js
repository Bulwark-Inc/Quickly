import { createIcons, icons } from 'lucide';
import Alpine from 'alpinejs'
import 'aos/dist/aos.css';
import AOS from 'aos';

window.Alpine = Alpine

Alpine.start()

document.addEventListener('DOMContentLoaded', () => {
    AOS.init({
        duration: 1000,
        once: true
    });
    createIcons({ icons });
});