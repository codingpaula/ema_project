from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from django.views.generic.edit import UpdateView
from django.http import HttpResponse, HttpResponseRedirect

from .models import Topic, Task
from .forms import TaskForm, TopicForm

def index(request):
    latest_topic_list = Topic.objects.order_by('-id')[:5]
    context = {'latest_topic_list': latest_topic_list}
    return render(request, 'matrix/index.html', context)

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

            new_topic = Topic(topic_name = topic_name,
                                topic_description = topic_description,
                                color = color)
            new_topic.save()
            return HttpResponseRedirect('/matrix/addedtopic')

        return render(request, self.template_name, {'form': form})

def addtopic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic_name = form.cleaned_data['topic_name']
            topic_description = form.cleaned_data['topic_description']

            new_topic = Topic(topic_name = topic_name,
                                topic_description = topic_description)
            new_topic.save()
            return HttpResponseRedirect('/matrix/addedtopic')
    else:
        form = TopicForm()

    return render(request, 'matrix/addtopic.html', {'form': form})

def addedtopic(request):
    return render(request, 'matrix/addedtopic.html')

def topics(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    return render(request, 'matrix/topic.html', {'topic': topic})

def tasks(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'matrix/task.html', {'task': task})

def adding(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task_name = form.cleaned_data['task_name']
            task_description = form.cleaned_data['task_description']
            due_date = form.cleaned_data['due_date']

            new_task = Task(task_name = task_name, task_description =
                            task_description, topic = topic, due_date =
                            due_date)
            new_task.save()
            return HttpResponseRedirect('/matrix/added/')
    else:
        form = TaskForm()

    return render(request, 'matrix/adding.html', {'form': form, 'topic': topic})

def added(request):
    return render(request, 'matrix/added.html')

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

def matrix(request):
    all_topics = Topic.objects.all()
    return render(request, 'matrix/matrix.html',
                    {'all_topics': all_topics})
