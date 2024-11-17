from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from unidecode import unidecode


User = get_user_model()

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
            name_transliterated = unidecode(self.name)
            self.slug = slugify(name_transliterated)
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
        blank=False,
        on_delete=models.SET_NULL,
    )
    slug = models.SlugField(
        verbose_name='Ссылочное поле(заполняется автоматически)',
        unique=True,
        null=False,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            name_transliterated = unidecode(self.name)
            self.slug = slugify(name_transliterated)
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
        return self.place_id
    
    class Meta:
        verbose_name = 'Фотографии заведения'
        verbose_name_plural = 'Фотографии заведений'

class Reviews(models.Model):
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
    created_at = models.DateTimeField(
        verbose_name='Поле для даты оставления ревью',
        null=False,
        blank=False,
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.user_id} {self.place_id} {self.text[:30]}'
    
    class Meta:
        verbose_name = 'Отзыв заведения'
        verbose_name_plural = 'Отзывы заведений'

class Questions(models.Model):
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
    created_at = models.DateTimeField(
        verbose_name='Поле для даты вопроса',
        null=False,
        blank=False,
        auto_now_add=True,
    )
    def __str__(self):
        return f'{self.user_id} {self.place_id} {self.text[:30]}'
    
    class Meta:
        verbose_name = 'Вопрос к заведению'
        verbose_name_plural = 'Вопросы к заведениям'

class Comments(models.Model):
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
    created_at = models.DateTimeField(
        verbose_name='Поле для даты оставления ревью',
        null=False,
        blank=False,
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.user_id} {self.text[:30]} {self.content_object}'
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class Votes(models.Model):
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
    vote_type = models.SmallIntegerField(choices=[(1, 'Upvote'), (-1, 'Downvote')])
    created_at = models.DateTimeField(
        verbose_name='Поле для даты оставления ревью',
        null=False,
        blank=False,
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.user_id} оставил {self.vote_type} к {self.content_object}'
    
    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        unique_together = ('user_id', 'content_type', 'object_id')