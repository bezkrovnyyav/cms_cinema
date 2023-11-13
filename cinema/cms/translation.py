from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(HomePage)
class HomePageTranslationOptions(TranslationOptions):
    fields = ('seo_text', )


