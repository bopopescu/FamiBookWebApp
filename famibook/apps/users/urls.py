from django.urls import include, path
from . import views

urlpatterns = [
    # path('users/', include('famibook.apps.users.urls')),

    path('', views.UserListView.as_view()),
]
