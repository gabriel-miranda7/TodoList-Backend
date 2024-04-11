from django.contrib import admin
from .models import Todo, TodoList

admin.site.register(TodoList) #Registra todoList na página admin
admin.site.register(Todo) #Registra todo na página admin

