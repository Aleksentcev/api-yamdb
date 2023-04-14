from rest_framework import serializers

from users.models import User


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email', 'username')
        model = User

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использование данного имени запрещено!'
            )
        if User.objects.filter(username=username) or User.objects.filter(email=email):
            raise serializers.ValidationError(
                'Имя пользователя или почта заняты! Используйте другие.'
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
