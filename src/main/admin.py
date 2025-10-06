from django.contrib import admin

# Register your models here.
from .models import User, Course, PDFModule
admin.site.register(User)
admin.site.register(Course)
admin.site.register(PDFModule)
