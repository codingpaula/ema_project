from django.forms import ModelForm
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from .models import Task, Topic
from .utils import get_user_colors
from orga.models import UserOrga

"""
create new Task
used in views.AddTaskView
"""
class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'task_description', 'due_date', 'importance', 'topic', 'done']
        widgets = {
            'task_name': forms.TextInput(
                attrs={'placeholder': 'Name'}
            ),
            'task_description': forms.Textarea(
                attrs={'placeholder': 'What is this task about?'}
            )
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs['user']
        kwargs.pop('user')
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['topic'].queryset = Topic.objects.filter(topic_owner=self.user)
        try:
            user_settings = UserOrga.objects.get(owner=self.user)
        except ObjectDoesNotExist:
            user_settings = UserOrga(owner=self.user)
            user_settings.save()
        self.initial['topic'] = user_settings.default_topic


"""
create new Topic
used in views.AddTopicView
"""
class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['topic_name', 'topic_description', 'color']
        widgets = {
            'color': forms.RadioSelect(choices=Topic.COLOR_OPTIONS),
        }

    def __init__(self, user, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        # get different list of choices here
        topics = Topic.objects.filter(topic_owner=user)
        choices = get_user_colors(self.fields["color"].choices, topics)
        self.fields["color"].choices = choices
        # set the topic_owner to the request.user by default
        self.instance.topic_owner = user
