from django.http import JsonResponse
from datetime import timedelta
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from .forms import FormCriarTarefa, FormCadastroUser, FormLogin
from App.models import Tarefas, Usuario

def App(request):
    return render(request, 'home.html')

def index(request):
    if 'email' not in request.session:
        messages.error(request, "Você precisa estar logado para acessar esta página.")
        return redirect('login')

    usuario_email = request.session['email']
    usuario = Usuario.objects.get(email=usuario_email)

    tarefas = Tarefas.objects.filter(usuario=usuario).order_by('ordem_apresentacao')

    data_limite_urgente = timezone.now() + timedelta(days=3)
    tarefas_urgentes = tarefas.filter(data_limite__lte=data_limite_urgente)

    tarefas_alto_custo = tarefas.filter(custo__gte=1000)

    tarefas_campos = []
    for index, tarefa in enumerate(tarefas):
        anterior = tarefas[index - 1] if index > 0 else None
        proxima = tarefas[index + 1] if index < len(tarefas) - 1 else None
        tarefas_campos.append({
            'tarefa': tarefa,
            'anterior': anterior,
            'proxima': proxima,
        })

    return render(request, 'lista-tarefas.html', {
        'usuario': usuario,
        'tarefas_campos': tarefas_campos,
        'tarefas_urgentes_count': tarefas_urgentes.count(),
        'tarefas_alto_custo_count': tarefas_alto_custo.count(),
    })

def cadastro(request):
    novo_user = FormCadastroUser(request.POST or None)
    if request.method == 'POST':
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

def login(request):
    usuario_logado = FormLogin(request.POST or None)
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            usuario = Usuario.objects.get(email=email)
            if check_password(senha, usuario.senha):
                request.session.set_expiry(timedelta(seconds=180))
                request.session['email'] = email
                messages.success(request, "Logado com sucesso!")
                return redirect('index')
            else:
                messages.error(request, "Dados incorretos.")
        except Usuario.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")

    context = {
        'form': usuario_logado
    }
    return render (request, 'login.html', context)

def criar_tarefa(request):
    if 'email' not in request.session:
        messages.error(request, "Você precisa estar logado para acessar esta página.")
        return redirect('login')

    try:
        usuario = Usuario.objects.get(email=request.session['email'])
    except Usuario.DoesNotExist:
        messages.error(request, "Usuário não encontrado.")
        return redirect('login')

    if request.method == 'POST':
        form = FormCriarTarefa(request.POST)
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.usuario = usuario
            tarefa.save()
            messages.success(request, "Tarefa criada com sucesso!")
            return redirect('index')
    else:
        form = FormCriarTarefa()
    return render(request, 'criar-tarefa.html', {'form': form})

def editar_tarefa(request, tarefa_id):
    if 'email' not in request.session:
        messages.error(request, "Você precisa estar logado para acessar esta página.")
        return redirect('login')
    try:
        usuario = Usuario.objects.get(email=request.session['email'])
    except Usuario.DoesNotExist:
        messages.error(request, "Usuário não encontrado.")
        return redirect('login')

    tarefa = get_object_or_404(Tarefas, id=tarefa_id, usuario=usuario)

    if request.method == 'POST':
        form = FormCriarTarefa(request.POST, instance=tarefa)
        if form.is_valid():
            nome_novo = form.cleaned_data['nome']
            if Tarefas.objects.filter(nome=nome_novo, usuario=usuario).exclude(id=tarefa_id).exists():
                messages.error(request, "Já existe uma tarefa com esse nome.")
            else:
                form.save()
                messages.success(request, "Tarefa atualizada com sucesso!")
                return redirect('index')
    else:
        form = FormCriarTarefa(instance=tarefa)
    return render(request, 'editar-tarefa.html', {'form': form, 'tarefa': tarefa})

def excluir_tarefa(request, tarefa_id):
    if 'email' not in request.session:
        messages.error(request, "Você precisa estar logado para realizar esta ação.")
        return redirect('login')

    tarefa = get_object_or_404(Tarefas, id=tarefa_id)

    if request.method == 'POST':
        if request.POST.get("confirm") == "Sim":
            tarefa.delete()
            messages.success(request, "Tarefa excluída com sucesso!")
        else:
            messages.info(request, "Exclusão cancelada.")
        return redirect('index')

    return render(request, 'deletar-tarefa.html', {'tarefa': tarefa})

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

def logout(request):
    if request.method == 'POST':
        try:
            del request.session['email']
            messages.success(request, "Você foi deslogado com sucesso.")
            return redirect('index')
        except KeyError:
            messages.error(request, "Erro ao tentar deslogar.")
        return redirect('login')

    return render(request, 'logout.html')
