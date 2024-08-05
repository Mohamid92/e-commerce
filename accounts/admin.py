from django.contrib import admin
from .models import Account
# Register your models here.
from django.contrib.auth.admin import UserAdmin

class AccountAdmin(UserAdmin):
    list_display = ('phone_number','username','email','last_login','date_joined')
    ordering = ('-date_joined',)
    list_filter = ()
    fieldsets = ()
    add_fieldsets = (
        ('User Registeration', {
            'classes': ('wide',),
            'fields': ('phone_number', 'email', 'username', 'password1', 'password2')}
        ),
    )
    filter_horizontal = ()
    
admin.site.register(Account, AccountAdmin)