from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Client, Employer
from .serializers import UserSerializer, ClientSerializer, EmployerSerializer

from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Client
from .serializers import UserSerializer, ClientSerializer

class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            client = Client.objects.create(user=user)
            client_serializer = ClientSerializer(client)
            return Response(client_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class EmployerViewSet(viewsets.ModelViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
