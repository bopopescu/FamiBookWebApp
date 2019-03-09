from .models import Bill
from .serializers import BillSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = (IsAuthenticated,)




# Many to Many ORM
# https://docs.djangoproject.com/en/1.11/topics/db/examples/many_to_many/
# Bills.users.add(user1, user2)
# Bills.users.create(...)
# Bills.users.all()
# Bills.objects.filter(user_id = 1)


#https://www.django-rest-framework.org/api-guide/viewsets/
#https: // github.com/twtrubiks/django-rest-framework-tutorial
   


# class ShareViewSet(viewsets.ModelViewSet):
#     queryset = Share.objects.all()
#     serializer_class = ShareSerializer
#     parser_classes = (JSONParser,)

#     def get_permissions(self):
#         if self.action in ('create',):
#             self.permission_classes = [IsAuthenticated]
#         return [permission() for permission in self.permission_classes]


 # [GET] api/shares/
    # def list(self, request, **kwargs):
    #     users = Share.objects.all()
    #     serializer = ShareSerializer(users, many=True)

    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # @permission_classes((IsAuthenticated,))
    # def create(self, request, **kwargs):
    #     name = request.data.get('name')
    #     users = Share.objects.create(name=name)
    #     serializer = ShareSerializer(users)

    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
