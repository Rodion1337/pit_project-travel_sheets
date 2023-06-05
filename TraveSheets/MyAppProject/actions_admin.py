import datetime

from django.contrib import admin
from django.http import HttpResponse


@admin.action(description="Проставления статуса согласования")
def status_approve(self, request, queryset):
    for i in queryset.order_by("sheets_date"):
        car = i.sheets_car
        date_sheets = i.sheets_date
        self.model.objects.filter(
            sheets_car=car, sheets_date__lte=date_sheets, status_approve=False
        ).update(status_approve=True)

    self.message_user(request, "Действие выполнено")


@admin.action(description="выгрузка данных в формате .csv")
def export_as_csv(self, request, queryset):
    import csv

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename={}.csv;".format(
        datetime.datetime.now()
    )
    response.write("\ufeff".encode("utf8"))
    writer = csv.writer(response)
    from django.db.models import Field

    writer.writerow(
        [
            field.name
            for field in self.model._meta.get_fields()
            if isinstance(field, Field)
        ]
    )
    for i in queryset:
        writer.writerow(
            [
                getattr(i, field.name)
                for field in i._meta.get_fields()
                if isinstance(field, Field)
            ]
        )
    return response
