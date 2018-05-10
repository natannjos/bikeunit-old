from django.contrib import admin
from .models import User
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .forms import UserAdminCreationForm, UserAdminForm

# Register your models here.

class UserAdmin( admin.ModelAdmin ):
    readonly_fields = ('last_login', 'password', 'token')
    search_fields = ('username', 'email')


admin.site.register(User, UserAdmin)
