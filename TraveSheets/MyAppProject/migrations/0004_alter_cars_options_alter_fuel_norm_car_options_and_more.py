# Generated by Django 4.1 on 2023-05-07 16:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MyAppProject', '0003_fuel_norm_car_fuel_coefficient_city_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cars',
            options={'ordering': ['reg_numb_car'], 'verbose_name': 'Автомобиль', 'verbose_name_plural': 'Автомобили'},
        ),
        migrations.AlterModelOptions(
            name='fuel_norm_car',
            options={'ordering': ['order_date'], 'verbose_name': 'Приказ установления норм расхода топлива', 'verbose_name_plural': 'Приказы установления норм расхода топлива'},
        ),
        migrations.RemoveField(
            model_name='fuel_norm_car',
            name='order_fuel',
        ),
        migrations.AddField(
            model_name='cars',
            name='company_car',
            field=models.BooleanField(default=True, verbose_name='Автомобиль компании'),
        ),
        migrations.AddField(
            model_name='cars',
            name='fuel_car',
            field=models.CharField(choices=[('80', 'АИ-80'), ('76', 'АИ-76'), ('92', 'АИ-92'), ('95', 'АИ-95'), ('98', 'АИ-98'), ('ДТ', 'ДТ'), (None, 'Марка топлива не указана')], default=None, max_length=5, verbose_name='Марка топлива'),
        ),
        migrations.AddField(
            model_name='cars',
            name='tank_car',
            field=models.FloatField(default=0, help_text='Введите объем бака установленного в автомобиле', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(300)], verbose_name='Объем бака в автомобиле'),
        ),
        migrations.AlterField(
            model_name='fuel_norm_car',
            name='fuel_coefficient_city',
            field=models.FloatField(default=0, help_text='Введите установленный повышающий коэффициент для крупных городов', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Повышающий коэффициент при передвижении в городе, %'),
        ),
        migrations.CreateModel(
            name='TravelSheetsList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sheets_date', models.DateField(verbose_name='Отчетная дата')),
                ('fuel_arrival', models.FloatField(default=0, help_text='Введите количество залитого топлива за день в бак автомобиля', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Поступление топлива, литров')),
                ('fuel_used', models.FloatField(default=0, verbose_name='Использовано топлива')),
                ('fuel_remain_date', models.FloatField(default=0, verbose_name='Остаток топлива')),
                ('fuel_economy', models.FloatField(default=0, verbose_name='Экономия(+) / Перерасход(-)')),
                ('odometer_day_start', models.FloatField(default=0, verbose_name='Показания одометра на начало дня')),
                ('odometer_on_day', models.FloatField(default=0, verbose_name='Показания одометра за день')),
                ('odometer_day_finish', models.FloatField(default=0, verbose_name='Показания одометра на конец дня')),
                ('sheets_car', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='MyAppProject.cars', unique_for_date=models.DateField(verbose_name='Отчетная дата'), verbose_name='Автомобиль')),
            ],
            options={
                'verbose_name': 'Путевой лист',
                'verbose_name_plural': 'Путевые листы',
                'ordering': ['-sheets_date'],
            },
        ),
    ]
