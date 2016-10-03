from django.forms import ModelForm
from django import forms
from django.conf import settings

from .models import Task, Topic
from .utils import get_user_colors
from orga.models import UserOrga

"""
create or edit Task
additional parameters: user
"""
class TaskForm(ModelForm):
    # Input-Formate und CSS zum Textfeld
    due_date = forms.DateTimeField(
                input_formats=settings.DATETIME_INPUT_FORMATS,
                widget=forms.TextInput(attrs={'class': 'dueDateInput'}))
    class Meta:
        model = Task
        fields = ['task_name', 'task_description', 'due_date', 'importance', 'topic', 'done']
        widgets = {
            'task_name': forms.TextInput(
                attrs={'placeholder': 'Name', 'class': 'form-control'}
            ),
            # Reihen dieses grossen Feldes begrenzen
            'task_description': forms.Textarea(
                attrs={
                        'placeholder': 'What is this task about?',
                        'class': 'form-control',
                        'rows': 5}
            ),
            'importance': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'topic': forms.Select(
                attrs={'class': 'form-control'}
            )
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs['user']
        kwargs.pop('user')
        super(TaskForm, self).__init__(*args, **kwargs)
        # nur die Topics des aufrufenden Users zur Auswahl geben
        self.fields['topic'].queryset = Topic.objects.filter(topic_owner=self.user)
        # wenn eine neue Aufgabe kreiert wird
        if not self.instance.task_name:
            # Unterstuetzung fuer Nutzer frueherer Versionen
            try:
                user_settings = UserOrga.objects.get(owner=self.user)
            except UserOrga.DoesNotExist:
                user_settings = UserOrga.objects.create(owner=self.user)
                user_settings.save()
            # Default Topic als Wert fuer neue Aufgaben setzen
            self.initial['topic'] = user_settings.default_topic

"""
create or edit Topic
additional parameters: user
"""
class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['topic_name', 'topic_description', 'color']
        widgets = {
            'color': forms.RadioSelect(choices=Topic.COLOR_OPTIONS),
            'topic_name': forms.TextInput(
                attrs={'placeholder': 'Name', 'class': 'form-control'}
            ),
            'topic_description': forms.Textarea(
                attrs={
                        'placeholder': 'What is this topic about?',
                        'class': 'form-control',
                        'rows': 5
                        }
            )
        }

    def __init__(self, user, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        # get different list of choices here
        topics = Topic.objects.filter(topic_owner=user)
        choices = get_user_colors(self.instance, self.fields["color"].choices, topics)
        self.fields["color"].choices = choices
        # set the topic_owner to the request.user by default
        self.instance.topic_owner = user
