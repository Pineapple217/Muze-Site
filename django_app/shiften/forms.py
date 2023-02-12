from django.forms import ModelForm, SelectDateWidget
from django.utils.translation import gettext as _
from django import forms
from .models import Onbeschikbaar, OnbeschikbaarHerhalend, Shiftlijst, Template

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
    

class AvailableForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix
        
        
    start = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'))
    end = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'))
    
    class Meta:
        model = Onbeschikbaar
        # fields = '__all__'
        exclude = ['lid']
        labels = {
           'start': _('Start'),
           'end': _('End'),
           'info': _('Info'),
        }

class AvailableRepForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix
    
    start_period = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'))
    end_period = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'))
    start = forms.TimeField(widget=forms.DateInput(attrs={'type': 'time'}, format='%H:%M'))
    end = forms.TimeField(widget=forms.DateInput(attrs={'type': 'time'}, format='%H:%M'))

    class Meta:
        model = OnbeschikbaarHerhalend
        # fields = '__all__'
        exclude = ['lid']
        labels = {
            'start_period': _('Start period'),
            'end_period': _('End period'),
            'weekday': _('weekday'),
            'start': _('Start'),
            'end': _('End'),
            'info': _('Info'),
        }

    def clean_weekday(self, *args, **kwargs):
        weekday = self.cleaned_data.get('weekday')
        if not 1 <= weekday <= 7:
            raise forms.ValidationError(_("weekday must be between 1 and 7"))
        return weekday

class ShiftlistCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date'})

    class Meta:
        model = Shiftlijst
        fields = ('name', 'date', 'type')

class ShiftlistCreateWithTemplateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix

        template_options = []
        for template in Template.objects.all():
            template_options.append((template.id, str(template)))

        self.fields['template'].choices = template_options

    template = forms.ChoiceField(required=True)
    date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

class ShiftlistEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        self.fields['is_active'].widget.attrs = {'role': 'switch'}

    class Meta:
        model = Shiftlijst
        fields = ('name', 'date', 'type', 'is_active')