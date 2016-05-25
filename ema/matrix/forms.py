from django.forms import ModelForm

from models import Task, Topic

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'task_description', 'due_date', 'importance']

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['topic_name', 'topic_description', 'color']
