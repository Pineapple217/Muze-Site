from django.contrib import admin

# Register your models here.

from .models import Lid

class LidAdmin(admin.ModelAdmin):
    list_display = ("__str__", "is_accepted")
    list_filter = ("is_accepted", )

admin.site.register(Lid, LidAdmin)
