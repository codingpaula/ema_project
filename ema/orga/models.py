from django.db import models
from django.conf import settings

from matrix.models import TimeStampedModel, Topic

class UserOrga(TimeStampedModel):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ONEMONTH = '0'
    TWOMONTH = '1'
    FOURMONTH = '2'
    URGENT_OPTIONS = [
        (ONEMONTH, '1 month'),
        (TWOMONTH, '2 months'),
        (FOURMONTH, '4 months')
    ]
    urgent_axis = models.CharField(max_length=1,
                                    choices=URGENT_OPTIONS,
                                    default=TWOMONTH)
    default_topic = models.ForeignKey(Topic, null=True, default=None)
    tele_username = models.TextField(max_length=30, blank=True)
    def __unicode__(self):
        return self.owner.username
