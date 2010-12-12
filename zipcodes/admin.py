from django.contrib import admin

from teams.admin import TeamAdmin
from teams.models import Team

from zipcodes.models import County, ZipCode, TeamCounty, TeamZipCode


# -- inlines --


class CountyInline(admin.TabularInline):

    model = TeamCounty
    extra = 1


class ZipCodeInline(admin.TabularInline):

    model = TeamZipCode
    extra = 1


# -- admins --


class ZipCodeAdmin(admin.ModelAdmin):

    list_display = ('county', 'zip_code', 'city', 'state', 'lat', 'long')


class ExtendedTeamAdmin(TeamAdmin):

    inlines = [
        CountyInline,
        ZipCodeInline,
    ] + TeamAdmin.inlines


admin.site.register(ZipCode, ZipCodeAdmin)

admin.site.unregister(Team)
admin.site.register(Team, ExtendedTeamAdmin)
