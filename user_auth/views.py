from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializers
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.hashers import check_password

@api_view(['POST'])  #Rota de registro de usuário
def register(request):
    existing_user = User.objects.filter(username=request.data.get('username', ''))
    if existing_user.exists():
        return Response({'error': 'Este nome de usuário já está em uso.'}, status=status.HTTP_403_FORBIDDEN)
    serializer = UserSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({token.key}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])  #Rota de login
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail" : "Incorrect Password"}, status=status.HTTP_404_NOT_FOUND)
    token, created= Token.objects.get_or_create(user=user)
    serializer = UserSerializers(instance=user)
    return Response({token.key})

@api_view(['PUT']) #Rota para alterar dados do usuário
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateUser(request):
    user = request.user
    new_username = request.data.get('username', None)
    new_password = request.data.get('password', None)
    if new_password and new_username:  #Verifica se o usuário quer alterar o username e a senha ao mesmo tempo
        return Response("Erro. Não é possível alterar a Password e o Username ao mesmo tempo", status=status.HTTP_400_BAD_REQUEST)
    if new_username and new_username == user.username: #Compara o username antigo com o novo
        return Response("O novo username não pode ser o mesmo", status=status.HTTP_400_BAD_REQUEST)
    if new_password and check_password(new_password, user.password): #Compara a senha antiga com a nova
        return Response("A nova senha não pode ser a mesma", status=status.HTTP_400_BAD_REQUEST)
    if new_username: #Altera o username
        user.username = new_username
        user.save()
        return Response("Username atualizado com sucesso", status=status.HTTP_200_OK)
    elif new_password: #Altera a password
        user.set_password(new_password)
        user.save()
        return Response("Password atualizada com sucesso", status=status.HTTP_200_OK)
        

@api_view(['GET']) #Retorna 
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def authenticate_token(request):
    return Response({"Ok"})
