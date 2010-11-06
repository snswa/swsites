from django.contrib import admin

import swfundraiser.models as m


r = admin.site.register
r(m.Donation)
