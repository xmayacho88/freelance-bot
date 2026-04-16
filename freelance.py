import os
import requests

print("Файл найден и запущен!")

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

if TOKEN and CHAT_ID:
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": CHAT_ID, "text": "✅ GitHub работает!"})
        print(f"Отправлено! Статус: {r.status_code}")
    except Exception as e:
        print(f"Ошибка: {e}")
else:
    print("Токены не найдены")