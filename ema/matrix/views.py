from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from django.views.generic.edit import UpdateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Topic, Task
from .forms import TaskForm, TopicForm

"""
view for startpage after login - matrix
hands over all topics of the current user
"""
@login_required(login_url='/account/login')
def matrix(request):
    all_topics = Topic.objects.filter(topic_owner=request.user.id)
    return render(request, 'matrix/matrix.html',
                    {'all_topics': all_topics})

"""
new topic:
uses TopicForm
"""
class AddTopicView(View):
    form_class = TopicForm
    template_name = 'matrix/addtopic.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            topic_name = form.cleaned_data['topic_name']
            topic_description = form.cleaned_data['topic_description']
            color = form.cleaned_data['color']
            topic_owner = request.user

            new_topic = Topic(topic_name = topic_name,
                                topic_description = topic_description,
                                color = color, topic_owner = topic_owner)
            new_topic.save()
            messages.info(request, 'Topic %s successfully created.' % new_topic.topic_name)
            return HttpResponseRedirect('/matrix/')

        return render(request, self.template_name, {'form': form})

"""
new task:
uses TaskForm
@params: topic_id
"""
class AddTaskView(View):
    form_class = TaskForm
    template_name = 'matrix/adding.html'

    def get(self, request, topic_id):
        topic = get_object_or_404(Topic, pk=topic_id)
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'topic': topic})

    def post(self, request, topic_id):
        topic = get_object_or_404(Topic, pk=topic_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            task_name = form.cleaned_data['task_name']
            task_description = form.cleaned_data['task_description']
            due_date = form.cleaned_data['due_date']
            importance = form.cleaned_data['importance']

            new_task = Task(task_name = task_name,
                                task_description = task_description,
                                due_date = due_date, importance = importance,
                                topic = topic)
            new_task.save()
            messages.info(request, 'Task %s successfully created.' % new_task.task_name)
            return HttpResponseRedirect('/matrix/')

        return render(request, self.template_name, {'form': form, 'topic': topic})

"""
shows all the topics of the logged in owner
@params: topic_id
Permission denied message if unsuccessful
"""
@login_required(login_url='/account/login')
def topics(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if topic.topic_owner == request.user:
        return render(request, 'matrix/topic.html', {'topic': topic})
    else:
        messages.info(request, 'Permission denied!')
        return HttpResponseRedirect('/matrix/')

"""
shows requested task details
@params: task_id
Permission denied message if unsuccessful
"""
@login_required(login_url='/account/login')
def tasks(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.topic.topic_owner == request.user:
        return render(request, 'matrix/task.html', {'task': task})
    else:
        messages.info(request, 'Permission denied!')
        return HttpResponseRedirect('/matrix/')

"""
TODO: editing
"""
def edittopic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    return render(request, 'matrix/topicediting.html', {'topic': topic})

def editing(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'matrix/taskediting.html', {'task': task})

class TaskUpdate(UpdateView):
    model = Task
    fields = ['task_name', 'task_description', 'importance', 'due_date']
    template_name_suffix = 'taskediting'
    
