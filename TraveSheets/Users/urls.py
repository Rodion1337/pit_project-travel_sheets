from django.urls import path
from Users import views

# from django.contrib.auth.views import LoginView


app_name = "Users"
urlpatterns = [
    # path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("change/", views.UserChangePassword.as_view(), name="UserChangePassword"),
]
