from django.db import models

from teams.models import Team


class ZipCode(models.Model):
    # import data from http://federalgovernmentzipcodes.us/free-zipcode-database.csv

    zip_code = models.CharField(max_length=5, db_index=True, unique=True)
    city = models.CharField(max_length=40)
    county = models.CharField(max_length=40, db_index=True, blank=True)
    state = models.CharField(max_length=2, db_index=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    long = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    teams = models.ManyToManyField('teams.Team', related_name='zip_codes', through='TeamZipCode')

    class Meta:
        ordering = ('county', 'city', 'zip_code')

    def __unicode__(self):
        return u'{county} county: {city}, {state} {zip}'.format(
            county=self.county.title(),
            city=self.city.title(),
            state=self.state.upper(),
            zip=self.zip_code,
        )

    def save(self, *args, **kwargs):
        self.city = self.city.upper()
        self.state = self.state.upper()
        if self.county:
            self.county = self.county.upper()
        super(ZipCode, self).save(*args, **kwargs)
        if self.county and County.objects.filter(name=self.county).count() == 0:
            County(name=self.county).save()


class County(models.Model):

    name = models.CharField(max_length=40, unique=True)
    teams = models.ManyToManyField('teams.Team', related_name='counties', through='TeamCounty')

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name.title()

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(County, self).save(*args, **kwargs)

    def zip_codes(self):
        return ZipCode.objects.filter(county=self.name)


class TeamZipCode(models.Model):

    zip_code = models.ForeignKey(ZipCode)
    team = models.ForeignKey(Team)

    class Meta:
        unique_together = (
            ('zip_code', 'team'),
        )

    def __unicode__(self):
        return u'{0} -> {1}'.format(self.zip_code, self.team)


class TeamCounty(models.Model):

    county = models.ForeignKey(County)
    team = models.ForeignKey(Team)

    class Meta:
        unique_together = (
            ('county', 'team'),
        )

    def __unicode__(self):
        return u'{0} -> {1}'.format(self.county, self.team)
