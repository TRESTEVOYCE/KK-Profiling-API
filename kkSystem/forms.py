from django import contrib, forms
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from kkprofiling_api.models import ProfilingInformations,YouthStatus,KKAddress
from events_api.models import Event
from sk_members_api.models import Member
 

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))



class ProfilingInformationsForm(forms.ModelForm):
    class Meta:
        model = ProfilingInformations
        fields = [
            'first_name', 'middle_name', 'last_name', 'birthdate', 'age', 
            'email', 'contact_number', 'sex', 'civil_status', 'educational_background'
        ]

class KKAddressForm(forms.ModelForm):
    class Meta:
        model = KKAddress
        fields = ['region', 'province', 'municipality_or_city', 'barangay', 'purok']

class YouthStatusForm(forms.ModelForm):
    class Meta:
        model = YouthStatus
        fields = [
            'youth_classification', 'youth_age_group', 'youth_with_specific_needs',
            'working_status', 'is_sk_voter', 'is_regular_voter', 
            'attended_kk_assembly', 'times_attended', 'did_not_attend_reason'
        ]

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'images']

class MemberUpdateForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'first_name', 'middle_name', 'last_name', 
            'age', 'birthdate', 'email', 
            'contact_number', 'sk_picture'
        ]
        # We define widgets purely for HTML input types (like dates), not for styles
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }