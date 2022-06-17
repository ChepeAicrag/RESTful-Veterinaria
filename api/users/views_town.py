from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import status

from .models import Town
from .serializers import TownSerializer


class ListTown(APIView):

    def get(self, request):
        towns = Town.objects.all().filter(status_delete=False)
        serializer = TownSerializer(towns, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
