from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .forms import CallbackForm
from services.models import Service
from .telegram_bot1 import telegram_notifier
import json


@csrf_exempt
@require_POST
def callback_request(request):
    print("🎯 ОБЫЧНАЯ ФОРМА ОТПРАВЛЕНА")
    form = CallbackForm(request.POST)

    if form.is_valid():
        print("✅ ФОРМА ВАЛИДНА")

        # Обрабатываем service_id из скрытого поля
        service_id = request.POST.get('service_id')
        service_name = None

        if service_id:
            try:
                service = Service.objects.get(id=service_id)
                callback = form.save(commit=False)
                callback.service = service
                callback.save()
                service_name = service.name
                print(f"📋 Услуга: {service_name}")
            except Service.DoesNotExist:
                callback = form.save()
                print("⚠️ Услуга не найдена")
        else:
            callback = form.save()
            print("ℹ️ Услуга не указана")

        # Отправляем в Telegram с информацией об услуге
        from .telegram_bot1 import telegram_notifier
        name = form.cleaned_data['name']
        phone = form.cleaned_data['phone']

        service_info = f"📋 Услуга: {service_name}" if service_name else ""
        telegram_notifier.send_notification(name, phone, service_info)

        print("✅ Telegram отправлен!")

        messages.success(request, 'Спасибо! Мы перезвоним вам в ближайшее время.')
        return redirect(reverse('home') + '#contacts')
    else:
        messages.error(request, 'Пожалуйста, проверьте правильность введенных данных.')
        return redirect(reverse('home') + '#contacts')