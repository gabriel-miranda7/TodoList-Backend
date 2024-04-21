from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import TodoList, Todo
from .serializers import TodoSerializer, TodoListSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes({IsAuthenticated})
def allTodoLists(req):   #endpoint para visualizar todas as listas todo
    if req.method == 'GET':
        todo_lists = TodoList.objects.filter(user=req.user)
        data = []
        for todo_list in todo_lists:
            todo_list_data = TodoListSerializer(todo_list).data
            todos = Todo.objects.filter(todoList=todo_list)
            todo_list_data['todos'] = TodoSerializer(todos, many=True).data
            data.append(todo_list_data)
        return Response(data)

@api_view(['POST', 'PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes({IsAuthenticated}) #verifica se o usuário está autorizado
def CreateTodoList(req):
    if req.method == 'POST':  #cria uma nova lista
        serializer = TodoListSerializer(data=req.data)
        if serializer.is_valid():
            todo_list_title = serializer.validated_data.get('title')
            if len(todo_list_title) > 30:
                return Response({"error": "Too long"}, status=status.HTTP_400_BAD_REQUEST)
            if TodoList.objects.filter(title=todo_list_title, user=req.user).exists():
                return Response({'error': 'Already exists'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.validated_data['user'] = req.user
            serializer.save()
            return Response({'message' : 'Todo List created'}, status=status.HTTP_201_CREATED) #Retorna o status 201
        return Response(status=status.HTTP_400_BAD_REQUEST) #Retorna bad request caso o serializer seja inválido
    elif req.method == 'PUT':
        if 'listId' not in req.data:
            return Response({'error': 'Todo list id is required'}, status=status.HTTP_400_BAD_REQUEST)
        list_id = req.data['listId']
        try:
            todo_list = TodoList.objects.get(id=list_id, user=req.user)
        except TodoList.DoesNotExist:
            return Response({'message': 'Todo list not found'}, status=status.HTTP_404_NOT_FOUND)
        
        new_title = req.data.get('newtitle')
        new_favorite = req.data.get('favorite')

        if new_title:
            todo_list.title = new_title
            todo_list.save()
            return Response({'message': 'Todo list title updated successfully'}, status=status.HTTP_200_OK)
        elif new_favorite is not None:  # Use 'is not None' to allow setting favorite to False
            todo_list.favorite = new_favorite
            todo_list.save()
            return Response({'message': 'Todo list favorite updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'New title or favorite is required for updating the todo list'}, status=status.HTTP_400_BAD_REQUEST)


 
@api_view(['POST', 'DELETE', 'PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes({IsAuthenticated}) #Cria um ToDo e adciona á uma todoList
def CreateTodo(req):
    if req.method == 'POST':
        if 'todoList' not in req.data: #Procura no request o nome da TodoList
            return Response({'error': 'Todo list title is required'}, status=status.HTTP_400_BAD_REQUEST)
        todo_list_title = req.data['todoList'] #Pega a Todolist pai
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
    
    elif req.method == 'DELETE':  #Método para deletar Todo
        if 'todoId' not in req.data:
            return Response({"message" : "Todo ID é exigido."}, status=status.HTTP_400_BAD_REQUEST)
        todo_id = req.data['todoId']
        try:
            todo = Todo.objects.get(id=todo_id)
        except Todo.DoesNotExist:
            return Response({'message': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)   
        todo.delete()  # Exclua o ToDo
        return Response({'message': 'Todo deleted successfully'}, status=status.HTTP_200_OK)
    
    elif req.method == 'PUT': #Método para editar Todo
        if 'todoId' not in req.data:
            return Response({"message" : "Todo ID é exigido."}, status=status.HTTP_400_BAD_REQUEST)
        todo_id = req.data['todoId']
        try:
            todo = Todo.objects.get(id=todo_id)
        except Todo.DoesNotExist:
            return Response({'message': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TodoSerializer(todo, data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes({IsAuthenticated}) 
def isComplete(req):
    if req.method == 'POST':
        if 'todoId' not in req.data:
            return Response({"message" : "Todo ID é exigido."}, status=status.HTTP_400_BAD_REQUEST)
        todo_id = req.data['todoId']
        try:
            todo = Todo.objects.get(id=todo_id)
            return Response({"complete" : todo.complete})
        except Todo.DoesNotExist:
            return Response({'message': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND) 
        
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes({IsAuthenticated}) 
def treatTrashBin(req):
    if req.method == 'PUT':
        if 'todoId' not in req.data:
            return Response({"message" : "Todo ID é exigido."}, status=status.HTTP_400_BAD_REQUEST)
        todo_id = req.data['todoId']
        try:
            todo_ = Todo.objects.get(id=todo_id)
        except Todo.DoesNotExist:
            return Response({'message': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND) 
        todo_.isOnTrashBin = not todo_.isOnTrashBin
        todo_.timeOfTrashBin = timezone.now()
        todo_.save()
        return Response(todo_.isOnTrashBin, status=status.HTTP_200_OK) 

