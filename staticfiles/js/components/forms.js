// Работа с формами
const Forms = {
    init: () => {
        Forms.initCallbackForm();
    },

    initCallbackForm: () => {
        const form = document.getElementById('callback-form');
        if (form) {
            form.addEventListener('submit', Forms.handleCallbackSubmit);
        }
    },

    handleCallbackSubmit: async (e) => {
        e.preventDefault();
        const form = e.target;
        const submitBtn = document.getElementById('submit-btn');
        const originalText = submitBtn.textContent;
        const messagesContainer = document.getElementById('form-messages');

        // Показываем загрузку
        submitBtn.textContent = 'Отправка...';
        submitBtn.disabled = true;
        messagesContainer.innerHTML = '';

        try {
            const formData = new FormData(form);
            const response = await fetch(form.action || '{% url "callback" %}', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            });

            const data = await response.json();

            if (data.success) {
                messagesContainer.innerHTML = `
                    <div class="bg-green-600 text-white p-4 rounded-lg mb-4 border border-green-500">
                        ✅ ${data.message}
                    </div>
                `;
                form.reset();
                setTimeout(() => messagesContainer.innerHTML = '', 5000);
            } else {
                messagesContainer.innerHTML = `
                    <div class="bg-red-600 text-white p-4 rounded-lg mb-4 border border-red-500">
                        ❌ ${data.message}
                    </div>
                `;
            }

        } catch (error) {
            console.error('Error:', error);
            messagesContainer.innerHTML = `
                <div class="bg-red-600 text-white p-4 rounded-lg mb-4 border border-red-500">
                    ❌ Ошибка сети. Попробуйте еще раз.
                </div>
            `;
        } finally {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    },

    focusOnCallbackForm: (serviceId = null) => {
        if (serviceId) {
            let serviceField = document.getElementById('service-field');
            if (!serviceField) {
                serviceField = document.createElement('input');
                serviceField.type = 'hidden';
                serviceField.name = 'service_id';
                serviceField.id = 'service-field';
                document.getElementById('callback-form').appendChild(serviceField);
            }
            serviceField.value = serviceId;
        }

        Utils.scrollToElement('contacts');

        setTimeout(() => {
            const nameField = document.getElementById('name-field');
            if (nameField) {
                nameField.classList.add('field-highlight', 'field-pulse');
                nameField.focus();
                nameField.setSelectionRange(0, 0);

                const removeHighlight = () => {
                    nameField.classList.remove('field-highlight', 'field-pulse');
                    nameField.removeEventListener('input', removeHighlight);
                };

                nameField.addEventListener('input', removeHighlight);
                setTimeout(removeHighlight, 3000);
            }
        }, 800);
    }
};