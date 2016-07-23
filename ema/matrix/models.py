from __future__ import unicode_literals

from django.conf import settings
from django.db import models

# Create your models here.
# meta class for the fields created and modified
class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating ''created''
    and ''modified'' fields.
    @source: 2scoops, page: 66
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Topic(TimeStampedModel):
    topic_owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    topic_name = models.CharField(max_length=30)
    topic_description = models.TextField(blank=True)
    """ TODO find color picker """
    color = models.CharField(max_length=15, default='red')
    def __unicode__(self):
        return self.topic_name

class Task(TimeStampedModel):
    task_name = models.CharField(max_length=200)
    task_description = models.TextField(blank=True)
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
    due_date = models.DateField(auto_now=False, auto_now_add=False)
    done = models.BooleanField(default=False)
    def __unicode__(self):
        return self.task_name
