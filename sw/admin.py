from django.contrib import admin

from sw.models import Interest


class InterestAdmin(admin.ModelAdmin):

    list_display = ('name', 'order')


admin.site.register(Interest, InterestAdmin)
