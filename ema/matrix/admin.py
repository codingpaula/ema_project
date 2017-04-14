from django.contrib import admin

from .models import Topic, Task

# Admin-Tool for tasks
# TODO verfeinern
class TaskInline(admin.TabularInline):
    model = Task
    # 2 is default for extra
    extra = 2

    # if there is only one or more than 2, get the number of Inlines
    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        return self.extra

# Admin-Tool for Topics
# TODO verfeinern
class TopicAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['topic_name']}),
        ('Information', {'fields': ['topic_description']}),
    ]
    inlines = [TaskInline]

admin.site.register(Topic, TopicAdmin)
admin.site.register(Task)
