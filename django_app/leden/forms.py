from django import forms
from .models import Lid
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ClearableFileInput, ModelForm
from django.forms.widgets import DateInput 
from django.utils.translation import gettext as _
import datetime
# from django.contrib.auth.password_validation import password_validators_help_text_html
class UserSignUpForm(UserCreationForm):
    # password1 = forms.CharField(
    #     label='',
    #     strip=False,
    #     widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': _('Password')}),
    #     help_text=password_validators_help_text_html(),
    # )
    # password2 = forms.CharField(
    #     label='',
    #     widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': _('Confirmation password')}),
    #     strip=False,
    #     help_text=_('Enter the same password as before, for verification.'),
    # )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

        # self.fields['username'].widget.attrs['placeholder'] = _('Username')
        # self.fields['first_name'].widget.attrs['placeholder'] = _('First name')
        # self.fields['last_name'].widget.attrs['placeholder'] = _('Last name')
        self.fields['email'].widget.attrs['pattern'] = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"

        # for field in self.fields:
        #     self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 
                  'email', 'password1', 'password2',)
        # labels = {
        #    'username': '',
        #    'first_name': '',
        #    'last_name': '',
        #    'email': '',
        # }

        
        

class LidSignUpForm(ModelForm):
    tel = forms.RegexField(regex=r'^\+[0-9]{2,3}\ [0-9]{3}(\ [0-9]{2}){3}$',
                           label= _('Phone number'),
                                                #    label= '',
                           help_text= _('Format example +32 989 91 23 12.'))

    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix

        self.fields['tel'].widget.attrs['pattern'] = r"[+][0-9]{2,3}[ ][0-9]{3}([ ][0-9]{2}){3}"
        # self.fields['date_of_birth'].widget.attrs['placeholder'] = _('Date of birth')
        # self.fields['gender'].widget.attrs['placeholder'] = _('Gender')
        # self.fields['street'].widget.attrs['placeholder'] = _('Street')
        # self.fields['house_number'].widget.attrs['placeholder'] = _('House number')
        # self.fields['zipcode'].widget.attrs['placeholder'] = _('Zipcode')
        # self.fields['residence'].widget.attrs['placeholder'] = _('Residence')
        # self.fields['discord_id'].widget.attrs['placeholder'] = _('Discord id')
        # self.fields['media'].widget.attrs['placeholder'] = _('Social media')

        # for field in self.fields:
        #     self.fields[field].widget.attrs['class'] = 'form-control'

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
            'residence': _('Residence'),
            'discord_id': _('Discord id'),
            'media': _('Social media'),
        }
        # labels = {
        #     'date_of_birth': "",
        #     'gender': "",
        #     'street': "",
        #     'house_number': "",
        #     'zipcode': "",
        #     'residence': "",
        #     'discord_id': "",
        #     'media': "",
        # }
    
    def clean_date_of_birth(self, *args, **kwargs):
        MIN_AGE = 15
        today = datetime.date.today()
        dob = self.cleaned_data.get("date_of_birth")
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < MIN_AGE: 
            raise forms.ValidationError(f"Je moet minstens {MIN_AGE} jaar oud zijn.")
        return dob
    

class UserUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 
                  'email')

class LidUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix
    class Meta:
        model = Lid
        fields = ('profile_picture', 'tel', 'gender', 'street',
                  'house_number', 'zipcode', 'residence', 'discord_id', 'media',)
        labels = {
            'profile_picture': _('Profile picture'),
            # 'date_of_birth': _('Date of birth'),
            'gender': _('Gender'),
            'street': _('Street'),
            'house_number': _('House nummer'),
            'zipcode': _('Zipcode'),
            'residence': _('Residence'),
            'discord_id': _('Discord id'),
            'media': _('Social media'),
        }

        widgets = {
                # 'date_of_birth': DateInput(attrs={'type': 'date'},
                #                            format=('%Y-%m-%d')),
                'profile_picture': ClearableFileInput(attrs={'class': 'photo-upload'})
        }

        help_texts = {
            'profile_picture': _('image size must be under 2MB.'),
        }
    def clean_date_of_birth(self, *args, **kwargs):
        MIN_AGE = 15
        today = datetime.date.today()
        dob = self.cleaned_data.get("date_of_birth")
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < MIN_AGE: 
            raise forms.ValidationError(f"Je moet minstens {MIN_AGE} jaar oud zijn.")
        return dob
    
        