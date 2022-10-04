from django.contrib import admin
from .models import Bitcoin

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'time']


admin.site.register(Bitcoin, UserAdmin)
