from uuid import uuid4
from django.db import models
from django.utils import timezone


class PersonManager(models.Manager):

    def get_current(self, entity_id, effective):
        return self.filter(effective__lte=effective).order_by('effective', 'created').last()

    def new(self, entity_id, effective, **kwargs):
        old = self.get_current(entity_id, effective) or Person(entity_id=entity_id)
        old.pk = None
        old.effective = effective
        old.created = timezone.now()
        for k, v in kwargs.items():
            setattr(old, k, v)
        old.save()
        return old


class Person(models.Model):
    entity_id = models.CharField(max_length=36, default=uuid4)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    effective = models.DateTimeField()
    created = models.DateTimeField(default=timezone.now)

    objects = PersonManager()

    def __str__(self):
        return "{}:{}:{}".format(self.entity_id, self.effective, self.created)

    class Meta:
        unique_together = ('entity_id', 'effective', 'created')
