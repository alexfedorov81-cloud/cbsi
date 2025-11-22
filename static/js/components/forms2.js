// Forms2: Simple scroll functions with field highlight
function scrollToSection(sectionId) {
    console.log('🎯 Scrolling to:', sectionId);
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

function focusOnCallbackForm(serviceId = null) {
    console.log('🎯 Focusing on form, serviceId:', serviceId);

    // СНАЧАЛА добавляем service_id в форму (БЕЗ задержки)
    if (serviceId) {
        let serviceField = document.getElementById('service-field');
        if (!serviceField) {
            serviceField = document.createElement('input');
            serviceField.type = 'hidden';
            serviceField.name = 'service_id';
            serviceField.id = 'service-field';
            const form = document.getElementById('callback-form');
            if (form) form.appendChild(serviceField);
        }
        serviceField.value = serviceId;
        console.log('✅ Service ID added:', serviceId);
    }

    // ПОТОМ скроллим к форме
    const contactsSection = document.getElementById('contacts');
    if (contactsSection) {
        contactsSection.scrollIntoView({ behavior: 'smooth' });
    }

    // Highlight and focus name field
    setTimeout(() => {
        const nameField = document.getElementById('name-field');
        if (nameField) {
            // Добавляем классы для подсветки
            nameField.classList.add('field-highlight', 'field-pulse');
            nameField.focus();
            nameField.setSelectionRange(0, 0);

            // Убираем подсветку при вводе или через время
            const removeHighlight = () => {
                nameField.classList.remove('field-highlight', 'field-pulse');
                nameField.removeEventListener('input', removeHighlight);
            };

            nameField.addEventListener('input', removeHighlight);
            setTimeout(removeHighlight, 3000);
        }
    }, 800);
}

console.log('✅ Forms2: Scroll functions with field highlight loaded');