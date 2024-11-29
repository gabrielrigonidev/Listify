from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.App, name="home"),
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path("tarefas/", views.index, name="index"),
    path('criar-tarefa/', views.criar_tarefa, name='criar-tarefa'),
    path('mover-tarefa/', views.trocar_posicoes, name='mover-tarefa'),
]
