from django.core import exceptions
from django.core.exceptions import ValidationError
import django.contrib.auth.password_validation as validators

from rest_framework import serializers
from rest_framework import exceptions

from users.models import User


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

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
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'is_active',
            'is_verified',
        ]
