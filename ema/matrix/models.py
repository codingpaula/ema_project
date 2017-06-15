"""Definiere Models Topic und Task."""
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    """
    meta class for the fields created and modified.

    An abstract base class model that provides self-updating ''created''
    and ''modified'' fields.
    @source: 2scoops, page: 66
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        """define abstract to inherit in other models."""

        abstract = True


class Topic(TimeStampedModel):
    """
    define model Topic.

    Fremdschluessel: topic owner
    Name
    Beschreibung
    Farben
    """

    topic_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    topic_name = models.CharField(max_length=30)
    topic_description = models.TextField(max_length=2000, blank=True)
    # colors plus displayed names
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
    color = models.CharField(
        max_length=15,
        choices=COLOR_OPTIONS,
        default=BLACK
    )

    def __unicode__(self):
        """Attribut, das bei Aufruf angezeigt wird."""
        return self.topic_name

    def get_absolute_url(self):
        """Referenzierung der einzelnen Instanzen ueber absolute URL."""
        return reverse('matrix:topics', kwargs={'topic_id': self.pk})


class Task(TimeStampedModel):
    """
    define model Task.

    Fremdschluessel: Topic: Topic
    Name: String (max=50)
    Beschreibung: String (max=3000)
    Wichtigkeit: String
    Due Date
    Erledigt
    Duration
    """

    # TODO Zahlen bei Importance
    task_name = models.CharField(max_length=50)
    task_description = models.TextField(max_length=3000, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    NOT_IMPORTANT = 0
    LESS_IMPORTANT = 1
    IMPORTANT = 2
    VERY_IMPORTANT = 3
    IMPORTANCE_OPTIONS = (
        (NOT_IMPORTANT, 'not important'),
        (LESS_IMPORTANT, 'less important'),
        (IMPORTANT, 'important'),
        (VERY_IMPORTANT, 'very important'),
    )
    importance = models.IntegerField(
        choices=IMPORTANCE_OPTIONS,
        default=LESS_IMPORTANT
    )
    due_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    done = models.BooleanField(default=False)
    duration = models.FloatField(blank=True, null=False, default=1)

    def __unicode__(self):
        """Attribut, das bei Aufruf angezeigt wird."""
        return self.task_name

    def get_absolute_url(self):
        """Referenzierung der einzelnen Instanzen ueber absolute URL."""
        return reverse('matrix:tasks', kwargs={'task_id': self.pk})
