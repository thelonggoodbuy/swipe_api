from django.contrib import admin

from .models import House



@admin.register(House)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "address")
    list_filter = ("id", "address")