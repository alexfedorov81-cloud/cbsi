import requests
import json


class TelegramNotifier:
    def __init__(self):
        self.bot_token = "8510941588:AAGlVGwV9B9DzIugOmwMYVi25SGXVmWTOpg"  # Замените на реальный токен
        self.chat_id = "743780549"  # Замените на реальный chat_id

    def send_notification(self, name, phone, service_info=""):
        print("=" * 50)
        print("🔄 НАЧАЛО ОТПРАВКИ TELEGRAM УВЕДОМЛЕНИЯ")
        print("=" * 50)

        # Проверяем токен и chat_id
        print(f"🔧 Токен: {'Установлен' if self.bot_token else 'ОТСУТСТВУЕТ'}")
        print(f"🔧 Chat ID: {'Установлен' if self.chat_id else 'ОТСУТСТВУЕТ'}")

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
                # Парсим JSON ошибки если есть
                try:
                    error_data = response.json()
                    print(f"❌ Описание ошибки: {error_data}")
                except:
                    pass
                return False

        except requests.exceptions.Timeout:
            print("❌ ТАЙМАУТ: Превышено время ожидания ответа от Telegram")
            return False
        except requests.exceptions.ConnectionError:
            print("❌ ОШИБКА ПОДКЛЮЧЕНИЯ: Не удалось соединиться с Telegram")
            return False
        except Exception as e:
            print(f"❌ НЕИЗВЕСТНАЯ ОШИБКА: {e}")
            return False
        finally:
            print("=" * 50)
            print("🔄 ЗАВЕРШЕНИЕ ОТПРАВКИ TELEGRAM УВЕДОМЛЕНИЯ")
            print("=" * 50)


# Создаем экземпляр
telegram_notifier = TelegramNotifier()