from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    """Модель сообществ"""
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=200,
        null=False,
        help_text='Дайте название модели'
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        help_text='Это слаг'
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        help_text='Опишите суть модели'
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    """Модель для управления записями в сообществе"""
    text = models.TextField(
        verbose_name='текст',
        help_text='введите текст'
    )

    pub_date = models.DateTimeField(
        verbose_name='дата публикации',
        auto_now_add=True,
        help_text='укажите дату публикации'
    )
    author = models.ForeignKey(
        User,
        verbose_name='автор',
        on_delete=models.CASCADE,
        related_name='posts',
        help_text='укажите автора'
    )
    group = models.ForeignKey(
        Group,
        verbose_name='сообщество',
        on_delete=models.CASCADE,
        related_name='group_posts',
        blank=True,
        null=True,
        help_text='укажите группу'
    )

    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    text = models.TextField()

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    created = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )
    
    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['user', 'author'], name='unique')
    ]
