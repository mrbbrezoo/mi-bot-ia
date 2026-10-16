
import os
from flask import Flask, request
import telebot
from groq import Groq

# Servidor y Telegram
app = Flask(__name__)
TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

# IA con Groq (Ultra rápida)
GROQ_KEY = os.environ.get('GROQ_API_KEY')
client = Groq(api_key=GROQ_KEY)

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + TOKEN)
    return "Bot de IA con Groq activado", 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy tu bot inteligente. Pregúntame lo que quieras y te responderé de inmediato. ⚡")

@bot.message_handler(func=lambda message: True)
def responder_con_groq(message):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": message.text}]
        )
        bot.reply_to(message, completion.choices.message.content)
    except Exception as e:
        bot.reply_to(message, "Hubo un pequeño error. Inténtalo de nuevo.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
