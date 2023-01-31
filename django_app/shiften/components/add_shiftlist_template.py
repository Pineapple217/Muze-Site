from django_unicorn.components import UnicornView
from django import forms
from shiften.models import Shiftlijst
from shiften.functions import create_month_shiftlist

from shiften.models import Template

class ShiftlistTemplateForm(forms.Form):
    template_id = forms.DecimalField(required=True)
    date = forms.DateField(required=True)

class AddShiftlistTemplateView(UnicornView):
    form_class = ShiftlistTemplateForm
    templates = Template.objects.none()

    template_id = ''
    date = ''

    def mount(self):
        self.load_templates()

    def load_templates(self):
        self.templates = Template.objects.all()

    def add_template(self):
        if not self.request.user.has_perm("shiften.add_shiftlijst"):
            return
        if not self.is_valid():
            return
        template = Template.objects.get(id=self.template_id)
        new_shiftlist = create_month_shiftlist(template, self.date)
        # self.parent.shiftlists |= Shiftlijst.objects.filter(pk = new_shiftlist.id)
        self.call("toggleModalById", "add-shiftlist-template")
