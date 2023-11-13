from django.urls import path
from .views import HomePageView

urlpatterns = [
    # home page
    path('', HomePageView.as_view(), name='main'),
    # end

]
