import logging
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from .models import Profile  # ✅ Changed to Profile
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__) 

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate against the built-in Django User
        user = authenticate(username=username, password=password)
        ip = request.META.get('REMOTE_ADDR')

        if user is not None:
            # Get the Profile associated with this User
            profile = Profile.objects.filter(user=user).first()
            refresh = RefreshToken.for_user(user)

            logger.info(f"LOGIN SUCCESS | User: {user.username} | ID: {user.id} | IP: {ip}")

            if not profile:
                logger.warning(f"LOGIN WARNING | No profile found for user: {user.username} | ID: {user.id} | IP: {ip}")
                return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(profile).data,
                'role': profile.role
            }, status=status.HTTP_200_OK)
        else:

            logger.warning(f"LOGIN FAILED | Username: {username} | IP: {ip}")
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class UserListCreateView(generics.ListCreateAPIView):
    # This view handles listing all profiles and creating new ones
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserDeleteView(generics.DestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]