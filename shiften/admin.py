from django.contrib import admin

# Register your models here.
from .models import Shift, Shiftlijst

admin.site.register(Shift)
admin.site.register(Shiftlijst)