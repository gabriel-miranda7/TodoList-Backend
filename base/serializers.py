from rest_framework import serializers
from .models import TodoList
from django.contrib.auth.models import User
from django.db import models

class TodoSerializer(serializers.Serializer):
    title = serializers.models.CharField(max_length=30)
    description = serializers.models.TextField(null=True, blank=True, max_length=500)
    complete = serializers.models.BooleanField(default=False)
    create = serializers.models.DateTimeField(auto_now_add=True)
    todoList = serializers.models.ForeignKey(TodoList, on_delete=models.CASCADE)

class TodoListSerializer(serializers.Serializer):
    user = serializers.models.ForeignKey(User, on_delete=models.CASCADE)
    title = serializers.models.CharField(max_length=30)