# padam_django/apps/fleet/tests/test_bus_overlap.py
from django.test import TestCase # type: ignore
from django.utils import timezone # type: ignore
from padam_django.apps.fleet.models import Bus, Driver, BusShift
from padam_django.apps.fleet.forms import BusShiftForm
from padam_django.apps.users.models import User

class BusOverlapTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_driver", password="testpassword")
        self.driver = Driver.objects.create(user=self.user)
        self.bus = Bus.objects.create(licence_plate="ABC123")

    def test_bus_shift_overlap(self):
        # Créer un premier trajet pour le bus
        start_time1 = timezone.now()
        end_time1 = start_time1 + timezone.timedelta(hours=2)
        BusShift.objects.create(bus=self.bus, driver=self.driver, start_time=start_time1, end_time=end_time1)

        # Essayer de créer un deuxième trajet qui se chevauche avec le premier
        start_time2 = start_time1 + timezone.timedelta(hours=1)
        end_time2 = start_time2 + timezone.timedelta(hours=2)

        form_data = {
            'bus': self.bus,
            'driver': self.driver,
            'start_time': start_time2,
            'end_time': end_time2
        }
        form = BusShiftForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("The route overlaps with another route for this bus.", form.errors['__all__'])

    def test_non_overlapping_bus_shift(self):
        # Créer un premier trajet pour le bus
        start_time1 = timezone.now()
        end_time1 = start_time1 + timezone.timedelta(hours=2)
        BusShift.objects.create(bus=self.bus, driver=self.driver, start_time=start_time1, end_time=end_time1)

        # Créer un deuxième trajet qui ne se chevauche pas
        start_time2 = end_time1 + timezone.timedelta(hours=1)
        end_time2 = start_time2 + timezone.timedelta(hours=2)

        form_data = {
            'bus': self.bus,
            'driver': self.driver,
            'start_time': start_time2,
            'end_time': end_time2
        }
        form = BusShiftForm(data=form_data)

        self.assertTrue(form.is_valid())
