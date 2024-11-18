from rest_framework import serializers
from .models import HealthRecord, ExerciseLog
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

def validate_bmi(value):
    if value < 10 or value > 100:
        raise ValidationError("BMI value is out of reasonable bounds.")
    return value

class HealthRecordSerializer(serializers.ModelSerializer):
    bmi = serializers.FloatField(validators=[validate_bmi])

    class Meta:
        model = HealthRecord
        fields = ['id', 'user', 'weight', 'height', 'bmi', 'blood_pressure', 'blood_sugar', 'heart_rate', 'recorded_at']
        read_only_fields = ('recorded_at',)

class ExerciseLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseLog
        fields = ['id', 'user', 'exercise_type', 'duration', 'calories_burned', 'date']

class UserSerializer(serializers.ModelSerializer):
    health_records = HealthRecordSerializer(many=True, read_only=True)
    exercise_logs = ExerciseLogSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'health_records', 'exercise_logs']
