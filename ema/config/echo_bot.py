from __future__ import absolute_import

from settings import TOKEN

import telebot

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

#@bot.message_handler(func=lambda m: True)
#def echo_all(message):
#    bot.reply_to(message, message.text)

@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, "I am the EMA Bot!")

bot.polling()
