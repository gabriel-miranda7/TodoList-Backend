from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import TodoList, Todo
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
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes({IsAuthenticated})
def allTodos(req):
    if req.method == 'GET':
        if 'todo_list_title' not in req.data: #Procura no request o nome da TodoList
         return Response({'error': 'Todo list title is required'}, status=status.HTTP_400_BAD_REQUEST)
        todo_list_title = req.data['todo_list_title'] #Pega a Todolist pai
        try: 
            todo_list = TodoList.objects.get(title=todo_list_title, user=req.user)
        except TodoList.DoesNotExist:
            return Response({'message': 'Todo list not found'}, status=status.HTTP_404_NOT_FOUND)
        todos = todo_list.todo_set.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes({IsAuthenticated}) #verifica se o usuário está autorizado
def CreateTodoList(req):
    if req.method == 'POST':  #cria uma nova lista
        serializer = TodoListSerializer(data=req.data)
        if serializer.is_valid():
            todo_list_title = serializer.validated_data.get('title')
            if TodoList.objects.filter(title=todo_list_title, user=req.user).exists():
                return Response({'error': 'Todo list with this title already exists'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.validated_data['user'] = req.user
            serializer.save()
            return Response({'message' : 'Todo List created'}, status=status.HTTP_201_CREATED) #Retorna o status 201
        return Response(status=status.HTTP_400_BAD_REQUEST) #Retorna bad request caso o serializer seja inválido
 
@api_view(['POST', 'DELETE', 'PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes({IsAuthenticated}) #Cria um ToDo e adciona á uma todoList
def CreateTodo(req):
    if req.method == 'POST':
        if 'todo_list_title' not in req.data: #Procura no request o nome da TodoList
            return Response({'error': 'Todo list title is required'}, status=status.HTTP_400_BAD_REQUEST)
        todo_list_title = req.data['todo_list_title'] #Pega a Todolist pai
        try: 
            todo_list = TodoList.objects.get(title=todo_list_title, user=req.user)
        except TodoList.DoesNotExist:
            return Response({'message': 'Todo list not found'}, status=status.HTTP_404_NOT_FOUND)
        req.data['todoList'] = todo_list.id  # Adiciona o título da lista todo ao dados do todo antes de serializá-lo 
        serializer = TodoSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif req.method == 'DELETE':
        if 'todo_id' not in req.data:
            return Response({"message" : "Todo ID é exigido."}, status=status.HTTP_400_BAD_REQUEST)
        todo_id = req.data['todo_id']
        try:
            todo = Todo.objects.get(id=todo_id)
        except Todo.DoesNotExist:
            return Response({'message': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)   
        todo.delete()  # Exclua o ToDo
        return Response({'message': 'Todo deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    elif req.method == 'PUT':
        if 'todo_id' not in req.data:
            return Response({"message" : "Todo ID é exigido."}, status=status.HTTP_400_BAD_REQUEST)
        todo_id = req.data['todo_id']
        try:
            todo = Todo.objects.get(id=todo_id)
        except Todo.DoesNotExist:
            return Response({'message': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TodoSerializer(todo, data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
