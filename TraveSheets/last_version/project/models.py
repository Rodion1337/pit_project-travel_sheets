from django.db import models
from users.models import User

# Create your models here.

class Cars(models.Model):
    '''
    Модель автомобиля по которому будет производиться отчёт за использованное топливо:
    name_car - марка авто
    reg_numb_car - номер регистрационных знаков выданных в ГАИ
    driver_car - водитель ответственный за авто
    '''
    name_car = models.CharField(verbose_name='Марка авто', max_length=30)
    reg_numb_car = models.TextField(verbose_name='Регистрационные знаки', unique=True,)
    driver_car = models.ForeignKey(User, verbose_name='Водитель', on_delete=models.PROTECT,)
    
    def __str__(self) -> str:
        return self.name_car + ' ' + self.reg_numb_car



class Fuel_norm_car(models.Model):
    '''
    Модель для хранения полной информации о приказе и присвоенных нормах расхода топлива
    '''
    def order_directory_path(instance, filename):
        '''функция для присвоения пути хранения приказа с каталогизацией по авто и номеру приказа'''
        return 'order_{0}/{1}.pdf'.format(instance.order_car.reg_numb_car, instance.order_number).replace(' ', '_')
    
    fuel=(
        ('80', 'АИ-80'),
        ('76', 'АИ-76'),
        ('92', 'АИ-92'),
        ('95', 'АИ-95'),
        ('98', 'АИ-98'),
        ('ДТ', 'ДТ'),
        (None, 'Марка топлива не указана'),
    )
    order_number = models.TextField(verbose_name='Номер приказа',)
    order_date = models.DateField(verbose_name='Дата приказа',)
    order_car = models.ForeignKey(Cars, verbose_name='Автомобиль', on_delete=models.PROTECT,)
    order_upd = models.DateField(verbose_name='Дата обновления', auto_now=True, )
    order_create = models.DateField(verbose_name='Дата создания', auto_now_add=True, )
    order_file = models.FileField(verbose_name='Скан приказа', upload_to=order_directory_path, max_length=100, )
    order_fuel = models.CharField(verbose_name='Марка топлива', max_length=5, choices=fuel, default=None, )
    fuel_consumption = models.FloatField(verbose_name='Норма расхода топлива', default=0)
    
    def __str__(self) -> str:
        return 'приказ №' + self.order_number + ' от ' + str(self.order_date)