from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model in the admin
    list_display = ('email', 'first_name', 'last_name', 'matric_number', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    # The fieldsets control the layout when editing a user in admin
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'matric_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    # Used when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'matric_number', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'first_name', 'last_name', 'matric_number')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')


# Register the custom user model with the custom admin
admin.site.register(User, UserAdmin)
