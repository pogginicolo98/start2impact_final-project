from django.contrib.auth import get_user_model
from django_registration.forms import RegistrationForm

UserModel = get_user_model()


class CustomUserForm(RegistrationForm):
    """
    Form for registering a new user account with 'CustomUser' as user model.
    """

    class Meta(RegistrationForm.Meta):
        model = UserModel
