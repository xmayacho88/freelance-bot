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
# ВАШИ НАВЫКИ (расширенные под всё, что вы делаете)
# ============================================
MY_SKILLS = [
    # Дизайн
    "дизайн", "логотип", "фигма", "photoshop", "illustrator", "coreldraw",
    "баннер", "визитка", "упаковка", "брендинг", "айдентика",
    "презентация", "инфографика", "полиграфия", "веб-дизайн",
    "интерфейс", "ui", "ux", "адаптив", "мобильный дизайн",
    
    # Кодинг / Разработка
    "python", "javascript", "html", "css", "php", "java", "c#", "c++",
    "react", "vue", "angular", "node.js", "django", "flask", "fastapi",
    "wordpress", "tilda", "сайт", "лендинг", "верстка", "интернет-магазин",
    "телеграм бот", "бот", "api", "парсинг", "скрапинг", "автоматизация",
    "backend", "frontend", "fullstack", "база данных", "sql",
    
    # Анализ / Маркетинг
    "анализ", "аналитика", "исследование", "маркетинг", "seo", "smm",
    "реклама", "таргет", "яндекс директ", "google ads", "контекст",
    "юзабилити", "аудит", "метрика", "аналитика данных",
    
    # Маркетплейсы (WB, Ozon)
    "wb", "wildberries", "озон", "ozon", "маркетплейс", "карточка товара",
    "инфографика wb", "сео wb", "продвижение wb", "ozon карточка",
    
    # Общее
    "нужен", "помощь", "сделать", "разработка", "создать", "написать",
    "сверстать", "нарисовать", "отрисовать", "спроектировать"
]

# ============================================
# ФИЛЬТР ПО ЦЕНЕ (от 2000 рублей)
# ============================================
MIN_PRICE = 2000

def check_price(text):
    """Проверяет, что цена >= 2000 рублей"""
    # Ищем цифры
    numbers = re.findall(r'(\d+)\s*(?:₽|руб|рублей|р\.|р)', text, re.IGNORECASE)
    for num_str in numbers:
        try:
            price = int(num_str)
            if price >= MIN_PRICE:
                return True, price
        except:
            pass
    
    # Ищем доллары (примерно 2000 руб = 20-25$)
    dollars = re.findall(r'(\d+)\s*\$\s*', text, re.IGNORECASE)
    for num_str in dollars:
        try:
            price_usd = int(num_str)
            if price_usd >= 20:  # ~2000 рублей
                return True, price_usd
        except:
            pass
    
    # Если цена не указана — показываем
    if "цена" not in text.lower() and "₽" not in text and "$" not in text:
        return True, None
    
    return False, None

# ============================================
# ОТПРАВКА В TELEGRAM
# ============================================
def send_tg(text):
    if not TOKEN or not CHAT_ID:
        print("❌ Нет токенов")
        return
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": text[:4096], "parse_mode": "HTML", "disable_web_page_preview": False}, timeout=30)
        print("✅ Отправлено в Telegram")
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")

# ============================================
# ПАРСЕРЫ (с прямой ссылкой на заказ)
# ============================================

def parse_kwork():
    orders = []
    try:
        print("🔍 Kwork...")
        feed = feedparser.parse("https://kwork.ru/projects/rss")
        for entry in feed.entries[:50]:
            title = entry.title
            description = entry.description if hasattr(entry, 'description') else ""
            full_text = title + " " + description
            
            # Проверка навыков
            if not any(s.lower() in full_text.lower() for s in MY_SKILLS):
                continue
            
            # Проверка цены
            price_ok, price_val = check_price(full_text)
            if not price_ok:
                continue
            
            price_str = f"💰 {price_val} ₽" if price_val else "💰 Цена не указана (возможно от 2000₽)"
            
            # Прямая ссылка на заказ
            order_id = entry.link.split('/')[-1]
            direct_link = entry.link
            
            orders.append({
                "title": title[:100],
                "link": direct_link,
                "price": price_str,
                "platform": "🔥 Kwork"
            })
        print(f"   ✅ {len(orders)} заказов от {MIN_PRICE}₽")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    return orders

def parse_freelancehunt():
    orders = []
    try:
        print("🔍 Freelancehunt...")
        feed = feedparser.parse("https://freelancehunt.com/rss/ru/projects.xml")
        for entry in feed.entries[:50]:
            title = entry.title
            description = entry.description if hasattr(entry, 'description') else ""
            full_text = title + " " + description
            
            if not any(s.lower() in full_text.lower() for s in MY_SKILLS):
                continue
            
            price_ok, price_val = check_price(full_text)
            if not price_ok:
                continue
            
            price_str = f"💰 {price_val}$" if price_val else "💰 Цена не указана"
            
            orders.append({
                "title": title[:100],
                "link": entry.link,
                "price": price_str,
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
        # У Habr нет RSS, поэтому даём ссылку с фильтром
        orders.append({
            "title": "Перейти на Habr Freelance (нужна ручная проверка цены)",
            "link": "https://freelance.habr.com/tasks",
            "price": "💰 Проверьте цену на сайте",
            "platform": "📘 Habr Freelance"
        })
        print(f"   ✅ Добавлена ссылка")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    return orders

def parse_weblancer():
    orders = []
    try:
        print("🔍 Weblancer...")
        orders.append({
            "title": "Перейти на Weblancer (нужна ручная проверка цены)",
            "link": "https://www.weblancer.net/projects/",
            "price": "💰 Проверьте цену на сайте",
            "platform": "🌐 Weblancer"
        })
        print(f"   ✅ Добавлена ссылка")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    return orders

def parse_fl():
    orders = []
    try:
        print("🔍 Fl.ru...")
        orders.append({
            "title": "Перейти на Fl.ru (нужна ручная проверка цены)",
            "link": "https://fl.ru/projects",
            "price": "💰 Проверьте цену на сайте",
            "platform": "📌 Fl.ru"
        })
        print(f"   ✅ Добавлена ссылка")
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
    print(f"💰 Мин. цена: {MIN_PRICE} ₽")
    print("=" * 50)
    
    all_orders = []
    all_orders.extend(parse_kwork())
    all_orders.extend(parse_freelancehunt())
    all_orders.extend(parse_habr())
    all_orders.extend(parse_weblancer())
    all_orders.extend(parse_fl())
    
    # Удаляем дубликаты
    seen = set()
    unique_orders = []
    for order in all_orders:
        if order['link'] not in seen:
            seen.add(order['link'])
            unique_orders.append(order)
    all_orders = unique_orders
    
    if all_orders:
        grouped = {}
        for order in all_orders:
            plat = order['platform']
            if plat not in grouped:
                grouped[plat] = []
            grouped[plat].append(order)
        
        msg = f"<b>🔍 НАЙДЕНО ЗАКАЗОВ: {len(all_orders)}</b>\n"
        msg += f"💰 Мин. цена: {MIN_PRICE} ₽\n"
        msg += f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
        msg += "─" * 30 + "\n\n"
        
        for platform, orders in grouped.items():
            msg += f"<b>{platform}</b> ({len(orders)})\n"
            for order in orders[:10]:
                msg += f"📌 <b>{order['title']}</b>\n"
                msg += f"{order['price']}\n"
                msg += f"🔗 <a href='{order['link']}'>Прямая ссылка на заказ</a>\n\n"
        
        send_tg(msg)
    else:
        msg = f"😴 <b>Заказов от {MIN_PRICE} ₽ не найдено</b>\n\n📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n💡 Попробуйте снизить MIN_PRICE в коде"
        send_tg(msg)
    
    print("=" * 50)
    print("✅ ГОТОВО")
    print("=" * 50)

if __name__ == "__main__":
    main()