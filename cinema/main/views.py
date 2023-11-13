from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'main/pages/home/index.html')


def get_movie_card(request):
    return render(request, 'main/pages/poster/movie_card.html')


def get_poster(request):
    return render(request, 'main/pages/poster/poster.html')


def get_soon(request):
    return render(request, 'main/pages/poster/soon.html')


def get_about_cinema(request):
    return render(request, 'main/pages/about_cinema/about_cinema.html')


def get_contacts(request):
    return render(request, 'main/pages/about_cinema/contacts.html')


def get_cafe_bar(request):
    return render(request, 'main/pages/about_cinema/cafe_bar.html')


def get_children_room(request):
    return render(request, 'main/pages/about_cinema/children_room.html')


def get_news(request):
    return render(request, 'main/pages/about_cinema/news.html')


def get_vip(request):
    return render(request, 'main/pages/about_cinema/vip.html')


def get_advertising(request):
    return render(request, 'main/pages/about_cinema/advertising.html')


def get_mobile_application(request):
    return render(request, 'main/pages/about_cinema/mobile_application.html')

























