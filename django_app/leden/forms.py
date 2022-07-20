from django import forms
from .models import Lid
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ClearableFileInput, ModelForm
from django.forms.widgets import DateInput 
from django.utils.translation import gettext as _
class UserSignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 
                  'email', 'password1', 'password2',)

class LidSignUpForm(ModelForm):
    tel = forms.RegexField(regex=r'^\+[0-9]{2,3}\ [0-9]{3}(\ [0-9]{2}){3}$',
                           label= _('Phone number'),
                           help_text= _('Format example +32 989 91 23 12.'))

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.label_suffix = ""  # Removes : as label suffix
    class Meta:
        model = Lid
        fields = ('tel', 'date_of_birth', 'gender', 'street',
                  'house_number', 'zipcode', 'residence', 'discord_id', 'media',)
        labels = {
            'date_of_birth': _('Date of birth'),
            'gender': _('Gender'),
            'street': _('Street'),
            'house_number': _('House nummer'),
            'zipcode': _('Zipcode'),
            'residence': _('Residenace'),
            'discord_id': _('Discord id'),
            'media': _('Social media'),
        }
        widgets = {
                'date_of_birth': DateInput(attrs={'type': 'date'})
            }

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 
                  'email')

class LidUpdateForm(ModelForm):
    class Meta:
        model = Lid
        fields = ('profile_picture', 'tel', 'date_of_birth', 'gender', 'street',
                  'house_number', 'zipcode', 'residence', 'discord_id', 'media',)
        labels = {
            'profile_picture': _('Profile picture'),
            'date_of_birth': _('Date of birth'),
            'gender': _('Gender'),
            'street': _('Street'),
            'house_number': _('House nummer'),
            'zipcode': _('Zipcode'),
            'residence': _('Residenace'),
            'discord_id': _('Discord id'),
            'media': _('Social media'),
        }

        widgets = {
                'date_of_birth': DateInput(attrs={'type': 'date'},
                                           format=('%Y-%m-%d')),
                'profile_picture': ClearableFileInput(attrs={'class': 'photo-upload'})
        }

        help_texts = {
            'profile_picture': _('image size must be under 2MB.'),
        }
    
        