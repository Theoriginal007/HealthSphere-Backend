from django.test import TestCase
from healthapp.utils import calculate_bmi, calculate_daily_calories

class UtilsTest(TestCase):

    def test_calculate_bmi_valid(self):
        # Testing BMI calculation with normal values
        bmi = calculate_bmi(70, 175)  # Weight 70kg, Height 175cm
        self.assertAlmostEqual(bmi, 22.86, places=2)

    def test_calculate_bmi_zero_height(self):
        # Test BMI calculation when height is zero (edge case)
        bmi = calculate_bmi(70, 0)  # Invalid height
        self.assertIsNone(bmi, "BMI should be None for zero height")

    def test_calculate_daily_calories_valid(self):
        # Testing daily calorie calculation for a moderately active person
        calories = calculate_daily_calories(25, 70, 175, 'female', activity_level='moderate')
        self.assertGreater(calories, 0, "Daily calories should be greater than 0")

    def test_calculate_daily_calories_invalid(self):
        # Testing for invalid gender input
        with self.assertRaises(ValueError):
            calculate_daily_calories(25, 70, 175, 'invalid_gender', activity_level='moderate')
