from django import forms
from .models import Lid
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.widgets import DateInput 
from django.utils.translation import gettext as _
class UserSignUpForm(UserCreationForm):
    # first_name = forms.CharField()
    # first_name.label = 'Voornaam'

    # last_name = forms.CharField()
    # last_name.label = 'Achternaam'

    # email = forms.EmailField()
    # email.label = 'E-mailadres'

    # tel = forms.RegexField(regex=r'^\+?1?\d{9,15}$')
    # tel.label = 'Telefoonnummer'

    # date_of_birth = forms.DateField()
    # date_of_birth.label = 'Geboortedatum'

    # gender = forms.ChoiceField()
    # gender.label = 'Gender'
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 
                  'email', 'password1', 'password2',)

    # def save(self, commit=True):
    #     user = super(UserSignUpForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #     return User

class LidSignUpForm(ModelForm):
    tel = forms.RegexField(regex=r'^\+[0-9]{2,3}\ [0-9]{3}(\ [0-9]{2}){3}$',
                           label= _('Phone number'),
                           help_text= _('Format example +32 989 91 23 12.'))

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
