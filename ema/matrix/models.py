from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Topic(models.Model):
    topic_name = models.CharField(max_length=30)
    topic_description = models.TextField()
    def __unicode__(self):
        return self.topic_name

class Task(models.Model):
    task_name = models.CharField(max_length=200)
    task_description = models.TextField()
    topic = models.ForeignKey(Topic)
    NOT_IMPORTANT = '0'
    LESS_IMPORTANT = '1'
    IMPORTANT = '2'
    VERY_IMPORTANT = '3'
    IMPORTANCE_OPTIONS = (
        (NOT_IMPORTANT, 'not important'),
        (LESS_IMPORTANT, 'less important'),
        (IMPORTANT, 'important'),
        (VERY_IMPORTANT, 'very important'),
    )
    importance = models.CharField(max_length=1,
                                choices=IMPORTANCE_OPTIONS,
                                default=LESS_IMPORTANT)
    date_created = models.DateField(auto_now=False, auto_now_add=True)
    date_complete = models.DateField(auto_now=False, auto_now_add=False)
    def __unicode__(self):
        return self.task_name
