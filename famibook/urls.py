"""famibook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from famibook.apps.daybooks.views import DaybookViewSet
from famibook.apps.categories.views import CategoryViewSet
from famibook.apps.bills.views import BillViewSet
from famibook.apps.users.views import UserViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

# docs settings
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='FamiBook API')


# resful api settings
router = DefaultRouter()
router.register(r'daybooks', DaybookViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'bills', BillViewSet)
router.register(r'users', UserViewSet)

daybookNestRouter = routers.NestedSimpleRouter(router, r'daybooks', lookup='daybook')
daybookNestRouter.register(r'bills', BillViewSet, base_name='daybook-bills')
userNestRouter = routers.NestedSimpleRouter(router, r'users', lookup='user')
userNestRouter.register(r'bills', BillViewSet, base_name='user-bills')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include(daybookNestRouter.urls)),
    path('api/v1/', include(userNestRouter.urls)),
    path('api/v1/rest-auth/', include('rest_auth.urls')),
    path('api/v1/rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api/v1/users/', include('famibook.apps.users.urls')),
    path('api/v1/docs/', schema_view),
]
