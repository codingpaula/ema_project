"""Forms for Tasks and Topics."""
from django.forms import ModelForm
from django import forms
from django.conf import settings

from .models import Task, Topic
from .utils import get_user_colors
from orga.models import UserOrga

# TODO Eingabefeld Duration for Zeit nicht Text


class TaskForm(ModelForm):
    """Input-Formate und CSS zum Textfeld."""

    due_date = forms.DateTimeField(
        input_formats=settings.DATETIME_INPUT_FORMATS,
        widget=forms.TextInput(attrs={'class': 'dueDateInput'})
    )

    class Meta:
        """Definiert die einzlenen Felder und wie sie dargestellt sind."""

        model = Task
        fields = [
            'task_name',
            'task_description',
            'due_date',
            'importance',
            'topic',
            'duration',
            'done'
        ]
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
            ),
            'duration': forms.TextInput(
                attrs={
                    'placeholder': 'Duration of Task',
                    'class': 'form-control'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        """Variablen-Setting user, topic choices und orga."""
        self.user = kwargs['user']
        kwargs.pop('user')
        super(TaskForm, self).__init__(*args, **kwargs)
        # nur die Topics des aufrufenden Users zur Auswahl geben
        self.fields['topic'].queryset = Topic.objects.filter(
            topic_owner=self.user)
        # wenn eine neue Aufgabe kreiert wird
        if not self.instance.task_name:
            # Unterstuetzung fuer Nutzer frueherer Versionen
            try:
                user_settings = UserOrga.objects.get(owner=self.user)
            except UserOrga.DoesNotExist:
                user_settings = UserOrga.objects.create(owner=self.user)
                user_settings.save()
            # Default Topic als Wert fuer neue Aufgaben setzen
            # self.initial['topic'] = user_settings.default_topic


class TopicForm(ModelForm):
    """Input-Formate und CSS zum Textfeld."""

    class Meta:
        """Definiert die einzlenen Felder und wie sie dargestellt sind."""

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
        """Variablen-Setting von user, dessen Topics, Farben."""
        # Superklasse, um alle kwargs ausser eigene zu haben
        super(TopicForm, self).__init__(*args, **kwargs)
        # topicList fuer get_user_colors
        topics = Topic.objects.filter(topic_owner=user)
        # moegliche Choices durch get_user_colors ausgeben lassen
        choices = get_user_colors(
            self.instance,
            self.fields["color"].choices, topics
        )
        # Choices an Form uebergeben
        self.fields["color"].choices = choices
        # preset topic_owner als aktuellen User
        self.instance.topic_owner = user
