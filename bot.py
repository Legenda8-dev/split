import os
import telebot
from telebot import types
from flask import Flask, request

# ==== ENV ====
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")

if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN не задан")

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# ==== HANDLERS ====
@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Здравствуй, дорогой клиент! Хочешь оплатить абонемент в СПЛИТ?"
    )
    show_subscriptions(message.chat.id)


def show_subscriptions(chat_id):
    keyboard = types.InlineKeyboardMarkup()

    subscriptions = [
        ("Basic 12", "https://pay.ya.ru/t/R9865A"),
        ("Basic 12 + массаж", "https://pay.ya.ru/t/6ljGvg"),
        ("Basic 6 + массаж", "https://pay.ya.ru/t/Qhdhkb"),
        ("Basic 6", "https://pay.ya.ru/t/UGm4wg"),
        ("Basic 4", "https://pay.ya.ru/t/cOMWkJ"),
        ("Basic 3", "https://pay.ya.ru/t/8fY37I"),
        ("Блок тренировок к Тренеру", "https://pay.ya.ru/t/h0xbkS"),
        ("Блок тренировок СПЛИТ (2 человека)", "https://pay.ya.ru/t/xlkYbD"),
    ]

    for name, url in subscriptions:
        keyboard.add(types.InlineKeyboardButton(text=name, url=url))

    bot.send_message(chat_id, "Выберите абонемент:", reply_markup=keyboard)


# ==== WEBHOOK ====
@app.route("/webhook", methods=["POST"])
def webhook():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "OK", 200


@app.route("/")
def index():
    return "Bot is running", 200


def setup_webhook():
    if RENDER_URL:
        bot.remove_webhook()
        bot.set_webhook(f"{RENDER_URL}/webhook")


setup_webhook()
