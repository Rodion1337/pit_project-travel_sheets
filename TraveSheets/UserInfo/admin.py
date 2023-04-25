from django.contrib import admin
from .models import *

# Register your models here.

class UserDopInfoAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserDopInfo, UserDopInfoAdmin)