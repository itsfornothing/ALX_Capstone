from django.urls import path
from .views import RegisterView, LoginView, CreateNoteView, NoteDetailView, NoteCategorySearchView, CategoryView, NoteTagSearchView


urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('notes', CreateNoteView.as_view(), name='notes'),
    path('note/title/<str:title>', NoteDetailView.as_view(), name='get_put_delete_by_title'),
    path('notes/search/category/<str:category>', NoteCategorySearchView.as_view(), name='search_by_category'),
    path('notes/search/tag/<str:tag>', NoteTagSearchView.as_view(), name='search_by_tag'),
    path('categories', CategoryView.as_view(), name='categories'),

    path('notes/bulkdelete/tag/<str:tag>', NoteTagSearchView.as_view(), name='delete_by_tag'),
    path('notes/bulkdelete/category/<str:category>', NoteCategorySearchView.as_view(), name='delete_by_category'),
]