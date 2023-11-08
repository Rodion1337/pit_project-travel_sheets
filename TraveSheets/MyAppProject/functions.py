from MyAppProject.models import TravelSheetsList

def remath_used_fuel(
    fuel_norm: float,
    fuel_coefficient_city: float,
    fuel_coefficient_cold: float,
    fuel_arrival: float,
    yesterday_day_fuel: float,
    yesterday_day_odometer: float,
    odometer_on_day_in_city: float,
    odometer_on_day_out_city: float,
    used_coefficient_cold: bool,
) -> tuple:
    """Функция предназначена для расчета исходя из вводных данных показателей
    одометра на конец дня, пробег за день, остаток топлива на конец дня и
    показатель экономии/пережога топлива

    Args:
        fuel_norm (float): норма расхода топлива, л/100км\n
        fuel_coefficient_city (float): Повышающий коэффициент при передвижении
        в городе, %\n
        fuel_coefficient_cold (float): Повышающий коэффициент на заморозки, %\n
        fuel_arrival (float): заправлено топлива за день\n
        yesterday_day_fuel (float): остаток топлива на конец прошлого / начало
        расчетного дня\n
        yesterday_day_odometer (float): показания одометра на конец прошлого /
        начало расчетного дня\n
        odometer_on_day_in_city (float): количество км, пробега по городу\n
        odometer_on_day_out_city (float): количество км, пробега за городом\n
        used_coefficient_cold (bool): Статус применения повышающего
        коэффициента на заморозки\n

    Returns:
        tuple: odometer_day_finish(float), fuel_used_on_day(float),
        fuel_day_finish(float), fuel_day_economi(float)
    """
    fuel_norm_city, fuel_norm_out_city = math_fuel_norm(
        fuel_norm, fuel_coefficient_city, fuel_coefficient_cold, used_coefficient_cold
    )

    used_fuel_in_city = round(odometer_on_day_in_city * fuel_norm_city / 100, 2)
    used_fuel_out_city = round(odometer_on_day_out_city * fuel_norm_out_city / 100, 2)
    fuel_used_on_day = round(used_fuel_in_city + used_fuel_out_city, 2)
    if (yesterday_day_fuel + fuel_arrival) >= fuel_used_on_day:
        fuel_day_finish = round(yesterday_day_fuel + fuel_arrival - fuel_used_on_day, 2)
        fuel_day_economi = 0
    else:
        fuel_day_finish = 0
        fuel_day_economi = round(
            fuel_used_on_day - (yesterday_day_fuel + fuel_arrival), 2
        )
    odometer_day_finish = round(
        yesterday_day_odometer + (odometer_on_day_in_city + odometer_on_day_out_city), 2
    )
    return (odometer_day_finish, fuel_used_on_day, fuel_day_finish, fuel_day_economi)


def math_fuel_norm(
    fuel_norm: float,
    fuel_coefficient_city: float,
    fuel_coefficient_cold: float,
    used_coefficient_cold: bool,
) -> tuple:
    """Функция предназначена для расчета норм расхода топлива в городе и
    за городом

    Args:
        fuel_norm (float): норма расхода топлива, л/100км\n
        fuel_coefficient_city (float): Повышающий коэффициент при передвижении
        в городе, %\n
        fuel_coefficient_cold (float): Повышающий коэффициент на заморозки, %\n
        used_coefficient_cold (bool): Статус применения повышающего
        коэффициента на заморозки\n

    Returns:
        tuple: fuel_norm_city (float), fuel_norm_out_city (float)
    """
    fuel_norm_city = fuel_norm * (
        1
        + (fuel_coefficient_city + fuel_coefficient_cold * used_coefficient_cold) / 100
    )
    fuel_norm_out_city = fuel_norm * (
        1 + (fuel_coefficient_cold * used_coefficient_cold / 100)
    )
    return fuel_norm_city, fuel_norm_out_city


def gen_month_days(sheets:object, car: object, year: int, month: int):
    """Данная функция предназначена для создание в БД записей дней (дат) не достающих за месяц.

    Args:
        sheets - дополняемый месяц (объект)
        user_id - числовой идентификатор пользователя
        year - год
        month - месяц
    """
    from calendar import monthrange
    from datetime import date, timedelta

    day_on_month = monthrange(year, month)[1]
    if len(sheets) != day_on_month:
        for i in range(1, day_on_month + 1):
            sheets.get_or_create(sheets_date=(date(year, month, i)), sheets_car=car)
        sheets = TravelSheetsList.objects.filter(
            sheets_car=car, sheets_date__year=year, sheets_date__month=month
        ).order_by("sheets_date")
    return "complied"

# print(math_fuel_norm(10, 5, 10, True))  # -> (11.5, 11.0)
# print(math_fuel_norm(10, 5, 10, False))  # -> (10.5, 10)
# print(remath_used_fuel(10, 5, 10, 20, 15.5, 13057, 100, 200, True))  # -> (13357, 33.5, 2.0, 0)
