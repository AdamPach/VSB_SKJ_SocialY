from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ApplicationUser, Follow


# Register your models here.

class ApplicationUserAdmin(UserAdmin):
    model = ApplicationUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_description', 'quote',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_description', 'quote',)}),
    )


admin.site.register(ApplicationUser, ApplicationUserAdmin)
admin.site.register(Follow)
