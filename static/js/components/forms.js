// Работа с формами
const Forms = {
    init: () => {
        Forms.initCallbackForm();
    },

    initCallbackForm: () => {
        const form = document.getElementById('callback-form');
        if (form) {
            console.log('✅ Форма обратного звонка инициализирована');
            form.addEventListener('submit', Forms.handleCallbackSubmit);
        } else {
            console.log('❌ Форма callback-form не найдена');
        }
    },

    handleCallbackSubmit: async (e) => {
        e.preventDefault();
        const form = e.target;
        const submitBtn = form.querySelector('button[type="submit"]') || document.getElementById('submit-btn');
        const originalText = submitBtn.textContent;
        const messagesContainer = document.getElementById('form-messages');

        console.log('🎯 Начата отправка формы обратного звонка');

        // Показываем загрузку
        submitBtn.textContent = 'Отправка...';
        submitBtn.disabled = true;
        if (messagesContainer) {
            messagesContainer.innerHTML = '';
        }

        try {
            const formData = new FormData(form);

            // Преобразуем FormData в обычный объект для JSON
            const data = {
                name: formData.get('name'),
                phone: formData.get('phone'),
                service_id: formData.get('service_id'),
                csrfmiddlewaretoken: formData.get('csrfmiddlewaretoken')
            };

            console.log('📦 Данные формы:', data);

            // Используем JSON вместо FormData
            const response = await fetch('/contacts/callback/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': data.csrfmiddlewaretoken  // ← ДОБАВИЛИ CSRF TOKEN
                },
                body: JSON.stringify(data)
            });

            console.log('📡 Ответ получен, статус:', response.status);

            const responseData = await response.json();

            console.log('📨 Данные ответа:', responseData);

            if (responseData.success) {
                if (messagesContainer) {
                    messagesContainer.innerHTML = `
                        <div class="bg-green-600 text-white p-4 rounded-lg mb-4 border border-green-500">
                            ✅ ${responseData.message}
                        </div>
                    `;
                }
                form.reset();

                console.log('✅ Форма успешно отправлена, Telegram уведомление должно быть отправлено');

                setTimeout(() => {
                    if (messagesContainer) {
                        messagesContainer.innerHTML = '';
                    }
                }, 5000);
            } else {
                if (messagesContainer) {
                    messagesContainer.innerHTML = `
                        <div class="bg-red-600 text-white p-4 rounded-lg mb-4 border border-red-500">
                            ❌ ${responseData.message}
                        </div>
                    `;
                }
            }

        } catch (error) {
            console.error('❌ Ошибка при отправке формы:', error);
            if (messagesContainer) {
                messagesContainer.innerHTML = `
                    <div class="bg-red-600 text-white p-4 rounded-lg mb-4 border border-red-500">
                        ❌ Ошибка сети. Попробуйте еще раз.
                    </div>
                `;
            }
        } finally {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    },

    focusOnCallbackForm: (serviceId = null) => {
        console.log('🎯 Фокусировка на форме, serviceId:', serviceId);

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

        // Используем Utils если он есть, иначе простой скролл
        if (typeof Utils !== 'undefined' && Utils.scrollToElement) {
            Utils.scrollToElement('contacts');
        } else {
            const contactsSection = document.getElementById('contacts');
            if (contactsSection) {
                contactsSection.scrollIntoView({ behavior: 'smooth' });
            }
        }

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

// Инициализация при загрузке документа
document.addEventListener('DOMContentLoaded', function() {
    Forms.init();
    console.log('🚀 Forms module initialized');
});