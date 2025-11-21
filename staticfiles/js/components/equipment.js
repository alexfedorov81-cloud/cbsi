// Функционал для блока оборудования
const Equipment = {
    init: () => {
        Equipment.initAnnotation();
    },

    initAnnotation: () => {
        const equipmentImage = document.querySelector('.equipment-image');
        const annotation = document.querySelector('.equipment-annotation');

        if (equipmentImage && annotation) {
            // Закрытие аннотации при клике вне ее
            document.addEventListener('click', (e) => {
                if (!equipmentImage.contains(e.target) && !annotation.contains(e.target)) {
                    annotation.style.opacity = '0';
                    annotation.style.visibility = 'hidden';
                }
            });

            // Открытие аннотации по клику на мобильных устройствах
            equipmentImage.addEventListener('click', (e) => {
                if (window.innerWidth <= 768) {
                    e.stopPropagation();
                    const isVisible = annotation.style.visibility === 'visible';

                    if (isVisible) {
                        annotation.style.opacity = '0';
                        annotation.style.visibility = 'hidden';
                    } else {
                        annotation.style.opacity = '1';
                        annotation.style.visibility = 'visible';
                    }
                }
            });

            // Предотвращение закрытия при клике на аннотацию
            annotation.addEventListener('click', (e) => {
                e.stopPropagation();
            });
        }
    }
};