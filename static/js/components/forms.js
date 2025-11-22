function focusOnCallbackForm(serviceId = null) {
    console.log('🎯 Focusing on form, serviceId:', serviceId);

    if (serviceId) {
        let serviceField = document.getElementById('service-field');
        if (!serviceField) {
            serviceField = document.createElement('input');
            serviceField.type = 'hidden';
            serviceField.name = 'service_id';
            serviceField.id = 'service-field';
            const form = document.getElementById('callback-form');
            if (form) {
                form.appendChild(serviceField);
            }
        }
        serviceField.value = serviceId;
    }

    // Simple scroll to contacts
    const contactsSection = document.getElementById('contacts');
    if (contactsSection) {
        contactsSection.scrollIntoView({ behavior: 'smooth' });
    }

    // Focus on name field after scroll
    setTimeout(() => {
        const nameField = document.getElementById('name-field');
        if (nameField) {
            nameField.focus();
        }
    }, 500);
}

console.log('✅ Forms: Standard HTML form submission enabled');