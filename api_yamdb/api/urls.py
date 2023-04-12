from rest_framework import routers
from django.urls import include, path

from .views import UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')


urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path('v1/auth/signup', ),
    path('v1/auth/token', ),
]
