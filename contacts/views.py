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
    print("🎯 ===== НАЧАЛО ОБРАБОТКИ ФОРМЫ =====")

    try:
        # Парсим JSON данные
        data = json.loads(request.body)
        print(f"📦 Получены данные: {data}")

        # Создаем форму с данными
        form_data = {
            'name': data.get('name', '').strip(),
            'phone': data.get('phone', '').strip()
        }

        form = CallbackForm(form_data)
        print(f"✅ Форма создана, валидна: {form.is_valid()}")

        if form.is_valid():
            print("🎉 ФОРМА ВАЛИДНА!")

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
                    print(f"📋 Услуга: {service_name}")
                except Service.DoesNotExist:
                    callback = form.save()
                    print("⚠️ Услуга не найдена")
            else:
                callback = form.save()
                print("ℹ️ Услуга не указана")

            # ===== ОТПРАВКА В TELEGRAM =====
            print("🔔 ОТПРАВЛЯЕМ В TELEGRAM...")
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']

            telegram_success = telegram_notifier.send_notification(name, phone)

            if telegram_success:
                print("✅ TELEGRAM ОТПРАВЛЕН УСПЕШНО!")
            else:
                print("❌ ОШИБКА ОТПРАВКИ TELEGRAM")

            # Возвращаем успешный ответ
            return JsonResponse({
                'success': True,
                'message': 'Спасибо! Мы перезвоним вам в ближайшее время.'
            })

        else:
            print("❌ ФОРМА НЕВАЛИДНА")
            print(f"🚨 Ошибки: {form.errors}")
            return JsonResponse({
                'success': False,
                'message': 'Пожалуйста, проверьте правильность введенных данных.'
            })

    except json.JSONDecodeError:
        print("❌ ОШИБКА JSON")
        return JsonResponse({
            'success': False,
            'message': 'Ошибка данных'
        })
    except Exception as e:
        print(f"❌ ОБЩАЯ ОШИБКА: {e}")
        return JsonResponse({
            'success': False,
            'message': 'Произошла ошибка'
        })
    finally:
        print("🎯 ===== КОНЕЦ ОБРАБОТКИ ФОРМЫ =====")