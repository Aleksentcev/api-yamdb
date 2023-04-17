from rest_framework import status, viewsets, mixins, permissions, filters
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.serializers import ValidationError
from rest_framework.decorators import action
from django.core.mail import send_mail
from django.db import IntegrityError
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS

from users.models import User
from .serializers import (
    UserSerializer,
    UserSignUpSerializer,
    UserGetTokenSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    ReviewSerializer,
    CommentSerializer,
)
from .permissions import IsAdminOrSuperUser, AdminOrReadOnly, IsAuthorOrReadOnlyPermission, IsAdminOrReadOnlyPermission
from reviews.models import Category, Genre, Title, Review, Comment


class UserSignUpViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, created = User.objects.get_or_create(
                **serializer.validated_data
            )
        except IntegrityError:
            raise ValidationError('Этот емейл уже занят')
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения YAMDb',
            message=f'Привет, {user.username}! '
                    f'Вот твой код: {confirmation_code}',
            from_email=None,
            recipient_list=(user.email,)
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserGetTokenViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserGetTokenSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = UserGetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data.get('username')
        )
        if default_token_generator.check_token(
            user,
            serializer.validated_data.get('confirmation_code')
        ):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminOrSuperUser)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False, methods=['GET', 'PATCH'],
        url_path='me', url_name='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        serializer = UserSerializer
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['GET', 'PATCH', 'DELETE'],
        url_path=r'(?P<username>[\w.@+-]+)',
        url_name='user_profile',
        permission_classes=(IsAdminOrSuperUser,)
    )
    def user_profile(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = PageNumberPagination
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer

    def get_queryset(self):
        queryset = Title.objects.all()
        category = self.request.query_params.get('category')
        genre = self.request.query_params.get('genre')
        if category is not None:
            queryset = queryset.filter(category__slug=category)
        if genre is not None:
            queryset = queryset.filter(genre__slug=genre)
        return queryset


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def get_title(self):
        return get_object_or_404(
            Title, id=self.kwargs['titles_id']
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title(),
        )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    pagination_class = PageNumberPagination

    def get_review(self):
        return get_object_or_404(
            Review, id=self.kwargs['review_id']
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
