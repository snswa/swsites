from django.contrib import admin

import fundraiser.models as m


r = admin.site.register
r(m.Donation)
