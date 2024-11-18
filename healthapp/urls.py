from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HealthRecordViewSet, ExerciseLogViewSet, UserViewSet

router = DefaultRouter()
router.register(r'healthrecords', HealthRecordViewSet)
router.register(r'exerciselogs', ExerciseLogViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
