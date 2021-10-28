from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

UserModel = get_user_model()


class CustomUserAdmin(UserAdmin):
    """
    In case of adding new fields for the CustomUser model,
    use the two commented fields 'add_form' (create form) and 'form' (update form).
    """

    # add_form =
    # form =
    model = UserModel
    list_display = ['username', 'email', 'is_staff']


admin.site.register(UserModel, CustomUserAdmin)
