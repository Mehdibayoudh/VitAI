from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

# Create your views here.
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        checkPassword = request.POST.get('checkPassword')

        if request.FILES.get('profile_image') is not None:
            profile_image = request.FILES.get('profile_image')
        else:
            profile_image = None

        if password != checkPassword:
            messages.error(request, "Passwords don't match.")
            return redirect('signup')

        if User.objects(email=email).first() is not None:
            messages.error(request, "User with this email already exists.")
            return redirect('signup')

        user = User(
            username=username,
            email=email,
            password=make_password(password),
            image=profile_image
        )

        user.save()
        messages.success(request, "User created successfully!")
        return redirect('signup')

    return render(request, 'signup.html')
