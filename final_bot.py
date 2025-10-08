
# VERSION 2.0_TEST ADD ADMIN - PANEL !!!

# VERSION 2.0 - WITH ADMIN PANEL AND CONTENT MANAGEMENT

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
import os
import threading
import json
import time

# Flask для рендеровского хостинга
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_IDS = [837888138]  # айдишник админа 

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")

# Создаем бота
bot = telebot.TeleBot(BOT_TOKEN)

# Файлы для хранения данных
CONTENT_FILE = 'content.json'
USERS_FILE = 'users.json'

# Загрузка контента
def load_content():
    try:
        with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        # Стартовый контент
        default_content = {
            "tech": {
                "title": "📚 Технические средства",
                "materials": [
                    "🔹 Тема 1: Основы технических средств",
                    "• Лекция: скоро будет",
                    "• Презентация: скоро будет"
                ]
            },
            "geo": {
                "title": "🌍 География", 
                "materials": [
                    "🔹 Тема 1: Физическая география",
                    "• Лекция: скоро будет",
                    "• Презентация: скоро будет"
                ]
            },
            "soc": {
                "title": "👥 Обществознание",
                "materials": [
                    "🔹 Тема 1: Основы общества", 
                    "• Лекция: скоро будет",
                    "• Презентация: скоро будет"
                ]
            },
            "cloud": {
                "title": "☁️ Облако общество/география",
                "materials": [
                    "📁 Google Drive с материалами:",
                    "https://drive.google.com/drive/folders/1wPT76zG8mo2zz_4ZIYpyS0FPZEioxkc3"
                ]
            },
            "contact": {
                "title": "📞 Связаться с преподавателем",
                "materials": [
                    "👨‍🏫 Тест Тестов Тестович",
                    "📞 Телефон: +7 000 000 00",
                    "🏢 Кабинет: (кабинет)",
                    "💬 Telegram: @tg_teacher"
                ]
            }
        }
        save_content(default_content)
        return default_content

def save_content(content):
    with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)

def load_users():
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

def is_admin(user_id):
    return user_id in ADMIN_IDS

# Загружаем контент при старте
content = load_content()

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    save_user(message.chat.id)
    
    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(content["tech"]["title"], callback_data='tech')
    btn2 = InlineKeyboardButton(content["geo"]["title"], callback_data='geo') 
    btn3 = InlineKeyboardButton(content["soc"]["title"], callback_data='soc')
    btn4 = InlineKeyboardButton(content["cloud"]["title"], callback_data='cloud')
    btn5 = InlineKeyboardButton(content["contact"]["title"], callback_data='contact')
    btn6 = InlineKeyboardButton("ℹ️ О боте", callback_data='about')
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    
    # Добавляем кнопку админа если пользователь админ
    if is_admin(message.from_user.id):
        markup.add(InlineKeyboardButton("⚙️ Админ-панель", callback_data='admin_panel'))
    
    bot.send_message(
        message.chat.id,
        """🎓 Учебный бот для изучения дисциплин: (VERSION 2.0)

- Технические средства 🖥️
- Обществознание ⚖️  
- География 🌍

❗Ниже, следуя по кнопкам вы можете нажать на дисциплину для просмотра материала.""",
        reply_markup=markup
    )

# АДМИН КОМАНДЫ
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ У вас нет прав доступа")
        return
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📝 Управление контентом", callback_data='admin_content'),
        InlineKeyboardButton("📢 Рассылка", callback_data='admin_broadcast'),
        InlineKeyboardButton("📊 Статистика", callback_data='admin_stats'),
        InlineKeyboardButton("⬅️ Главное меню", callback_data='back')
    )
    
    bot.send_message(
        message.chat.id,
        "⚙️ *Админ-панель*\n\nВыберите действие:",
        reply_markup=markup,
        parse_mode='Markdown'
    )

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    global content
    
    if call.data == 'back':
        show_main_menu(call)
        return
        
    elif call.data == 'admin_panel':
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "❌ Нет прав доступа")
            return
            
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("📝 Управление контентом", callback_data='admin_content'),
            InlineKeyboardButton("📢 Рассылка", callback_data='admin_broadcast'),
            InlineKeyboardButton("📊 Статистика", callback_data='admin_stats'),
            InlineKeyboardButton("⬅️ Главное меню", callback_data='back')
        )
        
        bot.edit_message_text(
            "⚙️ *Админ-панель*\n\nВыберите действие:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup,
            parse_mode='Markdown'
        )
        return
        
    elif call.data == 'admin_content':
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "❌ Нет прав доступа")
            return
            
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("📚 Технические средства", callback_data='edit_tech'),
            InlineKeyboardButton("🌍 География", callback_data='edit_geo'),
            InlineKeyboardButton("👥 Обществознание", callback_data='edit_soc'),
            InlineKeyboardButton("☁️ Облако", callback_data='edit_cloud'),
            InlineKeyboardButton("📞 Контакты", callback_data='edit_contact'),
            InlineKeyboardButton("⬅️ Назад", callback_data='admin_panel')
        )
        
        bot.edit_message_text(
            "📝 *Управление контентом*\n\nВыберите раздел для редактирования:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup,
            parse_mode='Markdown'
        )
        return
        
    elif call.data.startswith('edit_'):
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "❌ Нет прав доступа")
            return
            
        section = call.data.replace('edit_', '')
        bot.answer_callback_query(call.id, f"Редактирование раздела: {section}")
        
        # Сохраняем состояние редактирования
        bot.register_next_step_handler(call.message, process_content_edit, section)
        
        current_content = "\n".join(content[section]["materials"])
        bot.send_message(
            call.message.chat.id,
            f"✏️ *Редактирование раздела: {content[section]['title']}*\n\n"
            f"Текущее содержимое:\n{current_content}\n\n"
            f"📝 *Пришлите новое содержимое раздела:*\n"
            f"(каждая строка с новой строки)",
            parse_mode='Markdown'
        )
        return
        
    elif call.data == 'admin_broadcast':
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "❌ Нет прав доступа")
            return
            
        bot.answer_callback_query(call.id, "Подготовка рассылки")
        bot.register_next_step_handler(call.message, process_broadcast)
        
        bot.send_message(
            call.message.chat.id,
            "📢 *Рассылка сообщения*\n\n"
            "Пришлите сообщение которое будет отправлено всем пользователям:",
            parse_mode='Markdown'
        )
        return
        
    elif call.data == 'admin_stats':
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "❌ Нет прав доступа")
            return
            
        users = load_users()
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("⬅️ Назад", callback_data='admin_panel'))
        
        bot.edit_message_text(
            f"📊 *Статистика бота*\n\n"
            f"👥 Всего пользователей: *{len(users)}*\n"
            f"🕒 Последнее обновление: {time.strftime('%H:%M:%S')}",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup,
            parse_mode='Markdown'
        )
        return
        
    # Обработка обычных разделов контента
    elif call.data in content:
        text = f"{content[call.data]['title']} - Материалы:\n\n" + "\n".join(content[call.data]["materials"])
        
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("⬅️ Назад", callback_data='back'))
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )
        
    elif call.data == 'about':
        text = """
ℹ️ О боте (VERSION 2.0):

Этот бот создан для помощи студентам в изучении дисциплин:
• Технические средства
• География  
• Обществознание

📚 Функционал:
• Доступ к лекциям и презентациям
• Конспекты занятий  
• Контакты преподавателя
• Электронное облако с материалами

🔄 Обновления материалов происходят регулярно.
"""
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("⬅️ Назад", callback_data='back'))
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

def process_content_edit(message, section):
    global content
    if not is_admin(message.from_user.id):
        return
        
    new_materials = message.text.split('\n')
    content[section]["materials"] = new_materials
    save_content(content)
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("⬅️ В админ-панель", callback_data='admin_panel'))
    
    bot.send_message(
        message.chat.id,
        f"✅ *Содержимое раздела обновлено!*\n\n"
        f"Раздел: {content[section]['title']}\n"
        f"Изменения сохранены.",
        reply_markup=markup,
        parse_mode='Markdown'
    )

def process_broadcast(message):
    if not is_admin(message.from_user.id):
        return
        
    broadcast_text = message.text
    users = load_users()
    
    progress_msg = bot.send_message(
        message.chat.id,
        f"📤 *Начинаю рассылку...*\nПользователей: {len(users)}",
        parse_mode='Markdown'
    )
    
    success = 0
    errors = 0
    
    for user_id in users:
        try:
            bot.send_message(user_id, f"📢 *Важное сообщение:*\n\n{broadcast_text}", parse_mode='Markdown')
            success += 1
        except:
            errors += 1
    
    bot.edit_message_text(
        f"✅ *Рассылка завершена!*\n\n"
        f"📨 Успешно: {success}\n"
        f"❌ Ошибок: {errors}",
        message.chat.id,
        progress_msg.message_id,
        parse_mode='Markdown'
    )

def show_main_menu(call):
    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(content["tech"]["title"], callback_data='tech')
    btn2 = InlineKeyboardButton(content["geo"]["title"], callback_data='geo') 
    btn3 = InlineKeyboardButton(content["soc"]["title"], callback_data='soc')
    btn4 = InlineKeyboardButton(content["cloud"]["title"], callback_data='cloud')
    btn5 = InlineKeyboardButton(content["contact"]["title"], callback_data='contact')
    btn6 = InlineKeyboardButton("ℹ️ О боте", callback_data='about')
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    
    if is_admin(call.from_user.id):
        markup.add(InlineKeyboardButton("⚙️ Админ-панель", callback_data='admin_panel'))
    
    bot.edit_message_text(
        "🎓 Добро пожаловать в учебный бот!\n\nВыберите дисциплину:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

def run_bot():
    """Функция для запуска бота в отдельном потоке"""
    print("✅ Бот успешно запущен! (VERSION 2.0)")
    print("📱 Перейдите в Telegram и напишите /start вашему боту")
    print("⚙️ Админ-панель: /admin")
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"❌ Ошибка в работе бота: {e}")

if __name__ == '__main__':
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Запускаем Flask сервер для Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)