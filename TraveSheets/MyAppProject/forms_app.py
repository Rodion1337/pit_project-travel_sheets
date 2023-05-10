from django.forms import ModelForm
from MyAppProject.models import TravelSheetsList

class SheetsList_DayUpdate(ModelForm):
    class Meta:
        model = TravelSheetsList
        fields = ('fuel_arrival', 'odometer_on_day_in_city', 'odometer_on_day_out_city', 'travel_itinerary_start', 'travel_itinerary_finish', 'used_coefficient_cold')
        exclude = ('sheets_date', 'sheets_car', 'fuel_used',)

