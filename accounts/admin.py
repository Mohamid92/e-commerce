from django.contrib import admin
from .models import Account
# Register your models here.
from django.contrib.auth.admin import UserAdmin

class AccountAdmin(UserAdmin):
    list_display = ('phone_number','username','email','last_login','date_joined')
    ordering = ('-date_joined',)
    list_filter = ()
    fieldsets = ()
    filter_horizontal = ()
    
admin.site.register(Account, AccountAdmin)