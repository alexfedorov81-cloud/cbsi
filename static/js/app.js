// Главный файл приложения
document.addEventListener('DOMContentLoaded', () => {
    // Инициализация всех модулей
    Utils.initScrollAnimations();
    Utils.initSmoothScroll();
    Counters.init();
    Forms.init();
    Equipment.init();

    // Глобальные функции для использования в HTML
    window.scrollToSection = Utils.scrollToElement;
    window.focusOnCallbackForm = Forms.focusOnCallbackForm;
});