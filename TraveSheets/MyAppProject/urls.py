from django.urls import path
from MyAppProject import views

app_name = "MyApp"
urlpatterns = [
    path("", views.TravelSheetsAll, name="index"),
    path(
        "<int:year>/<int:month>/", views.TravelSheetsListTable, name="TravelSheetsList"
    ),
    path("<int:pk>/update/", views.SheetsList_DayUpdateView.as_view(), name="day-upd"),
    path(
        "<int:year>/<int:month>/print",
        views.TravelSheetsListTable_print,
        name="TravelSheetPrint",
    ),
]
