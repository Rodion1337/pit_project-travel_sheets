from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView
from requests import request
import bootstrap4
from .forms_users import LoginForm

# Create your views here.


def register(request):
    if request.method == 'POST':                                    #проверка типа обращения
        form = UserCreationForm(request.POST)                       #получение данных
        # next_url = request.POST.get('next') if request.POST.get('next') != '' else 'index/'
        next_url = request.POST.get('next', '/index') #элегантная альтернатива моему "топорному" варианту
        # next_url = request.POST.get('next') or reverse('HW23:index') (3й вариант)
        if form.is_valid():                                         #проверка валидности
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт {username}!')
            print(next_url)
            return HttpResponseRedirect(next_url)
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':                                    #проверка типа обращения
        form = LoginForm(request.POST)                              #получение данных
        next_url = request.POST.get('next', '/index')
        # print(next_url)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(next_url)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('HW23:index')

class UserChangePassword(PasswordChangeView):
    template_name = 'users/change_password.html'
    # print(request)
    success_url = reverse_lazy('HW23:games')
    success_message = 'Смена пароля прошла успешно'