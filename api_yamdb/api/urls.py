from django.urls import include, path
from rest_framework import routers

from .views import (
    UserViewSet,
    UserSignUpViewSet,
    UserGetTokenViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
)

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router_v1.register(
    r'titles/(?P<titles_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)


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
