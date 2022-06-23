from .models import Pet, Breed, TypePet

from rest_framework.serializers import ModelSerializer


class PetSerializer(ModelSerializer):

    class Meta:
        model = Pet
        exclude = ('status_delete', )

class BreedSerializer(ModelSerializer):

    class Meta:
        model = Breed
        exclude = ('status_delete', )


class TypePetSerializer(ModelSerializer):

    class Meta:
        model = TypePet
        exclude = ('status_delete', )

class ListBreedSerializer(ModelSerializer):

    type_pet = TypePetSerializer()
    class Meta:
        model = Breed
        exclude = ('status_delete', )
class ListPetSerializer(ModelSerializer):

    breed = ListBreedSerializer()
    class Meta:
        model = Pet
        exclude = ('status_delete', )