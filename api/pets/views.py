from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from .models import Breed, Pet, TypePet
from .serializers import BreedSerializer, PetSerializer, TypePetSerializer


class ListCreatePet(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        pets = Pet.objects.all().filter(status_delete=False)
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


class ListCreateBreed(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        breeds = Breed.objects.all().filter(status_delete=False)
        serializer = BreedSerializer(breeds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BreedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListUpdateDeleteBreed(APIView):

    permission_classes = [AllowAny]

    def get(self, request, id):
        breed = Breed.objects.all().filter(status_delete=False, pk=id)
        if not breed:
            return Response({'message': 'Tipo de mascota no encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = BreedSerializer(breed)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        breed = Breed.objects.filter(status_delete=False, id=id).first()
        if not breed:
            return Response({'message': 'Tipo de mascota no encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = BreedSerializer(breed, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        breed = Breed.objects.filter(status_delete=False, id=id).first()
        if not breed:
            return Response({'message': 'Raza no encontrada'}, status=status.HTTP_400_BAD_REQUEST)
        count_pets = Pet.objects.all().filter(breed=breed).count()
        if count_pets >= 1:
            return Response({'message': 'No puede eliminar esta raza, hay mascotas que dependen de ella'}, status=status.HTTP_400_BAD_REQUEST)
        breed.status_delete = True
        breed.save()
        return Response({'message': 'Raza eliminada satisfactoriamente'}, status=status.HTTP_200_OK)


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
        type_pet = TypePet.objects.all().filter(status_delete=False, id=id).first()
        if not type_pet:
            return Response({'message': 'Tipo de mascota no encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TypePetSerializer(type_pet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        type_pet = TypePet.objects.all().filter(status_delete=False, id=id).first()
        if not type_pet:
            return Response({'message': 'Tipo de mascota no encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TypePetSerializer(type_pet, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        type_pet = TypePet.objects.all().filter(status_delete=False, id=id).first()
        if not type_pet:
            return Response({'message': 'Tipo de mascota no encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        count_pets = Pet.objects.all().filter(type_pet=type_pet).count()
        if count_pets >= 1:
            return Response({'message': 'No puede eliminar esta raza, hay mascotas que dependen de ella'}, status=status.HTTP_400_BAD_REQUEST)
        type_pet.status_delete = True
        type_pet.save()
        return Response({'message': 'Tipo de mascota eliminada satisfactoriamente'}, status=status.HTTP_200_OK)
