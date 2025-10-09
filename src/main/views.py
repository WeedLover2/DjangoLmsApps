from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import User, Course, PDFModule

# Login
def StudentLogin(request):
    if request.method == 'POST':
        nim = request.POST.get('nim')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=nim, password=password)
        
        if user is not None and user.role == User.Role.STUDENT:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'studentlogin.html', {
                'message': 'Invalid NIM or password'
            })
    
    return render(request, 'studentlogin.html')

def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        nim = request.POST.get('nim')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(nim=nim).exists():
            return render(request, 'register.html', {'message': 'NIM already registered'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'message': 'Email already registered'})
        
        if len(password) < 6:
            return render(request, 'register.html', {'message': 'Password must be at least 6 characters long'})
        
        if password != request.POST.get('confirm_password'):
            return render(request, 'register.html', {'message': 'Passwords do not match'})
        
        # Create user with hashed password
        user = User.objects.create_user(
            email=email,
            full_name=full_name,
            nim=nim,
            password=password,
            role=User.Role.STUDENT
        )
        # Automatically login after registration
        login(request, user)
        return redirect('home')
    
    return render(request, 'register.html')

def landingpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'landingpage.html')


@login_required
def home(request):
    if request.user.role == User.Role.STUDENT:
        courses = Course.objects.filter(students=request.user)
        return render(request, 'home.html', {'courses': courses})
    elif request.user.role == User.Role.TEACHER:
        courses = Course.objects.filter(teacher=request.user)
        return render(request, 'home.html', {'courses': courses})
    else:
        return HttpResponse("Unauthorized", status=401)

def logout_view(request):
    logout(request)
    return redirect('student_login')
@login_required
def course_detail(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return HttpResponse("Course not found", status=404)
    
    if request.user.role == User.Role.STUDENT and request.user not in course.students.all():
        return HttpResponse("Unauthorized", status=401)
    
    pdf_modules = PDFModule.objects.filter(course=course)
    
    return render(request, 'classpage.html', {
        'course': course,
        'pdf_modules': pdf_modules
    })