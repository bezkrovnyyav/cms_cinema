import json
from datetime import timedelta
from math import floor
from babel.dates import format_date
from celery.result import AsyncResult
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.db.models import Count
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from user.forms import UserUpdateForm
from user.models import User
from .task import send_mailing
from .forms import CmsHallsForm, CmsCinemasForm, CmsHomePageUpdateForm, CmsTemplatesMailingForm, \
    CmsPageUpdateForm, CmsContactsPageUpdateForm, CmsHomePageBannerForm, CmsCarouselBannerForm, \
    CmsEventsForm, CmsImageForm, CmsSeoBlockForm, CmsMoviesForm, CmsBackgroundBannerForm, CmsPromotionsPageBannerForm
from .models import Gallery, Images, HomePageBanner, PromotionsPageBanner, CarouselBanner, \
    BackgroundBanner, Movies, Cinema, Halls, Seance, Events, Page, HomePage, ContactsPage, Client, TemplatesMailing


# Base class

class BaseCmsView(View, AccessMixin):
    """Check user is staff."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('login')
        else:
            if not request.user.is_staff:
                messages.error(request, f'Вы вошли в систему как {request.user.email}, '
                                        f'однако у вас недостаточно прав для просмотра данной страницы')
                return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class BaseCmsUpdate(UpdateView, BaseCmsView):
    """Base view for updating an existing object."""

    def form_valid(self, form):
        context = self.get_context_data()
        seo_block_form = context['seo_block_form']
        if 'gallery_formset' in context:
            gallery_formset = context['gallery_formset']
            if seo_block_form.is_valid() and gallery_formset.is_valid():
                seo_block_form.save()
                obj = form.save(commit=False)
                for image in gallery_formset:
                    if image.cleaned_data:
                        if image.is_valid():
                            images = image.save(commit=False)
                            images.gallery = obj.gallery
                            images.save()
                gallery_formset.save()
                obj.save()
                messages.success(self.request, 'Данные обновлены')
                return super().form_valid(form)
            return self.form_invalid(form)
        else:
            if seo_block_form.is_valid():
                seo_block_form.save()
                obj = form.save(commit=False)
                obj.save()
                messages.success(self.request, 'Данные обновлены')
                return super().form_valid(form)
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
        return super().form_invalid(form)


class BaseCmsCreate(CreateView, BaseCmsView):
    def form_invalid(self, form):
        messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
        return super().form_invalid(form)


# Base class end


# Statistics
class CmsStatisticsView(BaseCmsView):
    @staticmethod
    def get(request):
        users = User.objects.filter(is_staff=False)
        date = datetime.now()
        days = 7
        date_range = [date, date + timedelta(days=days)]
        client = Client.objects.filter(date__range=[date - timedelta(days=days), date])
        seance = Seance.objects.values('date').filter(date__range=date_range)
        seance_list, mobile, pc, every = [], [], [], []
        for i in range(days):
            date_for_seance = datetime.now() + timedelta(days=i)
            date_for_client = datetime.now() - timedelta(days=i)
            every.append({'is_every_count': client.filter(date=date_for_client).count()})
            mobile.append(
                {'is_mobile_count': client.values('is_mobile').exclude(is_mobile=False).filter(
                    date=date_for_client).count()})
            pc.append(
                {'is_pc_count': client.values('is_pc').exclude(is_pc=False).filter(
                    date=date_for_client).count()})
            seance_list.append(
                {'seance_count': seance.filter(date=date_for_seance).count()})

        context = {
            'date_range': json.dumps(
                [format_date((datetime.today() - timedelta(days=day)), "d MMM", locale='ru') for day in range(days)]
            ),
            'is_mobile': json.dumps(mobile),
            'is_pc': json.dumps(pc),
            'is_every': json.dumps(every),
            'users_count': users.count(),
            'count_seance': json.dumps(seance_list),
            'seance': json.dumps(
                [{'date': date} for date in [format_date((datetime.today() + timedelta(days=day)),
                                                         "d MMM", locale='ru') for day in range(days)]]
            ),
            'gender': json.dumps([
                {'women': users.filter(gender='f').count(),
                 'men': users.filter(gender='m').count()}
            ]),
            'top_movies': json.dumps(list(
                Seance.objects.values('movies__title').annotate(top=Count('movies__title')).order_by('movies')[:5]
            )),
        }
        return render(request, 'cms/pages/statistics.html', context)


# Statistics end


# banners
class CmsBannersCard(UpdateView, BaseCmsView):
    model = BackgroundBanner
    template_name = 'cms/pages/banners.html'
    success_url = reverse_lazy('banners')
    home_page_banner = modelformset_factory(HomePageBanner, form=CmsHomePageBannerForm,
                                            extra=0, can_delete=True)
    promotions_page_banner = modelformset_factory(PromotionsPageBanner, form=CmsPromotionsPageBannerForm,
                                                  extra=0, can_delete=True)

    def get_object(self, queryset=None):
        obj, _ = self.model.objects.get_or_create(value='banner')
        return obj

    def get_form(self, form_class=None):
        if form_class is None:
            return CmsBackgroundBannerForm(self.request.POST or None,
                                           self.request.FILES or None,
                                           instance=self.object)

    def get_context_data(self, *args, **kwargs):
        home_page_banner_carousel, _ = CarouselBanner.objects.get_or_create(
            value='home_page_banner')
        promotions_page_banner_carousel, _ = CarouselBanner.objects.get_or_create(
            value='promotions_page_banner')
        context = super(CmsBannersCard, self).get_context_data()

        context['home_page_banner_carousel'] = \
            CmsCarouselBannerForm(self.request.POST or None,
                                  prefix='home_page_banner_carousel',
                                  instance=home_page_banner_carousel)
        context['promotions_page_banner_carousel'] = \
            CmsCarouselBannerForm(self.request.POST or None,
                                  prefix='promotions_page_banner_carousel',
                                  instance=promotions_page_banner_carousel)
        context['home_page_banner'] = self.home_page_banner(self.request.POST or None,
                                                            self.request.FILES or None,
                                                            queryset=HomePageBanner.objects.all())

        context['promotions_page_banner'] = self.promotions_page_banner(self.request.POST or None,
                                                                        self.request.FILES or None,
                                                                        prefix='promotions',
                                                                        queryset=PromotionsPageBanner.objects.all())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        banner = context['home_page_banner']
        promotions_page_banner = context['promotions_page_banner']
        home_page_banner_carousel = context['home_page_banner_carousel']
        promotions_page_banner_carousel = context['promotions_page_banner_carousel']
        if banner.is_valid() and home_page_banner_carousel.is_valid() and \
                promotions_page_banner.is_valid() and promotions_page_banner_carousel.is_valid():
            obj = form.save(commit=False)
            banner.save()
            promotions_page_banner.save()
            home_page_banner_carousel.save()
            promotions_page_banner_carousel.save()
            obj.save()
            messages.success(self.request, 'Данные обновлены')
            return super().form_valid(form)
        return self.form_invalid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
        return super().form_invalid(form)


# banners end

# movies

class CmsMoviesListView(ListView, BaseCmsView):
    model = Movies
    template_name = 'cms/pages/movies/list_movie.html'

    def get_queryset(self):
        movies = self.model.objects.filter(date_premier__lte=datetime.today())
        movies_coming_soon = self.model.objects.filter(date_premier__gt=datetime.today())
        queryset = {
            'movies': movies,
            'movies_coming_soon': movies_coming_soon
        }
        return queryset


class CmsMoviesUpdateView(BaseCmsUpdate):
    model = Movies
    template_name = 'cms/pages/movies/update_movie.html'
    form_class = CmsMoviesForm
    success_url = reverse_lazy('list_movie')
    formset = modelformset_factory(Images, form=CmsImageForm, extra=0, can_delete=True)

    def get_context_data(self, *args, **kwargs):
        context = super(CmsMoviesUpdateView, self).get_context_data()
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None,
                                                    instance=self.object.seo_block)
        context['gallery_formset'] = self.formset(self.request.POST or None,
                                                  self.request.FILES or None,
                                                  queryset=Images.objects.filter(gallery=self.object.gallery))

        return context


class CmsMoviesCreateView(BaseCmsCreate):
    model = Movies
    template_name = 'cms/pages/movies/create_movie.html'
    form_class = CmsMoviesForm
    success_url = reverse_lazy('list_movie')
    formset = modelformset_factory(Images, form=CmsImageForm, extra=0, can_delete=True)

    def get_context_data(self, *args, **kwargs):
        context = super(CmsMoviesCreateView, self).get_context_data()
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None)
        context['gallery_formset'] = self.formset(self.request.POST or None,
                                                  self.request.FILES or None,
                                                  queryset=Images.objects.none())

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        seo_block_form = context['seo_block_form']
        gallery_formset = context['gallery_formset']
        if seo_block_form.is_valid() and gallery_formset.is_valid():
            seo_block_form.save()
            movie = form.save(commit=False)
            movie.seo_block = seo_block_form.instance
            gallery = Gallery.objects.create(title=movie.title)
            movie.gallery = get_object_or_404(Gallery, id=gallery.id)
            for image in gallery_formset:
                if image.cleaned_data:
                    if image.is_valid():
                        images = image.save(commit=False)
                        images.gallery = movie.gallery
                        images.save()
            gallery_formset.save()
            movie.save()
            messages.success(self.request, 'Добавлен новый фильм')
            return super().form_valid(form)
        return self.form_invalid(form)


class CmsMoviesDeleteView(DeleteView):
    model = Movies

    def get_success_url(self):
        messages.success(self.request, f'Фильм  {self.object.title} удалён!')
        return reverse_lazy('list_movie')


# movies end


# cinemas
class CmsCinemasListView(ListView, BaseCmsView):
    model = Cinema
    context_object_name = 'cinemas'
    template_name = 'cms/pages/cinemas/list_cinemas.html'

    def get_queryset(self):
        return super(CmsCinemasListView, self).get_queryset().order_by('id')


class CmsCinemasUpdateView(BaseCmsUpdate):
    model = Cinema
    template_name = 'cms/pages/cinemas/update_cinemas.html'
    form_class = CmsCinemasForm
    success_url = reverse_lazy('cinemas')
    formset = modelformset_factory(Images, form=CmsImageForm, extra=0, can_delete=True)

    def get_context_data(self, *args, **kwargs):
        context = super(CmsCinemasUpdateView, self).get_context_data()
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None,
                                                    instance=self.object.seo_block)
        context['gallery_formset'] = self.formset(self.request.POST or None,
                                                  self.request.FILES or None,
                                                  queryset=Images.objects.filter(gallery=self.object.gallery))
        context['list_halls'] = Halls.objects.filter(cinemas=self.object).order_by('id')
        context['cinemas_id'] = self.object.id
        return context


class CmsCinemasCreateView(BaseCmsCreate):
    model = Cinema
    template_name = 'cms/pages/cinemas/create_cinemas.html'
    success_url = reverse_lazy('cinemas')
    form_class = CmsCinemasForm
    formset = modelformset_factory(Images, form=CmsImageForm, extra=0, can_delete=True)

    def get_context_data(self, *args, **kwargs):
        context = super(CmsCinemasCreateView, self).get_context_data()
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None)
        context['gallery_formset'] = self.formset(self.request.POST or None,
                                                  self.request.FILES or None,
                                                  queryset=Images.objects.none())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        seo_block_form = context['seo_block_form']
        gallery_formset = context['gallery_formset']
        if seo_block_form.is_valid() and gallery_formset.is_valid():
            seo_block_form.save()
            cinemas = form.save(commit=False)
            cinemas.seo_block = seo_block_form.instance
            gallery = Gallery.objects.create(title=cinemas.title)
            cinemas.gallery = get_object_or_404(Gallery, id=gallery.id)
            for image in gallery_formset:
                if image.cleaned_data:
                    if image.is_valid():
                        images = image.save(commit=False)
                        images.gallery = cinemas.gallery
                        images.save()
            gallery_formset.save()
            cinemas.save()
            messages.success(self.request, 'Добавлен новый кинотеатр')
            return super().form_valid(form)
        return self.form_invalid(form)


class CmsCinemasDeleteView(DeleteView):
    """
    Delete cinemas
    """
    model = Cinema

    def get_success_url(self):
        messages.success(self.request, f'Кинотеатр  {self.object.title} удалён!')
        return reverse_lazy('cinemas')

    def get(self, request, *args, **kwargs):
        messages.error(request, 'Объект защищен от удаления!')
        return redirect('cinemas')


# cinemas end

# halls


class CmsHallsCreateView(BaseCmsCreate):
    """
    Create Halls
    """
    model = Halls
    template_name = 'cms/pages/halls/create_halls.html'
    form_class = CmsHallsForm
    formset = modelformset_factory(Images, form=CmsImageForm, extra=0, can_delete=True)

    def get_success_url(self):
        return reverse_lazy('cinemas_edit', kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, *args, **kwargs):
        context = super(CmsHallsCreateView, self).get_context_data()
        context['cinemas_id'] = self.kwargs.get('pk')
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None)
        context['gallery_formset'] = self.formset(self.request.POST or None,
                                                  self.request.FILES or None,
                                                  queryset=Images.objects.none())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        seo_block_form = context['seo_block_form']
        gallery_formset = context['gallery_formset']
        if seo_block_form.is_valid() and gallery_formset.is_valid():
            seo_block_form.save()
            halls = form.save(commit=False)
            halls.seo_block = seo_block_form.instance
            gallery = Gallery.objects.create(title=f"Зал-{halls.number}")
            halls.gallery = get_object_or_404(Gallery, id=gallery.id)
            halls.cinemas = get_object_or_404(Cinema, id=self.kwargs.get('pk'))
            for image in gallery_formset:
                if image.cleaned_data:
                    if image.is_valid():
                        images = image.save(commit=False)
                        images.gallery = halls.gallery
                        images.save()
            gallery_formset.save()
            halls.save()
            messages.success(self.request, 'Добавлен новый зал')
            return super().form_valid(form)
        return self.form_invalid(form)


class CmsHallsUpdateView(BaseCmsUpdate):
    model = Halls
    template_name = 'cms/pages/halls/update_halls.html'
    form_class = CmsHallsForm
    formset = modelformset_factory(Images, form=CmsImageForm, extra=0, can_delete=True)

    def get_success_url(self):
        return reverse_lazy('cinemas_edit', kwargs={'pk': self.kwargs.get('cinemas_id')})

    def get_context_data(self, *args, **kwargs):
        context = super(CmsHallsUpdateView, self).get_context_data()
        context['cinemas_id'] = self.kwargs.get('cinemas_id')
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None,
                                                    instance=self.object.seo_block)
        context['gallery_formset'] = self.formset(self.request.POST or None,
                                                  self.request.FILES or None,
                                                  queryset=Images.objects.filter(gallery=self.object.gallery))
        return context


class CmsHallsDeleteView(DeleteView):
    model = Halls

    def get_success_url(self):
        messages.success(self.request, f'Зал № {self.object.number} удалён!')
        return reverse_lazy('cinemas_edit', kwargs={'pk': self.kwargs.get('cinemas_id')})

    def get(self, request, *args, **kwargs):
        messages.error(request, 'Объект защищен от удаления!')
        return redirect('cinemas')


# halls end


# Events
class CmsPromotionListView(ListView, BaseCmsView):
    """
    list of promotion
    """
    model = Events
    context_object_name = 'promotions'
    template_name = 'cms/pages/promotions/list_promotions.html'


class CmsNewsListView(ListView, BaseCmsView):
    """
    list of news
    """
    model = Events
    context_object_name = 'news'
    template_name = 'cms/pages/news/list_news.html'


class CmsEventsCreateView(BaseCmsCreate):
    """
    Create a new events(news/promotions)
    """
    model = Events
    template_name = 'cms/pages/promotions/create_events.html'
    form_class = CmsEventsForm
    formset = modelformset_factory(Images, form=CmsImageForm, extra=0, can_delete=True)

    def get_success_url(self):
        url_request = self.request.get_full_path()
        if url_request == '/cms/promotions/create/':
            return reverse_lazy('promotions')
        else:
            return reverse_lazy('news')

    def get_context_data(self, *args, **kwargs):
        context = super(CmsEventsCreateView, self).get_context_data()
        context['get_path'] = self.request.get_full_path()
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None)
        context['gallery_formset'] = self.formset(self.request.POST or None,
                                                  self.request.FILES or None,
                                                  queryset=Images.objects.none())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        seo_block_form = context['seo_block_form']
        gallery_formset = context['gallery_formset']
        if seo_block_form.is_valid() and gallery_formset.is_valid():
            seo_block_form.save()
            promotion = form.save(commit=False)
            promotion.seo_block = seo_block_form.instance
            if self.request.get_full_path() == '/cms/promotions/create/':
                promotion.type = 'promotions'
            else:
                promotion.type = 'news'
            gallery = Gallery.objects.create(title=promotion.title)
            promotion.gallery = get_object_or_404(Gallery, id=gallery.id)
            for image in gallery_formset:
                if image.cleaned_data:
                    if image.is_valid():
                        images = image.save(commit=False)
                        images.gallery = promotion.gallery
                        images.save()
            gallery_formset.save()
            promotion.save()
            messages.success(self.request, 'Данные обновлены')
            return super().form_valid(form)
        return self.form_invalid(form)


class CmsEventsUpdateView(BaseCmsUpdate):
    """
    Update events(news/promotions)
    """
    model = Events
    template_name = 'cms/pages/promotions/update_events.html'
    form_class = CmsEventsForm
    formset = modelformset_factory(Images, form=CmsImageForm, extra=0, can_delete=True)

    def get_success_url(self):
        type_events = self.object.type
        if type_events == 'promotions':
            return reverse_lazy('promotions')
        else:
            return reverse_lazy('news')

    def get_context_data(self, *args, **kwargs):
        context = super(CmsEventsUpdateView, self).get_context_data()
        context['type_object'] = self.object.type
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None,
                                                    instance=self.object.seo_block)
        context['gallery_formset'] = self.formset(self.request.POST or None,
                                                  self.request.FILES or None,
                                                  queryset=Images.objects.filter(gallery=self.object.gallery))

        return context


class CmsEventsDeleteView(DeleteView):
    """
    Delete events(news/promotions)
    """
    model = Events
    template_name = 'cms/pages/promotions/list_promotions.html'

    def get_success_url(self):
        type_events = self.object.type
        if type_events == 'promotions':
            messages.success(self.request, 'Акция удалена!')
            return reverse_lazy('promotions')
        else:
            messages.success(self.request, 'Новость удалена!')
            return reverse_lazy('news')


# Events end


# pages
class CmsPagesListView(ListView, BaseCmsView):
    model = Page
    template_name = 'cms/pages/page/list_pages.html'

    def get_queryset(self):
        context = {
            'base_pages': self.model.objects.filter(is_base=True),
            'home_page': HomePage.objects.all(),
            'contacts_pages': ContactsPage.objects.all()[0],
            'pages': self.model.objects.filter(is_base=False)
        }
        return context


class CmsPageCreateView(BaseCmsCreate):
    model = Page
    template_name = 'cms/pages/page/create_page.html'
    success_url = reverse_lazy('pages')
    form_class = CmsPageUpdateForm
    formset = modelformset_factory(Images, form=CmsImageForm, extra=0, can_delete=True)

    def get_context_data(self, *args, **kwargs):
        context = super(CmsPageCreateView, self).get_context_data()
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None)
        context['gallery_formset'] = self.formset(self.request.POST or None,
                                                  self.request.FILES or None,
                                                  queryset=Images.objects.none())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        seo_block_form = context['seo_block_form']
        gallery_formset = context['gallery_formset']
        if seo_block_form.is_valid() and gallery_formset.is_valid():
            seo_block_form.save()
            page = form.save(commit=False)
            page.seo_block = seo_block_form.instance
            page.is_base = False
            gallery = Gallery.objects.create(title=page.title)
            page.gallery = get_object_or_404(Gallery, id=gallery.id)
            for image in gallery_formset:
                if image.cleaned_data:
                    if image.is_valid():
                        images = image.save(commit=False)
                        images.gallery = page.gallery
                        images.save()
            gallery_formset.save()
            page.save()
            messages.success(self.request, 'Добавлена новая страница')
            return super().form_valid(form)
        return self.form_invalid(form)


class CmsPageUpdateView(BaseCmsUpdate):
    """
    Update a CMS pages
    """
    model = Page
    template_name = 'cms/pages/page/update_page.html'
    success_url = reverse_lazy('pages')
    form_class = CmsPageUpdateForm
    formset = modelformset_factory(Images, form=CmsImageForm, extra=0, can_delete=True)

    def get_context_data(self, *args, **kwargs):
        context = super(CmsPageUpdateView, self).get_context_data()
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None,
                                                    instance=self.object.seo_block)
        context['gallery_formset'] = self.formset(self.request.POST or None,
                                                  self.request.FILES or None,
                                                  queryset=Images.objects.filter(gallery=self.object.gallery))
        return context


class CmsPageDeleteView(DeleteView):
    """
    Delete new pages
    """
    model = Page

    def get_success_url(self):
        messages.success(self.request, f'{self.object.title} удалена!')
        return reverse_lazy('pages')

    def get(self, request, *args, **kwargs):
        messages.error(request, 'Объект защищен от удаления!')
        return redirect('pages')


class CmsHomePageUpdateView(BaseCmsUpdate):
    """
    Update a CMS home page
    """
    model = HomePage
    template_name = 'cms/pages/page/main_page.html'
    success_url = reverse_lazy('pages')
    form_class = CmsHomePageUpdateForm

    def get_context_data(self, *args, **kwargs):
        context = super(CmsHomePageUpdateView, self).get_context_data()
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None,
                                                    instance=self.object.seo_block)
        return context


class CmsContactsUpdateView(UpdateView):
    """
        Update a CMS contacts page
    """
    model = ContactsPage
    template_name = 'cms/pages/page/contacts_page.html'

    def get_success_url(self):
        return reverse_lazy('pages')

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = modelformset_factory(ContactsPage, form=CmsContactsPageUpdateForm, extra=0)
        return form_class(self.request.POST or None,
                          self.request.FILES or None,
                          queryset=ContactsPage.objects.all())

    def get_context_data(self, *args, **kwargs):
        context = super(CmsContactsUpdateView, self).get_context_data()
        context['seo_block_form'] = CmsSeoBlockForm(self.request.POST or None,
                                                    instance=self.object.seo_block)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        seo_block_form = context['seo_block_form']
        if seo_block_form.is_valid():
            seo_block_form.save()
            for contacts in form:
                if contacts.cleaned_data:
                    if contacts.is_valid():
                        contacts = contacts.save(commit=False)
                        contacts.seo_block = seo_block_form.instance
                        contacts.save()
            form.save()
            messages.success(self.request, 'Данные обновлены')
            return super().form_valid(form)
        return self.form_invalid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
        return super().form_invalid(form)


# pages end


# users
class CmsUserListView(ListView, BaseCmsView):
    model = User
    context_object_name = 'users'
    template_name = 'cms/pages/users/list_users.html'


class CmsUserUpdateView(UpdateView):
    """
    Update User if request.user.is_superuser
    """
    model = User
    template_name = 'cms/pages/users/update_user.html'
    success_url = reverse_lazy('users')
    form_class = UserUpdateForm

    def form_valid(self, form):
        if self.request.user.is_superuser:
            self.object = form.save()
            username = form.cleaned_data['username']
            messages.success(self.request, f'Данные пользователя {username} обновлены')
            return super().form_valid(form)
        messages.warning(self.request, 'Для редактирования пользователей нужно иметь права администратора')
        return redirect('users')

    def form_invalid(self, form):
        messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
        return super().form_invalid(form)


class CmsUserDeleteView(DeleteView):
    """
    Delete users if request.user.is_superuser
    """
    model = User
    success_url = reverse_lazy('users')
    template_name = 'cms/pages/users/list_users.html'

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            messages.success(request, 'Пользователь удалён!')
            return self.delete(request, *args, **kwargs)
        messages.warning(request, 'Для удаления пользователей нужно иметь права администратора')
        return redirect('users')


# users end
# https://docs.djangoproject.com/en/4.2/releases/3.1/#id2
# Mailing to email
def mailing(request):
    if request.user.is_staff:
        if request.is_ajax():
            users_list = request.POST.get('users').split(',')
            template_id = request.POST['template_id']
            file = request.FILES.get('file_template')
            if file:
                task = send_mailing.delay(users_list, file.read().decode())
                template = TemplatesMailing(file=file)
                template.save()
                return JsonResponse({'task_id': task.task_id}, status=202)
            else:
                template = get_object_or_404(TemplatesMailing, id=template_id).file.read().decode()
                task = send_mailing.delay(users_list, template)
                return JsonResponse({'task_id': task.task_id}, status=202)
        context = {
            'users': User.objects.all(),
            'templates': TemplatesMailing.objects.all().order_by('-id')[:5],
            'form': CmsTemplatesMailingForm(request.POST or None,
                                            request.FILES or None,
                                            initial={'type_mailing': 'all'})
        }
        return render(request, 'cms/pages/mailing/mailing.html', context)
    return redirect('login')


def task_status(request, task_id):
    """
    Progress task
    """
    task = AsyncResult(task_id)
    if task.state == 'FAILURE' or task.state == 'PENDING':
        response = {
            'task_id': task_id,
            'state': task.state,
            'progression': '0',
        }
        return JsonResponse(response, status=200)
    current = task.info.get('current', 0)
    total = task.info.get('total', 1)
    progression = floor((int(current) / int(total)) * 100)
    response = {
        'task_id': task_id,
        'state': task.state,
        'progression': progression,
    }
    return JsonResponse(response, status=200)


class TemplatesMailingDelete(DeleteView):
    model = TemplatesMailing
    success_url = reverse_lazy('mailing')
    template_name = 'cms/pages/mailing/mailing.html'

# Mailing to email end
