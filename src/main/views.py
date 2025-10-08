from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import User, Course, PDFModule
# Create your views here.

# Login
def StudentLogin(request):
    if request.method == 'POST':
        nim = request.POST.get('nim')
        password = request.POST.get('password')
        
        print(f"📝 Received NIM: {nim}")
        print(f"📝 Received password: {password}")
        
        user = authenticate(request, username=nim, password=password)
        
        print(f"Authenticate returned: {user}")
        
        if user is not None:
            print(f"User role: {user.role}")
            if user.role == User.Role.STUDENT:
                login(request, user)
                print(f"✓ Login successful!")
                return HttpResponseRedirect('/home/')
            else:
                print(f"✗ User is not a student")
        else:
            print(f"✗ Authentication failed")
            
        return render(request, 'studentlogin.html', {'message': 'Invalid NIM or password'})
    
    return render(request, 'studentlogin.html')

def register(request, backend="django.contrib.auth.backends.ModelBackend"):
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
        
        user = User.objects.create_user(email=email, full_name=full_name, nim=nim, password=password, role=User.Role.STUDENT)
        user.save()
        return HttpResponseRedirect('/home/')
    return render(request, 'register.html')

def landingpage(request):
    return render(request, 'ProfilePage.html')

@login_required
def home(request):
    if request != None and request.user.is_authenticated:
        user = request.user
        return render(request, 'home.html', {'user': user})
    else:
        message = "You must be logged in to view this page."
        return HttpResponseRedirect('/studentlogin/')
    

