from django.db import models

from users.models import User


class TypePet(models.Model):
    name = models.CharField(max_length=255)
    status_delete = models.BooleanField(
        default=False, verbose_name='Status Delete')

    class Meta:
        verbose_name = 'TypePet'
        verbose_name_plural = 'TypesPet'
        db_table = 'TypePet'
        ordering = ('id', )


class Breed(models.Model):
    name = models.CharField(max_length=255)
    type_pet = models.ForeignKey(TypePet, on_delete=models.CASCADE)
    status_delete = models.BooleanField(
        default=False, verbose_name='Status Delete')

    class Meta:
        verbose_name = 'Breed'
        verbose_name_plural = 'Breedes'
        db_table = 'Breed'
        ordering = ('id', )


class Pet(models.Model):

    name = models.CharField(max_length=255)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status_delete = models.BooleanField(
        default=False, verbose_name='Status Delete')

    class Meta:
        verbose_name = 'Pet'
        verbose_name_plural = 'Pets'
        db_table = 'Pets'
        ordering = ('id', )
