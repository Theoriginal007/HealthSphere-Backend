# serializers.py for API module

from rest_framework import serializers
from healthapp.models import HealthRecord, UserProfile  # Assuming an additional UserProfile model
from django.contrib.auth.models import User

class HealthRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for HealthRecord model to handle serialization and deserialization.
    Includes validation methods to ensure data integrity.
    """
    class Meta:
        model = HealthRecord
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_data_field(self, value):
        """
        Custom validation for data fields (replace 'data_field' with actual field names).
        """
        if not value:
            raise serializers.ValidationError("This field cannot be empty")
        return value

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfile model, includes nested user information.
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'profile_picture']

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User object with additional user profile information.
    """
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']
