from django.forms import ModelForm, SelectDateWidget
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _l
from django import forms

from leden.models import Lid
from .models import Onbeschikbaar, OnbeschikbaarHerhalend, Shift, Shiftlijst, Template
from django.contrib.auth.models import User

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

        for field_name in self.fields:
            field = self.fields.get(field_name)  
            if field:
                field.label = _l(field.label)

    class Meta:
        model = Shiftlijst
        fields = ('name', 'date', 'type')

class ShiftlistCreateWithTemplateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix

        # TODO doe dit met comprehention
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

class ShiftAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        self.fields['start'].widget = forms.DateInput(attrs={'type': 'time'}, format='%H:%M')
        self.fields['end'].widget=forms.DateInput(attrs={'type': 'time'}, format='%H:%M')

    class Meta:
        model = Shift
        fields = ('date', 'start', 'end', 'max_shifters', 'extra_info')

class ShiftEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        self.fields['start'].widget = forms.DateInput(attrs={'type': 'time'}, format='%H:%M')
        self.fields['end'].widget=forms.DateInput(attrs={'type': 'time'}, format='%H:%M')

    class Meta:
        model = Shift
        fields = ('date', 'start', 'end', 'max_shifters', 'extra_info')

# TODO werkt maar is nie super mooi doet wel wat het moet tho
class SelectAttr(forms.Select):
    def __init__(self, modify_classes=()):
        super(SelectAttr, self).__init__()
        # set data
        self.modify_classes = modify_classes
    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option = super().create_option(
            name, value, label, selected, index, subindex, attrs
        )
        option['attrs'].update({
            'class': self.modify_classes[index]
        })
        return option

class ShiftEditShiftersFrom(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix

        shift = self.instance

        options = []
        attr = []
        attr.append('')
        for lid in Lid.objects.all():
            # print(str(lid), lid.is_available(shift))
            if lid.is_available(shift):
                attr.append('')
            else:
                attr.append('grijs')
            s = str(lid)
            opt = (lid.id, s)
            options.append(opt)
        options.insert(0, ('None', ''))

        shifters = list(shift.shifters.all())
        shifters_len = len(shifters)
        for i in range(shift.max_shifters):
            field = self.fields[f'shifter-{i}'] = forms.ChoiceField(required=False,
                                                            choices = options,
                                                            label='',
                                                            widget=SelectAttr(modify_classes=attr))
                                                            # widget=forms.Select(attrs={'class': 'grijs'}))
            if i < shifters_len:
                field.initial = (shifters[i].id, str(shifters[i]))
    
    def clean(self):
        ids = set()
        for i in range(self.instance.max_shifters):
            id = self.cleaned_data[f'shifter-{i}']
            if id != "None" and id is not None:
                ids.add(id)
        self.cleaned_data['shifters_ids'] = ids
    
    def save(self):
        shift = self.instance
        shift.shifters.clear();
        for id in self.cleaned_data.get('shifters_ids'):
            shift.shifters.add(Lid.objects.get(id=id))
        shift.save()

    class Meta():
        model = Shift
        fields = []
