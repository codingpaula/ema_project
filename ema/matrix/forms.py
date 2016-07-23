from django.forms import ModelForm

from models import Task, Topic

"""
create new Task
used in views.AddTaskView
"""
class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'task_description', 'due_date', 'importance']

"""
create new Topic
used in views.AddTopicView
"""
class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['topic_name', 'topic_description', 'color']
