from django.urls import path
from . import views

urlpatterns = [ 
    path('todolists', views.allTodoLists, name='all-todos-lists'),
    path('todolistnew', views.CreateTodoList, name='create-todo-list'),
    path('todonew', views.CreateTodo, name='create-todo'),
    path('iscomplete', views.isComplete, name='is-todo-complete'),
    path('trashaddremove', views.treatTrashBin, name='add-and-delete-todo-trashbin'),
    path('alltodos', views.getAllTodos, name='get-all-todos-from-user')
]