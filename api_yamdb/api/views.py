from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, filters

from users.models import User
from reviews.models import (
    Category, Genre, Title, Review, Comment
)
from .serializer import (
    TitleSerializer, ReviewSerializer, CommentSerializer
)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    # def perform_create(self, serializer):
    #     serializer.save()


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

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

    def get_review(self):
        return get_object_or_404(
            Review, id=self.kwargs['review_id']
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
