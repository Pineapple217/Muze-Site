from django.forms import ModelForm
from django.utils.translation import gettext as _

from shiften.models import Template
class TemplateForm(ModelForm):

    class Meta:
        model = Template
        fields = '__all__'
        labels = {
            'name': _('Name'),
            'template': _('Template'),
        }
    

# class EditTemplate(ModelForm):