from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields for the user profile can go here

class HealthRecord(models.Model):
    user = models.ForeignKey(User, related_name='health_records', on_delete=models.CASCADE)
    weight = models.FloatField()
    height = models.FloatField()
    bmi = models.FloatField()
    blood_pressure = models.CharField(max_length=50)
    blood_sugar = models.FloatField()
    heart_rate = models.IntegerField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.weight <= 0:
            raise ValidationError("Weight must be positive.")
        if self.height <= 0:
            raise ValidationError("Height must be positive.")
        self.calculate_bmi()

    def calculate_bmi(self):
        height_in_meters = self.height / 100
        self.bmi = self.weight / (height_in_meters ** 2)

    def __str__(self):
        return f"Health record for {self.user.username} at {self.recorded_at}"

    class Meta:
        ordering = ['-recorded_at']

class ExerciseLog(models.Model):
    user = models.ForeignKey(User, related_name='exercise_logs', on_delete=models.CASCADE)
    exercise_type = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()  # Duration in minutes
    calories_burned = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.exercise_type} on {self.date}"

    class Meta:
        ordering = ['-date']
