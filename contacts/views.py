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

        # Сохраняем заявку
        callback = form.save()

        # Отправляем в Telegram
        from .telegram_bot1 import telegram_notifier
        name = form.cleaned_data['name']
        phone = form.cleaned_data['phone']
        telegram_notifier.send_notification(name, phone)

        print("✅ Telegram отправлен!")

        messages.success(request, 'Спасибо! Мы перезвоним вам в ближайшее время.')
        return redirect(reverse('home') + '#contacts')
    else:
        messages.error(request, 'Пожалуйста, проверьте правильность введенных данных.')
        return redirect(reverse('home') + '#contacts')