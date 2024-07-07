
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


class AdminUser(UserAdmin):
    model = User

    list_display = ('firstName', 'lastName', 'email')

    list_filter = ('is_staff', 'is_superuser', 'is_active')

    search_fields = ('firstName', 'lastName', 'email')

    ordering = ('email',)


admin.site.register(User, AdminUser)
