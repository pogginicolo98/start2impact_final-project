from django_registration.forms import RegistrationForm
from users.models import CustomUser


class CustomUserForm(RegistrationForm):
    """
    Form for registering a new user account with 'CustomUser' as user model.
    """

    class Meta(RegistrationForm.Meta):
        model = CustomUser
