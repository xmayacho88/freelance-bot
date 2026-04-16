import requests
import feedparser
import os
import re
from datetime import datetime

# ============================================
# Telegram
# ============================================
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# ============================================
# НАСТРОЙКИ
# ============================================
MIN_PRICE = 2000

MY_SKILLS = [
    "дизайн", "логотип", "фигма", "photoshop", "illustrator",
    "python", "javascript", "html", "css", "сайт", "лендинг",
    "парсинг", "бот", "telegram", "wordpress", "wb", "озон",
    "анализ", "аналитика", "копирайтинг"
]

def send_tg(text):
    if not TOKEN or not CHAT_ID:
        print("❌ Нет токенов")
        return
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": text[:4000], "parse_mode": "HTML", "disable_web_page_preview": False}, timeout=30)
        print("✅ Отправлено")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def extract_price(text):
    """Извлекает цену из текста"""
    numbers = re.findall(r'(\d+)\s*₽', text)
    for num in numbers:
        try:
            price = int(num)
            if price >= MIN_PRICE:
                return price
        except:
            pass
    return None

def parse_kwork():
    orders = []
    try:
        print("🔍 Kwork...")
        feed = feedparser.parse("https://kwork.ru/projects/rss")
        for entry in feed.entries[:30]:
            title = entry.title
            link = entry.link
            description = entry.description if hasattr(entry, 'description') else ""
            full_text = title + " " + description
            
            # Проверка цены
            price = extract_price(full_text)
            if price is None and "₽" not in full_text:
                # Если цена не указана — пропускаем
                continue
            
            # Проверка навыков
            if not any(s.lower() in full_text.lower() for s in MY_SKILLS):
                continue
            
            price_str = f"💰 {price} ₽" if price else "💰 Цена не указана"
            
            orders.append({
                "title": title[:100],
                "link": link,
                "price": price_str,
                "platform": "🔥 Kwork"
            })
        print(f"   ✅ Найдено: {len(orders)}")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    return orders

def parse_freelancehunt():
    orders = []
    try:
        print("🔍 Freelancehunt...")
        feed = feedparser.parse("https://freelancehunt.com/rss/ru/projects.xml")
        for entry in feed.entries[:30]:
            title = entry.title
            link = entry.link
            description = entry.description if hasattr(entry, 'description') else ""
            full_text = title + " " + description
            
            # Поиск цены в долларах
            dollars = re.findall(r'(\d+)\s*\$\s*', full_text)
            price_rub = None
            for d in dollars:
                try:
                    price_rub = int(d) * 90
                    if price_rub >= MIN_PRICE:
                        break
                except:
                    pass
            
            if price_rub is None and "$" not in full_text:
                continue
            
            if not any(s.lower() in full_text.lower() for s in MY_SKILLS):
                continue
            
            price_str = f"💰 {int(price_rub/90)}$ (~{price_rub} ₽)" if price_rub else "💰 Цена не указана"
            
            orders.append({
                "title": title[:100],
                "link": link,
                "price": price_str,
                "platform": "⚡ Freelancehunt"
            })
        print(f"   ✅ Найдено: {len(orders)}")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    return orders

def main():
    print("=" * 50)
    print(f"🤖 ЗАПУСК ПАРСЕРА")
    print(f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print(f"💰 Мин. цена: {MIN_PRICE} ₽")
    print("=" * 50)
    
    all_orders = []
    all_orders.extend(parse_kwork())
    all_orders.extend(parse_freelancehunt())
    
    if all_orders:
        msg = f"<b>🔍 НАЙДЕНО ЗАКАЗОВ: {len(all_orders)}</b>\n"
        msg += f"💰 От {MIN_PRICE} ₽\n"
        msg += f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
        msg += "─" * 30 + "\n\n"
        
        for order in all_orders[:15]:
            msg += f"<b>{order['platform']}</b>\n"
            msg += f"📌 {order['title']}\n"
            msg += f"{order['price']}\n"
            msg += f"🔗 <a href='{order['link']}'>Прямая ссылка на заказ</a>\n\n"
        
        send_tg(msg)
    else:
        # ВРЕМЕННО: отправляем тестовые заказы для проверки
        test_msg = f"<b>⚠️ РЕАЛЬНЫХ ЗАКАЗОВ НЕТ</b>\n\n"
        test_msg += f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
        test_msg += f"💰 Фильтр: от {MIN_PRICE} ₽\n"
        test_msg += "─" * 30 + "\n\n"
        test_msg += "<b>🔧 Проверьте настройки:</b>\n"
        test_msg += "1. Убедитесь, что навыки в MY_SKILLS соответствуют вашим\n"
        test_msg += "2. Попробуйте снизить MIN_PRICE\n"
        test_msg += "3. Напишите мне, какие заказы вам нужны\n\n"
        test_msg += "<b>📌 ПРИМЕРЫ ЗАКАЗОВ, КОТОРЫЕ НАЙДУТСЯ:</b>\n"
        test_msg += "• Дизайн логотипа — 3000 ₽\n"
        test_msg += "• Сайт на Python — 5000 ₽\n"
        test_msg += "• Парсинг Wildberries — 4000 ₽\n"
        test_msg += "• Карточки товаров для WB — 2500 ₽"
        
        send_tg(test_msg)
    
    print("=" * 50)
    print("✅ ГОТОВО")
    print("=" * 50)

if __name__ == "__main__":
    main()