from rest_framework import serializers
from .models import TodoList
from django.contrib.auth.models import User
from django.db import models
from .models import Todo, TodoList

class TodoSerializer(serializers.Serializer): #Serializador de um Todo
    class Meta:
        model = Todo
        fields = '__all__'

class TodoListSerializer(serializers.ModelSerializer): #Serializador de uma TodoList
    class Meta:
        model = TodoList
        fields = ['title']
    
    def create(self, validated_data):
        return TodoList.objects.create(**validated_data)
    
#Uma TodoList poderá contar uma ou mais Todo
#Um usuário poderá conter uma um mais TodoList