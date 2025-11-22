from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.urls import reverse
from .forms import CallbackForm
from services.models import Service  # Добавляем импорт

# Импортируем наш Telegram бот
from .telegram_bot1 import telegram_notifier  # ← ДОБАВИТЬ ЭТУ СТРОЧКУ


@require_POST
def callback_request(request):
    print("🎯 ===== НАЧАЛО ОБРАБОТКИ ФОРМЫ ОБРАТНОГО ЗВОНКА =====")
    print(f"📋 Метод: {request.method}")
    print(f"📦 Данные POST: {request.POST}")
    print(f"🎯 AJAX запрос: {request.headers.get('X-Requested-With') == 'XMLHttpRequest'}")

    # Для JSON данных
    if request.content_type == 'application/json':
        try:
            import json
            data = json.loads(request.body)
            print(f"📨 JSON данные: {data}")
        except Exception as e:
            print(f"❌ Ошибка парсинга JSON: {e}")
            data = {}
    else:
        data = request.POST.dict()
        print(f"📨 Form данные: {data}")

    form = CallbackForm(data)
    print(f"✅ Форма создана: {form}")

    if form.is_valid():
        print("🎉 ФОРМА ВАЛИДНА!")
        print(f"📝 Очищенные данные: {form.cleaned_data}")

        # Обрабатываем service_id если он передан
        service_id = data.get('service_id')
        service_name = None

        if service_id:
            try:
                service = Service.objects.get(id=service_id)
                callback = form.save(commit=False)
                callback.service = service
                callback.save()
                service_name = service.name
                print(f"📋 Услуга найдена: {service_name}")
            except Service.DoesNotExist:
                callback = form.save()
                print("⚠️ Услуга не найдена")
        else:
            callback = form.save()
            print("ℹ️ Услуга не указана")

        # ===== TELEGRAM УВЕДОМЛЕНИЕ =====
        print("🔔 НАЧИНАЕМ ОТПРАВКУ В TELEGRAM")
        try:
            name = form.cleaned_data.get('name', '')
            phone = form.cleaned_data.get('phone', '')

            print(f"📞 Данные для Telegram - Имя: '{name}', Телефон: '{phone}'")

            service_info = f"📋 Услуга: {service_name}" if service_name else ""

            # Импортируем и отправляем
            from contacts.telegram_bot1 import telegram_notifier
            print("✅ Telegram notifier импортирован")

            success = telegram_notifier.send_notification(name, phone, service_info)

            if success:
                print("🎉 TELEGRAM УВЕДОМЛЕНИЕ УСПЕШНО ОТПРАВЛЕНО!")
            else:
                print("❌ ОШИБКА ОТПРАВКИ TELEGRAM УВЕДОМЛЕНИЯ")

        except ImportError as e:
            print(f"🚨 ОШИБКА ИМПОРТА Telegram: {e}")
        except Exception as e:
            print(f"🚨 ОБЩАЯ ОШИБКА Telegram: {e}")
            import traceback
            traceback.print_exc()

        # Обработка ответа
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            print("📡 Возвращаем JSON ответ для AJAX")
            return JsonResponse({
                'success': True,
                'message': 'Спасибо! Мы перезвоним вам в ближайшее время.'
            })
        else:
            print("📡 Возвращаем редирект для обычного запроса")
            messages.success(request, 'Спасибо! Мы перезвоним вам в ближайшее время.')
            return redirect(reverse('home') + '#contacts')

    else:
        print("❌ ФОРМА НЕВАЛИДНА")
        print(f"🚨 Ошибки формы: {form.errors}")
        error_message = 'Пожалуйста, проверьте правильность введенных данных.'
        for field, errors in form.errors.items():
            for error in errors:
                error_message = error
                break
            break

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': error_message
            })
        else:
            messages.error(request, error_message)
            return redirect(reverse('home') + '#contacts')

    print("🎯 ===== ЗАВЕРШЕНИЕ ОБРАБОТКИ ФОРМЫ =====")