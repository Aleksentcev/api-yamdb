from rest_framework import routers
from django.urls import include, path

from .views import UserViewSet, UserSignUpViewSet, UserGetTokenViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path(
        'v1/auth/signup/',
        UserSignUpViewSet.as_view({'post': 'create'}),
        name='signup'
    ),
    path(
        'v1/auth/token/',
        UserGetTokenViewSet.as_view({'post': 'create'}),
        name='token'
    ),
]
