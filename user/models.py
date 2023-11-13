from django.db import models
from django.contrib import auth
from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    
    GENDER = [
        ('m', ('Мужской')),
        ('f', ('Женский'))
    ]

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(max_length=150, unique=True, validators=[username_validator],
                                verbose_name='Псевдоним')
    first_name = models.CharField(max_length=150, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='E-mail')
    is_staff = models.BooleanField(default=False, verbose_name='Статус персонала')
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата присоединения')
    address = models.CharField(max_length=100, blank=True, verbose_name='Адресс')

    language = models.CharField(max_length=15)

    gender = models.CharField(max_length=5, default='', choices=GENDER, verbose_name='Пол')
    phone_number = models.TextField(blank=True, null=True, unique=True, verbose_name='Телефон')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    number_card = models.CharField(max_length=19, blank=True, verbose_name='Номер карты')
    town = models.ForeignKey('Town', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Город')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Town(models.Model):
    town_name = models.CharField(max_length=30, verbose_name='Город')

    class Meta:
        verbose_name = 'Город пользователя'
        verbose_name_plural = 'Город пользователя'

    def __str__(self):
        return f'{self.town_name}'
    