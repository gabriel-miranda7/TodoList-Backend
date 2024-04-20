from django.db import models
from django.contrib.auth.models import User

class TodoList(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)

    def __str__(self):  #Retorna a string titulo
        return self.title
    
    class Meta:
        ordering = ['title']  #Ordena os todos pelo titulo

class Todo(models.Model):  #Define os atributos de um ToDo
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True, max_length=500)
    complete = models.BooleanField(default=True)
    create = models.DateTimeField(auto_now_add=True)
    todoList = models.ForeignKey(TodoList, on_delete=models.CASCADE, null = True) #Cada TO-Do aponta para uma lista de TOdos
    isOnTrashBin = models.BooleanField(null=True, blank=True, default=False)
    timeOfTrashBin = models.DateTimeField(null=True, blank=True)

    def __str__(self):  #Retorna a string titulo
        return self.title
    
    class Meta:
        ordering = ['-complete']  #Ordena os todos pelos completos e pelos não completos
