import json
from django.shortcuts import get_object_or_404, render, render_to_response
from django.views.generic import View
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.views import redirect_to_login

from orga.models import UserOrga

from .models import Topic, Task
from .forms import TaskForm, TopicForm
from .utils import get_user_colors

# TODO was wird noch gebraucht was nicht?
"""
main view with matrix
provides:
    - all topics in django and in JSON
    - all tasks in django and in JSON
    - settings of current user
"""
@login_required()
def matrix(request):
    # alle Topics
    all_topics = Topic.objects.filter(topic_owner=request.user.id)
    to_data = {}
    # alle Topics als JSON
    data = [model_to_dict(instance) for instance in all_topics]
    to_data['topics'] = data
    topic_data = json.dumps(to_data, cls=DjangoJSONEncoder)
    # alle Aufgaben
    all_tasks = Task.objects.filter(topic__topic_owner=request.user.id, done=False)
    # alle Aufgaben als JSON
    data = [model_to_dict(instance) for instance in all_tasks]
    end_data = json.dumps(data, cls=DjangoJSONEncoder)
    # Forms
    task_form = TaskForm(user=request.user)
    # Settings
    try:
        settings_file = UserOrga.objects.get(owner=request.user)
    except UserOrga.DoesNotExist:
        settings_file = UserOrga.objects.create(owner=request.user)
        user_settings.save()
    return render(request, 'matrix/matrix.html',
                    {'all_topics': all_topics, 'end_data': end_data,
                    'topic_data': topic_data, 'task_form': task_form,
                    'settings_file': settings_file  })

# source: django docs:
#https://docs.djangoproject.com/en/1.8/topics/class-based-views/generic-editing/
class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        # Fehler uebergeben und korrekten Statuscode fuer die Behandlung mit AJAX
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        # bei AJAX werden nur nur ein JSON-Objekt der Aufgaben uebergeben
        if self.request.is_ajax():
            topic = form.instance.topic_id
            all_tasks = Task.objects.filter(topic__topic_owner=self.request.user.id, done=False)
            response_data = json.dumps([model_to_dict(instance) for instance in all_tasks], cls=DjangoJSONEncoder)
            return HttpResponse(response_data, content_type="application/json")
        else:
            return response

"""
verhindert den Zugriff auf Objekte, die nicht dem aufrufenden User gehoeren
"""
class PermissionDeniedMixin(object):
    def users_object_test(self, request):
        self.object = self.get_object()
        if isinstance(self.object, Topic):
            return self.object.topic_owner == request.user
        if isinstance(self.object, Task):
            return self.object.topic.topic_owner == request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.users_object_test(request):
            messages.info(request, "Permission Denied!")
            return redirect_to_login(request.get_full_path())
        return super(PermissionDeniedMixin, self).dispatch(
            request, *args, **kwargs)

"""
Abaenderung des django SuccessMessageMixin fuer AJAX Requests
"""
class AjaxSuccessMessageMixin(SuccessMessageMixin):
    def get_success_message(self, cleaned_data):
        if self.request.is_ajax():
            return None
        else:
            return self.success_message % cleaned_data

"""
erstellt eine Aufgabe
mit AJAX verwendbar
ruft die TaskForm mit dem zusaetzlichen Parameter user auf
"""
class TaskCreate(
        AjaxableResponseMixin,
        AjaxSuccessMessageMixin,
        CreateView):
    model = Task
    form_class = TaskForm
    # template_name = 'matrix/adding.html'
    success_message = "Task '%(task_name)s' was successfully created!"
    success_url = '/matrix/'

    def get_form_kwargs(self):
        kwargs = super(TaskCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

"""
bearbeitet Aufgabe
mit AJAX oder mit normalem Request verwendbar
ruft die TaskForm mit dem zusaetzlichen Parameter user auf
"""
class TaskUpdate(
        AjaxableResponseMixin,
        AjaxSuccessMessageMixin,
        PermissionDeniedMixin,
        UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'matrix/taskediting.html'
    success_message = "Task '%(task_name)s' was successfully modified!"
    success_url = '/matrix/'

    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs.get('task_id'))

    def get_form_kwargs(self):
        kwargs = super(TaskUpdate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

"""
loescht eine Aufgabe
nur fuer normale Requests
"""
class TaskDelete(SuccessMessageMixin, PermissionDeniedMixin, DeleteView):
    model = Task
    success_message = "Task '%(task_name)s' was successfully deleted!"
    success_url = '/matrix/'

    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs.get('task_id'))

"""
loescht eine Aufgabe
nur fuer AJAX-Requests
"""
class AjaxTaskDelete(PermissionDeniedMixin, SingleObjectMixin, View):
    model = Task

    def get_object(self):
        return Task.objects.get(pk=self.kwargs.get('task_id'))
        # do i really have to check this?

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        all_tasks = Task.objects.filter(topic__topic_owner=self.request.user.id, done=False)
        response_data = json.dumps([model_to_dict(instance) for instance in all_tasks], cls=DjangoJSONEncoder)
        return HttpResponse(response_data, content_type="application/json")

"""
erstellt ein Thema
nicht fuer AJAX-Requests
ruft das TopicForm mit dem zusaetzlichen Parameter user auf
"""
class TopicCreate(SuccessMessageMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'matrix/addtopic.html'
    success_message = "Topic '%(topic_name)s' was successfully created!"
    success_url = '/matrix/'

    def get_form_kwargs(self):
        kwargs = super(TopicCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

"""
bearbeitet ein Thema
nicht fuer AJAX-Requests
ruft das TopicForm mit dem zusaetzlichen Parameter user auf
"""
class TopicUpdate(SuccessMessageMixin, PermissionDeniedMixin, UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = 'matrix/topicediting.html'
    success_message = "Topic '%(topic_name)s' was successfully edited!"
    success_url = '/matrix/'

    def get_form_kwargs(self):
        kwargs = super(TopicUpdate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self):
        return get_object_or_404(Topic, pk=self.kwargs.get('topic_id'))

"""
loescht ein Thema
nicht fuer AJAX-Requests

"""
class TopicDelete(PermissionDeniedMixin, DeleteView):
    model = Topic
    success_url = '/matrix/'

    # delete cascade in models.py
    def post(self, request, *args, **kwargs):
        messages.info(request, 'Topic "%s" successfully deleted.' % self.get_object())
        return self.delete(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(Topic, pk=self.kwargs.get('topic_id'))

"""
shows the requested topic
@params: topic_id
Permission denied message if unsuccessful
"""
@login_required()
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
@login_required()
def tasks(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.topic.topic_owner == request.user:
        return render(request, 'matrix/task.html', {'task': task})
    else:
        messages.info(request, 'Permission denied!')
        return HttpResponseRedirect('/matrix/')

"""
shows all tasks that have been marked done, since they won't show up in the
matrix anymore
click on one to edit it
"""
@login_required()
def done_tasks(request):
    dones = Task.objects.filter(topic__topic_owner=request.user.id, done=True)
    return render(request, 'matrix/done_tasks.html', {'dones': dones})
