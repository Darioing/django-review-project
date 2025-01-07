from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from unidecode import unidecode
from django.core.exceptions import ValidationError
from django.db.models import Avg


User = get_user_model()


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Categories(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Категория заведения',
        help_text='Ресторан/фастфуд/бар',
        null=False,
        blank=False,
    )
    slug = models.SlugField(
        verbose_name='Ссылочное поле(заполняется автоматически)',
        unique=True,
        null=False,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Places(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название заведения',
        null=False,
        blank=False,
    )
    address = models.CharField(
        max_length=100,
        verbose_name='Адрес заведения',
        null=False,
        blank=False,
    )
    category_id = models.ForeignKey(
        Categories,
        verbose_name='Поле для связи с категорией заведения',
        help_text='Выберите категорию заведения',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="places"
    )
    about = models.CharField(
        max_length=500,
        verbose_name='О заведении',
        null=True,
        blank=True,
    )
    slug = models.SlugField(
        verbose_name='Ссылочное поле(заполняется автоматически)',
        unique=True,
        null=False,
        blank=True,
    )
    rating = models.FloatField(
        verbose_name='Средний рейтинг заведения',
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Заведение'
        verbose_name_plural = 'Заведения'


class PlacePhotos(models.Model):
    place_id = models.ForeignKey(
        Places,
        verbose_name='Поле для связи с заведением',
        help_text='Выберите заведение',
        null=False,
        blank=False,
        related_name='photos',
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        upload_to='images',
        verbose_name='Вставьте фото заведения',
        unique=True,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.place_id.name

    class Meta:
        verbose_name = 'Фотографии заведения'
        verbose_name_plural = 'Фотографии заведений'


class Reviews(TimestampMixin):
    place_id = models.ForeignKey(
        Places,
        verbose_name='Поле для связи с заведением',
        help_text='Выберите заведение',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    user_id = models.ForeignKey(
        User,
        verbose_name='Пользователь оставивший оценку',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    text = models.CharField(
        max_length=500,
        verbose_name='Письменный отзыв пользователя',
        help_text='Напишите о заведении',
        null=True,
        blank=True,
    )
    price = models.PositiveSmallIntegerField(
        verbose_name='Поле для оценки цены в заведении',
        help_text='Выберите оценку по критерию цена',
        null=False,
        blank=False,
        default=3,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ],
    )
    service = models.PositiveSmallIntegerField(
        verbose_name='Поле для оценки обслуживания в заведении',
        help_text='Выберите оценку по критерию обслуживания',
        null=False,
        blank=False,
        default=3,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ],
    )
    interior = models.PositiveSmallIntegerField(
        verbose_name='Поле для оценки инерьера в заведении',
        help_text='Выберите оценку по критерию интерьер',
        null=False,
        blank=False,
        default=3,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ],
    )

    def __str__(self):
        return f'{self.user_id} {self.place_id} {self.text[:30]}'

    class Meta:
        verbose_name = 'Отзыв заведения'
        verbose_name_plural = 'Отзывы заведений'
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'place_id', 'text'], name='unique_review')
        ]


class Questions(TimestampMixin):
    place_id = models.ForeignKey(
        Places,
        verbose_name='Поле для связи с заведением',
        help_text='Выберите заведение',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    user_id = models.ForeignKey(
        User,
        verbose_name='Пользователь оставивший оценку',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    text = models.CharField(
        max_length=200,
        verbose_name='Вопрос по заведению',
        help_text='Введите вопрос',
        null=False,
        blank=False,
    )

    def __str__(self):
        return f'{self.user_id} {self.place_id} {self.text[:30]}'

    class Meta:
        verbose_name = 'Вопрос к заведению'
        verbose_name_plural = 'Вопросы к заведениям'
        constraints = [
            models.UniqueConstraint(
                fields=['place_id', 'user_id', 'text'],
                name='unique_question'
            )
        ]


class Comments(TimestampMixin):
    user_id = models.ForeignKey(
        User,
        verbose_name='Пользователь оставивший комментарий',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    text = models.CharField(
        max_length=200,
        verbose_name='Комментарий',
        help_text='Введите комментарий',
        null=False,
        blank=False,
    )

    def __str__(self):
        return f'{self.user_id} {self.text[:30]} {self.content_object}'

    def clean(self):
        if not isinstance(self.content_object, (Questions, Reviews, Comments)):
            raise ValidationError(
                "Поле content_object должно ссылаться только на объекты Questions, Reviews или Comments.")

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'content_type', 'object_id', 'text'],
                name='unique_comment'
            )
        ]


class Votes(TimestampMixin):
    user_id = models.ForeignKey(
        User,
        verbose_name='Пользователь оставивший оценку',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    vote_type = models.SmallIntegerField(
        choices=[(1, 'Upvote'), (-1, 'Downvote')])

    def __str__(self):
        return f'{self.user_id} оставил {self.vote_type} к {self.content_object}'

    def clean(self):
        if self.vote_type not in [1, -1]:
            raise ValidationError("Неверный тип оценки: должен быть 1 или -1.")
        if not isinstance(self.content_object, (Questions, Comments, Reviews)):
            raise ValidationError(
                "Поле content_object должно ссылаться только на объекты Questions или Reviews.")

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'content_type', 'object_id'],
                name='unique_vote'
            )
        ]
