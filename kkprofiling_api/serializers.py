from rest_framework import serializers
from .models import ProfilingInformations, KKAddress, YouthStatus


class KKAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = KKAddress
        fields = '__all__'
class YouthStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = YouthStatus
        fields = '__all__'

class ProfilingInformationsSerializer(serializers.ModelSerializer):
    addresses = KKAddressSerializer(many=True, read_only=True)
    youth_statuses = YouthStatusSerializer(many=True, read_only=True)

    class Meta:
        model = ProfilingInformations
        fields = ['id', 'first_name', 'last_name', 'age', 'birthdate', 'email', 'contact_number', 'sex', 'civil_status', 'educational_background', 'date_added', 'addresses', 'youth_statuses']
