from django.db.models import Q
from django.utils import timezone

from config import settings
from matrix.models import Task, Topic
from orga.models import UserOrga

import telebot
import time

from datetime import datetime, timedelta

bot = telebot.TeleBot(settings.TOKEN)

def push_due_dates():
    to_push = check_tasks()
    for task in to_push:
        bot.send_message(task['user'], task['msg'])

def check_tasks():
    to_push = []
    jetzt = timezone.localtime(timezone.now())
    bis = jetzt+timedelta(minutes=-5)
    # eigentlich nur die die dran sind
    telis = UserOrga.objects.exclude(tele_username='')
    for teli in telis:
        tasks = Task.objects.filter(
                        due_date__lt=jetzt,
                        due_date__gt=bis,
                        done=False,
                        topic__topic_owner=teli.owner)
        for task in tasks:
            bundle = {
                'user': teli.tele_username,
                'msg': "Task '%s' is due now! Click here to see it: '%s/matrix/%s/taskediting'" % (task.task_name, settings.HOST_ADDRESS, task.id)
            }
            to_push.append(bundle)
        return to_push
