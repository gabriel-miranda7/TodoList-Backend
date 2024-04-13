from django.urls import path
from . import views

urlpatterns = [ 
    path('todolists/', views.allTodoLists, name='todosLists'),
    path('todos/', views.allTodos, name='all-todos'),
    path('todolistnew/', views.CreateTodoList, name='create-todo-list'),
    path('todonew/', views.CreateTodo, name='create-todo')
]