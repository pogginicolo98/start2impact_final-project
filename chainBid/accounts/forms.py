from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UsernameField
from django_registration.forms import RegistrationForm

UserModel = get_user_model()


class CustomRegistrationForm(RegistrationForm):
    """
    A form class for sign up new users.

    * username, password1, password2 and email are required.
    * password1 and password2 must match.
    """

    username = UsernameField(
        max_length=15,
        label='',
        required=True,
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'rounded-pill',
            'placeholder': 'Choose a username',
        }),
        help_text="Max 15 characters. Letters, digits and ./+/-/_ only.",
    )
    email = forms.CharField(
        max_length=45,
        label='',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'rounded-pill',
            'placeholder': 'Your email',
        }),
    )
    password1 = forms.CharField(
        max_length=30,
        label='',
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'rounded-pill',
            'placeholder': 'New password',
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        max_length=30,
        label='',
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'rounded-pill',
            'placeholder': 'Confirm password',
        }),
        help_text="Enter the same password as before, for verification.",
    )

    class Meta(RegistrationForm.Meta):
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']


class CustomLoginForm(AuthenticationForm):
    """
    A form for authenticating users.

    * username and password are required.
    * username and password must match with user's credentials.
    """

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(
        max_length=15,
        label='',
        required=True,
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'rounded-pill',
            'placeholder': 'Username',
        }),
    )
    password = forms.CharField(
        max_length=30,
        label='',
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'rounded-pill',
            'placeholder': 'Password',
        }),
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    A form that lets a user change their password by entering their old password.

    * old_password, new_password1 and new_password2 are required.
    * old_password must match with user's credentials.
    * new_password1 and new_password2 must match.
    """

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)

    old_password = forms.CharField(
        max_length=30,
        label='',
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autofocus': True,
            'class': 'rounded-pill',
            'placeholder': 'Current password',
        }),
    )
    new_password1 = forms.CharField(
        max_length=30,
        label='',
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'rounded-pill',
            'placeholder': 'New password',
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        max_length=30,
        label='',
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'rounded-pill',
            'placeholder': 'Confirm password',
        }),
        help_text="Enter the same password as before, for verification.",
    )
