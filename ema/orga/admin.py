"""Add models to Admin Tool."""
from django.contrib import admin

# Register your models here.
from .models import UserOrga


class SettingsAdmin(admin.ModelAdmin):
    """Orga Objekt hinzufuegen."""

    fieldsets = [
        ('User', {'fields': ['owner']}),
        ('Settings', {'fields': ['urgent_axis', 'default_topic']})
    ]


admin.site.register(UserOrga, SettingsAdmin)
