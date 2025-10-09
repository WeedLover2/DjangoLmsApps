
from django.contrib import admin
from django.urls import path
from main.views import StudentLogin, home, landingpage, register, logout_view, course_detail, teacherlogin, download_pdf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('studentlogin/', StudentLogin, name='student_login'),
    path('teacherlogin/', teacherlogin, name='teacher_login'),
    path('home/', home, name='home'),
    path('', landingpage, name='landingpage'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),  
    path('course/<int:course_id>/', course_detail, name='course_detail'),  
    path('pdf/download/<int:pdf_id>/', download_pdf, name='download_pdf'),  # ← Add this
]
