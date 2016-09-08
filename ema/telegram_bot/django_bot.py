from __future__ import absolute_import
from datetime import datetime, timedelta, time

from django.core.management.base import BaseCommand

from ema.orga.models import UserOrga
from ema.matrix.models import Task, Topic

import telebot

from daemon_command import DaemonCommand

def start_telebot():

    bot = telebot.TeleBot(settings.TELEBOT_TOKEN)

    @bot.message_handler(commands=['hello', 'today', 'week', 'reminder'])
    def command_list(message):
        text = message.text
        if 'hello' in text:
            bot.send_message(message.chat.id, "Hello %s!" % (message.from_user.first_name))
        elif 'today' in text:
            todays_tasks(message.from_user.id, 'today')
        elif 'week' in text:
            todays_tasks(message.from_user.id, 'week')

    bot.polling()

class Command(DaemonCommand):

    STDOUT = '../log/telebot.err'
    STDERR = STDOUT

    def loop_callback(self):
        start_telebot()
        time.sleep(2.5)

def todays_tasks(user_id, mode):
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
        bot.send_message(user_id,
                        "These are your tasks for today: ")
