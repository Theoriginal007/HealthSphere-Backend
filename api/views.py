# views.py for API module

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import HealthRecordSerializer, UserSerializer
from .authentication import generate_jwt_token, get_user_from_token, get_token_from_request
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
import logging

logger = logging.getLogger(__name__)

class HealthRecordView(APIView):
    """
    API endpoint to manage health records.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            records = HealthRecord.objects.all()
            serializer = HealthRecordSerializer(records, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching health records: {e}")
            return Response({'error': 'Failed to fetch records'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = HealthRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Health record created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.warning("Invalid data submitted for health record")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    """
    API endpoint for user login and JWT generation.
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            token = generate_jwt_token(user)
            serializer = UserSerializer(user)
            logger.info(f"User {username} logged in successfully")
            return Response({'token': token, 'user': serializer.data}, status=status.HTTP_200_OK)
        else:
            logger.warning(f"Failed login attempt for user: {username}")
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class HealthRecordDetailView(APIView):
    """
    API endpoint for retrieving, updating, or deleting a specific health record.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            record = HealthRecord.objects.get(pk=pk)
            serializer = HealthRecordSerializer(record)
            return Response(serializer.data)
        except HealthRecord.DoesNotExist:
            logger.warning(f"Health record with ID {pk} not found")
            return Response({'error': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching health record: {e}")
            return Response({'error': 'Failed to retrieve record'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
