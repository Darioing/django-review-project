from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    FIO = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'FIO', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            FIO=validated_data['FIO'],
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Добавляем дополнительные данные в токен
        token['email'] = user.email
        token['FIO'] = user.FIO
        return token


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'FIO', 'email', 'image', 'date_joined']
        read_only_fields = ['id', 'email', 'date_joined']

    def update(self, instance, validated_data):
        """
        Метод для обновления данных пользователя.
        """
        print("upd")
        # Обновляем FIO, если оно передано
        if 'FIO' in validated_data:
            instance.FIO = validated_data['FIO']

        # Обновляем аватар, если он передан
        if 'image' in validated_data:
            instance.image = validated_data['image']

        # Сохраняем изменения в базе данных
        instance.save()

        return instance
