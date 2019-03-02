from .models import Daybook
from .serializers import DaybookSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class DaybookViewSet(viewsets.ModelViewSet):
    queryset = Daybook.objects.all()
    serializer_class = DaybookSerializer
    permission_classes = (IsAuthenticated,)
