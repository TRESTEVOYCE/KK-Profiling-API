from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ProfilingInformations, YouthStatus, KKAddress
from .serializers import ProfilingInformationsSerializer, KKAddressSerializer, YouthStatusSerializer, YouthSyncSerializer

# ==========================================
# 🔄 NEW MOBILE SYNC ENDPOINT
# ==========================================
class YouthSyncView(APIView):
    """
    Handles bulk/offline synchronization payloads sent from the Flutter mobile app.
    """
    permission_classes = [IsAuthenticated] # Ensures only logged-in accounts can sync data

    def post(self, request, *args, **kwargs):
        sync_data = request.data
        
        print("--- Mobile App Sync Payload Received ---")
        print(sync_data)
        print("-----------------------------------------")
        
        # 1. Deduplication Guard: Check if this person already exists in SQLite
        first_name = sync_data.get('first_name', '').strip()
        last_name = sync_data.get('last_name', '').strip()
        birthdate = sync_data.get('birthdate')

        duplicate_exists = ProfilingInformations.objects.filter(
            first_name__iexact=first_name,
            last_name__iexact=last_name,
            birthdate=birthdate
        ).exists()

        if duplicate_exists:
            return Response(
                {
                    "status": "conflict",
                    "message": f"Profile for {first_name} {last_name} already exists on the server."
                },
                status=status.HTTP_409_CONFLICT
            )

        # 2. Pass the dictionary data to our specialized nested serializer
        serializer = YouthSyncSerializer(data=sync_data)
        
        if serializer.is_valid():
            # This triggers the custom create() method we wrote inside serializers.py!
            serializer.save() 
            
            return Response(
                {
                    "status": "success",
                    "message": f"Profile for {first_name} {last_name} successfully saved to database.",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        
        # 3. Fallback: If payload layout structure is malformed, return errors
        print(f"❌ Serializer Validation Failed: {serializer.errors}")
        return Response(
            {
                "status": "error",
                "message": "Data validation failed.",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


# ==========================================
# 📋 EXISTING GENERIC VIEWS
# ==========================================
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