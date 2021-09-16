from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser, Profile


class CustomUserAdmin(UserAdmin):
    """
    In case of adding new fields for the CustomUser model,
    use the two commented fields 'add_form' (create form) and 'form' (update form).
    """

    # add_form =
    # form =
    model = CustomUser
    list_display = ['username', 'email', 'is_staff']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
