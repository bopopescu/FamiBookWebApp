from django.db import models
from django.contrib.auth.models import AbstractUser
from ..daybooks.models import Daybook

# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUser(AbstractUser):
    GENDER_TYPES = (
        (0, 'woman'),
        (1, 'man'),
    )
    daybook = models.ForeignKey(Daybook,
                                related_name='users',
                                on_delete=models.SET_NULL,
                                blank=True,
                                null=True)
    avatar = models.FileField(upload_to='uploads/avatars/')
    birthday = models.DateField(blank=True,
                                null=True)
    gender = models.IntegerField(blank=True,
                                 null=True,
                                 choices=GENDER_TYPES)

    def __str__(self):
        return self.email


# @admin.site.register(CustomUser)
# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ['username', 'email', 'daybook', 'avatar']

