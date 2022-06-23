from rest_framework.serializers import ModelSerializer, Serializer

from users.serializers import ListUserSerializer
from pets.serializers import ListPetSerializer, PetSerializer
from .models import Appointment, TypeService


class TypeServiceSerializer(ModelSerializer):

    class Meta:
        model = TypeService
        exclude = ('status_delete', )


class ListAppointmentSerializer(ModelSerializer):

    user = ListUserSerializer()
    type_service = TypeServiceSerializer()
    pet = ListPetSerializer()

    class Meta:
        model = Appointment
        exclude = ('status_delete', )


class AppointmentSerializer(ModelSerializer):

    class Meta:
        model = Appointment
        exclude = ('status_delete', )

    def to_representation(self, instance):
        return ListAppointmentSerializer(instance).data


class AppointmentValidateData(Serializer):
    class Meta:
        model = Appointment
        exclude = ('status_delete', 'user', 'pet')


class ValidateJSONAppointment(Serializer):
    pet = PetSerializer()
    appointment = AppointmentValidateData()
