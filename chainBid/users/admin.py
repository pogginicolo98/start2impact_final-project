from django.contrib import admin
from users.models import CustomUser, Profile


admin.site.register(CustomUser)
admin.site.register(Profile)
