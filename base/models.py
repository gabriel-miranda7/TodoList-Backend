from django.db import models
from django.contrib.auth.models import User

class TodoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)

    def __str__(self):  #Retorna a string titulo
        return self.title
    
    class Meta:
        ordering = ['title']  #Ordena os todos pelo titulo

class Todo(models.Model):  #Define os atributos de um ToDo
    title = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True, max_length=500)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)
    todoList = models.ForeignKey(TodoList, on_delete=models.CASCADE, null = True) #Cada TO-Do aponta para uma lista de TOdos

    def __str__(self):  #Retorna a string titulo
        return self.title
    
    class Meta:
        ordering = ['complete']  #Ordena os todos pelos completos e pelos não completos
