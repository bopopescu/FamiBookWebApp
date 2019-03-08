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

    # TODO search daybook

    @action(detail=False, methods=['post'])
    def join(self, request):
        print(request.user.daybook)
        try:
            daybook = Daybook.objects.get(
                name=request.data['name'], id=request.data['id'])
            request.user.daybook = daybook
            request.user.save()
            result = {'Success to join the daybook'}    # TODO DaybookSerializer(daybook).data
            return Response(result, status=status.HTTP_200_OK)
        except Daybook.DoesNotExist:
            daybook = None
            result = {'Fail to join the daybook'}
            return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def exit(self, request):
        request.user.daybook = None
        request.user.save()
        result = {}
        return Response(result, status=status.HTTP_200_OK)

    # 127.0.0.1:8000/api/v1/daybooks/join/
    # parameter: name, id

    # @action(methods=['post'], detail=True, permission_classes=[IsAdminOrIsSelf],
    #         url_path='change-password', url_name='change_password')
    # def set_password(self, request, pk=None):
    #     ...


    # # /api/music/{pk}/detail/
    # @detail_route(methods=['get'])
    # def detail(self, request, pk=None):
    #     music = get_object_or_404(Music, pk=pk)
    #     result = {
    #         'singer': music.singer,
    #         'song': music.song
    #     }

    #     return Response(result, status=status.HTTP_200_OK)

    # @detail_route(methods=['post'])
    # def set_password(self, request, pk=None):
    #     user = self.get_object()
    #     serializer = PasswordSerializer(data=request.DATA)
    #     if serializer.is_valid():
    #         user.set_password(serializer.data['password'])
    #         user.save()
    #         return Response({'status': 'password set'})
    #     else:
    #         return Response(serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)

# join daybook
#https: // github.com/twtrubiks/django-rest-framework-tutorial/blob/master/musics/views.py
