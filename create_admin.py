import os
import django

# Настройка Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbsi_site.settings')
django.setup()

from django.contrib.auth import get_user_model


def create_superuser():
    User = get_user_model()

    # Данные суперпользователя (можно изменить)
    username = 'admin'
    email = 'admin@cbsi.ru'
    password = 'admin123'  # Смени после первого входа!

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"✅ Суперпользователь создан!")
        print(f"👤 Логин: {username}")
        print(f"🔑 Пароль: {password}")
        print("⚠️  Не забудь сменить пароль после первого входа!")
    else:
        print("ℹ️  Суперпользователь уже существует")


if __name__ == '__main__':
    create_superuser()