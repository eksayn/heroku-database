import telebot
import psycopg2

from config import *
bot = telebot.TeleBot(BOT_TOKEN)

conn=psycopg2.connect(DB_URI,sslmode='require')
cur=conn.cursor()
# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    id = message.from_user.id
    username=message.from_user.first_name
    bot.reply_to(message,f"Hello {username}")
    cur.execute("INSERT INTO users(id, username, message) VALUES(%s, %s, %s)",(id,username,message.text))
    conn.commit()


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
