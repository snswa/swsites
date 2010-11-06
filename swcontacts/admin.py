from django.contrib import admin
from django.contrib.contenttypes import generic

import swcontacts.models as m


class AddressInline(generic.GenericTabularInline):

    model = m.Address
    extra = 1


class PhoneInline(generic.GenericTabularInline):

    model = m.Phone
    extra = 1


class EmailInline(generic.GenericTabularInline):

    model = m.Email
    extra = 1


class RelationshipInline(generic.GenericTabularInline):

    model = m.Relationship
    ct_field = 'whom_content_type'
    ct_fk_field = 'whom_object_id'
    extra = 1


class PersonAdmin(admin.ModelAdmin):

    inlines = [
        EmailInline,
        PhoneInline,
        AddressInline,
        RelationshipInline,
        ]


class OrganizationAdmin(admin.ModelAdmin):

    inlines = [
        EmailInline,
        PhoneInline,
        AddressInline,
        RelationshipInline,
        ]


r = admin.site.register
r(m.Person, PersonAdmin)
r(m.Organization, OrganizationAdmin)
