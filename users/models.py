from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    avatar = models.ImageField(upload_to='users', blank=True, null=True, verbose_name='Аватар пользователя')
    number_phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Номер телефона')
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name="Страна")
    token = models.CharField(max_length=100, verbose_name="Токен", blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'