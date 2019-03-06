from rest_framework import serializers
from .models import Daybook


class DaybookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Daybook
        fields = '__all__'  # can set different column ('id', 'name')
