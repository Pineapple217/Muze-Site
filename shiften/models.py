from tabnanny import verbose
from django.db import models

from leden.models import Lid
from django.utils.translation import gettext as _

class Shiftlijst(models.Model):
    date = models.DateField()
    TYPES = [
        ('month', _('month')),
        ('event', _('event'))
    ]
    type = models.CharField(max_length = 100, choices=TYPES)

    def __str__(self):
        return self.date.strftime('%Y %B')
    
    class Meta:
       verbose_name_plural = "Shiftlijsten" 

class Shift(models.Model):
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()

    shifters = models.ManyToManyField(Lid, blank=True)
    shift_list = models.ForeignKey(Shiftlijst, on_delete=models.CASCADE)
    def __str__(self):
       return f'{self.date.strftime("%Y %B %d")} | {self.start.isoformat(timespec = "minutes")} - {self.end.isoformat(timespec = "minutes")}'
    