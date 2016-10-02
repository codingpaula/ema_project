from django.core.management.base import BaseCommand
from django.utils import timezone

from config import settings
from matrix.models import Task, Topic
from orga.models import UserOrga

import telebot
from telebot import types

from datetime import datetime, timedelta

from daemon_command import DaemonCommand

commands = {
    'hello': 'Say hello to the EMA Bot!',
    'tasks': 'Select which tasks you want to see',
    'help': 'Gives you information about the available commands',
    'howtosetup': 'Tells you what you have to do to use this bot with your EMA account',
    'registered': 'Check if you are registered to this bot and if yes with what EMA account'
}

hiddenKeyBoard = types.ReplyKeyboardHide()

markup = types.ReplyKeyboardMarkup()
one_day = types.KeyboardButton('one day')
one_week = types.KeyboardButton('one week')
overdue = types.KeyboardButton('overdue')

def task_to_message(task):
    importance = int(task.importance)+1
    due_date = timezone.localtime(task.due_date).strftime(format='%d/%m/%Y %H:%M')
    return "Task '%s' of Topic '%s': \n importance: %s, due date: %s \n" % (task.task_name, task.topic, importance, due_date)

def task_message(task_queryset, mode):
    if task_queryset.count() > 0:
        answer = ""
        for task in task_queryset:
            answer = answer + task_to_message(task)
        return answer
    else:
        if mode == 'overdue':
            return "You don't have tasks that are overdue!"
        else:
            return "You don't have tasks %s!" % mode

def start_telebot():
    markup.add(one_day, one_week, overdue)
    bot = telebot.TeleBot(settings.TOKEN)
    def not_registered_message(chat_id):
        bot.send_message(
                chat_id,
                "Sorry, you are not registered yet! Run /howtosetup to find out how to register!",
                reply_markup=hiddenKeyBoard
        )

    # say hello to the telebot
    @bot.message_handler(commands=['hello'])
    def command_hello(message):
        bot.send_message(
                message.chat.id,
                "Hello %s!" % (message.from_user.first_name),
                reply_markup=hiddenKeyBoard
        )

    # show all available commands
    @bot.message_handler(commands=['help'])
    def command_help(message):
        help_text = "These commands are available for the EMA Bot: \n"
        for command in commands:
            help_text += "/" + command + ": "
            help_text += commands[command] + "\n"
        bot.send_message(
                message.chat.id,
                help_text,
                reply_markup=hiddenKeyBoard
        )

    @bot.message_handler(commands=['howtosetup'])
    def command_howtosetup(message):
        setup_text = "To set up your EMApp account with this bot, simply log into the EMApp and go to Account."
        setup_chat_id = "Enter your chat id into the tele username field and click save: %s!" % (message.from_user.id)
        msg = setup_text + "\n" + setup_chat_id
        bot.send_message(
                message.chat.id,
                msg,
                reply_markup=hiddenKeyBoard
        )

    @bot.message_handler(commands=['registered'])
    def command_registered(message):
        try:
            user_orga = UserOrga.objects.get(tele_username=message.from_user.id)
            bot.send_message(
                    message.chat.id,
                    "You are registered with the EMApp! username: %s" % (user_orga.owner.username),
                    reply_markup=hiddenKeyBoard
            )
        except:
            not_registered_message(message.chat.id)

    @bot.message_handler(commands=['tasks'])
    def command_tasks(message):
        bot.send_message(
                    message.chat.id,
                    "Which of your tasks do you want see?",
                    reply_markup=markup
        )

    @bot.message_handler(func=lambda message: message.text == "one day")
    def command_one_day(message):
        try:
            user_orga = UserOrga.objects.get(tele_username=message.from_user.id)
            jetzt = timezone.localtime(timezone.now())
            bis = jetzt+timedelta(days=1)
            tasks = Task.objects.filter(
                            due_date__gt=jetzt,
                            due_date__lt=bis,
                            done=False,
                            topic__topic_owner=user_orga.owner
            )
            msg = task_message(tasks, 'today')
            bot.send_message(
                    message.chat.id,
                    msg,
                    reply_markup=markup
            )
        except:
            not_registered_message(message.chat.id)

    @bot.message_handler(func=lambda message: message.text == "one week")
    def command_one_week(message):
        try:
            user_orga = UserOrga.objects.get(tele_username=message.from_user.id)
            tasks = Task.objects.filter(
                            due_date__gt=timezone.now(),
                            due_date__lt=timezone.now()+timedelta(days=7),
                            done=False,
                            topic__topic_owner=user_orga.owner
            )
            msg = task_message(tasks, 'this week')
            bot.send_message(
                    message.chat.id,
                    msg,
                    reply_markup=markup
            )
        except:
            not_registered_message(message.chat.id)

    @bot.message_handler(func=lambda message: message.text == "overdue")
    def command_overdue(message):
        try:
            user_orga = UserOrga.objects.get(tele_username=message.from_user.id)
            tasks = Task.objects.filter(
                            due_date__lt=timezone.now(),
                            done=False,
                            topic__topic_owner=user_orga.owner
            )
            msg = task_message(tasks, 'overdue')
            bot.send_message(
                    message.chat.id,
                    msg,
                    reply_markup=markup
            )
        except:
            not_registered_message(message.chat.id)

    bot.polling()

class Command(DaemonCommand):

    STDOUT = 'telebot.err'
    STDERR = STDOUT

    def loop_callback(self):
        start_telebot()
