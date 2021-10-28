from accounts.forms import CustomLoginForm, CustomPasswordChangeForm, CustomRegistrationForm
from django.contrib.auth import views
from django_registration.backends.one_step.views import RegistrationView
from django.urls import path

urlpatterns = [
    path('register/',
         RegistrationView.as_view(
             form_class=CustomRegistrationForm,
             success_url='/'
         ), name='django_registration_register'),
    path('login/', views.LoginView.as_view(form_class=CustomLoginForm), name='login'),
    path('password_change/', views.PasswordChangeView.as_view(form_class=CustomPasswordChangeForm), name='password_change'),
]
