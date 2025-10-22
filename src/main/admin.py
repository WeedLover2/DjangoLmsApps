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

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'get_student_count')
    list_filter = ('teacher',)
    search_fields = ('name', 'description', 'teacher__full_name')

    fieldsets = (
        ('Course Info', {
            'fields': ('name', 'description', 'teacher')
        }),
        ('Enrolled Students', {
            'fields': ('students',),
            'description': 'Select students to enroll in this course'
        }),
    )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "students":
            kwargs["queryset"] = User.objects.filter(role=User.Role.STUDENT)
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = User.objects.filter(role=User.Role.TEACHER)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_student_count(self, obj):
        return obj.students.count()
    get_student_count.short_description = 'Students Enrolled'

class PDFModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'uploaded_by')
    list_filter = ('course', 'uploaded_by')
    search_fields = ('title', 'description', 'course__name')
    
    fieldsets = (
        ('PDF Information', {
            'fields': ('title', 'description', 'file', 'course')
        }),
        ('Upload Info', {
            'fields': ('uploaded_by',)
        }),
    )
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "uploaded_by":
            kwargs["queryset"] = User.objects.filter(role=User.Role.TEACHER)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(PDFModule, PDFModuleAdmin)