from __future__ import absolute_import

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
from .views import TopicCreate, TaskCreate, TaskUpdate, AjaxTaskDelete
from .views import TopicUpdate, TaskDelete, TopicDelete

# TODO unneccessary pages entfernen
urlpatterns = [
    # /matrix/
    url(r'^$', views.matrix, name='matrix'),
    # /matrix/addtopic
    url(r'^addtopic/$',
            login_required(TopicCreate.as_view()),
            name='addtopic'),
    # /matrix/5/
    url(r'^(?P<topic_id>[0-9]+)/$', views.topics, name='topics'),
    # /matrix/5/tasks
    url(r'^(?P<task_id>[0-9]+)/tasks/$', views.tasks, name='tasks'),
    # /matrix/5/adding
    url(r'^adding/$',
            login_required(TaskCreate.as_view()),
            name='adding'),
    # /matrix/5/edittopic
    url(r'^(?P<topic_id>[0-9]+)/edittopic/$',
            login_required(TopicUpdate.as_view()),
            name='topicediting'),
    # /matrix/5/deletetopic
    url(r'^(?P<topic_id>[0-9]+)/deletetopic/$',
            login_required(TopicDelete.as_view()),
            name='topicdeleting'),
    # /matrix/5/taskediting
    url(r'^(?P<task_id>[0-9]+)/taskediting/$',
            login_required(TaskUpdate.as_view()),
            name='taskediting'),
    # /matrix/5/taskdeleting
    url(r'^(?P<task_id>[0-9]+)/taskdeleting/$',
            login_required(TaskDelete.as_view()),
            name='taskdeleting'),
    # /matrix/done_tasks
    url(r'^done_tasks/$', views.done_tasks, name='done_tasks'),
    # ajax-urls
    # /matrix/5/taskdelete
    url(r'^(?P<task_id>[0-9]+)/taskdelete/$',
            login_required(AjaxTaskDelete.as_view()),
            name='taskdelete'),
]
