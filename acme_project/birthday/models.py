from django.contrib.auth import get_user_model

from django.db import models

from django.urls import reverse

from . import validators


User = get_user_model()


class Tag(models.Model):
    tag = models.CharField(
        max_length=20,
        verbose_name='Тег',
    )

    def __str__(self):
        return self.tag


class Birthday(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор записи',
        null=True,
        related_name='birthdays',
    )
    first_name = models.CharField(
        max_length=20,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=20,
        verbose_name='Фамилия',
        blank=True,
        help_text='Необязательное поле',
    )
    description = models.TextField(
        max_length=200,
        verbose_name='Описание',
        blank=True,
        help_text='Необязательное поле',
    )
    birthday = models.DateField(
        verbose_name='Дата рождения',
        validators=(validators.real_age,),
    )
    image = models.ImageField(
        verbose_name='Фото',
        blank=True,
        upload_to='birthday_images',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        blank=True,
        help_text='Удерживайте Ctrl для выбора нескольких вариантов',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=[
                    'first_name',
                    'last_name',
                    'birthday',
                ],
                name='Unique person constraint',
            ),
        )

    def get_absolute_url(self):
        # С помощью функции reverse() возвращаем URL объекта.
        return reverse('birthday:detail', kwargs={'pk': self.pk})


class Congratulation(models.Model):
    text = models.TextField(verbose_name='Текст поздравления')
    birthday = models.ForeignKey(
        Birthday,
        on_delete=models.CASCADE,
        related_name='congratulations',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('created_at',)
