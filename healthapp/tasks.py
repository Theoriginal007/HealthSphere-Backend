from celery import shared_task
from .models import HealthRecord, ExerciseLog
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta

@shared_task(bind=True)
def send_weekly_health_report(self, user_id):
    try:
        user = User.objects.get(id=user_id)
        records = HealthRecord.objects.filter(user=user, recorded_at__gte=now() - timedelta(days=7))
        total_exercise = ExerciseLog.objects.filter(user=user, date__gte=now() - timedelta(days=7)).aggregate(Sum('calories_burned'))

        report = f"Weekly Health Report for {user.username}:\n\n"
        report += f"Total health records: {records.count()}\n"
        report += f"Total calories burned: {total_exercise['calories_burned__sum']}\n"

        send_mail(
            'Weekly Health Report',
            report,
            'health@healthsphere.com',
            [user.email],
            fail_silently=False,
        )
        return f"Weekly report sent to {user.email}"
    except Exception as e:
        raise self.retry(exc=e, countdown=60 * 5)

@shared_task
def clean_up_old_records():
    cutoff_date = now() - timedelta(days=365)
    HealthRecord.objects.filter(recorded_at__lte=cutoff_date).delete()
    return "Old health records cleaned up."
