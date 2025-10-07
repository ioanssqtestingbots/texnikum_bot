import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import os
BOT_TOKEN = os.environ['BOT_TOKEN']

# Создаем бота
bot = telebot.TeleBot(BOT_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создаем клавиатуру
    markup = InlineKeyboardMarkup(row_width=1)
    
    btn1 = InlineKeyboardButton("📚 Технические средства", callback_data='tech')
    btn2 = InlineKeyboardButton("🌍 География", callback_data='geo') 
    btn3 = InlineKeyboardButton("👥 Обществознание", callback_data='soc')
    btn4 = InlineKeyboardButton("📞 Связаться с преподавателем", callback_data='contact')
    btn5 = InlineKeyboardButton("ℹ️ О боте", callback_data='about')
    
    markup.add(btn1, btn2, btn3, btn4, btn5)
    
    bot.send_message(
        message.chat.id,
        """🎓 Учебный бот для изучения дисциплин:

- Технические средства 🖥️
- Обществознание ⚖️
- География 🌍

❗Ниже, следуя по кнопкам вы можете нажать на дисциплину для просмотра материала.""",
        reply_markup=markup
    )

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'tech':
        text = """
📚 Технические средства - Материалы:

🔹 Тема 1: Основы технических средств
• Лекция: скоро будет
• Презентация: скоро будет

🔹 Тема 2: Классификация технических средств  
• Лекция: скоро будет
• Конспект: скоро будет

🔹 Тема 3: Применение в учебном процессе
• Лекция: скоро будет
"""
    elif call.data == 'geo':
        text = """
🌍 География - Материалы:

🔹 Тема 1: Физическая география
• Лекция: скоро будет
• Презентация: скоро будет

🔹 Тема 2: Экономическая география
• Лекция: скоро будет

🔹 Тема 3: Политическая география  
• Конспект: скоро будет
"""
    elif call.data == 'soc':
        text = """
👥 Обществознание - Материалы:

🔹 Тема 1: Основы общества
• Лекция: скоро будет
• Презентация: скоро будет

🔹 Тема 2: Политическая система
• Лекция: скоро будет

🔹 Тема 3: Экономические отношения
• Конспект: скоро будет
"""
    elif call.data == 'contact':
        text = """
📞 Контакты преподавателя:

👨‍🏫 Тест Тестов Тестович
📞 Телефон: +7 000 000 00
🏢 Кабинет: (кабинет)
💬 Telegram: @ tg_teacher

"""
    elif call.data == 'about':
        text = """
ℹ️ О боте:

Этот бот создан для помощи студентам в изучении дисциплин:
• Технические средства
• География  
• Обществознание

📚 Функционал:
• Доступ к лекциям и презентациям
• Конспекты занятий  
• Контакты преподавателя

🔄 Обновления материалов происходят регулярно.
"""
    elif call.data == 'back':
        # Возврат к главному меню
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("📚 Технические средства", callback_data='tech'),
            InlineKeyboardButton("🌍 География", callback_data='geo'),
            InlineKeyboardButton("👥 Обществознание", callback_data='soc'),
            InlineKeyboardButton("📞 Связаться с преподавателем", callback_data='contact'),
            InlineKeyboardButton("ℹ️ О боте", callback_data='about')
        )
        bot.edit_message_text(
            "🎓 Добро пожаловать в учебный бот!\n\nВыберите дисциплину:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )
        return
    
    # Кнопка "Назад" для всех разделов кроме главного меню
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("⬅️ Назад", callback_data='back'))
    
    # Редактируем сообщение вместо отправки нового
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

# Запуск бота
print("✅ Бот успешно запущен!")
print("📱 Перейдите в Telegram и напишите /start вашему боту")
print("⏹️ Для остановки нажмите Ctrl+C")

bot.infinity_polling()