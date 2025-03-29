from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('owner', 'name')


class Note(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notes')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='notes')
    tags = models.JSONField(default=list, blank=True)
    content = models.TextField()
    summary = models.TextField(blank=True)
    reminder_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('owner', 'title') 
