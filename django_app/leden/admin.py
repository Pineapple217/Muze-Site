from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe

import simple_history

# Register your models here.

from .models import Lid


class ProductImagesInline(admin.TabularInline):
    model = Lid


class LidAdmin(simple_history.admin.SimpleHistoryAdmin):
    list_display = ("__str__", "user_name", "is_accepted")
    list_filter = ("is_accepted",)
    
    def user_name(self, lid):
        url=reverse("admin:auth_user_change", args=[lid.user.id])
        # url = f"../../auth/user/{lid.user.id}"
        link = '<a href="%s">%s</a>' % (url, lid.user)
        return mark_safe(link)


admin.site.register(Lid, LidAdmin)


# class UserAdminCustom(UserAdmin):
class UserAdminCustom(simple_history.admin.SimpleHistoryAdmin, UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("is_staff", "is_superuser")
    search_fields = ("username",)


admin.site.unregister(User)
admin.site.register(User, UserAdminCustom)
