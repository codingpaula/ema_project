import json
from django.shortcuts import get_object_or_404, render, render_to_response
from django.views.generic import View
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder

from orga.models import UserOrga

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
    all_tasks = Task.objects.filter(topic__topic_owner=request.user.id, done=False)
    data = [model_to_dict(instance) for instance in all_tasks]
    response_data = {}
    response_data['objects'] = data
    end_data = json.dumps(response_data, cls=DjangoJSONEncoder)
    task_form = TaskForm(user=request.user.id)
    # locals()
    return render(request, 'matrix/matrix.html',
                    {'all_topics': all_topics, 'all_tasks': all_tasks,
                    'end_data': end_data, 'topic_data': topic_data,
                    'task_form': task_form})

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
            messages.info(request, 'Topic "%s" successfully created.' % new_topic.topic_name)
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
            messages.info(request, 'Task "%s" successfully created.' % new_task.task_name)
            return HttpResponseRedirect('/matrix/')

        return render(request, self.template_name, {'form': form})


# source: django docs:
#https://docs.djangoproject.com/en/1.8/topics/class-based-views/generic-editing/
class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            print "got something"
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            print "got something"
            data = {
                'task_name': self.object.task_name,
                'task_description': self.object.task_description,
                'due_date': self.object.due_date,
                'importance': self.object.importance,
                'topic': self.object.topic,
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

class TaskCreate(SuccessMessageMixin, AjaxableResponseMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'matrix/adding.html'
    success_message = "Task '%(task_name)s' was successfully created!"
    success_url = '/matrix'

    def get_form_kwargs(self):
        kwargs = super(TaskCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    #def get_initial(self):
    #    initial = super(TaskCreate, self).get_initial()
    #    if (UserOrga.objects.get(owner=self.request.user)!= None):
    #        user_settings = UserOrga.objects.get(owner=self.request.user)
            # Copy the dictionary so we don't accidentally change a mutable dict
    #        initial = initial.copy()
    #        initial['topic'] = user_settings.default_topic
    #        return initial
    #    else:
    #        return initial

class TopicCreate(SuccessMessageMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'matrix/addtopic.html'
    success_message = "Topic '%(topic_name)s' was successfully created!"
    success_url = '/matrix'

    def get_form_kwargs(self):
        kwargs = super(TopicCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task_name = request.POST.get('task_name')
            task_description = request.POST.get('task_description')
            due_date = request.POST.get('due_date')
            importance = request.POST.get('importance')
            topic = Topic.objects.get(pk=request.POST.get('topic'))

            new_task = Task(task_name = task_name, task_description =
                        task_description, topic = topic, due_date =
                        due_date, importance = importance)
            new_task.save()
            task = Task.objects.filter(task_name=task_name)
            all_tasks = Task.objects.filter(topic__topic_owner=request.user.id, done=False)
            data = json.dumps([model_to_dict(instance) for instance in all_tasks], cls=DjangoJSONEncoder)
            response_data = {}
            response_data['objects'] = data
            print("did do json")
            # messages.info("Task '%(task_name)s' was successfully created!")
            return HttpResponse(data, content_type="application/json")
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

class AJAXCreateTaskView(View):
    def post(self, request):
        form = TaskForm(request.POST, user=request.user.id)
        # if form.is_valid():


    def get(self, request):
        form = TaskForm(user=request.user.id)

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
shows all tasks that have been marked done, since they won't show up in matrix
anymore
"""
@login_required(login_url='/account/login')
def done_tasks(request):
    dones = Task.objects.filter(topic__topic_owner=request.user.id, done=True)
    return render(request, 'matrix/done_tasks.html', {'dones': dones})

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
    fields = ['task_name', 'task_description', 'importance', 'due_date', 'done']
    template_name = 'matrix/taskediting.html'
    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs.get('task_id'))

class TaskDelete(DeleteView):
    model = Task
    success_url = '/matrix/matrix.html'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        objects_topic = Topic.objects.get(pk=self.object.topic)
        if objects_topic.topic_owner == request.user:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        else:
            messages.info(request, 'Permission denied!')

    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs.get('task_id'))

class TopicUpdate(UpdateView):
    model = Topic
    fields = ['topic_name', 'topic_description', 'color']
    template_name = 'matrix/topicediting.html'
    def get_object(self):
        return get_object_or_404(Topic, pk=self.kwargs.get('topic_id'))

class TopicDelete(DeleteView):
    model = Topic
    success_url = '/matrix/'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.topic_owner == request.user:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        else:
            messages.info(request, 'Permission denied!')
            return HttpResponseRedirect('/matrix/')

    # delete cascade in models.py
    def post(self, request, *args, **kwargs):
        messages.info(request, 'Topic "%s" successfully deleted.' % self.get_object())
        return self.delete(request, *args, **kwargs)

    # TODO cancel button
    def get_object(self):
        return get_object_or_404(Topic, pk=self.kwargs.get('topic_id'))
