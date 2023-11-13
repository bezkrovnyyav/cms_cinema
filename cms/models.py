from django.conf import settings
from django.db import models
import os


# Create your models here.

class Client(models.Model):
    """
    Model for UI Statistics
    """
    objects = None
    date = models.DateField(null=True)
    is_mobile = models.BooleanField(default=False)
    is_tablet = models.BooleanField(default=False)
    is_pc = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date}"


class TemplatesMailing(models.Model):
    """
    Templates mailing  model
    """
    objects = None
    created_date = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to='mailing/')

    def __str__(self):
        return os.path.basename(self.file.name)


class SeoBlock(models.Model):
    """
    Seo block model
    """
    objects = None
    url = models.URLField(verbose_name='url')
    title_seo = models.CharField(max_length=100, verbose_name='Заголовок')
    keywords = models.CharField(max_length=100, verbose_name='Ключевые слова')
    description_seo = models.TextField(blank=True, default='', verbose_name='Описание')

    class Meta:
        verbose_name = 'Seo блок'
        verbose_name_plural = 'Seo блок'

    def __str__(self):
        return f'{self.title_seo}'


class Gallery(models.Model):
    """
    Gallery model
    """
    objects = None
    title = models.CharField(max_length=200, verbose_name='Заголовок')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Галерею'
        verbose_name_plural = 'Галерея'


class Images(models.Model):
    """
    Images model
    """
    objects = None
    image = models.ImageField(upload_to='gallery/', verbose_name='Картинка', unique=True)
    gallery = models.ForeignKey('Gallery', on_delete=models.CASCADE, verbose_name='Галерея')

    class Meta:
        verbose_name = 'Картинку'
        verbose_name_plural = 'Картинки'


class HomePageBanner(models.Model):
    objects = None
    image = models.ImageField(upload_to='banners/home_page/', verbose_name='Баннер', unique=True)
    url = models.URLField(verbose_name='url')
    text = models.CharField(max_length=150, verbose_name='Текст')

    class Meta:
        verbose_name = 'Баннер главной верх'
        verbose_name_plural = 'Баннер главной верх'


class PromotionsPageBanner(models.Model):
    objects = None
    image = models.ImageField(upload_to='banners/promotions/', verbose_name='Баннер', unique=True)
    url = models.URLField(verbose_name='url')

    class Meta:
        verbose_name = 'Баннер акции'
        verbose_name_plural = 'Баненер акции'


class CarouselBanner(models.Model):
    INTERVAL = [
        (5000, '5сек'),
        (10000, '10сек'),
        (30000, '30сек')
    ]

    objects = None
    value = models.CharField(max_length=25, unique=True, verbose_name='Баннер')
    active = models.BooleanField(default=True, verbose_name='Активна')
    interval = models.IntegerField(choices=INTERVAL, default=INTERVAL[0][0], verbose_name='Интервал')

    class Meta:
        verbose_name = 'Карусель'
        verbose_name_plural = 'Карусель'


class BackgroundBanner(models.Model):
    BACKGROUND = 'BG'
    BACKGROUND_IMAGE = 'BI'

    TYPE = [
        (BACKGROUND, 'Просто фон'),
        (BACKGROUND_IMAGE, 'Фото на фон'),
    ]

    objects = None
    banner = models.ImageField(upload_to='banners/background/', verbose_name='Баннер', unique=True)
    type = models.CharField(max_length=2, choices=TYPE, verbose_name='Тип',
                            default=BACKGROUND)
    value = models.CharField(max_length=6, default='banner')

    class Meta:
        verbose_name = 'Баннер задний фон'
        verbose_name_plural = 'Баннер задний фон'


class Movies(models.Model):
    objects = None
    title = models.CharField(max_length=100, verbose_name='Название фильма')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='movies/', verbose_name='Главная картинка', unique=True)
    link = models.URLField(verbose_name='Ссылка на трейлер')
    date_premier = models.DateField(verbose_name='Дата премьеры', null=True)
    active = models.BooleanField(default=True, verbose_name='Активен')
    type_3d = models.BooleanField(verbose_name='3D', default=False)
    type_2d = models.BooleanField(verbose_name='2D', default=True)
    type_imax = models.BooleanField(verbose_name='IMAX', default=False)
    gallery = models.ForeignKey(Gallery, null=True, on_delete=models.SET_NULL, verbose_name='Галерея картинок')
    seo_block = models.ForeignKey(SeoBlock, null=True, on_delete=models.SET_NULL, verbose_name='SEO блок')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class Cinema(models.Model):
    objects = None
    title = models.CharField(max_length=100, verbose_name='Название кинотеатра')
    description = models.TextField(verbose_name='Описание')
    conditions = models.TextField(verbose_name='Условия')
    logo = models.ImageField(upload_to='cinema/logo/', verbose_name='Логотип', unique=True)
    photo = models.ImageField(upload_to='cinema/photo/', verbose_name='Фото верхнего баннера', unique=True)
    gallery = models.ForeignKey(Gallery, null=True, on_delete=models.SET_NULL, verbose_name='Галерея картинок')
    seo_block = models.ForeignKey(SeoBlock, null=True, on_delete=models.SET_NULL, verbose_name='SEO блок')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Кинотеатр'
        verbose_name_plural = 'Кинотеатры'


class Halls(models.Model):
    objects = None
    number = models.PositiveIntegerField(verbose_name='Номер зала')
    description = models.TextField(verbose_name='Описание зала')
    layout = models.ImageField(upload_to='halls/layout',
                               verbose_name='Схема зала',
                               unique=True)
    banner = models.ImageField(upload_to='halls/banners',
                               verbose_name='Верхний баннер',
                               unique=True)
    creation_date = models.DateField(auto_now=True, null=True, verbose_name='Дата создания')
    gallery = models.ForeignKey(Gallery, null=True, on_delete=models.SET_NULL,
                                verbose_name='Галерея картинок')
    seo_block = models.ForeignKey(SeoBlock, null=True, on_delete=models.SET_NULL,
                                  verbose_name='SEO блок')
    cinemas = models.ForeignKey(Cinema, null=True, on_delete=models.SET_NULL,
                                verbose_name='Кинотеатр')

    class Meta:
        verbose_name = 'Зал'
        verbose_name_plural = 'Залы'

    def __str__(self):
        return f"{self.number}"
        # return f"Зал №{self.number}-{self.cinemas}"


class Seance(models.Model):
    objects = None
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    ticket_price = models.PositiveIntegerField(verbose_name='Цена билета')
    halls = models.ForeignKey(Halls, on_delete=models.CASCADE, verbose_name='Зал')
    movies = models.ForeignKey(Movies, on_delete=models.CASCADE, verbose_name='Фильм')

    class Meta:
        verbose_name = 'Сеанс'
        verbose_name_plural = 'Сеансы'

    def __str__(self):
        return f"Сеанс от {self.date}-{self.time}"


class Ticket(models.Model):
    objects = None
    row = models.PositiveIntegerField(verbose_name='Ряд')
    place = models.PositiveIntegerField(verbose_name='Место')
    type = models.BooleanField(default=True, verbose_name='Тип(покупка или бронь)')
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, verbose_name='Сеанс')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Посетитель')

    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'


class Events(models.Model):
    objects = None
    TYPE_EVENTS = [
        ('news', 'Новость'),
        ('promotions', 'Акция'),
    ]

    title = models.CharField(max_length=100, verbose_name='Название события')
    date_published = models.DateField(verbose_name='Дата публикации')
    is_published = models.BooleanField(default=True, verbose_name='Опубликована')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='news/', verbose_name='Главная картинка', unique=True)
    link = models.URLField(verbose_name='Ссылка на видео')
    type = models.CharField(max_length=10, choices=TYPE_EVENTS, verbose_name='Тип события')
    gallery = models.ForeignKey(Gallery, null=True, on_delete=models.SET_NULL, verbose_name='Галерея картинок')
    seo_block = models.ForeignKey(SeoBlock, null=True, on_delete=models.SET_NULL, verbose_name='SEO блок')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'


class Page(models.Model):
    objects = None
    title = models.CharField(max_length=100, verbose_name='Название')
    active = models.BooleanField(default=True, verbose_name='Активна')
    is_base = models.BooleanField(default=True, verbose_name='Базовая страница')
    creation_date = models.DateField(auto_now_add=True, null=True, verbose_name='Дата создания')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='pages/', verbose_name='Главная картинка', unique=True)
    gallery = models.ForeignKey(Gallery, null=True, on_delete=models.SET_NULL, verbose_name='Галерея картинок')
    seo_block = models.ForeignKey(SeoBlock, null=True, on_delete=models.SET_NULL, verbose_name='SEO блок')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Страницу'
        verbose_name_plural = 'Страницы'


class HomePage(models.Model):
    objects = None
    phone_number1 = models.CharField(max_length=15, verbose_name='')
    phone_number2 = models.CharField(max_length=15, verbose_name='')
    active = models.BooleanField(default=True, verbose_name='')
    creation_date = models.DateField(auto_now_add=True, null=True, verbose_name='Дата создания')
    seo_text = models.TextField(verbose_name='')
    seo_block = models.ForeignKey(SeoBlock, null=True, on_delete=models.SET_NULL, verbose_name='SEO блок')

    class Meta:
        verbose_name = 'Домашняя страницу'
        verbose_name_plural = 'Домашнюю страница'


class ContactsPage(models.Model):
    objects = None
    title = models.CharField(max_length=100, verbose_name='Название кинотеатра')
    active = models.BooleanField(default=True, verbose_name='Активна')
    creation_date = models.DateField(auto_now_add=True, null=True, verbose_name='Дата создания')
    address = models.TextField(verbose_name='Адресс')
    coordinates = models.CharField(max_length=100, verbose_name='Координаты для карты')
    logo = models.ImageField(upload_to='pages/contacts/',
                             verbose_name='Логотип',
                             unique=True)
    seo_block = models.ForeignKey(SeoBlock, null=True, on_delete=models.SET_NULL, verbose_name='SEO блок')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
