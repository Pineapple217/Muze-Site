from django.forms import ModelForm
from django.utils.translation import gettext as _

from .models import Template
class TemplateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix

    class Meta:
        model = Template
        fields = '__all__'
        labels = {
            'name': _('Name'),
            'template': _('Template'),
        }
        help_texts = {
            'template': '''{
                            "schedule": [
                                {
                                "day": 0,
                                "start": "00:00",
                                "end": "00:00",
                                "max": 0
                                }
                            ]
                            }'''
        }
    

# class EditTemplate(ModelForm):