from .models import Daybook
from .serializers import DaybookSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


# Create your views here.
class DaybookViewSet(viewsets.ModelViewSet):
    queryset = Daybook.objects.all()
    serializer_class = DaybookSerializer
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['post'])
    def join(self, request):
        print(request.user.daybook)
        try:
            daybook = Daybook.objects.get(
                name=request.data['name'], id=request.data['id'])
            request.user.daybook = daybook
            request.user.save()
            result = {
                'message': 'Success to join the daybook',
                'data': DaybookSerializer(daybook).data}
            return Response(result, status=status.HTTP_200_OK)
        except Daybook.DoesNotExist:
            daybook = None
            result = {'message': 'Fail to join the daybook'}
            return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def exit(self, request):
        request.user.daybook = None
        request.user.save()
        result = {}
        return Response(result, status=status.HTTP_200_OK)
