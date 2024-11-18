from django.test import TestCase
from django.contrib.auth.models import User
from celery.result import AsyncResult
from .tasks import send_weekly_health_report, clean_up_old_records
from unittest.mock import patch
from django.core.mail import send_mail

class CeleryTasksTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    @patch('healthapp.tasks.send_mail')
    def test_send_weekly_health_report(self, mock_send_mail):
        # Mocking the email send task
        task_result = send_weekly_health_report.apply_async(args=[self.user.id])
        task_result.get()  # Simulate completion of the task
        self.assertTrue(mock_send_mail.called)
        self.assertIn('Weekly Health Report', mock_send_mail.call_args[0][1])
        self.assertIn(self.user.email, mock_send_mail.call_args[0][3])

    @patch('healthapp.tasks.HealthRecord.objects.filter')
    def test_clean_up_old_records(self, mock_filter):
        # Simulate record deletion during cleanup
        mock_filter.return_value.delete.return_value = None
        task_result = clean_up_old_records.apply_async()
        task_result.get()  # Simulate completion of the task
        mock_filter.return_value.delete.assert_called_once()

    def test_send_weekly_health_report_fail(self):
        # Simulate failure in the report sending task
        with self.assertRaises(Exception):
            send_weekly_health_report.apply_async(args=[9999])  # Non-existent user
