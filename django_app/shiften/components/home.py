import datetime
from django_unicorn.components import UnicornView, QuerySetType
from shiften.models import Shiftlijst
from django import forms

from django.utils.timezone import now

class ShifterlistForm(forms.ModelForm):
    class Meta:
        model = Shiftlijst
        fields = ('name', 'date', 'type')

    date = forms.DateField(required=True)

class HomeView(UnicornView):
    form_class = ShifterlistForm
    shiftlists: QuerySetType[Shiftlijst] = None
    name: str = ''
    date = ''
    type: str = ''

    def mount(self):
        if self.request.user.has_perm('shiften.change_shiftlijst'):
            self.shiftlists = Shiftlijst.objects.all()
        else:
            self.shiftlists = Shiftlijst.objects.filter(is_active=True)

    def add(self):
        if not self.request.user.has_perm("shiften.change_shiftlijst"):
            return
        if not self.is_valid():
            self.name = ''
            return
        if type == 'month':
            date = datetime.date(date.year, date.month, 1)
        new_shiftlist = Shiftlijst.objects.create(
                                            date = self.date,
                                            type = self.type,
                                            name = self.name)
        self.name = ''
        self.date = ''
        self.type = ''
        self.shiftlists |= Shiftlijst.objects.filter(pk = new_shiftlist.id)
        self.call("toggleModalById", "add-shiftlist-normal")

    def add_template(self):

        new_shiftlist = create_month_shiftlist(template, shiftlist_date)
        self.shiftlists |= Shiftlijst.objects.filter(pk = new_shiftlist.id)
        self.call("toggleModalById", "add-shiftlist-template")