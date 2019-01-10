from django.db import models
from sample.models.base import Entity


class Address(Entity):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)
