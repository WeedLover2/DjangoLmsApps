from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Course, PDFModule

class UserAdmin(BaseUserAdmin):
    # Display in list view
    list_display = ('email', 'full_name', 'nim', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'nim', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'nim', 'role', 'password1', 'password2'),
        }),
    )
    
    search_fields = ('email', 'full_name', 'nim')
    ordering = ('email',)

# Use UserAdmin for User model
admin.site.register(User, UserAdmin)
admin.site.register(Course)
admin.site.register(PDFModule)