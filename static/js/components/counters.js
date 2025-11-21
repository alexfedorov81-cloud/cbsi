// Анимация счетчиков
const Counters = {
    init: () => {
        // Ищем герой-секцию по разным возможным классам
        const heroSection = document.querySelector('.hero-overlay') ||
                           document.querySelector('.hero-gradient') ||
                           document.querySelector('.hero-section');

        if (heroSection) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        Counters.animateAll();
                        // Останавливаем наблюдение после первого срабатывания
                        observer.unobserve(entry.target);
                    }
                });
            }, {
                threshold: 0.3,  // Срабатывает когда 30% секции видно
                rootMargin: '-50px' // Небольшой отступ от верха
            });

            observer.observe(heroSection);
        } else {
            // Если не нашли секцию, запускаем сразу
            setTimeout(() => Counters.animateAll(), 1000);
        }
    },

    animateCounter: (elementId, finalValue, duration = 2000) => {
        const element = document.getElementById(elementId);
        if (!element) return;

        let start = 0;
        const increment = finalValue / (duration / 16);

        function updateCounter() {
            start += increment;
            if (start < finalValue) {
                element.textContent = Math.floor(start);
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = finalValue;
            }
        }
        updateCounter();
    },

    animateAll: () => {
        console.log('Запуск анимации счетчиков...');

        const counter1 = document.getElementById('counter1');
        const counter2 = document.getElementById('counter2');
        const counter3 = document.getElementById('counter3');

        if (counter1 && counter2 && counter3) {
            try {
                const testsCompleted = parseInt(counter1.getAttribute('data-value')) || 1250;
                const corporateClients = parseInt(counter2.getAttribute('data-value')) || 89;
                const yearsExperience = parseInt(counter3.getAttribute('data-value')) || 12;

                console.log('Значения счетчиков:', testsCompleted, corporateClients, yearsExperience);

                Counters.animateCounter('counter1', testsCompleted);
                Counters.animateCounter('counter2', corporateClients);
                Counters.animateCounter('counter3', yearsExperience);
            } catch (error) {
                console.error('Ошибка анимации счетчиков:', error);
                // Запасные значения
                Counters.animateCounter('counter1', 1250);
                Counters.animateCounter('counter2', 89);
                Counters.animateCounter('counter3', 12);
            }
        } else {
            console.error('Не найдены элементы счетчиков');
        }
    }
};