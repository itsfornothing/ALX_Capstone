from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Note, Category
from datetime import timezone, datetime
from openai import OpenAI
from dotenv import load_dotenv
import os



load_dotenv()
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
    

class LoginSerializer(serializers.Serializer):
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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class NoteSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = serializers.ListField(child=serializers.CharField(max_length=50), allow_empty=True)


    class Meta:
        model = Note
        fields = ['title', 'category', 'tags', 'content', 'summary', 
                  'reminder_date', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_category(self, value):
        user = self.context['request'].user
        if not isinstance(value, dict) or 'name' not in value:
            raise serializers.ValidationError("Invalid category format.")
        
        category_name = value['name']
        category, created = Category.objects.get_or_create(name=category_name.lower(), owner=user)
        return category
    

    def validate_reminder_date(self, value):
        if value < datetime.now(timezone.utc).date():
            raise serializers.ValidationError("Reminder date cannot be in the past.")
        return value
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        content = validated_data['content']
        

        client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("DEEPSEEK_API"),
        )

        try:
            completion = client.chat.completions.create(
            
            extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>", 
            "X-Title": "<YOUR_SITE_NAME>",
            },
            extra_body={},
            model="deepseek/deepseek-r1:free",
            messages=[
                {
                "role": "user",
                "content": f"Summarize this article: {content}"
                }
                ]
            )
            validated_data['summary'] = completion.choices[0].message.content
        except Exception as e:
            validated_data['summary'] = "Sorry, Summary unavailable due to an API error."

       
        return super().create(validated_data)
    

    def update(self, instance, validated_data):
        if validated_data['content'] != instance.content:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("DEEPSEEK_API"),
            )

            try:
                completion = client.chat.completions.create(

                extra_headers={
                    "HTTP-Referer": "<YOUR_SITE_URL>", 
                    "X-Title": "<YOUR_SITE_NAME>",
                    },
                    extra_body={},
                    model="deepseek/deepseek-r1:free",
                    messages=[
                        {
                        "role": "user",
                        "content": f"Summarize this article: {validated_data['content']}"
                        }
                        ]
                )
                validated_data['summary'] = completion.choices[0].message.content
            except Exception as e:
                validated_data['summary'] = "Sorry, Summary unavailable due to an API error."
        return super().update(instance, validated_data)

