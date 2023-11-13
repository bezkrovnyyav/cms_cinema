import json
from datetime import timedelta

from django.conf import settings
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, DetailView
from cms.models import HomePageBanner, CarouselBanner, PromotionsPageBanner, BackgroundBanner, Movies, HomePage, Seance, \
    Cinema, Halls, Images, Ticket, SeoBlock, Events, ContactsPage, Page


# Create your views here.

# Home page


class HomePageView(ListView):
    model = HomePage
    template_name = 'main/pages/home/index.html'

    def get_context_data(self, **kwargs):
        today = datetime.now()
        movies = Movies.objects.all()
        context = super(HomePageView, self).get_context_data()
        context['today'] = today
        context['list_movie_today'] = Seance.objects.filter(date=today).select_related('movies').distinct('movies')
        context['list_movie_premier'] = movies.filter(date_premier__range=[today, today + timedelta(days=7)])
        context['list_movie_soon'] = movies.filter(date_premier__gt=today).order_by('date_premier')
        context['home_page_data'] = HomePage.objects.all().first()
        context['promotion_banner'] = PromotionsPageBanner.objects.all()
        context['background'] = BackgroundBanner.objects.all().first()
        context['header_banner'] = HomePageBanner.objects.all()
        context['banner_carousel'] = CarouselBanner.objects.filter(value='home_page_banner').first()
        context['promotion_carousel'] = CarouselBanner.objects.filter(value='promotions_page_banner').first()
        context['seo_block'] = SeoBlock.objects.filter(id=context['home_page_data'].seo_block_id).first()
        return context


# Home page end

