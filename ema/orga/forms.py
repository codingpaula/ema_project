from django.forms import ModelForm
from django import forms

from .models import UserOrga
from matrix.models import Topic

class OrgaForm(ModelForm):
    class Meta:
        model = UserOrga
        fields = ['urgent_axis', 'default_topic']
        widgets = {
            'default_topic': forms.Select(
                attrs = {'required': False}
            )
        }

    def __init__(self, user, *args, **kwargs):
        super(OrgaForm, self).__init__(*args, **kwargs)
        # get different list of choices here
        topics = Topic.objects.filter(topic_owner=user)
        self.fields['default_topic'].queryset = topics
        
