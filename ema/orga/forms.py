from django.forms import ModelForm
from django import forms

from config.settings import TOKEN
import telebot

from .models import UserOrga
from matrix.models import Topic

class OrgaForm(ModelForm):
    class Meta:
        model = UserOrga
        fields = ['urgent_axis', 'default_topic']
        widgets = {
            'urgent_axis': forms.Select(
                attrs = {'class': 'form-control'}
            ),
            'default_topic': forms.Select(
                attrs = {'required': False, 'class': 'form-control'}
            )
        }

    def __init__(self, user, *args, **kwargs):
        super(OrgaForm, self).__init__(*args, **kwargs)
        # get different list of choices here
        topics = Topic.objects.filter(topic_owner=user)
        self.fields['default_topic'].queryset = topics

class BotForm(ModelForm):
    class Meta:
        model = UserOrga
        fields = ['tele_username']
        widgets = {
            'tele_username': forms.TextInput(
                attrs = {'required': False, 'class': 'form-control'}
            )
        }

    def clean(self):
        cleaned_data = super(BotForm, self).clean()
        #if self.has_changed():  # new instance or existing updated (form has data to save)
        if self.instance.pk is not None:  # new instance only
            if self.instance.tele_username != cleaned_data['tele_username']:
                if self.instance.tele_username is not None:
                    send_telegram_message(cleaned_data['tele_username'])
        return cleaned_data

def send_telegram_message(user_id):
    bot = telebot.TeleBot(TOKEN)
    msg = 'Congrats! You registered for the EMA Bot'
    bot.send_message(user_id, msg)
