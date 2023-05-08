from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from MyAppProject.models import TravelSheetsList, Cars, User
from django.contrib.auth.decorators import login_required
from requests import request

# Create your views here.

# @login_required(login_url='users:login')
# class TravelSheetsListCreate(CreateView):
#     model = TravelSheetsList
#     template_name = 'TravelSheetsCreate.html'
#     form_class = UserTravelSheetsList
#     # success_url = reverse_lazy('HW23:games')


@login_required(login_url='users:login')
def TravelSheetsList(request, month, year):
    # game_odj = get_object_or_404(Games, slug = game_slug)
    user_id = request.user.id
    car = Cars.objects.get(driver_car=user_id)
    sheets = TravelSheetsList.objects.filter(sheets_car=car).filter(sheets_date__year=year, sheets_date__month=month)
    return render(request, 'TravelSheetsList.html', context={'days' : sheets,})
