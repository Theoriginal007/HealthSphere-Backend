# authentication.py for API module

import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

# Function to create JWT token
def generate_jwt_token(user):
    """
    Generate a JWT token for user authentication.

    Parameters:
    - user: User object for which to create the token

    Returns:
    - token: Encoded JWT token as a string
    """
    payload = {
        'user_id': user.id,
        'username': user.username,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=2)  # Token expiration set to 2 hours
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

# Function to decode JWT token
def decode_jwt_token(token):
    """
    Decode and validate a JWT token.

    Parameters:
    - token: JWT token as a string

    Returns:
    - payload: Decoded token data
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Token has expired")
    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Invalid token")

# Middleware-like function to authenticate user using JWT token
def get_user_from_token(token):
    """
    Get a User object from a valid JWT token.

    Parameters:
    - token: JWT token as a string

    Returns:
    - user: User object or raises an exception if invalid
    """
    try:
        payload = decode_jwt_token(token)
        user = User.objects.get(id=payload['user_id'])
        return user
    except ObjectDoesNotExist:
        raise AuthenticationFailed("User not found")
    except Exception as e:
        raise AuthenticationFailed(f"Authentication error: {e}")

# Function to extract token from request headers
def get_token_from_request(request):
    """
    Extract the JWT token from the authorization header.

    Parameters:
    - request: Django/DRF request object

    Returns:
    - token: Extracted token as a string
    """
    auth_header = get_authorization_header(request).split()
    if not auth_header or auth_header[0].lower() != b'bearer':
        raise AuthenticationFailed("Authorization header must start with Bearer")
    
    if len(auth_header) == 1:
        raise AuthenticationFailed("Token missing")
    elif len(auth_header) > 2:
        raise AuthenticationFailed("Invalid token format")

    return auth_header[1].decode('utf-8')
