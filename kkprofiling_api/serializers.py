from rest_framework import serializers
from .models import ProfilingInformations, KKAddress, YouthStatus

# --- CORE INDIVIDUAL MODEL SERIALIZERS ---

class KKAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = KKAddress
        fields = ['region', 'province', 'municipality_or_city', 'barangay', 'purok']
        read_only_fields = ['id', 'date_added']  # Guard against missing timestamps from mobile


class YouthStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = YouthStatus
        fields = [
            'youth_classification', 'youth_age_group', 'youth_with_specific_needs',
            'working_status', 'is_sk_voter', 'is_regular_voter', 
            'attended_kk_assembly', 'times_attended', 'did_not_attend_reason'
        ]
        read_only_fields = ['id', 'date_added']  # Guard against missing timestamps from mobile

    def to_internal_value(self, data):
        # Create a mutable copy of the incoming query parameters dict
        data = data.copy() if hasattr(data, 'copy') else dict(data)
        
        # Intercept and scrub boolean "False", false, or empty string indicators
        specific_needs = data.get('youth_with_specific_needs')
        if specific_needs in [False, 'False', 'false', 'N/A', '']:
            data['youth_with_specific_needs'] = None
            
        return super().to_internal_value(data)
        

class ProfilingInformationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilingInformations
        fields = [
            'id', 'first_name', 'middle_name', 'last_name', 'age', 'birthdate', 
            'email', 'contact_number', 'sex', 'civil_status', 'educational_background', 'date_added'
        ]


# --- SPECIALIZED BULK NESTED SYNC SERIALIZER ---

class YouthSyncSerializer(serializers.ModelSerializer):
    # Match these names exactly with what your Flutter JSON payload sends!
    address = KKAddressSerializer(source='addresses')
    youth_status = YouthStatusSerializer(source='youth_statuses')

    class Meta:
        model = ProfilingInformations
        fields = [
            'first_name', 'middle_name', 'last_name', 'age', 'birthdate', 
            'email', 'contact_number', 'sex', 'civil_status', 
            'educational_background', 'address', 'youth_status'
        ]

    def create(self, validated_data):
        # 1. FIX: Pop using the 'source' strings, NOT the field names!
        address_data = validated_data.pop('addresses', None)
        youth_status_data = validated_data.pop('youth_statuses', None)

        # 2. Save the parent Profile into db.sqlite3 safely
        profile = ProfilingInformations.objects.create(**validated_data)

        # 3. Create the Address row linked back to our fresh parent profile ID
        if address_data:
            KKAddress.objects.create(kk_name=profile, **address_data)

        # 4. Create the Youth Status row linked back to our fresh parent profile ID
        if youth_status_data:
            YouthStatus.objects.create(kk_name=profile, **youth_status_data)

        return profile

    def to_internal_value(self, data):
        # ... Your excellent data scrubbing logic remains completely unchanged here!
        if hasattr(data, 'dict'):
            data = data.dict()
        else:
            data = dict(data)

        gender_map = {'Male': 'male', 'Female': 'female'}
        civil_status_map = {
            'Single': 'single', 'Married': 'married', 'Widowed': 'widowed', 
            'Separated': 'separated', 'Divorced': 'divorced', 'Annulled': 'annulled',
            'Live-in': 'live_in', 'Unknown': 'unknown'
        }
        education_map = {
            'Elementary Undergraduate': 'elementary_level',
            'Elementary Graduate': 'elementary_graduate',
            'High School Undergraduate': 'highschool_level',
            'High School Graduate': 'highschool_graduate',
            'Vocational Graduate': 'vocational_graduate',
            'College Undergraduate': 'college_level',
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

        if 'youth_status' in data and isinstance(data['youth_status'], dict):
            status_data = dict(data['youth_status'])
            
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
                'Employed': 'employed', 'Unemployed': 'unemployed', 
                'Self-Employed': 'self_employed', 'Looking for Job': 'looking_for_job',
                'Not Looking for Job': 'not_looking_for_job'
            }

            if status_data.get('youth_classification') in classification_map:
                status_data['youth_classification'] = classification_map[status_data['youth_classification']]
            if status_data.get('youth_age_group') in age_group_map:
                status_data['youth_age_group'] = age_group_map[status_data['youth_age_group']]
            if status_data.get('working_status') in working_status_map:
                status_data['working_status'] = working_status_map[status_data['working_status']]
                
            if status_data.get('youth_with_specific_needs') == '':
                status_data['youth_with_specific_needs'] = None
            if status_data.get('did_not_attend_reason') == '':
                status_data['did_not_attend_reason'] = None

            data['youth_status'] = status_data

        return super().to_internal_value(data)