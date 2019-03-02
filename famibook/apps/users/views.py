from rest_framework import generics
from . import models
from . import serializers

class UserListView(generics.ListCreateAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer




from .models import CustomUser
from .serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

#https://juejin.im/post/5a66d262f265da3e317e4cc5
#http://drf.jiuyou.info/#/drf/authentication?id=basicauthentication
#https://www.django-rest-framework.org/api-guide/views/
