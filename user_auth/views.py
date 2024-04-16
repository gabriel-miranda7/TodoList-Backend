from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializers
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

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

@api_view(['GET']) #Retorna 
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def authenticate_token(request):
    return Response({"Ok"})
