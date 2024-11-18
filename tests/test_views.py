from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import HealthRecord, ExerciseLog
from .serializers import HealthRecordSerializer, ExerciseLogSerializer
from rest_framework import serializers

class HealthRecordViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_create_health_record(self):
        # Test POST request to create a health record
        data = {
            'weight': 70,
            'height': 175,
            'blood_pressure': '120/80',
            'blood_sugar': 95.5,
            'heart_rate': 70
        }
        response = self.client.post('/api/v1/healthrecords/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_health_record_invalid(self):
        # Test invalid data
        data = {
            'weight': 0,
            'height': 175,
            'blood_pressure': '120/80',
            'blood_sugar': 95.5,
            'heart_rate': 70
        }
        response = self.client.post('/api/v1/healthrecords/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_health_records_pagination(self):
        # Test paginated health record listing
        for i in range(15):
            HealthRecord.objects.create(
                user=self.user,
                weight=70,
                height=175,
                blood_pressure="120/80",
                blood_sugar=95.5,
                heart_rate=70
            )
        response = self.client.get('/api/v1/healthrecords/?page=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)  # Should return 5 records per page

    def test_user_authentication_required(self):
        # Ensure user is authenticated to access the health records
        self.client.logout()
        response = self.client.get('/api/v1/healthrecords/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ExerciseLogViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_create_exercise_log(self):
        data = {
            'exercise_type': 'Running',
            'duration': 30,
            'calories_burned': 300
        }
        response = self.client.post('/api/v1/exHere’s an improved and enhanced version of your test code that covers broader cases, implements more edge cases, and uses more efficient practices to ensure thorough and scalable testing.

### 1. **Enhanced `test_models.py` (Unit Tests for Models)**

Enhancements:
- More robust test cases for model validation.
- Test edge cases for health record fields and calculations.

```python
from django.test import TestCase
from django.contrib.auth.models import User
from .models import HealthRecord, ExerciseLog
from django.core.exceptions import ValidationError

class HealthRecordModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_create_health_record_valid(self):
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
        with self.assertRaises(ValidationError):
            HealthRecord.objects.create(
                user=self.user,
                weight=-10,
                height=175,
                blood_pressure="120/80",
                blood_sugar=95.5,
                heart_rate=70
            )

    def test_bmi_calculation_edge_case(self):
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
        exercise_log = ExerciseLog.objects.create(
            user=self.user,
            exercise_type='Running',
            duration=30,
            calories_burned=300
        )
        self.assertEqual(exercise_log.exercise_type, 'Running')
        self.assertEqual(exercise_log.calories_burned, 300)
        self.assertEqual(exercise_log.user.username, 'testuser')
