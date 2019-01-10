from django.db import models
from django.contrib.postgres.fields import ArrayField
from sample.models.base import Entity
from sample.models.address import Address


class Person(Entity):
    """
    there could be a metaclass to clean up the need to have a field and property both
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    address_entity_ids = ArrayField(models.CharField(max_length=36), default=list)

    @property
    def addresses(self):
        return Address.objects.get_current_list(self.address_entity_ids, self.effective)
