from rest_framework import generics
from .models import ProfilingInformations, YouthStatus, KKAddress
from .serializers import ProfilingInformationsSerializer, KKAddressSerializer, YouthStatusSerializer
from rest_framework.permissions import IsAuthenticated


class ProfilingInformationsViewSet(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ProfilingInformations.objects.all()
    serializer_class = ProfilingInformationsSerializer

class ProfilingInformationsDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ProfilingInformations.objects.all()
    serializer_class = ProfilingInformationsSerializer

class KKAddressViewSet(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = KKAddress.objects.all()
    serializer_class = KKAddressSerializer

class KKAddressDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = KKAddress.objects.all()
    serializer_class = KKAddressSerializer  

class YouthStatusViewSet(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = YouthStatus.objects.all()
    serializer_class = YouthStatusSerializer 

class YouthStatusDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = YouthStatus.objects.all()
    serializer_class = YouthStatusSerializer
