from django.forms import Form


class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)
