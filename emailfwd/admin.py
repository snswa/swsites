from django.contrib import admin

from emailfwd.models import ForwardedEmailAddress, EmailDestination


class EmailDestinationInline(admin.TabularInline):

    model = EmailDestination


class ForwardedEmailAddressAdmin(admin.ModelAdmin):

    inlines = [
        EmailDestinationInline,
    ]
    list_display = ['name', 'domain']
    search_fields = ['name']
    ordering = ['name']


admin.site.register(ForwardedEmailAddress, ForwardedEmailAddressAdmin)
