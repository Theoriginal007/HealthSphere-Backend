# urls.py for API module

from django.urls import path, include
from .views import HealthRecordView, UserLoginView, HealthRecordDetailView

app_name = 'api'

urlpatterns = [
    path('health-records/', HealthRecordView.as_view(), name='health-records-list'),
    path('health-records/<int:pk>/', HealthRecordDetailView.as_view(), name='health-record-detail'),
    path('login/', UserLoginView.as_view(), name='user-login'),
]
