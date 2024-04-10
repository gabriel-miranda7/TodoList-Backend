from django.contrib import admin
from .models import Todo, TodoList

admin.site.register(TodoList) #Registra uma todoList na página admin
admin.site.register(Todo) #Registra uma todo na página admin
# Register your models here.
