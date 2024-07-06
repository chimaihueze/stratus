
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


class AdminUser(UserAdmin):
    model = User

    list_display = ('first_name', 'last_name', 'email', 'is_staff')

    list_filter = ('is_staff', 'is_superuser', 'is_active')

    search_fields = ('first_name', 'last_name', 'email')

    ordering = ('email',)


admin.site.register(User, AdminUser)
