from django.urls import path
from . import views

urlpatterns = [
    path('', views.App, name="home"),
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path("tarefas/", views.index, name="index"),
    path('criar-tarefa/', views.criar_tarefa, name='criar-tarefa'),
    path('mover-tarefa/', views.trocar_posicoes, name='mover-tarefa'),
    path('tarefas/editar/<int:tarefa_id>/', views.editar_tarefa, name='editar-tarefa'),
    path('tarefas/excluir/<int:tarefa_id>/', views.excluir_tarefa, name='excluir-tarefa'),
    path('logout/', views.logout, name='logout'),
]
