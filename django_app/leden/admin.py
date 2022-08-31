from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

import simple_history
# Register your models here.

from .models import Lid

class LidAdmin(simple_history.admin.SimpleHistoryAdmin):
    list_display = ("__str__", "user", "is_accepted")
    list_filter = ("is_accepted", )

admin.site.register(Lid, LidAdmin)


# class UserAdminCustom(UserAdmin):
class UserAdminCustom(simple_history.admin.SimpleHistoryAdmin, UserAdmin):
   list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
   list_filter = ('is_staff', 'is_superuser')
   search_fields = ('username', )

admin.site.unregister(User)
admin.site.register(User, UserAdminCustom)