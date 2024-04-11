from django.urls import path
from . import views

urlpatterns = [ 
    path('todolists/', views.allTodoLists, name='todosLists'),
    path('todolist/<str:list_title>/', views.TodoListGet, name='todolist-get-by-name'),
    path('todolistnew/', views.CreateTodoList, name='create-todo-list')
]