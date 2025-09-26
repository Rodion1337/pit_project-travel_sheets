from calendar import monthrange
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from MyAppProject.forms_app import SheetsList_DayUpdate
from MyAppProject.models import Cars, TravelSheetsList, User, fuel_mark
from requests import request
from Users.models import Profile
from MyAppProject.functions import gen_month_days

# Create your views here.


class SheetsList_DayUpdateView(UpdateView):
    # форма для обновления данных
    model = TravelSheetsList
    template_name = "TravelSheetsUpdate.html"
    form_class = SheetsList_DayUpdate

    def get_success_url(self):
        return self.request.GET.get("next")


@login_required(login_url="Users:login")
def TravelSheetsListTable(request, year, month):
    # Вывод талицы данных за месяц для обновления или дополнения
    user_id = request.user.id
    car = get_object_or_404(Cars, driver_car=user_id)

    for i in fuel_mark:
        if i[0] == car.fuel_car:
            fuel_mark_print = i[1]

    sheets = TravelSheetsList.objects.filter(
        sheets_car=car, sheets_date__year=year, sheets_date__month=month
        ).order_by("sheets_date")

    if len(sheets) != monthrange(year, month)[1]:
        # print(f'начата генерация {len(sheets)}')
        if gen_month_days(sheets, car, year, month) == 'complied':
            sheets = TravelSheetsList.objects.filter(
            sheets_car=car, sheets_date__year=year, sheets_date__month=month
            ).order_by("sheets_date")
            # print(f'генерация окончена {len(sheets)}')
            return render(
            request,
            "TravelSheetsList.html",
            context={"days": sheets, "fuel_mark": fuel_mark_print},
            )
    else:
        # print('без генерации')
        return render(
        request,
        "TravelSheetsList.html",
        context={"days": sheets, "fuel_mark": fuel_mark_print},
        )




@login_required(login_url="Users:login")
def TravelSheetsAll(request):
    # вывод путевых листов за каждый месяц в разрезе годов и месяцев
    user_id = request.user.id
    car = get_object_or_404(Cars, driver_car=user_id)
    treetslist_all = (
        TravelSheetsList.objects.filter(sheets_car=car, sheets_date__day=28)
        .values_list("sheets_date__year", "sheets_date__month")
        .order_by("-sheets_date")
    )
    last_travel_sheets = (
        TravelSheetsList.objects.filter(sheets_car=car).order_by("sheets_date").last()
    )
    # print("last_travel_sheets", last_travel_sheets)
    next_month = (
        last_travel_sheets.sheets_date + timedelta(days=1)
        if last_travel_sheets
        else Profile.objects.get(user=user_id).last_approve + timedelta(days=1)
    )
    up_month = f"{next_month.year}/{next_month.month}"
    year_month_list = {}
    for i in treetslist_all:
        if i[0] in year_month_list:
            x = year_month_list[i[0]]
            x.append(i[1])
        else:
            year_month_list.setdefault(
                i[0],
                [
                    i[1],
                ],
            )
    return render(
        request,
        "index.html",
        context={"year_month_list": year_month_list, "up_month": up_month},
    )


def TravelSheetsListTable_print(request, year, month):
    user_id = request.user.id
    car = get_object_or_404(Cars, driver_car=user_id)
    for i in fuel_mark:
        if i[0] == car.fuel_car:
            fuel_mark_print = i[1]
    sheets = TravelSheetsList.objects.filter(
        sheets_car=car, sheets_date__year=year, sheets_date__month=month
    ).order_by("sheets_date")
    day_on_month = monthrange(year, month)[1]
    if len(sheets) != day_on_month:
        for i in range(1, day_on_month + 1):
            # print(i,month,year,car,'day_on_month', day_on_month)
            sheets.get_or_create(sheets_date=(date(year, month, i)), sheets_car=car)
    return render(
        request,
        "TravelSheetsList_print.html",
        context={"days": sheets, "fuel_mark": fuel_mark_print},
    )
