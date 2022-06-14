from django.urls import reverse
from django.conf import settings

from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

import jwt
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate

from .models import User
from .utils import Util
from .serializers import UserSignupSerializer, UserLoginSerializer


# SIGNUP
"""
    User singup.  Input example:
    {
        "name":"NameExample",
        "email":"email@email.com",
        "password": "mysuperpassword"
    }
"""


class UserSignupView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        data = request.data
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')

        absurl = 'http://' + current_site + \
            relativeLink + "?token=" + str(token)
        email_body = 'Gracias por registrarte a Get Talent, por favor verifica tu correo electrónico en la siguiente liga:\n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Get Talent, Confirma tu correo electrónico'}
        Util.send_email(data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

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


# LOGIN
"""
    User login.  Input example:
    {
        "email":"email@email.com",
        "password": "mysuperpassword"
    }
"""


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
                'msg': 'Exitosamente logueado',
                'tokens': tokens
            }
            return Response(data, status=status.HTTP_200_OK)

        # Valida si el correo existe
        user_email = User.objects.filter(email=email)
        if not user_email.exists():
            raise ValidationError({
                'msg': 'No existe una cuenta con este correo registrado'
            })

        # Valida que el email este verificado
        user_active = User.objects.get(email=email)
        if user_active == False:
            raise ValidationError({
                'msg': 'La cuenta no ha está activada, por favor verifica tu email'
            })

        # Valida que la contraseña sea correcta
        user = User.objects.get(email=email)
        while not User.objects.filter(password=password):
            while user.login_attempts < 3:
                user.login_attempts += 1
                user.save()
                if user.login_attempts == 1:
                    raise ValidationError({
                        'msg': 'Contraseña incorrecta, trata de nuevo'
                    })
                elif user.login_attempts == 2:
                    raise ValidationError({
                        'msg': 'Contraseña incorrecta, si acumulas tres fallas puedes bloquear tu cuenta'
                    })
            else:
                user.is_active = False
                user.save()
                raise ValidationError(
                    {'msg': 'Por seguridad, la cuenta ha sido bloqueada'})
