from django.db import models

class Tarefas(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    custo = models.DecimalField(max_digits=10, decimal_places=2)
    data_limite = models.DateField()
    ordem_apresentacao = models.IntegerField(unique=True)

    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.id and not self.ordem_apresentacao:
            max_ordem = Tarefas.objects.aggregate(models.Max('ordem_apresentacao'))['ordem_apresentacao__max'] or 0
            self.ordem_apresentacao = max_ordem + 1
        super().save(*args, **kwargs)

class Usuario(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)