from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import (
    TitleViewSet, ReviewViewSet, CommentViewSet
)

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<titles_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    # path('api-token-auth/', views.obtain_auth_token),
]
