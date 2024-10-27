from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth import login

class UserManager(BaseUserManager):
    '''
    Переопределяем User Manager для запроса
    дополнительных полей при создании суперпользователя
    '''

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        '''Create and save a user with the given email, and
        password.
        '''
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.'
            )

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    '''
    Кастомная модель пользователя
    '''

    first_name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='Имя',
    )
    second_name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='Фамилия',
    )
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        verbose_name='Электронная почта',
    )
    is_staff = models.BooleanField(
        _('Модератор'),
        default=False,
        help_text=_(
            'Определяет может ли пользователь войти в админ панель'
        ),
    )
    is_superuser = models.BooleanField(
        _('Администратор'),
        default=False,
        help_text=_(
            'Определяет имеет ли пользователь все привелегии'
        ),
    )
    is_active = models.BooleanField(
        _('Активный'),
        default=True,
    )
    date_joined = models.DateTimeField(
        _('Дата регистрации'),
        default=timezone.now,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'second_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'