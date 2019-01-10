from uuid import uuid4
from django.db import models
from django.utils import timezone


class EntityManager(models.Manager):

    def get_current(self, entity_id, effective):
        return self.filter(entity_id=entity_id, effective__lte=effective).order_by('effective', 'created').last()

    def get_current_list(self, entity_ids, effective):
        sql = """
            SELECT *
            FROM {table} a
            WHERE a.entity_id = ANY(%(entities)s)
            AND a.effective = (SELECT max(aa.effective)
                FROM {table} aa
                WHERE aa.effective <= %(effective)s
                AND aa.entity_id = a.entity_id
            )
            AND a.created = (SELECT max(bb.created)
                FROM {table} bb
                WHERE bb.effective <= %(effective)s
                AND bb.entity_id = a.entity_id
            )
            ;
        """.format(table=self.model._meta.db_table)
        params = {"entities": entity_ids, "effective": effective}
        return self.raw(sql, params=params)

    def new(self, entity_id, effective, **kwargs):
        old = self.get_current(entity_id, effective) or self.model(entity_id=entity_id)
        old.pk = None
        old.effective = effective
        old.created = timezone.now()
        for k, v in kwargs.items():
            setattr(old, k, v)
        old.save()
        return old


class Entity(models.Model):
    entity_id = models.CharField(max_length=36, default=uuid4)
    effective = models.DateTimeField()
    created = models.DateTimeField(default=timezone.now)

    objects = EntityManager()

    class Meta:
        abstract = True
        unique_together = ('entity_id', 'effective', 'created')

    def __str__(self):
        return "{}:{}:{}".format(self.entity_id, self.effective, self.created)
