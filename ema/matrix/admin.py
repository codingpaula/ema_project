from django.contrib import admin

# Register your models here.
from .models import Topic, Task

class TaskInline(admin.TabularInline):
    model = Task
    # 2 is default for extra
    extra = 2

    # if there is only one or more than 2, get the number of Inlines
    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        return self.extra

class TopicAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['topic_name']}),
        ('Information', {'fields': ['topic_description']}),
    ]
    inlines = [TaskInline]

admin.site.register(Topic, TopicAdmin)
admin.site.register(Task)
