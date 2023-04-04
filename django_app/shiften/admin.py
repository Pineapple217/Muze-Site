from csv import list_dialects
from django.contrib import admin
import simple_history

# Register your models here.
from .models import Onbeschikbaar, OnbeschikbaarHerhalend, Shift, Shiftlijst, Template

class ShiftAdmin(simple_history.admin.SimpleHistoryAdmin):
    list_display =  ("__str__", "shift_list")
    history_list_display = ["shifter_count"]
    list_filter = ("shift_list",)

    def shifter_count(self, obj):
        return obj.shifters.count()

admin.site.register(Shift, ShiftAdmin)

class ShiftlijdtAdmin(simple_history.admin.SimpleHistoryAdmin):
    list_display = ("__str__", "date", "type", "is_active")
    list_filter = ("is_active", )

admin.site.register(Shiftlijst, ShiftlijdtAdmin)
admin.site.register(Template)
admin.site.register(Onbeschikbaar)
admin.site.register(OnbeschikbaarHerhalend)