from csv import list_dialects
from django.contrib import admin

# Register your models here.
from .models import Onbeschikbaar, OnbeschikbaarHerhalend, Shift, Shiftlijst, Template

class ShiftAdmin(admin.ModelAdmin):
    list_display =  ("__str__", "shift_list")
    list_filter = ("shift_list",)

admin.site.register(Shift, ShiftAdmin)

class ShiftlijdtAdmin(admin.ModelAdmin):
    list_display = ("__str__", "date", "type", "is_active")
    list_filter = ("is_active", )

admin.site.register(Shiftlijst, ShiftlijdtAdmin)
admin.site.register(Template)
admin.site.register(Onbeschikbaar)
admin.site.register(OnbeschikbaarHerhalend)