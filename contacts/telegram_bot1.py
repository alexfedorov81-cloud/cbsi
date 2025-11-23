import urllib.request
import urllib.parse
import json


class TelegramNotifier:
    def __init__(self):
        self.bot_token = "8510941588:AAGlVGwV9B9DzIugOmwMYVi25SGXVmWTOpg"
        # ОБА получателя - вы и новый человек
        self.chat_ids = ["743780549", "772715507"]

    def send_notification(self, name, phone, service_info=""):
        try:
            message = f"🎯 НОВАЯ ЗАЯВКА\n👤 Имя: {name}\n📞 Телефон: {phone}"
            if service_info:
                message += f"\n{service_info}"

            print(f"📨 Telegram сообщение: {message}")

            success_count = 0

            # Отправляем каждому получателю
            for chat_id in self.chat_ids:
                url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
                data = {
                    "chat_id": chat_id,
                    "text": message
                }

                data_encoded = urllib.parse.urlencode(data).encode('utf-8')
                req = urllib.request.Request(url, data=data_encoded, method='POST')

                with urllib.request.urlopen(req, timeout=10) as response:
                    if response.status == 200:
                        print(f"✅ Telegram отправлен для chat_id: {chat_id}")
                        success_count += 1

            return success_count > 0

        except Exception as e:
            print(f"❌ Ошибка Telegram: {e}")
            return False


telegram_notifier = TelegramNotifier()