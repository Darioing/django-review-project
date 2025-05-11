import random
import os

from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
import uuid
import json
import os
from django.conf import settings
from datetime import datetime


User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    FIO = serializers.CharField(
        required=True,
        max_length=150,
        error_messages={
            'blank': 'ФИО обязательно для заполнения',
            'max_length': 'ФИО не должно превышать 150 символов'
        }
    )

    class Meta:
        model = User
        fields = ['email', 'FIO', 'password']
        extra_kwargs = {
            'email': {
                'error_messages': {
                    'invalid': 'Введите корректный email',
                    'required': 'Email обязателен'
                }
            }
        }

    def create(self, validated_data):
        request = self.context.get('request')
        if not request:
            raise serializers.ValidationError("Request object is missing")

        email = validated_data['email']
        token = str(uuid.uuid4())

        # Подготовка данных для сохранения
        user_data = {
            'email': email,
            'FIO': validated_data['FIO'],
            # Хешируем пароль!
            'password': make_password(validated_data['password']),
            'token': token,
            'created_at': str(datetime.now())
        }

        # Сохраняем в файл вместо сессии
        pending_dir = os.path.join(settings.BASE_DIR, 'pending_users')
        os.makedirs(pending_dir, exist_ok=True)

        file_path = os.path.join(pending_dir, f"{token}.json")
        with open(file_path, 'w') as f:
            json.dump(user_data, f, indent=2)

        # Создаем "письмо" в файл
        email_dir = os.path.join(settings.BASE_DIR, 'email_links')
        os.makedirs(email_dir, exist_ok=True)

        verification_url = f"http://127.0.0.1:8000/api/verify/{token}/"
        with open(os.path.join(email_dir, f"{email}.txt"), 'w') as f:
            f.write(f"Ссылка для подтверждения: {verification_url}\n")
            f.write(f"Срок действия: 24 часа\n")
            f.write(f"Файл с данными: {file_path}\n")

        # Возвращаем только email (пароль не возвращаем)
        return {'email': email, 'status': 'pending_verification'}


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
