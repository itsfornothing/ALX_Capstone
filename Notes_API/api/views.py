import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from datetime import datetime, timedelta, timezone
from django.conf import settings
from .serializers import RegisterationSerializer, LoginSerializer



def generate_token(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.now(timezone.utc) + timedelta(hours=24),
        'iat': datetime.now(timezone.utc),
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = generate_token(user)
            return Response({'token': token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = generate_token(user)
            return Response({'token': token}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    

class JWTAuthentication:
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            user = User.objects.get(id=payload['user_id'])
            return (user, token)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            return None
        
    def authenticate_header(self, request):
        return 'Bearer'