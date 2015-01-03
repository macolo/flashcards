from django.contrib import admin
from usermgmt.models import UserValidationCode
# Register your models here.

# Manage cards
class UserValidationCodeAdmin(admin.ModelAdmin):
    list_display = ('get_user_name', 'get_user_email', 'hash')

admin.site.register(UserValidationCode, UserValidationCodeAdmin)