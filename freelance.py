import requests
import feedparser
import os
import re
from datetime import datetime

# ============================================
# Telegram (из секретов GitHub)
# ============================================
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# ============================================
# РАСШИРЕННЫЕ НАВЫКИ (почти всё)
# ============================================
MY_SKILLS = [
    "python", "javascript", "html", "css", "php", "java",
    "дизайн", "логотип", "фигма", "photoshop", "illustrator",
    "копирайтинг", "текст", "статья", "перевод", "пост",
    "парсинг", "бот", "telegram", "api", "сайт", "лендинг",
    "видеомонтаж", "smm", "instagram", "рилс", "wordpress",
    "нужен", "помощь", "сделать", "разработка", "создать"
]

# ============================================
# ОТПРАВКА В TELEGRAM
# ============================================
def send_tg(text):
    if not TOKEN or not CHAT_ID:
        print("❌ Нет токенов")
        return
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": text[:4000], "disable_web_page_preview": True}, timeout=30)
        print("✅ Отправлено")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

# ============================================
# ПАРСЕРЫ
# ============================================

def parse_kwork():
    orders = []
    try:
        print("🔍 Kwork...")
        feed = feedparser.parse("https://kwork.ru/projects/rss")
        for entry in feed.entries[:20]:
            title = entry.title
            if any(s.lower() in title.lower() for s in MY_SKILLS):
                price = "💰 Цена не указана"
                if "₽" in title:
                    match = re.search(r'(\d+)\s*₽', title)
                    if match:
                        price = f"💰 {match.group(1)} ₽"
                orders.append({
                    "title": title[:80],
                    "link": entry.link,
                    "price": price,
                    "platform": "🔥 Kwork"
                })
        print(f"   ✅ {len(orders)} заказов")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    return orders

def parse_freelancehunt():
    orders = []
    try:
        print("🔍 Freelancehunt...")
        feed = feedparser.parse("https://freelancehunt.com/rss/ru/projects.xml")
        for entry in feed.entries[:20]:
            title = entry.title
            if any(s.lower() in title.lower() for s in MY_SKILLS):
                price = "💰 Цена не указана"
                if "$" in title:
                    match = re.search(r'(\d+)\s*\$\s*', title)
                    if match:
                        price = f"💰 {match.group(1)}$"
                orders.append({
                    "title": title[:80],
                    "link": entry.link,
                    "price": price,
                    "platform": "⚡ Freelancehunt"
                })
        print(f"   ✅ {len(orders)} заказов")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    return orders

def parse_habr():
    orders = []
    try:
        print("🔍 Habr Freelance...")
        orders.append({
            "title": "Свежие заказы на Habr",
            "link": "https://freelance.habr.com/tasks",
            "price": "💰 Смотрите на сайте",
            "platform": "📘 Habr Freelance"
        })
        print(f"   ✅ Добавлена ссылка на Habr")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    return orders

def parse_weblancer():
    orders = []
    try:
        print("🔍 Weblancer...")
        orders.append({
            "title": "Свежие заказы на Weblancer",
            "link": "https://www.weblancer.net/projects/",
            "price": "💰 Смотрите на сайте",
            "platform": "🌐 Weblancer"
        })
        print(f"   ✅ Добавлена ссылка на Weblancer")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    return orders

def parse_fl():
    orders = []
    try:
        print("🔍 Fl.ru...")
        orders.append({
            "title": "Свежие заказы на Fl.ru",
            "link": "https://fl.ru/projects",
            "price": "💰 Смотрите на сайте",
            "platform": "📌 Fl.ru"
        })
        print(f"   ✅ Добавлена ссылка на Fl.ru")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    return orders

# ============================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================

def main():
    print("=" * 50)
    print(f"🤖 ЗАПУСК ПАРСЕРА")
    print(f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print("=" * 50)
    
    # Собираем все заказы
    all_orders = []
    all_orders.extend(parse_kwork())
    all_orders.extend(parse_freelancehunt())
    all_orders.extend(parse_habr())
    all_orders.extend(parse_weblancer())
    all_orders.extend(parse_fl())
    
    # Удаляем дубликаты по ссылке
    seen = set()
    unique_orders = []
    for order in all_orders:
        if order['link'] not in seen:
            seen.add(order['link'])
            unique_orders.append(order)
    
    all_orders = unique_orders
    
    # Формируем отчёт
    if all_orders:
        grouped = {}
        for order in all_orders:
            plat = order['platform']
            if plat not in grouped:
                grouped[plat] = []
            grouped[plat].append(order)
        
        msg = f"<b>🔍 НАЙДЕНО ЗАКАЗОВ: {len(all_orders)}</b>\n"
        msg += f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
        msg += "─" * 30 + "\n\n"
        
        for platform, orders in grouped.items():
            msg += f"<b>{platform}</b> ({len(orders)})\n"
            for order in orders[:7]:
                msg += f"📌 <b>{order['title']}</b>\n"
                msg += f"{order['price']}\n"
                msg += f"🔗 <a href='{order['link']}'>Смотреть заказ</a>\n\n"
        
        send_tg(msg)
    else:
        msg = f"😴 <b>Заказов не найдено</b>\n\n📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n💡 Проверьте навыки в файле freelance.py"
        send_tg(msg)
    
    print("=" * 50)
    print("✅ ГОТОВО")
    print("=" * 50)

if __name__ == "__main__":
    main()