from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Topic, Task

def index(request):
    latest_topic_list = Topic.objects.order_by('-id')[:5]
    context = {'latest_topic_list': latest_topic_list}
    return render(request, 'matrix/index.html', context)

def topics(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    return render(request, 'matrix/topic.html', {'topic': topic})

def tasks(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'matrix/task.html', {'task': task})

def adding(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    return render(request, 'matrix/adding.html', {'topic': topic})
