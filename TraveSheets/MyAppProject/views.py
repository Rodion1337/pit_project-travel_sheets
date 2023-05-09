from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from MyAppProject.models import TravelSheetsList, Cars, User
from django.contrib.auth.decorators import login_required
from requests import request
from calendar import monthrange
from MyAppProject.models import fuel_mark
from datetime import date

# Create your views here.

# @login_required(login_url='users:login')
# class TravelSheetsListCreate(CreateView):
#     model = TravelSheetsList
#     template_name = 'TravelSheetsCreate.html'
#     form_class = UserTravelSheetsList
#     # success_url = reverse_lazy('HW23:games')


@login_required(login_url='users:login')
def TravelSheetsListTable(request, year, month):
    # game_odj = get_object_or_404(Games, slug = game_slug)
    user_id = request.user.id
    car = Cars.objects.get(driver_car=user_id)
    for i in fuel_mark:
        if i[0]==car.fuel_car:
            fuel_mark_print = i[1]
    sheets = TravelSheetsList.objects.filter(sheets_car=car, sheets_date__year=year, sheets_date__month=month).order_by('sheets_date')
    day_on_month = monthrange(year, month)[1]
    if len(sheets) != day_on_month:
        print(f'не хватает дней, найдено {len(sheets)}, должно быть {day_on_month}')
        for i in range(1,day_on_month+1):
            sheets.get_or_create(sheets_date=(date(year,month,i)), sheets_car=car)
    return render(request, 'TravelSheetsList.html', context={'days':sheets, 'fuel_mark':fuel_mark_print})
