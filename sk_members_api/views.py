from rest_framework import viewsets
from sk_members_api.serializers import MemberSerializer
from .models import Member
# Create your views here.


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

