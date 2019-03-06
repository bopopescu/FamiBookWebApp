from django.urls import path
from . import views
urlpatterns = [
    # path('users/', include('famibook.apps.users.urls')),
    path('', views.UserViewSet),
]
