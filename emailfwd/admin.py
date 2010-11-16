from django.contrib import admin

from emailfwd.models import ForwardedEmailAddress, EmailDestination


class EmailDestinationInline(admin.TabularInline):

    model = EmailDestination


class ForwardedEmailAddressAdmin(admin.ModelAdmin):

    inlines = [
        EmailDestinationInline,
    ]


admin.site.register(ForwardedEmailAddress, ForwardedEmailAddressAdmin)
