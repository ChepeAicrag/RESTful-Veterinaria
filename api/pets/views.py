from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from .models import Breed, Pet, TypePet
from .serializers import BreedSerializer, PetSerializer, TypePetSerializer


class ListCreatePet(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        pets = None
        user = request.user
        if(user.is_superuser):
            pets = Pet.objects.all().filter(status_delete=False)
        else:
            pets = Pet.objects.all().filter(status_delete=False, user=user)
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data.setdefault('user', request.user.id)
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListUpdateDeletePet(APIView):

    permission_classes = [AllowAny]

    def get(self, request, id):
        pet = Pet.objects.all().filter(id=id, status_delete=False)
        serializer = PetSerializer(pet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        pet = Pet.objects.all().filter(id=id, status_delete=False)
        if not pet:
            return Response({'message': 'No existe la mascota con id dado'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PetSerializer(pet, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        pet = Pet.objects.all().filter(id=id, status_delete=False)
        if not pet:
            return Response({'message': 'No existe la mascota con id dado'}, status=status.HTTP_400_BAD_REQUEST)
        pet.status_delete = True
        pet.save()
        return Response({'message': 'Mascota eliminada satisfactoriamente'}, status=status.HTTP_200_OK)


def validateTypePet(id):
    type_pet = TypePet.objects.filter(status_delete=False, id=id).first()
    if not type_pet:
        return Response({'message': 'No existe el tipo de mascota con id dado'}, status=status.HTTP_400_BAD_REQUEST)
    return type_pet


class ListCreateTypePet(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        types = TypePet.objects.all().filter(status_delete=False)
        serializer = TypePetSerializer(types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TypePetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListUpdateDeleteTypePet(APIView):

    permission_classes = [AllowAny]

    def get(self, request, id):
        type_pet = validateTypePet(id)
        if type(type_pet) is Response:
            return type_pet
        serializer = TypePetSerializer(type_pet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        type_pet = validateTypePet(id)
        if type(type_pet) is Response:
            return type_pet
        serializer = TypePetSerializer(type_pet, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        type_pet = validateTypePet(id)
        if type(type_pet) is Response:
            return type_pet
        count_pets = Pet.objects.all().filter(type_pet=type_pet).count()
        if count_pets >= 1:
            return Response({'message': 'No puede eliminar esta tipo de mascota, hay mascotas que dependen de ella'}, status=status.HTTP_400_BAD_REQUEST)
        count_breeds = Breed.objects.all().filter(type_pet=type_pet).count()
        if count_breeds >= 1:
            return Response({'message': 'No puede eliminar esta tipo de mascota, hay razas que dependen de ella'}, status=status.HTTP_400_BAD_REQUEST)
        type_pet.status_delete = True
        type_pet.save()
        return Response({'message': 'Tipo de mascota eliminada satisfactoriamente'}, status=status.HTTP_200_OK)


class ListCreateBreed(APIView):

    permission_classes = [AllowAny]

    def get(self, request, id):
        type_pet = validateTypePet(id)
        if type(type_pet) is Response:
            return type_pet
        breeds = Breed.objects.all().filter(status_delete=False, type_pet=type_pet)
        serializer = BreedSerializer(breeds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        type_pet = validateTypePet(id)
        if type(type_pet) is Response:
            return type_pet
        request.data.setdefault('type_pet', type_pet.id)
        serializer = BreedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def validateBreed(id):
    breed = Breed.objects.all().filter(status_delete=False, id=id)
    if not breed:
        return Response({'message': 'Tipo de mascota no encontrado'}, status=status.HTTP_400_BAD_REQUEST)
    return breed


class ListUpdateDeleteBreed(APIView):

    permission_classes = [AllowAny]

    def get(self, request, id, id_breed):
        type_pet = validateTypePet(id)
        if type(type_pet) is Response:
            return type_pet
        breed = validateBreed(id_breed)
        serializer = BreedSerializer(breed)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, id_breed):
        type_pet = validateTypePet(id)
        if type(type_pet) is Response:
            return type_pet
        breed = validateBreed(id_breed)
        serializer = BreedSerializer(breed, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id, id_breed):
        type_pet = validateTypePet(id)
        if type(type_pet) is Response:
            return type_pet
        breed = validateBreed(id_breed)
        count_pets = Pet.objects.all().filter(breed=breed).count()
        if count_pets >= 1:
            return Response({'message': 'No puede eliminar esta raza, hay mascotas que dependen de ella'}, status=status.HTTP_400_BAD_REQUEST)
        breed.status_delete = True
        breed.save()
        return Response({'message': 'Raza eliminada satisfactoriamente'}, status=status.HTTP_200_OK)
