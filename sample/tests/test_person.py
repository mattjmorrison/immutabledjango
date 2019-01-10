"""

Theory: make a django model immutable - turn off deletes & updates to the database entirely
the model will have an effective date and a created date....

Person, for example...

class Person
  ... person fields ...
  effective_date
  created_date
  entity_id

The entity_id will always be the same for that person. (this is what external systems can use to reference the person)

if you want that Person as of today - get the latest created_date row....

if you want that Person as of another date get the latest created_date row with the latest effetive date row prior to the requested date

to "replace a row" -> same effective date with newer created date

to "delete a row" -> not a thing - just remove the thing using that entity_id


"""

from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from sample.models import Person


class ImmutablePersonTests(TestCase):

    def test_create_person_and_get_person(self):
        p = Person.objects.create(first_name='Matt', effective=timezone.now())
        self.assertEqual(p, Person.objects.get(first_name='Matt'))

    def test_create_new_version_of_same_person_and_get_current(self):
        p1 = Person.objects.create(first_name='Matt', effective=timezone.now() - timedelta(days=10))
        p2 = Person.objects.create(first_name='Matt', effective=timezone.now() + timedelta(days=10), entity_id=p1.entity_id)
        self.assertEqual(p1, Person.objects.get_current(p2.entity_id, timezone.now()))
        self.assertEqual(p2, Person.objects.get_current(p2.entity_id, timezone.now() + timedelta(days=20)))
        self.assertEqual(None, Person.objects.get_current(p2.entity_id, timezone.now() - timedelta(days=20)))

    def test_can_create_new_version(self):
        p1 = Person.objects.create(first_name='Matt', effective=timezone.now() - timedelta(days=10))
        p2 = Person.objects.new(p1.entity_id, timezone.now() + timedelta(days=10), first_name='Matthew')
        self.assertEqual("Matt", Person.objects.get_current(p1.entity_id, timezone.now()).first_name)
        self.assertEqual("Matthew", Person.objects.get_current(p1.entity_id, timezone.now() + timedelta(days=11)).first_name)

    def test_can_create_new_version_when_prior_version_does_not_exist(self):
        p1 = Person.objects.create(first_name='Matt', effective=timezone.now())
        p2 = Person.objects.new(p1.entity_id, timezone.now() - timedelta(days=10), first_name='Matthew')
        self.assertEqual("Matt", Person.objects.get_current(p1.entity_id, timezone.now() + timedelta(days=1)).first_name)
        self.assertEqual("Matthew", Person.objects.get_current(p1.entity_id, timezone.now() - timedelta(days=5)).first_name)
