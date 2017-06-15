"""Define Fields for Admin Tool."""

from django.contrib import admin

from .models import Topic, Task


class TaskInline(admin.TabularInline):
    """Admin-Tool for tasks."""

    # TODO verfeinern
    model = Task
    # 2 is default for extra
    extra = 2

    def get_extra(self, request, obj=None, **kwargs):
        """If there is only one or more than 2, get the number of Inlines."""
        if obj:
            return 0
        return self.extra


class TopicAdmin(admin.ModelAdmin):
    """Admin-Tool for Topics."""

    # TODO verfeinern
    fieldsets = [
        (None, {'fields': ['topic_name']}),
        ('Information', {'fields': ['topic_description']}),
    ]
    inlines = [TaskInline]


admin.site.register(Topic, TopicAdmin)
admin.site.register(Task)
