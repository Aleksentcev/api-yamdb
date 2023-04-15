from rest_framework import serializers
from django.core.validators import RegexValidator

from users.models import User


class UserSignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[RegexValidator(regex=r'^[\w.@+-]+$')]
    )
    email = serializers.EmailField(
        required=True,
        max_length=254
    )

    class Meta:
        fields = ('email', 'username')
        model = User

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использование данного имени запрещено!'
            )
        return data


class UserGetTokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        model = User
