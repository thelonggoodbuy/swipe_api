from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "is_superuser", "is_staff")
    list_filter = ("is_superuser",)

