from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication



from .serializers import HouseSerializer
from .models import House


from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class TokenBearerAuthentication(TokenAuthentication):
    keyword = 'Bearer'


class HouseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenBearerAuthentication]
    serializer_class = HouseSerializer
    queryset = House.objects.all()