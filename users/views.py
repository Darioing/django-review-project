import logging
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from rest_framework.decorators import action
from .permissions import IsOwnerOrReadOnly
import random
import uuid
import os
from datetime import datetime, timedelta
from django.conf import settings
import logging
import json
from django.urls import reverse


User = get_user_model()


logger = logging.getLogger(__name__)


class UserRegistrationView(APIView):
    def post(self, request):
        logger.info(f"Начало регистрации. Данные: {request.data}")

        serializer = UserRegistrationSerializer(
            data=request.data,
            context={'request': request}
        )

        if not serializer.is_valid():
            logger.error(f"Ошибки валидации: {serializer.errors}")
            return Response(serializer.errors, status=400)

        try:
            email = serializer.validated_data['email']
            verification_token = str(uuid.uuid4())

            # Сохраняем данные во временное хранилище
            pending_user = {
                'email': email,
                'FIO': serializer.validated_data['FIO'],
                'password': serializer.validated_data['password'],
                'token': verification_token,
                'created_at': str(datetime.now())
            }

            # Записываем в файл (вместо сессии)
            pending_dir = os.path.join(settings.BASE_DIR, 'pending_users')
            os.makedirs(pending_dir, exist_ok=True)
            user_file = os.path.join(pending_dir, f"{verification_token}.json")

            with open(user_file, 'w') as f:
                json.dump(pending_user, f, indent=2)

            # Создаем файл с ссылкой (для тестирования)
            verification_url = f"http://127.0.0.1:8000/user/verify-email/{verification_token}/"
            email_dir = os.path.join(settings.BASE_DIR, 'email_links')
            os.makedirs(email_dir, exist_ok=True)

            with open(os.path.join(email_dir, f"{email}.txt"), 'w') as f:
                f.write(f"Ссылка для подтверждения: {verification_url}\n")
                f.write(f"Срок действия: 24 часа\n")
                f.write(f"Файл: {user_file}\n")

            logger.info(f"Ссылка сохранена в файл для {email}")

            return Response({
                'message': 'Ссылка для подтверждения отправлена',
                'test_link': verification_url  # Для удобства тестирования
            }, status=200)

        except Exception as e:
            logger.error(f"Ошибка регистрации: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Internal server error'},
                status=500
            )


class VerifyEmailView(APIView):
    def get(self, request, token):
        try:
            pending_dir = os.path.join(settings.BASE_DIR, 'pending_users')
            token_file = os.path.join(pending_dir, f"{token}.json")

            if not os.path.exists(token_file):
                return redirect(reverse('users:custom_login') + '?error=invalid_token')

            with open(token_file) as f:
                user_data = json.load(f)

            # Проверка на просроченность токена
            created_at = datetime.fromisoformat(user_data['created_at'])
            if datetime.now() - created_at > timedelta(hours=24):
                os.remove(token_file)
                return redirect(reverse('users:custom_login') + '?error=expired_token')

            user = User.objects.create_user(
                email=user_data['email'],
                FIO=user_data['FIO'],
                password=user_data['password']
            )

            os.remove(token_file)
            return redirect(f"{settings.FRONTEND_URL}/login")

        except Exception as e:
            logger.error(f"Verify email error: {str(e)}")
            return redirect(reverse('users:custom_login') + '?error=server_error')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавить пользовательские данные в токен
        token['FIO'] = user.FIO
        token['email'] = user.email
        token['user_id'] = user.id
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Добавить user_id в ответ
        data['user_id'] = self.user.id

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Вы авторизованы!"})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Вы успешно вышли из аккаунта."}, status=200)
        except Exception as e:
            return Response({"error": "Произошла ошибка при выходе."}, status=400)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerOrReadOnly]
        elif self.action == 'me':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @action(detail=False, methods=['get', 'patch'], url_path='me', permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
