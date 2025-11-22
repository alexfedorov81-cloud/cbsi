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
    form = CallbackForm(request.POST)

    if form.is_valid():
        # Обрабатываем service_id если он передан
        service_id = request.POST.get('service_id')
        service_name = None

        if service_id:
            try:
                service = Service.objects.get(id=service_id)
                callback = form.save(commit=False)
                callback.service = service
                callback.save()
                service_name = service.name  # ← Сохраняем название услуги
            except Service.DoesNotExist:
                callback = form.save()
        else:
            callback = form.save()

        # === ДОБАВЛЯЕМ ОТПРАВКУ В TELEGRAM ===
        try:
            name = form.cleaned_data.get('name', '')
            phone = form.cleaned_data.get('phone', '')

            # Формируем сообщение с информацией об услуге
            message_service = f" по услуге: {service_name}" if service_name else ""

            # Отправляем уведомление
            telegram_notifier.send_notification(name, phone, message_service)

        except Exception as e:
            # Логируем ошибку, но не прерываем выполнение
            print(f"Ошибка отправки в Telegram: {e}")
        # =====================================

        # Для AJAX запросов
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Спасибо! Мы перезвоним вам в ближайшее время.'
            })
        else:
            messages.success(request, 'Спасибо! Мы перезвоним вам в ближайшее время.')
            return redirect(reverse('home') + '#contacts')
    else:
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