from django.core.management.base import BaseCommand

from config import settings
from matrix.models import Task, Topic
from orga.models import UserOrga

import telebot
from telebot import types

from daemon_command import DaemonCommand

commands = {
    'hello': 'Say hello to the EMA Bot!',
    'tasks': 'Select which tasks you want to see',
    'help': 'Gives you information about the available commands',
    'howtosetup': 'Tells you what you have to do to use this bot with your EMA account'
}

def start_telebot():

    bot = telebot.TeleBot(settings.TOKEN)

    @bot.message_handler(commands=['hello'])
    def command_list(message):
        bot.send_message(message.chat.id, "Hello %s!" % (message.from_user.first_name))

    @bot.message_handler(commands=['help'])
    def command_help(message):
        help_text = "These commands are available for the EMA Bot: \n"
        for command in commands:
            help_text += "/" + command + ": "
            help_text += commands[command] + "\n"
        bot.send_message(message.chat.id, help_text)

    @bot.message_handler(commands=['howtosetup'])
    def command_howtosetup(message):
        setup_text = "To set up your EMA account with this bot, simply go to your account at the EMApp and go to Account."
        setup_chat_id = "There you have to enter your chat id: %s!" % (message.from_user.id)
        msg = setup_text + "\n" + setup_chat_id
        bot.send_message(message.chat.id, msg)

    @bot.message_handler(commands=['tasks'])
    def command_tasks(message):
        markup = types.ReplyKeyboardMarkup()
        one_day = types.KeyboardButton('one day')
        one_week = types.KeyboardButton('one week')
        overdue = types.KeyboardButton('overdue')
        markup.add(one_day, one_week, overdue)
        bot.send_message(
                    message.chat.id,
                    "Which of your tasks do you want see?",
                    reply_markup=markup)

    #@bot.message_handler(func=lambda message: )

    bot.polling()

class Command(DaemonCommand):

    STDOUT = '../log/telebot.err'
    STDERR = STDOUT

    def loop_callback(self):
        start_telebot()
        time.sleep(2.5)
