from datetime import timedelta

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from MyAppProject.functions import remath_used_fuel
from MyAppProject.models import Fuel_norm_car, TravelSheetsList

# @receiver(post_save, sender=TravelSheetsList)
# def first_update_approve(sender, instance, created, **kwargs):
#     if created:
#         car = instance.sheets_car
#         date = instance.sheets_date
#         sheets_mount = TravelSheetsList.objects.filter(sheets_car=car).order_by('sheets_date').first


@receiver(post_save, sender=TravelSheetsList)
def update_info_on_month(sender, instance, **kwargs):
    """
    Данный сигнал предназначен для перехвата в момент сохранения данных за
    день, для пересчета ряда показателей и их отражения в БД
    """

    # получение первичного набора данных сигнала
    car = instance.sheets_car
    year_signal = instance.sheets_date.year
    month_signal = instance.sheets_date.month
    status_approve_signal = instance.status_approve
    sheets_date_signal = instance.sheets_date

    # получение набора дней за определенный месяц и год, с обновленной даты
    sheets_mount = TravelSheetsList.objects.filter(
        sheets_car=car, sheets_date__gte=sheets_date_signal
    ).order_by("sheets_date")

    if not status_approve_signal:
        for i in sheets_mount:
            # цикл обработки каждого дня месяца

            # получение последнего приказа устанавливающего норму расхода топлива
            # на день пересчета или ранее
            sheets_date = i.sheets_date
            fuel_norms_all = (
                Fuel_norm_car.objects.filter(order_car=car, order_date__lte=sheets_date)
                .order_by("order_date")
                .last()
            )
            fuel_norm = fuel_norms_all.fuel_consumption
            fuel_coefficient_city = fuel_norms_all.fuel_coefficient_city
            fuel_coefficient_cold = fuel_norms_all.fuel_coefficient_cold

            #  получение данных на конец предыдущего дня
            sheet_yesterday = TravelSheetsList.objects.filter(sheets_car=car)

            # проверка месяца, на полноту в нем дней (если не все созданы),
            # в случаи недостачи - создаются отсутствующие
            if len(sheet_yesterday) == 1:
                sheet_yesterday = TravelSheetsList.objects.create(
                    sheets_car=car,
                    sheets_date=(sheets_date - timedelta(days=1)),
                    status_approve=True,
                )
                # print("create obj", sheet_yesterday)
            else:
                # print(
                #     False,
                #     len(sheet_yesterday) == 0,
                #     len(sheet_yesterday),
                #     sheet_yesterday,
                # )
                sheet_yesterday = TravelSheetsList.objects.filter(
                    sheets_car=car, sheets_date__lt=sheets_date
                ).first()
            yesterday_day_fuel = sheet_yesterday.fuel_day_fihish
            yesterday_day_odometer = sheet_yesterday.odometer_day_finish

            #  передача данных для расчета показателей и получение данных
            (
                odometer_day_finish,
                fuel_used_on_day,
                fuel_day_finish,
                fuel_day_economy,
            ) = remath_used_fuel(
                fuel_norm,
                fuel_coefficient_city,
                fuel_coefficient_cold,
                i.fuel_arrival,
                yesterday_day_fuel,
                yesterday_day_odometer,
                i.odometer_on_day_in_city,
                i.odometer_on_day_out_city,
                i.used_coefficient_cold,
            )
            fuel_used_on_day_norm = round(fuel_used_on_day - fuel_day_economy, 2)
            odometer_on_day = i.odometer_on_day_in_city + i.odometer_on_day_out_city

            #  обновление данных за пересчитанный день
            day_update = TravelSheetsList.objects.get(
                sheets_car=car, sheets_date=sheets_date
            )

            day_update.fuel_used = fuel_used_on_day_norm
            day_update.fuel_used_actually = fuel_used_on_day
            day_update.fuel_day_start = yesterday_day_fuel
            day_update.fuel_day_fihish = fuel_day_finish
            day_update.fuel_economy = fuel_day_economy
            day_update.odometer_day_start = yesterday_day_odometer
            day_update.odometer_on_day = odometer_on_day
            day_update.odometer_day_finish = odometer_day_finish
            TravelSheetsList.objects.bulk_update(
                [day_update],
                [
                    "fuel_used",
                    "fuel_used_actually",
                    "fuel_day_start",
                    "fuel_day_fihish",
                    "fuel_economy",
                    "odometer_day_start",
                    "odometer_on_day",
                    "odometer_day_finish",
                ],
            )
