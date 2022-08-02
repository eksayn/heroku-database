import telebot
import psycopg2

from config import *
bot = telebot.TeleBot(API_TOKEN)

conn=psycopg2.connect(DB_URI,sslmode='require')
cur=conn.cursor()
# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    id = message.from_user.id
    username=message.from_user.name
    bot.reply_to(message,f"Hello {username}")
    cur.execute(f"SELECT user_id FROM messages WHERE user_id = {id}")
    result=cur.fetchone()

    if not result:
        cur.execute("INSERT INTO messages(user_id, user_name, message) VALUES(%s, %s, %s)",(id,username,message))
        conn.commit()


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
