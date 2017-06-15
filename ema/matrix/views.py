"""Connect parts, called by urls.py."""
import json
from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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


@login_required()
def matrix(request):
    """
    To display taks and topics.

    provides:
        - all topics in django and in JSON
        - all tasks in django and in JSON
        - settings of current user
    """
    # alle Topics
    all_topics = Topic.objects.filter(topic_owner=request.user.id)
    to_data = {}
    # alle Topics als JSON
    data = [model_to_dict(instance) for instance in all_topics]
    to_data['topics'] = data
    topic_data = json.dumps(to_data, cls=DjangoJSONEncoder)
    # alle Aufgaben
    all_tasks = Task.objects.filter(
        topic__topic_owner=request.user.id,
        done=False
    )
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
        settings_file.save()
    return render(
        request,
        'matrix/matrix.html',
        {'all_topics': all_topics, 'end_data': end_data,
            'topic_data': topic_data, 'task_form': task_form,
            'settings_file': settings_file}
    )


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.

    Must be used with an object-based FormView (e.g. CreateView)
    @source: django docs
    https://docs.djangoproject.com/en/1.8/topics/class-based-views/generic-editing/
    """

    def form_invalid(self, form):
        """Response bei Fehler."""
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        # Fehler uebergeben, korrekter Statuscode fuer die Behandlung mit AJAX
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        """Response bei gueltigen Daten."""
        response = super(AjaxableResponseMixin, self).form_valid(form)
        # bei AJAX werden nur nur ein JSON-Objekt der Aufgaben uebergeben
        if self.request.is_ajax():
            topic = form.instance.topic_id
            all_tasks = Task.objects.filter(
                topic__topic_owner=self.request.user.id,
                done=False)
            response_data = json.dumps(
                [model_to_dict(instance) for instance in all_tasks],
                cls=DjangoJSONEncoder)
            return HttpResponse(response_data, content_type="application/json")
        else:
            return response


class PermissionDeniedMixin(object):
    """Verhindert den Zugriff auf Objekte, die nicht dem User gehoeren."""

    def users_object_test(self, request):
        """Testen, ob das Objekt dem User gehoert."""
        self.object = self.get_object()
        if isinstance(self.object, Topic):
            return self.object.topic_owner == request.user
        if isinstance(self.object, Task):
            return self.object.topic.topic_owner == request.user

    def dispatch(self, request, *args, **kwargs):
        """Weiterleiten oder Abblocken."""
        if not self.users_object_test(request):
            messages.info(request, "Permission Denied!")
            return redirect_to_login(request.get_full_path())
        return super(PermissionDeniedMixin, self).dispatch(
            request, *args, **kwargs)


class AjaxSuccessMessageMixin(SuccessMessageMixin):
    """Override django SuccessMessageMixin fuer AJAX Requests."""

    def get_success_message(self, cleaned_data):
        """Verhindern der success message bei AJAX-Requests."""
        if self.request.is_ajax():
            return None
        else:
            return self.success_message % cleaned_data


class TaskCreate(
        AjaxableResponseMixin,
        AjaxSuccessMessageMixin,
        CreateView):
    """
    Erstellt eine Aufgabe.

    mit AJAX verwendbar
    ruft die TaskForm mit dem zusaetzlichen Parameter user auf
    """

    model = Task
    form_class = TaskForm
    # template_name = 'matrix/adding.html'
    success_message = "Task '%(task_name)s' was successfully created!"
    success_url = '/matrix/'

    def get_form_kwargs(self):
        """Add user to form kwargs."""
        kwargs = super(TaskCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TaskUpdate(
        AjaxableResponseMixin,
        AjaxSuccessMessageMixin,
        PermissionDeniedMixin,
        UpdateView):
    """
    Bearbeitet Aufgabe.

    mit AJAX oder mit normalem Request verwendbar
    ruft die TaskForm mit dem zusaetzlichen Parameter user auf
    """

    model = Task
    form_class = TaskForm
    template_name = 'matrix/taskediting.html'
    success_message = "Task '%(task_name)s' was successfully modified!"
    success_url = '/matrix/'

    def get_object(self):
        """Richtige Aufgabe abrufen."""
        return get_object_or_404(Task, pk=self.kwargs.get('task_id'))

    def get_form_kwargs(self):
        """User zu den Form Kwargs hinzufuegen."""
        kwargs = super(TaskUpdate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TaskDelete(SuccessMessageMixin, PermissionDeniedMixin, DeleteView):
    """
    Loescht eine Aufgabe.

    nur fuer normale Requests
    """

    model = Task
    success_message = "Task '%(task_name)s' was successfully deleted!"
    success_url = '/matrix/'

    def get_object(self):
        """Richtige Aufgabe abrufen."""
        return get_object_or_404(Task, pk=self.kwargs.get('task_id'))


class AjaxTaskDelete(PermissionDeniedMixin, SingleObjectMixin, View):
    """
    Loescht eine Aufgabe.

    nur fuer AJAX-Requests
    """

    model = Task

    def get_object(self):
        """Richtige Aufgabe abrufen."""
        return Task.objects.get(pk=self.kwargs.get('task_id'))
        # TODO do i really have to check this?

    def post(self, *args, **kwargs):
        """Override post to delete right task with AJAX."""
        self.object = self.get_object()
        self.object.delete()
        all_tasks = Task.objects.filter(
            topic__topic_owner=self.request.user.id,
            done=False)
        response_data = json.dumps(
            [model_to_dict(instance) for instance in all_tasks],
            cls=DjangoJSONEncoder)
        return HttpResponse(response_data, content_type="application/json")


class TopicCreate(SuccessMessageMixin, CreateView):
    """
    Erstellt ein Thema.

    nicht fuer AJAX-Requests
    ruft das TopicForm mit dem zusaetzlichen Parameter user auf
    """

    model = Topic
    form_class = TopicForm
    template_name = 'matrix/addtopic.html'
    success_message = "Topic '%(topic_name)s' was successfully created!"
    success_url = '/matrix/'

    def get_form_kwargs(self):
        """Add User to form kwargs."""
        kwargs = super(TopicCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TopicUpdate(SuccessMessageMixin, PermissionDeniedMixin, UpdateView):
    """
    Bearbeitet ein Thema.

    nicht fuer AJAX-Requests
    ruft das TopicForm mit dem zusaetzlichen Parameter user auf
    """

    model = Topic
    form_class = TopicForm
    template_name = 'matrix/topicediting.html'
    success_message = "Topic '%(topic_name)s' was successfully edited!"
    success_url = '/matrix/'

    def get_form_kwargs(self):
        """Add User to form kwargs."""
        kwargs = super(TopicUpdate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self):
        """Richtige Topic abrufen."""
        return get_object_or_404(Topic, pk=self.kwargs.get('topic_id'))


class TopicDelete(PermissionDeniedMixin, DeleteView):
    """
    Loescht ein Thema.

    nicht fuer AJAX-Requests
    """

    model = Topic
    success_url = '/matrix/'

    def post(self, request, *args, **kwargs):
        """Delete cascade in models.py."""
        messages.info(
            request,
            'Topic "%s" successfully deleted.' % self.get_object())
        return self.delete(request, *args, **kwargs)

    def get_object(self):
        """Richtiges Topic abrufen."""
        return get_object_or_404(Topic, pk=self.kwargs.get('topic_id'))


@login_required()
def topics(request, topic_id):
    """
    To show the requested topic.

    @params: topic_id
    Permission denied message if unsuccessful
    """
    topic = get_object_or_404(Topic, pk=topic_id)
    if topic.topic_owner == request.user:
        return render(request, 'matrix/topic.html', {'topic': topic})
    else:
        messages.info(request, 'Permission denied!')
        return HttpResponseRedirect('/matrix/')


@login_required()
def tasks(request, task_id):
    """
    To show the requested task details.

    @params: task_id
    Permission denied message if unsuccessful
    """
    task = get_object_or_404(Task, pk=task_id)
    if task.topic.topic_owner == request.user:
        return render(request, 'matrix/task.html', {'task': task})
    else:
        messages.info(request, 'Permission denied!')
        return HttpResponseRedirect('/matrix/')


@login_required()
def done_tasks(request):
    """
    To show all tasks that have been marked done.

    since they won't show up in the matrix anymore
    click on one to edit it
    """
    dones = Task.objects.filter(topic__topic_owner=request.user.id, done=True)
    return render(request, 'matrix/done_tasks.html', {'dones': dones})
