from django.urls import path
from django.contrib.auth.views import LoginView
from MyAppProject import views
from django.views.decorators.cache import cache_page

app_name = 'MyApp'
urlpatterns = [
    path('/', views.index, name='index'),
]
