from django_unicorn.components import UnicornView
from shiften.models import Shiftlijst
from django import forms
import datetime

class ShifterlistForm(forms.ModelForm):
    class Meta:
        model = Shiftlijst
        fields = ('name', 'date', 'type')


class AddShiftlistNormalView(UnicornView):
    form_class = ShifterlistForm
    name: str = ''
    date = ''
    type: str = ''

    def add(self):
        if not self.request.user.has_perm("shiften.add_shiftlijst"):
            return
        if not self.is_valid():
            self.name = ''
            return
        if self.name == 'None':
            self.name == None
             
        new_shiftlist = Shiftlijst.objects.create(
                                            date = self.date,
                                            type = self.type,
                                            name = self.name)
        self.name = ''
        self.date = ''
        self.type = ''
        # self.parent.shiftlists |= Shiftlijst.objects.filter(pk = new_shiftlist.id)
        self.call("toggleModalById", "add-shiftlist-normal")
        