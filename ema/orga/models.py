from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

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
    default_topic = models.ForeignKey(Topic, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    tele_username = models.TextField(max_length=30, blank=True, null=True, default=None, unique=True)
    def __unicode__(self):
        return self.owner.username

# die Erstellung eines UserOrga-Objekts wird an die Speicherung des User-
# Objektes gebunden
@receiver(post_save, sender=User)
def create_user_orga(sender, instance, created, **kwargs):
    if created:
        UserOrga.objects.create(owner=instance)

@receiver(post_save, sender=User)
def save_user_orga(sender, instance, created, **kwargs):
    if created:
        instance.userorga.save()
