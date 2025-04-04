import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta, timezone
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .serializers import RegisterationSerializer, LoginSerializer, NoteSerializer, CategorySerializer  
from .models import Note, Category
from .authentication import JWTAuthentication
from rest_framework.permissions import AllowAny



def generate_token(user):
    expire_time = datetime.now(timezone.utc) + timedelta(days=7)
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': expire_time,
        'iat': datetime.now(timezone.utc),
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token, expire_time


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token, expire_time = generate_token(user)
            return Response({'token': token, 'expires_at': expire_time}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = generate_token(user)
            return Response({'token': token}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    

class CreateNoteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = NoteSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        
        all_notes = Note.objects.filter(owner=request.user)
        serializer = NoteSerializer(all_notes, many=True, context={'request': request}) 

        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    

class NoteDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, title):
       
        try:
            note = Note.objects.filter(title__icontains=title, owner=request.user)
            serializer = NoteSerializer(note, many=True, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Note.DoesNotExist:
            return Response({"status": "error", "message": "Note with the provided title not found"}, status=status.HTTP_404_NOT_FOUND)

    
    def put(self, request, title):
        try:
            note = Note.objects.get(title__icontains=title, owner=request.user)
            serializer = NoteSerializer(note, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Note.DoesNotExist:
            return Response({"status": "error", "message": "Note with the provided title not found"}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, title):
        try:
            note = Note.objects.filter(title__icontains=title, owner=request.user)
            if note.exists():
                note.delete()
                return Response({"status": "success", 'msg': 'Note deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Note.DoesNotExist:
            return Response({"status": "error", "message": "Note with the provided title not found"}, status=status.HTTP_404_NOT_FOUND)
        


class NoteCategorySearchView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def get(self, request, category):
        try:
            note = Note.objects.filter(category__name__icontains=category, category__owner=request.user)
            serializer = NoteSerializer(note, many=True, context={'request': request})

            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        except Note.DoesNotExist:
            return Response({"status": "error", "message": f"Notes with {category} category not found"}, status=status.HTTP_404_NOT_FOUND)
        

    def delete(self, request, category):
        try:
            note = Note.objects.filter(category__name__icontains=category, category__owner=request.user)
            if note.exists():
                note.delete()
                return Response({"status": "success", 'msg': 'Note deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        except Note.DoesNotExist:
            return Response({"status": "error", "message": f"Notes with {category} category not found"}, status=status.HTTP_404_NOT_FOUND)
        

class CategoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        all_categories = Category.objects.filter(owner=request.user)
        serializer = CategorySerializer(all_categories, many=True, context={'request': request}) 

        if not all_categories.exists():
            return Response({"status": "empty", "message": "No categories found."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class NoteTagSearchView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def get(self, request, tag):
        try:
            note = Note.objects.filter(tags__contains=tag, owner=request.user)
            serializer = NoteSerializer(note, many=True, context={'request': request})

            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        except Note.DoesNotExist:
            return Response({"status": "error", "message": f"Notes with {tag} tag not found"}, status=status.HTTP_404_NOT_FOUND)
        

    def delete(self, request, tag):
        try:
            note = Note.objects.filter(tags__contains=[tag], owner=request.user)
            if note.exists():
                note.delete()
                return Response({"status": "success", 'msg': 'Note deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        except Note.DoesNotExist:
            return Response({"status": "error", "message": f"Notes with {tag} tag not found"}, status=status.HTTP_404_NOT_FOUND)
        
