from rest_framework import serializers
from .models import ProfilingInformations, KKAddress, YouthStatus

# --- CORE INDIVIDUAL MODEL SERIALIZERS ---

class KKAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = KKAddress
        fields = ['id', 'region', 'province', 'municipality_or_city', 'barangay', 'purok', 'date_added']

class YouthStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = YouthStatus
        fields = [
            'id', 'youth_classification', 'youth_age_group', 'youth_with_specific_needs',
            'working_status', 'is_sk_voter', 'is_regular_voter', 
            'attended_kk_assembly', 'times_attended', 'did_not_attend_reason', 'date_added'
        ]

class ProfilingInformationsSerializer(serializers.ModelSerializer):
    """
    Standard CRUD Serializer used by your existing ProfilingInformations ViewSets.
    """
    class Meta:
        model = ProfilingInformations
        fields = [
            'id', 'first_name', 'middle_name', 'last_name', 'age', 'birthdate', 
            'email', 'contact_number', 'sex', 'civil_status', 'educational_background', 'date_added'
        ]


# --- SPECIALIZED BULK NESTED SYNC SERIALIZER ---

class YouthSyncSerializer(serializers.ModelSerializer):
    # Keep your existing nested address and status serializers active here:
    address = KKAddressSerializer()
    youth_status = YouthStatusSerializer()

    class Meta:
        model = ProfilingInformations
        fields = '__all__'
    
    def create(self, validated_data):
        # 1. Pop the nested dictionary structures out before creating the parent
        address_data = validated_data.pop('address', None)
        youth_status_data = validated_data.pop('youth_status', None)

        # 2. Get the actual Model classes linked to those nested fields
        # (This automatically reads the models from KKAddressSerializer and YouthStatusSerializer)
        AddressModel = self.fields['address'].Meta.model
        YouthStatusModel = self.fields['youth_status'].Meta.model

        # 3. Create the child instances in SQLite first
        address_instance = None
        if address_data:
            address_instance = AddressModel.objects.create(**address_data)

        youth_status_instance = None
        if youth_status_data:
            youth_status_instance = YouthStatusModel.objects.create(**youth_status_data)

        # 4. Attach the saved child instances back into the main payload as foreign keys
        # ⚠️ NOTE: Make sure 'address' and 'youth_status' match your database column names!
        if address_instance:
            validated_data['address'] = address_instance
        if youth_status_instance:
            validated_data['youth_status'] = youth_status_instance

        # 5. Save the primary profile records cleanly
        return ProfilingInformations.objects.create(**validated_data)

    def to_internal_value(self, data):
        data = data.copy()

        # 1. Demographic Choices Mapping
        gender_map = {
            'Male': 'male',
            'Female': 'female'
        }
        civil_status_map = {
            'Single': 'single', 
            'Married': 'married', 
            'Widowed': 'widowed', 
            'Separated': 'separated',
            'Divorced': 'divorced',
            'Annulled': 'annulled',
            'Live-in': 'live_in',
            'Unknown': 'unknown'
        }
        education_map = {
            'Elementary Undergraduate': 'elementary_level',
            'Elementary Graduate': 'elementary_graduate',
            'High School Undergraduate': 'highschool_level',
            'High School Graduate': 'highschool_graduate',
            'Vocational Graduate': 'vocational_graduate',
            'College Undergraduate': 'college_level',       # Maps 'College Undergraduate' -> 'college_level'
            'College Graduate': 'college_graduate',
            'Master Level': 'master_level',
            'Doctorate Level': 'doctorate_level',
            'Doctorate Graduate': 'doctorate_graduate'
        }

        if data.get('sex') in gender_map:
            data['sex'] = gender_map[data['sex']]
        if data.get('civil_status') in civil_status_map:
            data['civil_status'] = civil_status_map[data['civil_status']]
        if data.get('educational_background') in education_map:
            data['educational_background'] = education_map[data['educational_background']]

        # 2. Deep Nested Youth Status Choices Mapping
        if 'youth_status' in data and isinstance(data['youth_status'], dict):
            status_data = data['youth_status'].copy()
            
            classification_map = {
                'In-School Youth': 'in_school_youth', 
                'Out-of-School Youth': 'out_of_school_youth', 
                'Working Youth': 'working_youth'
            }
            age_group_map = {
                'Child Youth (15-17)': 'child_youth', 
                'Core Youth (18-24)': 'core_youth', 
                'Adult Youth (25-30)': 'young_adult'
            }
            working_status_map = {
                'Employed': 'employed', 
                'Unemployed': 'unemployed', 
                'Self-Employed': 'self_employed',
                'Looking for Job': 'looking_for_job',
                'Not Looking for Job': 'not_looking_for_job'
            }

            if status_data.get('youth_classification') in classification_map:
                status_data['youth_classification'] = classification_map[status_data['youth_classification']]
            if status_data.get('youth_age_group') in age_group_map:
                status_data['youth_age_group'] = age_group_map[status_data['youth_age_group']]
            if status_data.get('working_status') in working_status_map:
                status_data['working_status'] = working_status_map[status_data['working_status']]
                
            data['youth_status'] = status_data

        return super().to_internal_value(data)