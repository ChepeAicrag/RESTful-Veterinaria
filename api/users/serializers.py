from django.core import exceptions
from django.urls import reverse
from django.core.exceptions import ValidationError
import django.contrib.auth.password_validation as validators

from rest_framework import serializers
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Address, Role, Town, User
from .utils import Util


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('status_delete', )

        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        user = User(**data)
        errors = dict()
        password = data.get('password')
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"

        # Requerimientos de la contraseña
        if not any(x.isupper() for x in password):
            raise ValidationError(
                'La contraseña debe contener al menos una letra mayúscula')

        if not any(x.isdigit() for x in password):
            raise ValidationError(
                'La contraseña debe contener al menos un número')

        if not any(x in special_characters for x in password):
            raise ValidationError(
                'La contraseña debe contener al menos un caráter especial')

        if len(password) > 20:
            raise ValidationError(
                'La contraseña debe contener máximo 20 caracteres')

        try:
            validators.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSignupSerializer, self).validate(data)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        token = RefreshToken.for_user(user).access_token
        current_site = 'localhost:8000'
        relativeLink = reverse('email-verify')
        absurl = 'http://' + current_site + \
            relativeLink + "?token=" + str(token)
        email_body = 'Gracias por registrarte a , por favor verifica tu correo electrónico en la siguiente liga:\n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Confirma tu correo electrónico'}
        Util.send_email(data)
        return user

    def to_representation(self, instance):
        return ListUserSerializer(instance).data


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
        ]


class TownSerializer(serializers.ModelSerializer):

    class Meta:
        model = Town
        exclude = ('status_delete', )


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        exclude = ('status_delete', )


class ValidateUser(serializers.Serializer):

    class Meta:
        model = User
        exclude = ('status_delete', 'address')


class ValidateAddress(serializers.Serializer):

    class Meta:
        model = Address
        exclude = ('status_delete', 'town')


class ValidatorJSONUser(serializers.Serializer):

    town = TownSerializer()
    user = ValidateUser()
    address = ValidateAddress()


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        exclude = ('status_delete', )


class ListUserSerializer(serializers.ModelSerializer):

    role = RoleSerializer()
    address = AddressSerializer()

    class Meta:
        model = User
        exclude = ('status_delete', 'created_at', 'updated_at',
                   'groups', 'user_permissions', 'is_superuser', 'password', 'is_verified', 'is_staff')
