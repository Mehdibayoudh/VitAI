from venv import logger

from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .context_processors import user_context
from .models import User
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives
import logging
from django.views.decorators.http import require_POST
logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    context = user_context(request)  # Get user context
    if context['user']:  # Check if user exists in context
        return render(request, 'home.html', context)  # Render home page with user context
    else:
        return render(request, 'signup.html')  # Show the signup page if not logged in

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects(username=username).first()

        if user and user.check_password(password):
            request.session['user_id'] = str(user.id)  # Store the user ID in session
            return redirect('home')
        else:
            # Authentication failed
            return render(request, 'signup.html', {'error': 'Invalid username or password'})

    return render(request, 'signup.html')


def logout_view(request):
    request.session.flush()  # Clear the session
    return redirect('home')  # Redirect to the home page after logout


def generate_token():
    """Generates a random token for email verification."""
    return get_random_string(64)

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

        # Check if passwords match
        if password != checkPassword:
            messages.error(request, "Passwords don't match.")
            return redirect('signup')

        # Check if the email already exists
        if User.objects.filter(email=email):  # Change this line
            messages.error(request, "User with this email already exists.")
            return redirect('signup')

        # Create the user but keep them inactive until email is verified
        user = User(
            username=username,
            email=email,
            password=make_password(password),
            image=profile_image,
            is_active=False  # Mark user as inactive until email is verified
        )
        user.save()

        # Generate verification token
        token = generate_token()

        # Save the token
        user.verification_token = token
        user.save()

        # Prepare email verification link
        current_site = get_current_site(request)
        verification_link = reverse('verify_email', args=[urlsafe_base64_encode(force_bytes(user.pk)), token])
        full_link = f"http://{current_site.domain}{verification_link}"

        # Send verification email
        subject = "Verify your email"
        text_message = render_to_string('verifyemail.txt', {
            'user': user,
            'verification_link': full_link
        })
        html_message = render_to_string('verifyemail.html', {
            'user': user,
            'verification_link': full_link
        })

        email = EmailMultiAlternatives(subject, text_message, 'admin@yourdomain.com', [email])
        email.attach_alternative(html_message, "text/html")  # Attach HTML version

        try:
            email.send()
            messages.success(request, "User created successfully! Please verify your email to activate your account.")
            return redirect('signup')
        except Exception as e:
            messages.error(request, "There was an error sending the verification email.")
            return redirect('signup')


    return render(request, 'signup.html')


def verify_email(request, uidb64, token):
    global logger
    try:
        logger = logging.getLogger(__name__)

        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        # Debugging logs
        logger.debug(f"User retrieved: {user.username}, is_active: {user.is_active}, token: {user.verification_token}")
        user.is_active = True
        user.save()

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and user.verification_token == token:
        user.is_active = True
        user.verification_token = ""  # Clear the token after successful verification
        user.save()

        # Debugging log after saving
        logger.debug(f"User saved: {user.username}, is_active: {user.is_active}")

        messages.success(request, "Email verified successfully! You can now log in.")
        return redirect('signup')  # Redirect to signup page after successful verification
    else:
        messages.error(request, "Invalid verification link.")
        return redirect('signup')


def resend_verification(request):
    # Logic to resend the verification email
    # For example, you might need to get the user's email and resend the email.
    messages.success(request, "Verification email resent!")
    return redirect('signup')  # Redirect to signup or another appropriate page

def profile(request):
    return render(request, 'profile.html')  # Show the signup page if not logged in

@csrf_exempt  # Allow CSRF for simplicity; consider using decorators to protect this in production.
def update_username(request, user_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_username = data.get('username')

        try:
            user = User.objects.get(id=user_id)
            user.username = new_username
            user.save()

            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found.'})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


@require_POST
def delete_user(request, user_id):
        user = User.objects.get(id=user_id)
        user.delete()  # Delete the user if found
        return redirect('signup')

