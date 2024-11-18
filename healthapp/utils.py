def calculate_bmi(weight, height):
    height_in_meters = height / 100
    return weight / (height_in_meters ** 2)

def calculate_daily_calories(age, weight, height, gender, activity_level='moderate'):
    if gender == 'male':
        calories = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        calories = 10 * weight + 6.25 * height - 5 * age - 161

    activity_factors = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    return calories * activity_factors.get(activity_level, 1.55)
