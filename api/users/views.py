from django.conf import settings
from django.db import transaction
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

import jwt
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import Role, User
from .serializers import AddressSerializer, TownSerializer, UserSignupSerializer, UserLoginSerializer, ValidatorJSONUser


class UserSignupView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        data = request.data.copy()
        serializer = ValidatorJSONUser(data=data)
        serializer.is_valid(raise_exception=True)
        user = data.get('user')
        address = data.get('address')
        town = data.get('town')
        role = Role.objects.filter(id=user['role'])
        if not role:
            return Response({'message': 'El rol dado no existe'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TownSerializer(data=town)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                address['town'] = serializer.data['id']
                serializer = AddressSerializer(
                    data=address)
                if not serializer.is_valid():
                    raise ValidationError(serializer.errors)
                serializer.save()
                user['address'] = serializer.data['id']
                serializer = UserSignupSerializer(data=user)
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
            return Response({'message': 'Error al registrar usuario'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# VERIFICAR EMAIL


class VerifyEmail(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()

            if not user.is_active:
                user.is_active = True
                user.save()

            return Response({'message': 'Cuenta activada exitosamente'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'message': 'La liga de activación expiró'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            return Response({'message': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)


class ResourceView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        user = User.objects.filter(is_verified=True)
        serializer = UserSignupSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserLoginView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        password = serializer.data['password']
        user = authenticate(username=email, password=password)
        if user:
            tokens = get_tokens_for_user(user)
            data = {
                'message': 'Exitosamente logueado',
                'tokens': tokens
            }
            return Response(data, status=status.HTTP_200_OK)

        # Valida si el correo existe
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({
                'message': 'No existe una cuenta con este correo registrado'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Valida que el email este verificado
        if not user.is_active:
            return Response({
                'message': 'La cuenta no ha está activada, por favor verifica tu email'
            }, status=status.HTTP_400_BAD_REQUEST)
