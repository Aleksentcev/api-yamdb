from django.db.models import Avg
from rest_framework import serializers
from datetime import datetime as dt


from reviews.models import (
    Title, Review, Comment)


class CategorySerializer(serializers.ModelSerializer):
    pass


class GenreSerializer(serializers.ModelSerializer):
    pass


class TitleSerializer(serializers.ModelSerializer):
    title = serializers.PrimaryKeyRelatedField(read_only=True)
    genre = serializers.SlugRelatedField(
        slug_field='name', read_only=True
    )
    category = serializers.SlugRelatedField(
        slug_field='name', read_only=True
    )
    avg_score = serializers.SerializerMethodField()

    class Meta:
        fields = ('__all__')
        model = Title

    def get_avg_score(self, data):
        return round(Review.objects.filter(
            title=data.pk).aggregate(
            Avg('score')).get('score__avg'))

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

    def validate(self, data):
        author = self.context['request'].user
        if self.context['request'].method == 'POST' and Review.objects.filter(
                author=author).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ('__all__')
        model = Comment
