from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from sample.models.person import Person
from sample.models.address import Address


class RelationshipTests(TestCase):

    def test_person_has_a_related_address(self):
        a1 = Address.objects.create(effective=timezone.now() - timedelta(days=10), zip_code=12345)
        a2 = Address.objects.create(effective=timezone.now(), zip_code=67890)
        a3 = Address.objects.new(a1.entity_id, effective=timezone.now(), zip_code=99999)
        a4 = Address.objects.new(a2.entity_id, effective=a2.effective, zip_code=11111)
        p1 = Person.objects.create(first_name="Matt", effective=timezone.now(), address_entity_ids=[str(a1.entity_id), str(a2.entity_id)])
        with self.assertNumQueries(1):
            self.assertCountEqual([a3, a4], p1.addresses)
