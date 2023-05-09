from django.dispatch import receiver
from django.db.models.signals import pre_save
from MyAppProject.models import TravelSheetsList, Fuel_norm_car
from datetime import timedelta
from MyAppProject.functions import remath_used_fuel


@receiver(pre_save, sender=TravelSheetsList)
def update_info_on_month(sender, instance, **kwargs):
    """
    Данный сигнал предназначен для перехвата в момент сохранения данных за
    день, для пересчета ряда показателей и их отражения в
    """

    car = instance.sheets_car
    year, month = instance.sheets_date.year, instance.sheets_date.month
    sheets_mount = TravelSheetsList.objects.filter(
        sheets_car=car, sheets_date__year=year,
        sheets_date__month=month).order_by('sheets_date')
    sheet_last_approve = TravelSheetsList.objects.filter(
        sheets_car=car, status_approve=True).order_by('sheets_date').last()
    for i in sheets_mount:
        # получение последнего приказа устанавливающего норму расхода топлива
        # на день пересчета или ранее
        sheets_date = i.sheets_date
        fuel_norms_all = Fuel_norm_car.objects.filter(
            order_car=car, order_date__lte=sheets_date).order_by(
                'order_date').last()
        fuel_norm = fuel_norms_all.fuel_consumption
        fuel_coefficient_city = fuel_norms_all.fuel_coefficient_city
        fuel_coefficient_cold = fuel_norms_all.fuel_coefficient_cold

        #  определение предшествующего дня для получения исходных данных
        if sheet_last_approve.sheets_date.month == (sheets_date - timedelta(1)).month:
            yesterday_day_fuel = sheet_last_approve.fuel_day_fihish
            yesterday_day_odometer = sheet_last_approve.odometer_day_finish
        else:
            sheet_yesterday = TravelSheetsList.objects.get(sheets_date=(
                sheets_date - timedelta(1)))
            yesterday_day_fuel = sheet_yesterday.fuel_day_fihish
            yesterday_day_odometer = sheet_yesterday.odometer_day_finish

        #  передача данных для расчета показателей и получение данных
        odometer_day_finish, fuel_used_on_day, fuel_day_finish, fuel_day_economy = remath_used_fuel(
            fuel_norm,fuel_coefficient_city, fuel_coefficient_cold,
            i.fuel_arrival, yesterday_day_fuel, yesterday_day_odometer,
            i.odometer_on_day_in_city,i.odometer_on_day_out_city,
            i.used_coefficient_cold)
        fuel_used_on_day_norm = fuel_used_on_day-fuel_day_economy
        odometer_on_day = i.odometer_on_day_in_city+i.odometer_on_day_out_city

        #  обновление данных за пересчитанный день
        TravelSheetsList.objects.filter(sheets_car=car, sheets_date=i.sheets_date).update(
            fuel_used=fuel_used_on_day_norm, fuel_used_actually=fuel_used_on_day,
            fuel_day_start=yesterday_day_fuel, fuel_day_fihish=fuel_day_finish,
            fuel_economy=fuel_day_economy, odometer_day_start=yesterday_day_odometer,
            odometer_on_day=odometer_on_day,
            odometer_day_finish=odometer_day_finish, sheets_status=False)
