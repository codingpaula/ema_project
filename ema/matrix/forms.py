from django.forms import ModelForm
from django import forms

from .models import Task, Topic
from .utils import get_user_colors

"""
create new Task
used in views.AddTaskView
"""
class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'task_description', 'due_date', 'importance', 'topic', 'done']
        """
        widgets = {
            'task_name': forms.TextInput(
                attrs={'id': 'taskName', 'required': True, 'placeholder': 'Name'}
            ),
            'task_description': forms.Textarea(
                attrs={'id': 'taskDescription', 'placeholder': 'What is this task about?'}
            ),
            'due_date': forms.DateTimeInput(
                attrs={'id': 'taskDate', 'required': True}
            ),
            'importance': forms.Select(
                attrs={'id': 'importance', 'required': True}
            )
        }
        """

    def __init__(self, *args, **kwargs):
        self.user = kwargs['user']
        kwargs.pop('user')
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['topic'].queryset = Topic.objects.filter(topic_owner=self.user)

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
        self.instance.topic_owner = user
