from django.urls import path
from .views import RegisterView, LoginView, CreateNoteView, NoteDetailView, NoteCategorySearchView, CategoryView, NoteTitleSearchView


urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('notes', CreateNoteView.as_view(), name='notes'),
    path('note/<int:note_id>', NoteDetailView.as_view(), name='note_by_id'),
    path('note/search/title/<str:title>', NoteTitleSearchView.as_view(), name='note_by_title'),
    path('notes/search/category/<str:category>', NoteCategorySearchView.as_view(), name='note_by_category'),
    path('categories', CategoryView.as_view(), name='categories'),
]