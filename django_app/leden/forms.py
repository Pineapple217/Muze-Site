from django import forms
from .models import Lid
from constance import config
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ClearableFileInput, ModelForm
from django.forms.widgets import DateInput 
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _l
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

        for field_name in self.fields:
            field = self.fields.get(field_name)  
            if field:
                field.widget.attrs['placeholder'] =  field.label

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
                           label= _l('Phone number'),
                           help_text= _l('Format example +32 989 91 23 12.'))

    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),
                                    label=_l('Date of birth'))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix

        self.fields['tel'].widget.attrs['pattern'] = r"[+][0-9]{2,3}[ ][0-9]{3}([ ][0-9]{2}){3}"
        self.fields['media'].widget.attrs['role'] = 'switch'

        for field_name in self.fields:
            field = self.fields.get(field_name)  
            if field:
                field.widget.attrs['placeholder'] =  field.label
                # field.label = _l(field.label)

        # for field in self.fields:
        #     self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Lid
        fields = ('tel', 'date_of_birth', 'gender', 'street',
                  'house_number', 'zipcode', 'residence', 'discord_id', 'media',)
        labels = {
            'gender': _l('Gender'),
            'street': _l('Street'),
            'house_number': _l('House nummer'),
            'zipcode': _l('Zipcode'),
            'residence': _l('Residence'),
            'discord_id': _l('Discord id'),
            'media': _l('Social media'),
        }
    
    def clean_date_of_birth(self, *args, **kwargs):
        MIN_AGE = config.MIN_AGE
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
            'profile_picture': _l('Profile picture'),
            # 'date_of_birth': _l('Date of birth'),
            'gender': _l('Gender'),
            'street': _l('Street'),
            'house_number': _l('House nummer'),
            'zipcode': _l('Zipcode'),
            'residence': _l('Residence'),
            'discord_id': _l('Discord id'),
            'media': _l('Social media'),
        }

        widgets = {
                # 'date_of_birth': DateInput(attrs={'type': 'date'},
                #                            format=('%Y-%m-%d')),
                'profile_picture': ClearableFileInput(attrs={'class': 'photo-upload'})
        }

        help_texts = {
            'profile_picture': _l('Image size must be under %(max)s MB.') % {'max': config.PP_MAX_SIZE_MB},
        }
    def clean_date_of_birth(self, *args, **kwargs):
        MIN_AGE = config.MIN_AGE
        today = datetime.date.today()
        dob = self.cleaned_data.get("date_of_birth")
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < MIN_AGE: 
            raise forms.ValidationError(f"Je moet minstens {MIN_AGE} jaar oud zijn.")
        return dob
    
        