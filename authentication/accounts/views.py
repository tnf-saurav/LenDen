from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from lenden import settings
from django.core.mail import send_mail
from .models import UserRegister
from .forms import SignUpForm
from django.db import transaction


# Create your views here.
def home(request):
    return render(request, "index.html")

def signup(request):
    if request.method == 'POST':
        print(request.POST) 
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.save()

                     # Debugging: Verify user saved to database
                    if user.id is not None:
                        print(f"User saved to database with ID: {user.id}")
                    else:
                        print("Failed to save user to database")

                    
                    businessname = form.cleaned_data.get('businessname')
                    username = form.cleaned_data.get('username')
                    phone = form.cleaned_data.get('phone')
                    email = form.cleaned_data.get('email')
                    
                    # Debugging: Print user information
                    print(f"User created: {user.username}, {user.email}, {user.businessname}, {user.phone}")


                    # Send welcome email
                    subject = "Welcome to LenDen"
                    message = f"Hello {businessname}!!\nWelcome to LenDen\nThank you for visiting our website.\nWe have sent you a confirmation email. Please confirm it to complete your registration."
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [email]
                    send_mail(subject, message, from_email, to_list, fail_silently=True)

                    login(request, user)
                    messages.success(request, f'Account created for {username}!')
                    return redirect('signin')
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
                print(f"An error occurred: {e}")

        else:
            print(form.errors) 
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {'form': form})

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass1']

         # Debug: Print submitted credentials
        print(f"Submitted credentials: username={username}, password={password}")


        user = authenticate(request, username=username, password=password)

        if user is not None:
            print("User authenticated successfully")
            login(request, user)
            businessname = user.businessname
            messages.success(request, f"Hello {businessname}, you're successfully logged in.")
            return render(request, "index.html", {'businessname': businessname})
        else:
            print("Authentication failed")
            messages.error(request, "Invalid credentials, please try again.")
            return redirect('signin')
    return render(request, "accounts/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')