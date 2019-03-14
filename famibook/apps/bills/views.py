from .models import Bill
from ..users.models import CustomUser
from .serializers import BillSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        Bills = Bill.objects
        # date query
        if ('start_date' in self.request.data) and ('end_date' in self.request.data):
            Bills = Bills.filter(date__range=(self.request.data['start_date'], self.request.data['end_date']))
        elif ('start_date' in self.request.data):
            Bills = Bills.filter(date__gte=self.request.data['start_date'])
        elif ('end_date' in self.request.data):
            Bills = Bills.filter(date__lte=self.request.data['end_date'])
        # nest routes
        if 'daybook_pk' in self.kwargs:
            Bills = Bills.filter(daybook=self.kwargs['daybook_pk'])
        elif 'user_pk' in self.kwargs:
            Bills = Bills.filter(users=self.kwargs['user_pk'])
        return Bills
