from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

from .choices import roles


class Role(models.Model):

    name = models.CharField(max_length=100, null=False, verbose_name='Nombre')
    description = models.CharField(
        max_length=100, null=False, verbose_name='Descripcion')
    isSuperAdmin = models.BooleanField(
        default=False, verbose_name='Super admin')
    status_delete = models.BooleanField(
        default=False, verbose_name='Status Delete')

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        db_table = 'Role'
        ordering = ('id', )


class Address(models.Model):

    number = models.IntegerField()
    state = models.CharField(max_length=255)
    street = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        db_table = 'Address'
        ordering = ('id', )


class UserManager(BaseUserManager):

    def create_user(self, name, email, password=None, **kwargs):

        user = self.model(
            name=name, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, email, password=None, **kwargs):

        user = self.model(
            name=name, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


# Modelo de la aplicacion.
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    role = models.ForeignKey(Role, choices=roles, on_delete=models.CASCADE)
    address = models.ForeignKey(Adress, choices=roles, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'Users'
        ordering = ('id', )
