from django.contrib import admin
from MyAppProject.models import Cars, Fuel_norm_car

# Register your models here.


class CarsAdmin(admin.ModelAdmin):
    pass


class Fuel_norm_carAdmin(admin.ModelAdmin):
    pass


admin.site.register(Cars, CarsAdmin)
admin.site.register(Fuel_norm_car, Fuel_norm_carAdmin)
