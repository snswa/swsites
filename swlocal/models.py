from django.db import models

from zipcodes.models import County, ZipCode


def teams_for_zip_code(zip_code):
    regional_teams = set()
    try:
        zip_code = ZipCode.objects.get(zip_code=zip_code)
    except ZipCode.DoesNotExist:
        pass
    else:
        regional_teams.update(zip_code.teams.all())
        # Also look for teams that match the ZIP code's county.
        county = County.objects.get(name=zip_code.county)
        regional_teams.update(county.teams.all())
    return regional_teams
