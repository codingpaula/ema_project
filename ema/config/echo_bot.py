from __future__ import absolute_import

from settings import TOKEN
from matrix import Task, Topic
from orga import UserOrga

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

@bot.message_handler(commands=['today'])
def send_todays_tasks(message):
    try:
        user_settings = UserOrga.objects.get(tele_username=user_id)
    except UserOrga.DoesNotExist:
        bot.send_message(user_id, "Sorry, you haven't registered your phonse to this bot yet! Please got to the Account page of the EMA app and add your user_id there.")
    else:
        today = datetime.now().date()
        today_start = datetime.combine(today, time())
        if mode == 'today':
            tomorrow = today + timedelta(1)
            today_end = datetime.combine(tomorrow, time())
            users_tasks = Task.objects.filter(
                            topic__topic_owner=user_settings.owner,
                            due_date__lte=today_start,
                            due_date__gte=today_end)
        elif mode == 'week':
            end_of_week = today + timedelta(7)
            week = datetime.combine(end_of_week, time())
            users_tasks = Task.objects.filter(
                            topic__topic_owner=user_settings.owner,
                            due_date__lte=today_start,
                            due_date__gte=week)
    bot.reply_to(message, msg)

bot.polling()
