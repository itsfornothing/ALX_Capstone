from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


deepseek = "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"


class RegisterationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True,required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'Username already exists'})
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True,required=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = User.objects.filter(email=email).first()

        if user:
            user_authenticate = authenticate(username=user.username, password=password)

            if user_authenticate:
                data['user'] = user_authenticate
                return data
            
        raise serializers.ValidationError({'error': 'Invalid credentials'})