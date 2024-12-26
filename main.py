import telebot
import google.generativeai as genai
from secret import *


bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GOOGLE_API)

model = genai.GenerativeModel('gemini-pro') 

# Функция для общения с AI
def ask_google_ai(prompt):
    try:
        # Дополнительная настройка для тона общения как психолог
        context = (
            "Ты — дружелюбный и поддерживающий психолог. "
            "Твоя цель — помогать пользователю чувствовать себя лучше, давать советы и проявлять сочувствие. "
            "Будь вежливым, тактичным и внимательным к эмоциям собеседника."
            "Разговаривай на том языке на котором тебе обращаеться собеседник! и да если собесдник разговаривает на украинском или белоруском то разговаривай сними на русском не разговаривай на украинском !"
        )
        full_prompt = f"{context}\n{prompt}"
        response = model.generate_content(full_prompt)  # Генерация ответа
        return response.text  # Возвращаем текст
    except Exception as e:
        return "Извините, я не смог обработать ваш запрос. Попробуйте ещё раз."


# Приветствие при старте
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я ваш личный помощник-психолог. 😊\n"
        "Я здесь, чтобы выслушать вас и поддержать. Как вы себя чувствуете сегодня?"
    )


# Обработчик сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text  # Получаем сообщение от пользователя
    response = ask_google_ai(user_input)  # Запрашиваем ответ у AI
    bot.send_message(message.chat.id, response)  # Отправляем ответ


# Запускаем бота
bot.polling()
