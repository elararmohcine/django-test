# padam_django/apps/fleet/forms.py
from django import forms # type: ignore
from .models import BusShift

class BusShiftForm(forms.ModelForm):
    class Meta:
        model = BusShift
        fields = ['bus', 'driver', 'start_time', 'end_time']

    def clean(self):
        cleaned_data = super().clean()
        bus = cleaned_data.get('bus')
        driver = cleaned_data.get('driver')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if bus and driver and start_time and end_time:
            # Vérification des chevauchements pour le bus
            bus_overlaps = BusShift.objects.filter(
                bus=bus,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exclude(pk=self.instance.pk)

            if bus_overlaps.exists():
                raise forms.ValidationError("The route overlaps with another route for this bus.")

            # Vérification des chevauchements pour le chauffeur
            driver_overlaps = BusShift.objects.filter(
                driver=driver,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exclude(pk=self.instance.pk)

            if driver_overlaps.exists():
                raise forms.ValidationError("The driver is already assigned to another route during this period.")

        return cleaned_data
