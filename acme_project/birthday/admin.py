from django.contrib import admin

from . import models


class BirthdayAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'description',
        'birthday',
    )


admin.site.register(models.Birthday, BirthdayAdmin)
admin.site.register(models.Tag)
