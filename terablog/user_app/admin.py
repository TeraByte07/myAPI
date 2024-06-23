# admin.py
from django.contrib import admin
from .models import CustomUser

@admin.action(description='Approve selected users as authors')
def make_author(modeladmin, request, queryset):
    queryset.update(is_author=True, is_author_requested=False)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'is_author', 'is_author_requested']
    actions = [make_author]

admin.site.register(CustomUser, CustomUserAdmin)
