# contacts/telegram_bot1.py
import requests
import json


class TelegramNotifier:
    def __init__(self):
        self.bot_token = "8510941588:AAGlVGwV9B9DzIugOmwMYVi25SGXVmWTOpg"
        self.chat_id = "743780549"  # Пока оставляем старый

    def get_updates(self):
        """Получить последние обновления и найти chat_id"""
        print("🔄 Получаем обновления от Telegram...")
        url = f"https://api.telegram.org/bot{self.bot_token}/getUpdates"

        try:
            response = requests.get(url, timeout=10)
            print(f"📡 Статус: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print("📨 Ответ от Telegram API:")
                print(json.dumps(data, indent=2, ensure_ascii=False))

                if data['ok'] and data['result']:
                    print("\n✅ Найдены сообщения! Доступные chat_id:")
                    for update in data['result']:
                        if 'message' in update:
                            chat = update['message']['chat']
                            print(f"👤 Имя: {chat.get('first_name', 'N/A')} | "
                                  f"Username: @{chat.get('username', 'N/A')} | "
                                  f"Chat ID: {chat['id']} | "
                                  f"Тип: {chat['type']}")
                    return data
                else:
                    print("❌ Нет сообщений. Напишите вашему боту в Telegram!")
                    return None
            else:
                print(f"❌ Ошибка API: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return None

    def send_notification(self, name, phone, service_info=""):
        print("=" * 50)
        print("🔄 НАЧАЛО ОТПРАВКИ TELEGRAM УВЕДОМЛЕНИЯ")
        print("=" * 50)

        message = f"""🎯 Новая заявка с сайта ЦВСИ

👤 Имя: {name}
📞 Телефон: {phone}
{service_info}

⚠️ Не забудьте перезвонить!"""

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

        data = {
            "chat_id": self.chat_id,
            "text": message
        }

        print(f"📝 Сообщение: {message}")
        print(f"🌐 URL: {url}")
        print(f"📦 Данные: {data}")

        try:
            print("🔄 Отправляем запрос к Telegram API...")
            response = requests.post(url, data=data, timeout=10)

            print(f"📡 Статус ответа: {response.status_code}")
            print(f"📨 Текст ответа: {response.text}")

            if response.status_code == 200:
                print("✅ УСПЕХ: Уведомление отправлено в Telegram!")
                return True
            else:
                print(f"❌ ОШИБКА: Telegram API вернул статус {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"❌ Описание ошибки: {error_data}")
                except:
                    pass
                return False

        except Exception as e:
            print(f"❌ НЕИЗВЕСТНАЯ ОШИБКА: {e}")
            return False
        finally:
            print("=" * 50)


# Создаем экземпляр
telegram_notifier = TelegramNotifier()