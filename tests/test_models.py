from django.test import TestCase
from django.contrib.auth.models import User
from .models import HealthRecord, ExerciseLog
from django.core.exceptions import ValidationError

class HealthRecordModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_create_health_record_valid(self):
        # Test valid data
        health_record = HealthRecord.objects.create(
            user=self.user,
            weight=70,
            height=175,
            blood_pressure="120/80",
            blood_sugar=95.5,
            heart_rate=70
        )
        self.assertAlmostEqual(health_record.bmi, 22.86, places=2)
        self.assertEqual(health_record.user.username, 'testuser')
        self.assertEqual(health_record.blood_pressure, "120/80")

    def test_create_health_record_invalid_weight(self):
        # Test if weight cannot be zero or negative
        with self.assertRaises(ValidationError):
            health_record = HealthRecord.objects.create(
                user=self.user,
                weight=0,
                height=175,
                blood_pressure="120/80",
                blood_sugar=95.5,
                heart_rate=70
            )

    def test_create_health_record_invalid_height(self):
        # Test if height cannot be zero or negative
        with self.assertRaises(ValidationError):
            health_record = HealthRecord.objects.create(
                user=self.user,
                weight=70,
                height=0,
                blood_pressure="120/80",
                blood_sugar=95.5,
                heart_rate=70
            )

    def test_bmi_calculation_edge_case(self):
        # Test BMI calculation for extreme values
        health_record = HealthRecord.objects.create(
            user=self.user,
            weight=500,
            height=250,
            blood_pressure="120/80",
            blood_sugar=95.5,
            heart_rate=70
        )
        self.assertEqual(health_record.calculate_bmi(), 20.0)

class ExerciseLogModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_create_exercise_log(self):
        # Create a test exercise log with valid data
        exercise_log = ExerciseLog.objects.create(
            user=self.user,
            exercise_type='Running',
            duration=30,
            calories_burned=300
        )
        self.assertEqual(exercise_log.exercise_type, 'Running')
        self.assertEqual(exercise_log.calories_burned, 300)
        self.assertEqual(exercise_log.user.username, 'testuser')

    def test_create_exercise_log_invalid_duration(self):
        # Test invalid exercise duration (negative)
        with self.assertRaises(ValidationError):
            exercise_log = ExerciseLog.objects.create(
                user=self.user,
                exercise_type='Running',
                duration=-30,
                calories_burned=300
            )
