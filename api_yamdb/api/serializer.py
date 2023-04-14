from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from datetime import datetime as dt

from users.models import User
from reviews.models import (
    Category, Genre, Title, Review, Comment)


class CategorySerializer(serializers.ModelSerializer):
    pass


class GenreSerializer(serializers.ModelSerializer):
    pass


class TitleSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    genre = serializers.SlugRelatedField(
        slug_field='name', read_only=True
    )
    category = serializers.SlugRelatedField(
        slug_field='name', read_only=True
    )

    class Meta:
        fields = ('__all__')
        model = Title

    def validate(self, data):
        title_date = self.context['request'].year
        current_date = dt.date.today().year
        if title_date > current_date:
            raise serializers.ValidationError(
                "Дата выхода не может быть больше текущей"
            )
        return data


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name', read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ('__all__')
        model = Review
        validators = UniqueTogetherValidator(
            queryset=Comment.objects.all(),
            fields=['review', 'username']
        )


class CommentSerializer(serializers.ModelSerializer):
    # review = serializers.SlugRelatedField(
    #     slug_field='title', read_only=True
    # )
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ('__all__')
        model = Comment


    # def validate(self, data):
    #     user = self.context['reuest'].user
