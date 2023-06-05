from django.apps import AppConfig


class MyappprojectConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "MyAppProject"

    def ready(self):
        from MyAppProject import signals
