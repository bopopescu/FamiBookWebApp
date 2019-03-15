from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ('id', 'email', 'password',
                  'avatar', 'daybook', 'birthday',
                  'gender', 'date_joined', 'last_login')
