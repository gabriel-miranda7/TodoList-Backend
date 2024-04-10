from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status

from .models import Todo, TodoList
from .serializers import TodoSerializer, TodoListSerializer

def allTodoLists(req):   #endpoint para visualizar todas as listas todo
    if req.method == 'GET':
        TodosLists = TodoList.objects.all() #pega todas as todosLists
        serializer = TodoListSerializer(TodosLists) #serializa os dados
        return JsonResponse(serializer.data, safe=False)

def TodoListGet(req, list_title): 
    if req.method == 'GET':  #endpoint para visualizar lista
        try:
            Todo_List = TodoList.objects.get(title=list_title)
            serializer = TodoSerializer(Todo_List)
            return JsonResponse(serializer.data)
        except TodoList.DoesNotExist:
            return JsonResponse({'message' : 'Lista inexistente'})
    
    if req.method == 'POST':  #cria uma nova lista
        serializer = TodoListSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save(owner=req.user)
            return JsonResponse(status=status.HTTP_201_CREATED) #Retorna o status 201
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST) #Retorna bad request caso o serializer seja inválido