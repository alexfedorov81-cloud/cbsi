import requests


class TelegramNotifier:
    def __init__(self):
        self.bot_token = "ВАШ_ТОКЕН_ОТ_BOTFATHER"
        self.chat_id = "ВАШ_CHAT_ID"

    def send_notification(self, name, phone, service_info=""):
        message = f"""🎯 *Новая заявка с сайта ЦВСИ*

👤 *Имя:* {name}
📞 *Телефон:* `{phone}`
{service_info}

⚠️ *Не забудьте перезвонить!*"""

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

        data = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }

        try:
            response = requests.post(url, data=data)
            return response.status_code == 200
        except Exception as e:
            print(f"Telegram error: {e}")
            return False


# Создаем экземпляр
telegram_notifier = TelegramNotifier()