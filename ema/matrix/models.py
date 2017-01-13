from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models

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
    topic_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic_name = models.CharField(max_length=30)
    topic_description = models.TextField(max_length=2000, blank=True)
    BLACK = 'black'
    GREY = 'grey'
    ROSYBROWN = 'rosybrown'
    SADDLEBROWN = 'saddlebrown'
    CRIMSON = 'crimson'
    ORANGERED = 'orangered'
    DARKORANGE = 'darkorange'
    GOLD = 'gold'
    YELLOWGREEN = 'yellowgreen'
    OLIVEDRAB = 'olivedrab'
    FORESTGREEN = 'forestgreen'
    DARKTURQUOISE = 'darkturquoise'
    DODGERBLUE = 'dodgerblue'
    ROYALBLUE = 'royalblue'
    MEDIUMBLUE = 'mediumblue'
    HOTPINK = 'hotpink'
    DEEPPINK = 'deeppink'
    MEDIUMVIOLETRED = 'mediumvioletred'
    PURPLE = 'purple'
    REBECCAPURPLE = 'rebeccapurple'
    MEDIUMORCHID = 'mediumorchid'
    COLOR_OPTIONS = [
        (BLACK, 'black'),
        (GREY, 'grey'),
        (ROSYBROWN, 'rosybrown'),
        (SADDLEBROWN, 'brown'),
        (CRIMSON, 'red'),
        (ORANGERED, 'orangered'),
        (DARKORANGE, 'orange'),
        (GOLD, 'yellow'),
        (YELLOWGREEN, 'lightgreen'),
        (OLIVEDRAB, 'olive'),
        (FORESTGREEN, 'green'),
        (DARKTURQUOISE, 'turquoise'),
        (DODGERBLUE, 'lightblue'),
        (ROYALBLUE, 'royalblue'),
        (MEDIUMBLUE, 'blue'),
        (HOTPINK, 'pink'),
        (DEEPPINK, 'deeppink'),
        (MEDIUMVIOLETRED, 'violet'),
        (PURPLE, 'purple'),
        (REBECCAPURPLE, 'darkpurple'),
        (MEDIUMORCHID, 'orchid'),
    ]
    color = models.CharField(max_length=15,
                            choices=COLOR_OPTIONS,
                            default=BLACK)

    def __unicode__(self):
        return self.topic_name

    def get_absolute_url(self):
        return reverse('matrix:topics', kwargs={'topic_id': self.pk})


class Task(TimeStampedModel):
    task_name = models.CharField(max_length=50)
    task_description = models.TextField(max_length=3000, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
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
    due_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    done = models.BooleanField(default=False)

    def __unicode__(self):
        return self.task_name

    def get_absolute_url(self):
        return reverse('matrix:tasks', kwargs={'task_id': self.pk})
