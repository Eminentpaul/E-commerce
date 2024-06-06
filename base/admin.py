from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class UsersAdmin(UserAdmin):
    list_display = ['first_name', 'last_name',
                    'username', 'email',  'phone_number', 'image']
    list_display_links = ['username', 'first_name', 'last_name', 'email']
    filter_horizontal = ()
    fieldsets = ()

admin.site.register(User, UsersAdmin)