from django.http import JsonResponse
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.db import transaction
from .forms import FormCriarTarefa, FormCadastroUser, FormLogin
from App.models import Tarefas, Usuario

def App(request):
    return render(request, 'home.html')

def index(request):
    if 'email' not in request.session:
        messages.error(request, "Você precisa estar logado para acessar esta página.")
        return redirect('login')

    tarefas = Tarefas.objects.order_by('ordem_apresentacao')
    tarefas_contexto = []

    for index, tarefa in enumerate(tarefas):
        anterior = tarefas[index - 1] if index > 0 else None
        proxima = tarefas[index + 1] if index < len(tarefas) - 1 else None
        tarefas_contexto.append({
            'tarefa': tarefa,
            'anterior': anterior,
            'proxima': proxima,
        })
    return render(request, 'lista-tarefas.html', {'tarefas_contexto': tarefas_contexto})

def cadastro(request):
    novo_user = FormCadastroUser(request.POST or None)
    if request.POST:
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "E-mail já esta sendo utilizado!")
        elif novo_user.is_valid():
            novo_user.instance.senha = make_password(senha)
            novo_user.save()
            messages.success(request, "Usuário cadastrado com sucesso!")
            return redirect('index')
    context = {
        'form': novo_user
    }
    return render(request, 'cadastro.html', context)

def criar_tarefa(request):
    if request.method == 'POST':
        form = FormCriarTarefa(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = FormCriarTarefa()
    return render(request, 'criar-tarefa.html', {'form': form})

def trocar_ordem_apresentacao(id_1, id_2):
    with transaction.atomic():
        task1 = Tarefas.objects.get(id=id_1)
        task2 = Tarefas.objects.get(id=id_2)

        task1_ordem = task1.ordem_apresentacao
        task2_ordem = task2.ordem_apresentacao

        Tarefas.objects.filter(id=id_1).update(ordem_apresentacao=-99999)
        Tarefas.objects.filter(id=id_2).update(ordem_apresentacao=task1_ordem)
        Tarefas.objects.filter(id=id_1).update(ordem_apresentacao=task2_ordem)
        
def trocar_posicoes(request):
    if request.method == 'POST':
        tarefa_cima = request.POST.get("task1_id")
        tarefa_baixo = request.POST.get("task2_id")

        if not (tarefa_cima and tarefa_baixo):
            return JsonResponse({"error": "Missing task IDs"}, status=400)

        try:
            trocar_ordem_apresentacao(int(tarefa_cima), int(tarefa_baixo))
            return redirect('index')
        except ValueError as e:
            return JsonResponse({
                "error": str(e),
                "task1_id": tarefa_cima,
                "task2_id": tarefa_baixo
            }, status=404)
        except Exception as e:
            return JsonResponse({
                "error": "An unexpected error occurred",
                "details": str(e),
                "task1_id": tarefa_cima,
                "task2_id": tarefa_baixo
            }, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

def login(request):
    formLogin = FormLogin(request.POST or None)

    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            usuario = Usuario.objects.get(email=email)
            if check_password(senha, usuario.senha):
                request.session.set_expiry(timedelta(seconds=60))
                request.session['email'] = email
                messages.success(request, "Logado com sucesso!")
                return redirect('index')
            else:
                messages.error(request, "Senha incorreta.")
        except Usuario.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")

    context = {
        'form': formLogin
    }
    return render (request, 'login.html', context)
    
