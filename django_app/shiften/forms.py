from django.forms import ModelForm
from django.utils.translation import gettext as _

from .models import Template
class TemplateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix

    class Meta:
        model = Template
        # fields = '__all__'
        fields = ('name', 'template')
        # labels = {
        #     'name': _('Name'),
        #     'template': _('Template'),
        # }
#         help_text = {
#             'template': '''{
#   "schedule": [
#     {
#       "day": 5,
#       "start": "15:30",
#       "end": "19:00",
#       "max": 3
#     }
#   ]
# }'''
#         }
    

# class EditTemplate(ModelForm):