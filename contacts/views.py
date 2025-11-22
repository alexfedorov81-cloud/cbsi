from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.urls import reverse
from .forms import CallbackForm
import traceback


@require_POST
def callback_request(request):
    print("🎯 ОБЫЧНАЯ ФОРМА ОТПРАВЛЕНА")

    try:
        form = CallbackForm(request.POST)
        print(f"✅ Форма создана, данные: {request.POST}")

        if form.is_valid():
            print("✅ ФОРМА ВАЛИДНА")
            print(f"📝 Очищенные данные: {form.cleaned_data}")

            # Обрабатываем service_id
            service_id = request.POST.get('service_id')
            print(f"🔍 Service ID из формы: {service_id}")

            service_name = None

            if service_id:
                try:
                    from services.models import Service
                    service = Service.objects.get(id=service_id)
                    print(f"📋 Услуга найдена: {service.title}")
                    callback = form.save(commit=False)
                    callback.service = service
                    callback.save()
                    service_name = service.title
                except Exception as e:
                    print(f"⚠️ Ошибка при обработке услуги: {e}")
                    callback = form.save()
            else:
                callback = form.save()
                print("ℹ️ Услуга не указана")

            # Отправляем в Telegram
            try:
                from .telegram_bot1 import telegram_notifier
                name = form.cleaned_data['name']
                phone = form.cleaned_data['phone']
                service_info = f"📋 Услуга: {service_name}" if service_name else ""

                print(f"📤 Отправляем в Telegram: {name}, {phone}, {service_info}")
                telegram_notifier.send_notification(name, phone, service_info)
                print("✅ Telegram отправлен!")

            except Exception as e:
                print(f"⚠️ Ошибка Telegram: {e}")
                print(traceback.format_exc())

            messages.success(request, 'Спасибо! Мы перезвоним вам в ближайшее время.')
            return redirect(reverse('home') + '#contacts')
        else:
            print(f"❌ ФОРМА НЕВАЛИДНА: {form.errors}")
            messages.error(request, 'Пожалуйста, проверьте правильность введенных данных.')
            return redirect(reverse('home') + '#contacts')

    except Exception as e:
        print(f"🚨 КРИТИЧЕСКАЯ ОШИБКА: {e}")
        print(traceback.format_exc())
        messages.error(request, 'Произошла ошибка. Пожалуйста, попробуйте позже.')
        return redirect(reverse('home') + '#contacts')