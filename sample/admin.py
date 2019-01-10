from django.contrib import admin
from sample.models.person import Person
from sample.models.address import Address

admin.site.register(Person)
admin.site.register(Address)
