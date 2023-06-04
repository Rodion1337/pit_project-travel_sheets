from django.contrib import admin
from MyAppProject.models import Cars, Fuel_norm_car, TravelSheetsList
from MyAppProject.actions_admin import export_as_csv, status_approve

# Register your models here.


class CarsAdmin(admin.ModelAdmin):
    search_fields = ('name_car', 'reg_numb_car', 'driver_car', 'fuel_car', 'company_car')
    fields = ('name_car', 'reg_numb_car', 'driver_car', 'fuel_car', 'company_car')
    list_display = ('name_car', 'reg_numb_car', 'driver_car', 'fuel_car', 'company_car')
    list_filter = ('name_car', 'reg_numb_car', 'driver_car', 'fuel_car', 'company_car')


class Fuel_norm_carAdmin(admin.ModelAdmin):
    search_fields = ('order_number', 'order_date', 'order_car')
    list_display = ('order_number', 'order_date', 'order_car')
    list_filter = ('order_number', 'order_date', 'order_car')


class TravelSheetsListAdmin(admin.ModelAdmin):
    search_fields = ('sheets_car', 'sheets_date', 'status_approve', 'sheets_car.driver_car')
    list_display = ('sheets_car', 'sheets_date', 'status_approve')
    list_filter = ('sheets_car', 'sheets_date', 'status_approve')
    actions = [export_as_csv, status_approve]

admin.site.register(Cars, CarsAdmin)
admin.site.register(Fuel_norm_car, Fuel_norm_carAdmin)
admin.site.register(TravelSheetsList, TravelSheetsListAdmin)
