from django.db import models
from padam_django.apps.geography.models import Place


class Driver(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='driver')

    def __str__(self):
        return f"Driver: {self.user.username} (id: {self.pk})"


class Bus(models.Model):
    licence_plate = models.CharField("Name of the bus", max_length=10)

    class Meta:
        verbose_name_plural = "Buses"

    def __str__(self):
        return f"Bus: {self.licence_plate} (id: {self.pk})"

class BusShift(models.Model):
    bus = models.ForeignKey('Bus', on_delete=models.CASCADE, related_name='shifts')
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE, related_name='shifts')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['bus', 'start_time', 'end_time'],
                name='unique_bus_shift'
            ),
            models.UniqueConstraint(
                fields=['driver', 'start_time', 'end_time'],
                name='unique_driver_shift'
            )
        ]

        indexes = [
            models.Index(fields=['bus', 'start_time', 'end_time']),
            models.Index(fields=['driver', 'start_time', 'end_time']),
        ]

    def __str__(self):
        return f"BusShift (Bus: {self.bus}, Driver: {self.driver})"

class BusStop(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='bus_stops')
    bus_shift = models.ForeignKey('BusShift', on_delete=models.CASCADE, related_name='bus_stops', null=True)
    stop_order = models.PositiveIntegerField("Order of the stop in the bus route")

    class Meta:
        unique_together = (("bus_shift", "stop_order"),)
        ordering = ['stop_order']

    def __str__(self):
        return f"BusStop: {self.place.name} (Order: {self.stop_order})"
