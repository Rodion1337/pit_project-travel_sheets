from django.urls import path
from MyAppProject import views

app_name = 'MyApp'
urlpatterns = [
    path('<int:year>/<int:month>/', views.TravelSheetsListTable, name='TravelSheetsList'),
    path('<int:pk>/update/', views.SheetsList_DayUpdateView.as_view(), name='day-upd'),
    path('', views.TravelSheetsAll, name='index'),
]
