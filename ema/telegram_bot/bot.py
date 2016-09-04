from django.config import settings
from django.db.models.signals import post_save
from matrix.models import Task

import telebot

def send_telebot_msg(sender,instance,**kwargs):
    if kwargs['created']:
        tb = telebot.TeleBot(settings.TELEBOT_TOKEN)
        message = '[Your Task]\n%sadmin/blog/article/%s' % (settings.HOST,instance.id)
        tb.send_message(24781498, message)

post_save.connect(send_telebot_msg, sender=Task)
