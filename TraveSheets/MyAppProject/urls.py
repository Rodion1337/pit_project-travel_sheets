from django.urls import path
from MyAppProject import views

app_name = 'MyApp'
urlpatterns = [
    path('<int:year>/<int:month>', views.TravelSheetsList, name='TravelSheetsList'),
]
