from rest_framework import serializers
from .models import TodoList
from django.contrib.auth.models import User
from django.db import models

class TodoSerializer(serializers.Serializer): #Serializador de um Todo
    title = serializers.models.CharField(max_length=30)
    description = serializers.models.TextField(null=True, blank=True, max_length=500)
    complete = serializers.models.BooleanField(default=False)
    create = serializers.models.DateTimeField(auto_now_add=True)
    todoList = serializers.models.ForeignKey(TodoList, on_delete=models.CASCADE)

class TodoListSerializer(serializers.Serializer): #Serializador de uma TodoList
    user = serializers.models.ForeignKey(User, on_delete=models.CASCADE)
    title = serializers.models.CharField(max_length=30)

#Uma TodoList poderá contar uma ou mais Todo
#Um usuário poderá conter uma um mais TodoList