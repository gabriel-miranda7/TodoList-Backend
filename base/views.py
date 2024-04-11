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