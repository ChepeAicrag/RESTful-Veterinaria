from .models import Pet, Breed, TypePet

from rest_framework.serializers import ModelSerializer


class PetSerializer(ModelSerializer):

    class Meta:
        model = Pet
        exclude = ('status_delete', )
