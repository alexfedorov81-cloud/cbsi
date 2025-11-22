import urllib.request
import urllib.parse
import json


class TelegramNotifier:
    def __init__(self):
        self.bot_token = "8510941588:AAGlVGwV9B9DzIugOmwMYVi25SGXVmWTOpg"
        self.chat_id = "743780549"

    def send_notification(self, name, phone, service_info=""):
        try:
            message = f"🎯 НОВАЯ ЗАЯВКА\n👤 Имя: {name}\n📞 Телефон: {phone}"

            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": message
            }

            data_encoded = urllib.parse.urlencode(data).encode('utf-8')
            req = urllib.request.Request(url, data=data_encoded, method='POST')

            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    print("✅ Telegram отправлен!")
                    return True
                return False

        except Exception as e:
            print(f"❌ Ошибка Telegram: {e}")
            return False


telegram_notifier = TelegramNotifier()