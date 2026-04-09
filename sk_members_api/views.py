from rest_framework import generics
from sk_members_api.serializers import MemberSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Member
# Create your views here.


class MemberListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class MemberRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

