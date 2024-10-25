

import httpx  # Use httpx for asynchronous HTTP requests

from django.contrib.auth.hashers import make_password

from django.shortcuts import  redirect
from django.contrib import messages
import json
from .context_processors import user_context
from .models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives
import logging
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
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
        face_image = request.FILES.get('face_image')  # Get the uploaded image

        # Validate password and user existence
        if not validate_passwords(password, checkPassword) or user_exists(email):
            return redirect('signup')

        # Process face image and create user
        user, file_url = create_user(username, email, password, face_image)
        if user is None:
            return redirect('signup')  # Handle user creation failure

        # Generate verification token and send email
        if not send_verification_email(user, request):
            messages.error(request, "There was an error sending the verification email.")
            return redirect('signup')

        messages.success(request, "User created successfully! Please verify your email.")
        return redirect('signup')

    return render(request, 'signup.html')


def validate_passwords(password, checkPassword):
    if password != checkPassword:
        messages.error(None, "Passwords don't match.")
        return False
    return True


def user_exists(email):
    if User.objects.filter(email=email).first():
        messages.error(None, "User with this email already exists.")
        return True
    return False


def create_user(username, email, password, face_image):
    # Save the uploaded image and create user
    file_url = None
    if face_image:
        fs = FileSystemStorage()
        filename = fs.save(face_image.name, face_image)
        file_url = fs.url(filename)  # Store the file URL

    else:
        logger.error("No face image uploaded.")

    user = User(
        username=username,
        email=email,
        password=make_password(password),
        is_active=False,
        face_image=face_image,  # Save original uploaded image
        url=file_url,
    )

    user.save()
    return user, file_url


def send_verification_email(user, request):
    token = generate_token()
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

    email = EmailMultiAlternatives(subject, text_message, 'admin@yourdomain.com', [user.email])
    email.attach_alternative(html_message, "text/html")

    try:
        email.send()
        return True
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False


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

def capture(request):
    return render(request, 'users.html')  # Render home page with user context



@csrf_exempt  # Only for testing; consider proper CSRF handling in production
def save_face_image(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse the JSON data
            face_dimensions = data.get('face_dimensions')  # Get face dimensions
            landmarks = data.get('landmarks')  # Get facial landmarks
            face_token = data.get('face_token')  # Get the face token
            user_id = data.get('user')  # Get the user ID from the request

            # Log the received face dimensions, landmarks, and face token
            logger.info(f'Received face dimensions: {face_dimensions}')
            logger.info(f'Received landmarks: {landmarks}')
            logger.info(f'Received face token: {face_token}')
            logger.info(f'Received user ID: {user_id}')

            if not face_dimensions or not landmarks or not face_token or not user_id:
                return JsonResponse({'status': 'error', 'message': 'Face dimensions, landmarks, face token, and user ID are required.'}, status=400)

            # Check if the user exists using the user ID
            try:
                user = User.objects.get(id=user_id)  # Retrieve the user by ID
                user.face_dimensions = {
                    'face_rectangle': face_dimensions,
                    'landmarks': landmarks,
                    'face_token': face_token  # Update with face token
                }
                user.save()  # Save changes
                return JsonResponse({'status': 'success', 'message': 'User updated successfully.'})
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)

        except json.JSONDecodeError:
            logger.error('Invalid JSON received.')
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'}, status=400)


@csrf_exempt  # Use with caution; consider using proper CSRF handling
def check_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            face_token = data.get('face_token', None)

            if face_token is None:
                return JsonResponse({'redirect': False}, status=400)  # No face token, no redirect

            users = list(User.objects.all())
            best_similarity_score = 0
            matched_user = None

            with httpx.Client() as client:
                for user in users:
                    compare_response = client.post('https://api-us.faceplusplus.com/facepp/v3/compare', data={
                        'api_key': 'LK1kVhRZWfuwuECyIZxjwDipDBIey5Y3',
                        'api_secret': 'QDpBathJGWwXXNXwG5Ze4jE8UfgCuX_t',
                        'face_token1': face_token,
                        'face_token2': user.face_dimensions['face_token']
                    })

                    compare_result = compare_response.json()
                    similarity_score = compare_result.get('confidence', 0)

                    if similarity_score > best_similarity_score:
                        best_similarity_score = similarity_score
                        matched_user = user

            if best_similarity_score >= 85:
                request.session['user_id'] = str(matched_user.id)
                return JsonResponse({'redirect': True})  # Signal to frontend to redirect

            return JsonResponse({'redirect': False})  # No match, no redirect

        except json.JSONDecodeError:
            logger.error('Invalid JSON received.')
            return JsonResponse({'redirect': False}, status=400)

    return JsonResponse({'redirect': False}, status=400)



@csrf_exempt  # Use with caution; consider using proper CSRF handling
def check_page_user(request):
    return render(request, 'userDetails.html')  # Render home page with user context