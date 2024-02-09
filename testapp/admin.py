from django.contrib import admin

from testapp.models import AModel, AModelEditForm


class AModelAdmin(admin.ModelAdmin):
    form = AModelEditForm


admin.site.register(AModel, AModelAdmin)
