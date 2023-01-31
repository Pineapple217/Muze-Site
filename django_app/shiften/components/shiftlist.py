from django.shortcuts import get_object_or_404
from django_unicorn.components import UnicornView
from django.forms import ValidationError
from shiften.models import Shift, Shiftlijst
from django import forms
import datetime


# validitie kan beter in theorie maar kan niet door beperking in unicorn
# https://github.com/adamghill/django-unicorn/issues/220
# class ShifterlistForm(forms.ModelForm):
#     class Meta:
#         model = Shiftlijst
#         fields = ('name', 'date', 'type', 'is_active')


class ShiftlistView(UnicornView):
    # form_class = ShifterlistForm
    list_id = None
    shiftlist: Shiftlijst = None
    shifts = Shift.objects.none()

    def mount(self):
        self.list_id = self.kwargs['list_id']
        self.load_shiftlist()
        self.load_shifts()

    def load_shiftlist(self):
        # neemt list id uit de url
        self.shiftlist = get_object_or_404(Shiftlijst, id  = self.list_id)
        self.call("disableName")

    def load_shifts(self):
        self.shifts = self.shiftlist.shift_set.all().order_by('date', 'start')
    
    def save(self):
        if not self.request.user.has_perm("shiften.edit_shiftlijst"):
            return
        try:
            self.shiftlist.save()
            self.call("toggleModalById", "edit-shiftlist")
        except:
            self.load_shiftlist()
            # raise ValidationError({"shiftlist": "Validation error"}, code="required")
            
