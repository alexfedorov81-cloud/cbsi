// Forms2: Simple scroll functions
function scrollToSection(sectionId) {
    console.log('🎯 Scrolling to:', sectionId);
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

function focusOnCallbackForm(serviceId = null) {
    console.log('🎯 Focusing on form, serviceId:', serviceId);
    
    // Scroll to contacts form
    const contactsSection = document.getElementById('contacts');
    if (contactsSection) {
        contactsSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    // Add service_id if needed
    if (serviceId) {
        setTimeout(() => {
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
        }, 500);
    }
}

console.log('✅ Forms2: Scroll functions loaded');