from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import User, Course, PDFModule
import mimetypes

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

def teacherlogin(request, ):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user is not None and user.role == User.Role.TEACHER:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'teacherlogin.html', {
                'message': 'Invalid email or password'
            })
    
    return render(request, 'teacherlogin.html')

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
    print(f"home called for user:", request.user.id, request.user.email)
    if request.user.role == User.Role.STUDENT:
        courses = Course.objects.filter(students=request.user)
        print(f"student courses:", list(courses.values('id','name')))
        return render(request, 'home.html', {'courses': courses})
    elif request.user.role == User.Role.TEACHER:
        courses = Course.objects.filter(teacher=request.user)
        return render(request, 'home.html', {'courses': courses})
    elif request.user.role == User.Role.ADMIN:
        courses = Course.objects.all()
        return render(request, 'home.html', {'courses': courses})
    else:
        return HttpResponse("Unauthorized", status=401)

def logout_view(request):
    logout(request)
    return redirect('student_login')

@login_required
def course_detail(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    if request.user.role == User.Role.STUDENT:

        if request.user not in course.students.all():

            return HttpResponse("You are not enrolled in this course", status=403)

    elif request.user.role == User.Role.TEACHER:

        if course.teacher != request.user:

            return HttpResponse("You are not the teacher of this course", status=403)

    pdf_modules = PDFModule.objects.filter(course=course)
    return render(request, 'classpage.html', {
        'course': course,
        'pdf_modules': pdf_modules
    })

@login_required
def download_pdf(request, pdf_id):

    pdf = get_object_or_404(PDFModule, id=pdf_id)

    if request.user.role == User.Role.STUDENT:

        if request.user not in pdf.course.students.all():

            return HttpResponse("You are not enrolled in this course", status=403)
    elif request.user.role == User.Role.TEACHER:

        if pdf.course.teacher != request.user:

            return HttpResponse("You are not the teacher of this course", status=403)
    else:

        return HttpResponse("Unauthorized", status=401)

    if not pdf.file:

        raise Http404("PDF file not found")

    try:
        response = FileResponse(pdf.file.open('rb'), content_type='Media/pdf')
        response['Content-Disposition'] = f'attachment; filename="{pdf.title}.pdf"'
        return response
    except FileNotFoundError:
        raise Http404("PDF file not found on server")