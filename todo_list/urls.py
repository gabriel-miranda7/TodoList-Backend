
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')), #Conecta a rota da base com o projeto.
    path('authenticate/', include('user_auth.urls')) #Conecta ao sistema de autenticação
]
