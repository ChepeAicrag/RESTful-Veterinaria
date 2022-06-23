
from django.db import transaction
from django.forms import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny


from pets.serializers import PetSerializer
from .models import Appointment, TypeService
from .serializers import AppointmentSerializer, TypeServiceSerializer, ValidateJSONAppointment

# Create your views here.


class CreateListTypeService(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        types_services = TypeService.objects.all().filter(status_delete=False)
        serializer = TypeServiceSerializer(types_services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TypeServiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateListAppoinment(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == 1:
            appointments = Appointment.objects.all().filter(status_delete=False)
        else:
            appointments = Appointment.objects.all().filter(
                status_delete=False, user=request.user)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        data['pet']['user'] = request.user.id
        ValidateJSONAppointment(data=data).is_valid(raise_exception=True)
        serializer = PetSerializer(data=data['pet'])
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                data["appointment"]["pet"] = serializer.data['id']
                data["appointment"]["user"] = serializer.data['user']
                serializer = AppointmentSerializer(data=data['appointment'])
                if not serializer.is_valid():
                    raise ValidationError(serializer.errors)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            transaction.rollback()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            transaction.rollback()
            print(error)
            return Response({'message': 'Error en el servidor al registrar cita'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListDeleteTypeService(APIView):

    permission_classes = [AllowAny]

    def get(self, request, id):
        appointment = Appointment.objects.all().filter(
            status_delete=False, id=id).first()
        if not appointment:
            return Response({'message': 'El tipo de serivicio no existe'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        pass
