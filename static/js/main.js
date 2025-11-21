// Основные утилиты
const Utils = {
    // Плавная прокрутка к элементу
    scrollToElement: (elementId, behavior = 'smooth') => {
        const element = document.getElementById(elementId);
        if (element) {
            element.scrollIntoView({ behavior });
        }
    },

    // Инициализация анимаций появления
    initScrollAnimations: () => {
        const elements = document.querySelectorAll('.fade-in');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, { threshold: 0.1 });

        elements.forEach(element => observer.observe(element));
    },

    // Добавление плавной прокрутки для якорных ссылок
    initSmoothScroll: () => {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    }
};