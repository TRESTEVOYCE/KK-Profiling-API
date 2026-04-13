from rest_framework import serializers
from django.contrib.auth.models import User as DjangoUser
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    # READ-ONLY: For displaying data in GET requests
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    # WRITE-ONLY: For taking input in POST requests
    reg_username = serializers.CharField(write_only=True, required=True)
    reg_email = serializers.EmailField(write_only=True, required=True)
    password1 = serializers.CharField(write_only=True, required=True, min_length=8)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'reg_username', 'reg_email', 'password1', 'password2', 'role']

    def validate(self, data):
        # 1. Check if passwords match
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password2": "Passwords do not match."})

        # 2. Check if username is already taken in the main User table
        if DjangoUser.objects.filter(username=data['reg_username']).exists():
            raise serializers.ValidationError({"reg_username": "This username is already taken."})
            
        return data

    def create(self, validated_data):
        # 3. Pull out the User data
        username = validated_data.pop('reg_username')
        email = validated_data.pop('reg_email')
        password = validated_data.pop('password1')
        validated_data.pop('password2') # Cleanup

        # 4. Create the core account
        base_user = DjangoUser.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # 5. Create the Profile (role) linked to that account
        profile = Profile.objects.create(user=base_user, **validated_data)
        return profile