"""chainBid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from core.views import IndexTemplateView
from django.contrib import admin
from django.urls import include, path, re_path
from django_registration.backends.one_step.views import RegistrationView
from users.forms import CustomUserForm

# https://django-registration.readthedocs.io/en/3.2/
# https://django-registration.readthedocs.io/en/3.2/custom-user.html
# https://django-registration.readthedocs.io/en/3.2/one-step-workflow.html

urlpatterns = [
    # Administrator panel
    path('admin/', admin.site.urls),

    # Session authentication
    path('accounts/register/',
         RegistrationView.as_view(
             form_class=CustomUserForm,
             success_url='/'
         ), name='django_registration_register'),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    # Browsable API authentication
    path('api-auth/', include('rest_framework.urls')),

    # Token authentication
    path('api/rest-auth/', include('rest_auth.urls')),
    path('api/rest-auth/registration/', include('rest_auth.registration.urls')),

    # # Auctions endpoints
    # path('api/', include('auctions.api.urls')),

    # Homepage
    re_path(r"^.*$", IndexTemplateView.as_view(), name='entry-point'),  # Accept all kind of urls
]
