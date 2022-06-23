from django.db import models
from users.models import User
from pets.models import Pet


class TypeService(models.Model):
    name = models.CharField(max_length=255)
    status_delete = models.BooleanField(
        default=False, verbose_name='Status Delete')

    class Meta:
        verbose_name = 'TypeService'
        verbose_name_plural = 'TypeServices'
        db_table = 'TypeService'
        ordering = ('id', )


class Appointment(models.Model):
    hour = models.TimeField(null=False)
    date = models.DateField(null=False)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=255, null=False, default='Agendada')
    type_service = models.ForeignKey(TypeService, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    status_delete = models.BooleanField(
        default=False, verbose_name='Status Delete')

    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        db_table = 'Appointment'
        ordering = ('id', )
