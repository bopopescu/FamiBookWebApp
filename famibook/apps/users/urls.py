from django.urls import include, path
from . import views

urlpatterns = [
    # path('users/', include('famibook.apps.users.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('users/', views.UserListView.as_view()),
]
