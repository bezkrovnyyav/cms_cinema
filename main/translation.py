from modeltranslation.translator import register, TranslationOptions
from cms.models import Movies, HomePageBanner, Cinema, Halls, Events, Page, ContactsPage, HomePage


@register(HomePageBanner)
class HomePageBannerTranslationOptions(TranslationOptions):
    fields = ('text',)


@register(Movies)
class MoviesTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Cinema)
class CinemaTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'conditions')


@register(Halls)
class HallsTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(Events)
class EventsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(ContactsPage)
class ContactsPageTranslationOptions(TranslationOptions):
    fields = ('title', 'address')


@register(HomePage)
class HomePageTranslationOptions(TranslationOptions):
    fields = ('seo_text',)
