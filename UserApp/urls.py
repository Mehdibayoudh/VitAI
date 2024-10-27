from django.urls import path
from . import views

urlpatterns = [

    path('signup', views.signup, name='signup'),

    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('resend-verification/', views.resend_verification, name='resend_verification'),  # Add this line
    path('login', views.login_view, name='loginuser'),  # Add this line for the login view
    path('logout', views.logout_view, name='logout'),
    path('profile', views.profile, name='profile'),
    path('update-username/<str:user_id>/', views.update_username, name='update_username'),
    path('users/delete/<str:user_id>/', views.delete_user, name='delete_user'),  # Use <str> for ObjectId
    path('capture/', views.capture, name='capture'),
    path('save_face_image/', views.save_face_image, name='save_face_image'),
    path('check_user/', views.check_user, name='check_user'),
    path('page_check_user/', views.check_page_user, name='check_page_user'),

]
