# Generated by Django 4.1 on 2023-05-06 23:53

import MyAppProject.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MyAppProject', '0002_alter_fuel_norm_car_order_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='fuel_norm_car',
            name='fuel_coefficient_city',
            field=models.FloatField(default=0, help_text='Введите установленный повышающий коэффициент для крупных городов', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Повышающий коэффициент на "город", %'),
        ),
        migrations.AddField(
            model_name='fuel_norm_car',
            name='fuel_coefficient_cold',
            field=models.FloatField(default=0, help_text='Введите установленный повышающий коэффициент для низких температур', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Повышающий коэффициент на заморозки, %'),
        ),
        migrations.AlterField(
            model_name='fuel_norm_car',
            name='fuel_consumption',
            field=models.FloatField(default=0, help_text='Введите расход топлива в литрах на 100км', verbose_name='Норма расхода топлива'),
        ),
        migrations.AlterField(
            model_name='fuel_norm_car',
            name='order_car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='MyAppProject.cars', unique_for_date=models.DateField(verbose_name='Дата приказа'), verbose_name='Автомобиль'),
        ),
        migrations.AlterField(
            model_name='fuel_norm_car',
            name='order_file',
            field=models.FileField(unique_for_date=models.DateField(verbose_name='Дата приказа'), upload_to=MyAppProject.models.Fuel_norm_car.order_directory_path, validators=[django.core.validators.FileExtensionValidator(['pdf'])], verbose_name='Скан приказа'),
        ),
        migrations.AlterField(
            model_name='fuel_norm_car',
            name='order_number',
            field=models.TextField(max_length=15, unique=True, verbose_name='Номер приказа'),
        ),
    ]