from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator

# Create your models here.


class Cars(models.Model):
    '''
    Модель автомобиля по которому будет производиться отчёт
    за использованное топливо:
    name_car - марка авто
    reg_numb_car - номер регистрационных знаков выданных в ГАИ
    driver_car - водитель ответственный за авто
    fuel_car - марка топлива
    company_car - флаг отношения машины к компании
    '''
    fuel_mark = (
        ('80', 'АИ-80'),
        ('76', 'АИ-76'),
        ('92', 'АИ-92'),
        ('95', 'АИ-95'),
        ('98', 'АИ-98'),
        ('ДТ', 'ДТ'),
        (None, 'Марка топлива не указана'),
        )
    name_car = models.CharField(verbose_name='Марка авто', max_length=30)
    reg_numb_car = models.CharField(verbose_name='Регистрационные знаки', unique=True, max_length=10)
    driver_car = models.ForeignKey(User, verbose_name='Водитель', on_delete=models.PROTECT)
    fuel_car = models.CharField(verbose_name='Марка топлива', max_length=5, choices=fuel_mark, default=None)
    company_car = models.BooleanField(verbose_name='Автомобиль компании', default=True)
    tank_car = models.FloatField(verbose_name='Объем бака в автомобиле', default=0, validators=[MinValueValidator(0), MaxValueValidator(300)], help_text='Введите объем бака установленного в автомобиле')

    def __str__(self) -> str:
        return self.name_car + ' ' + self.reg_numb_car

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ['reg_numb_car']


class Fuel_norm_car(models.Model):
    '''
    Модель для хранения полной информации о приказе и присвоенных
    нормах расхода топлива
    '''
    def order_directory_path(instance, filename: str) -> str:
        '''
        функция для присвоения пути хранения приказа с каталогизацией
        по авто и номеру приказа
        '''
        return 'order_{0}/{1}.pdf'.format(instance.order_car.reg_numb_car,
                                          instance.order_number).replace(' ',
                                                                         '_')

    order_number = models.CharField(verbose_name='Номер приказа', unique=True, max_length=15)
    order_date = models.DateField(verbose_name='Дата приказа',)
    order_car = models.ForeignKey(Cars, verbose_name='Автомобиль', on_delete=models.PROTECT, unique_for_date='order_date')

    order_upd = models.DateField(verbose_name='Дата обновления', auto_now=True, editable=False)
    order_create = models.DateField(verbose_name='Дата создания', auto_now_add=True, editable=False)

    order_file = models.FileField(verbose_name='Скан приказа', upload_to=order_directory_path, max_length=100, validators=[FileExtensionValidator(['pdf'])], unique_for_date='order_date')

    fuel_consumption = models.FloatField(verbose_name='Норма расхода топлива', default=0, help_text='Введите расход топлива в литрах на 100км')
    fuel_coefficient_city = models.FloatField(verbose_name='Повышающий коэффициент при передвижении в городе, %', default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],help_text='Введите установленный повышающий коэффициент для крупных городов')
    fuel_coefficient_cold = models.FloatField(verbose_name='Повышающий коэффициент на заморозки, %', default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text='Введите установленный повышающий коэффициент для низких температур')


    def __str__(self) -> str:
        return 'приказ №' + self.order_number + ' от ' + str(self.order_date.strftime("%d.%m.%Y"))

    class Meta:
        verbose_name = 'Приказ установления норм расхода топлива'
        verbose_name_plural = 'Приказы установления норм расхода топлива'
        ordering = ['order_date']


class TravelSheetsList(models.Model):
    sheets_date = models.DateField(verbose_name='Отчетная дата',)
    sheets_car = models.ForeignKey(Cars, verbose_name='Автомобиль', on_delete=models.PROTECT, unique_for_date='sheets_date', editable=False)
    fuel_arrival = models.FloatField(verbose_name='Поступление топлива, литров', default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],help_text='Введите количество залитого топлива за день в бак автомобиля')
    fuel_used = models.FloatField(verbose_name='Использовано топлива', default=0, editable=False)
    fuel_remain_date = models.FloatField(verbose_name='Остаток топлива', default=0, editable=False)
    fuel_economy = models.FloatField(verbose_name='Экономия(+) / Перерасход(-)', default=0, editable=False)
    odometer_day_start = models.FloatField(verbose_name='Показания одометра на начало дня', default=0, editable=False)
    odometer_on_day = models.FloatField(verbose_name='Показания одометра за день', default=0)
    odometer_day_finish = models.FloatField(verbose_name='Показания одометра на конец дня', default=0, editable=False)
    sheets_status = models.BooleanField(verbose_name='Статус требуется ли пересчитать данные за день', default=True, editable=False)
    status_aprove = models.BooleanField(verbose_name='Статус согласования бухгалтером', default=False, editable=False)

    def __str__(self) -> str:
        return (f'Путевой лист на {self.sheets_car.name_car} гос.номер {self.sheets_car.reg_numb_car} за {self.sheets_date.strftime("%d.%m.%Y")}')

    class Meta:
        verbose_name = 'Путевой лист'
        verbose_name_plural = 'Путевые листы'
        ordering = ['-sheets_date']
