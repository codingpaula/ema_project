import json
from django.shortcuts import get_object_or_404, render, render_to_response
from django.views.generic import View
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder

from .models import Topic, Task
from .forms import TaskForm, TopicForm
from .utils import get_user_colors

"""
view for startpage after login - matrix
hands over all topics of the current user
"""
@login_required(login_url='/account/login')
def matrix(request):
    all_topics = Topic.objects.filter(topic_owner=request.user.id)
    to_data = {}
    data = [model_to_dict(instance) for instance in all_topics]
    to_data['topics'] = data
    topic_data = json.dumps(to_data, cls=DjangoJSONEncoder)
    all_tasks = Task.objects.filter(topic__topic_owner=request.user.id)
    data = [model_to_dict(instance) for instance in all_tasks]
    response_data = {}
    response_data['objects'] = data
    end_data = json.dumps(response_data, cls=DjangoJSONEncoder)
    return render(request, 'matrix/matrix.html',
                    {'all_topics': all_topics, 'all_tasks': all_tasks,
                    'end_data': end_data, 'topic_data': topic_data})

"""
new topic:
uses TopicForm
"""
class AddTopicView(View):
    form_class = TopicForm
    template_name = 'matrix/addtopic.html'

    def get(self, request):
        form = self.form_class(user=request.user.id)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(user=request.user.id, data=request.POST)
        if form.is_valid():
            topic_owner = request.user
            topic_name = form.cleaned_data['topic_name']
            topic_description = form.cleaned_data['topic_description']
            color = form.cleaned_data['color']

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
    login_url = '/account/login/'
    form_class = TaskForm
    template_name = 'matrix/adding.html'

    def get(self, request):
        form = TaskForm(user=request.user.id)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # topic = get_object_or_404(Topic, pk=topic_id)
        form = TaskForm(request.POST, user=request.user.id)
        if form.is_valid():
            task_name = form.cleaned_data['task_name']
            task_description = form.cleaned_data['task_description']
            due_date = form.cleaned_data['due_date']
            importance = form.cleaned_data['importance']
            topic = form.cleaned_data['topic']

            new_task = Task(task_name = task_name,
                                task_description = task_description,
                                due_date = due_date, importance = importance,
                                topic = topic)
            new_task.save()
            messages.info(request, 'Task %s successfully created.' % new_task.task_name)
            return HttpResponseRedirect('/matrix/')

        return render(request, self.template_name, {'form': form})

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

class TaskCreate(CreateView):
    model = Task
    fields = ['task_name', 'task_description', 'importance', 'due_date']
    template_name = 'matrix/adding.html'

class TaskUpdate(UpdateView):
    model = Task
    #form_class = TaskForm
    fields = ['task_name', 'task_description', 'importance', 'due_date']
    template_name = 'matrix/taskediting.html'
    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs.get('task_id'))

class TaskDelete(DeleteView):
    model = Task
    success_url = 'matrix/matrix.html'
    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs.get('task_id'))

class TopicUpdate(UpdateView):
    model = Topic
    fields = ['topic_name', 'topic_description', 'color']
    template_name = 'matrix/topicediting.html'
    def get_object(self):
        return get_object_or_404(Topic, pk=self.kwargs.get('topic_id'))
