from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ProfilingInformations, YouthStatus, KKAddress
from .serializers import ProfilingInformationsSerializer, KKAddressSerializer, YouthStatusSerializer, YouthSyncSerializer
import traceback
import sys

# ==========================================
# 🔄 NEW MOBILE SYNC ENDPOINT
# ==========================================

class YouthSyncView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        sync_data = request.data
        
        # 1. Deduplication Check
        first_name = sync_data.get('first_name', '').strip()
        last_name = sync_data.get('last_name', '').strip()
        birthdate = sync_data.get('birthdate')

        if ProfilingInformations.objects.filter(
            first_name__iexact=first_name,
            last_name__iexact=last_name,
            birthdate=birthdate
        ).exists():
            return Response(
                {"status": "conflict", "message": f"Profile for {first_name} {last_name} already exists."},
                status=status.HTTP_409_CONFLICT
            )

        # 2. Schema Validation
        serializer = YouthSyncSerializer(data=sync_data)
        if serializer.is_valid():
            try:
                # 💥 The 500 crash occurs here—let's trap it safely
                serializer.save() 
                
                return Response(
                    {"status": "success", "message": "Saved successfully.", "data": serializer.data},
                    status=status.HTTP_201_CREATED
                )
            except Exception as db_error:
                # Extract the exact database issue context
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = traceback.extract_tb(exc_tb)[-1][2]
                line_no = traceback.extract_tb(exc_tb)[-1][1]
                
                error_summary = f"[{type(db_error).__name__}] in {fname}() line {line_no}: {str(db_error)}"
                
                print("\n💥💥💥 DATABASE CRASH DETAILS 💥💥💥")
                print(error_summary)
                traceback.print_exc()
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
                
                # Send the clean string details straight to Flutter
                return Response(
                    {
                        "status": "server_error",
                        "error_type": type(db_error).__name__,
                        "error_details": str(db_error),
                        "failed_at_function": fname,
                        "line_number": line_no
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(
            {"status": "error", "message": "Validation failed.", "errors": serializer.errors},
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