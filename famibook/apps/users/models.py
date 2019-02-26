from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from ..daybooks.models import Daybook

class CustomUser(AbstractUser):
    daybook = models.ForeignKey(Daybook, related_name='users', on_delete=models.SET_NULL, blank=True, null=True)
    avatar = models.FileField(upload_to='uploads/avatars/')

    def __str__(self):
        return self.email
