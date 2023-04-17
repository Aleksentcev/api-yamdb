from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'role',
        'email',
        'first_name',
        'last_name',
        'bio',
    )


admin.site.register(User, UserAdmin)
