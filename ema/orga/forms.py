from django.forms import ModelForm
from django import forms

from config.settings import TOKEN
import telebot

from .models import UserOrga
from matrix.models import Topic

"""
Form fuer die Editierung der Matrix bezogenen Einstellungen eines Nutzers
zusaetzlicher Parameter: user
"""
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
        # reduziere choices auf Nutzereigene Themen
        topics = Topic.objects.filter(topic_owner=user)
        self.fields['default_topic'].queryset = topics

"""
Form fuer die Editierung der Telegram Nutzer ID
stellt die Verbindung zum EMA Bot dar
"""
class BotForm(ModelForm):
    class Meta:
        model = UserOrga
        fields = ['tele_username']
        widgets = {
            'tele_username': forms.TextInput(
                attrs = {'required': False, 'class': 'form-control'}
            )
        }

    # Bestaetigung an den Nutzer mit dieser ID schicken
    def clean_tele_username(self):
        new_username = self.cleaned_data['tele_username']
        # wenn das neue leer ist
        if not self.cleaned_data['tele_username']:
            # alte auch leer
            if self.instance.tele_username is None:
                pass
            # alte nicht leer
            else:
                send_telegram_unregister(self.instance.tele_username)
        # wenn das neue nicht leer ist
        else:
            if self.instance.tele_username != self.cleaned_data['tele_username']:
                send_telegram_message(self.cleaned_data['tele_username'])
        # Umgehen des unique-Wert-Problems in den Models
        return self.cleaned_data['tele_username'] or None

# Hilfsfunktion fuer die Versendung von Nachrichten mit dem Bot
def send_telegram_message(user_id):
    bot = telebot.TeleBot(TOKEN)
    msg = 'Congrats! You registered for the EMA Bot'
    bot.send_message(user_id, msg)

def send_telegram_unregister(user_id):
    bot = telebot.TeleBot(TOKEN)
    msg = 'You successfully unregistered from the EMA Bot'
    bot.send_message(user_id, msg)
