from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from .models import Pet
from .serializers import PetSerializer


class CreateListPet(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        pets = Pet.objects.all().filter(status_delete=False)
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PetSerializer(pets, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListUpdateDeletePet(APIView):

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
