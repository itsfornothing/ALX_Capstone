from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from django.contrib.auth.models import User
from django.conf import settings




class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            user = User.objects.get(id=payload['user_id'])
            return (user, token)
        
        except ExpiredSignatureError:
            raise AuthenticationFailed("Your token has expired!")
        
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found!")
        
        except InvalidTokenError:
            raise AuthenticationFailed("You have provided invalid token!")
        
    def authenticate_header(self, request):
        return 'Bearer'
    