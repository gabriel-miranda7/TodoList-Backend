from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Todo, TodoList
from .serializers import TodoSerializer, TodoListSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes({IsAuthenticated})
def allTodoLists(req):   #endpoint para visualizar todas as listas todo
    if req.method == 'GET':
        TodosLists = TodoList.objects.filter(user=req.user) #pega todas as todosLists
        serializer = TodoListSerializer(TodosLists, many = True) #serializa os dados
        return Response(serializer.data)

@api_view(['GET'])
def TodoListGet(req, list_title): 
    if req.method == 'GET':  #endpoint para visualizar lista
        try:
            Todo_List = TodoList.objects.get(title=list_title)
            serializer = TodoSerializer(Todo_List)
            return JsonResponse(serializer.data)
        except TodoList.DoesNotExist:
            return JsonResponse({'message' : 'Lista inexistente'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes({IsAuthenticated}) #verifica se o usuário está autorizado
def CreateTodoList(req):
    if req.method == 'POST':  #cria uma nova lista
        if not req.user.is_authenticated: #verifica se o usuário está autorizado
            return JsonResponse({'message': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = TodoListSerializer(data=req.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = req.user
            serializer.save()
            return Response(status=status.HTTP_201_CREATED) #Retorna o status 201
        return Response(status=status.HTTP_400_BAD_REQUEST) #Retorna bad request caso o serializer seja inválido
 
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes({IsAuthenticated}) #Cria um ToDo e adciona á uma todoList
def CreateTodo(req):
    if not req.user.is_authenticated: #Verifica se o usuário está autenticado
        return JsonResponse({'message': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    if 'todo_list_title' not in req.data: #Procura no request o nome da TodoList
         return Response({'error': 'Todo list title is required'}, status=status.HTTP_400_BAD_REQUEST)
    todo_list_title = req.data['todo_list_title'] #Pega a Todolist pai
    try: 
        todo_list = TodoList.objects.get(title=todo_list_title, user=req.user)
    except TodoList.DoesNotExist:
        return JsonResponse({'message': 'Todo list not found'}, status=status.HTTP_404_NOT_FOUND)
    req.data['todoList'] = todo_list.id  # Adiciona o título da lista todo ao dados do todo antes de serializá-lo 
    serializer = TodoSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
