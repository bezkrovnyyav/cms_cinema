from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin


# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass

@admin.register(TemplatesMailing)
class TemplatesMailingAdmin(admin.ModelAdmin):
    pass

@admin.register(SeoBlock)
class SeoBlockAdmin(admin.ModelAdmin):
    pass


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    pass


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    pass

@admin.register(CarouselBanner)
class CarouselBannerAdmin(admin.ModelAdmin):
    pass

@admin.register(HomePageBanner)
class HomePageBannerAdmin(admin.ModelAdmin):
    pass


@admin.register(PromotionsPageBanner)
class PromotionsPageBannerAdmin(admin.ModelAdmin):
    pass


@admin.register(BackgroundBanner)
class BackgroundBannerAdmin(admin.ModelAdmin):
    pass


@admin.register(Movies)
class MoviesAdmin(admin.ModelAdmin):
    pass


@admin.register(Halls)
class HallsAdmin(admin.ModelAdmin):
    pass


@admin.register(Seance)
class SeanceAdmin(admin.ModelAdmin):
    pass


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    pass


@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    pass


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    pass


@admin.register(ContactsPage)
class ContactsPageAdmin(admin.ModelAdmin):
    pass
