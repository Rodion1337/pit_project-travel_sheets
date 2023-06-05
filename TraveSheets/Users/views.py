from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from requests import request

from .forms_users import LoginForm

# Create your views here.


# def register(request):
#     if request.method == "POST":  # проверка типа обращения
#         form = UserCreationForm(request.POST)  # получение данных
#         # next_url = request.POST.get('next') if request.POST.get('next') != '' else 'index/'
#         next_url = request.POST.get(
#             "next", "/index"
#         )  # элегантная альтернатива моему "топорному" варианту
#         # next_url = request.POST.get('next') or reverse('HW23:index') (3й вариант)
#         if form.is_valid():  # проверка валидности
#             form.save()
#             username = form.cleaned_data.get("username")
#             messages.success(request, f"Создан аккаунт {username}!")
#             return HttpResponseRedirect(next_url)
#     else:
#         form = UserCreationForm()
#     return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":  # проверка типа обращения
        form = LoginForm(request.POST)  # получение данных
        next_url = (
            request.POST.get("next")
            if request.POST.get("next")
            else reverse_lazy("MyApp:index")
        )
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(next_url)
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("Users:login")


class UserChangePassword(PasswordChangeView):
    template_name = "users/change_password.html"
    success_url = reverse_lazy("MyApp:index")
    success_message = "Смена пароля прошла успешно"
