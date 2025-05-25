from django.db import models

class Paciente(models.Model):
    nome = models.CharField(max_length=40)  
    email = models.EmailField(unique=True)  
    telefone = models.CharField(max_length=15, blank=True, null=True)  # Telefone do paciente (opcional)

    def __str__(self):
        return self.nome

class Medico(models.Model):
    nome = models.CharField(max_length=40)  
    especialidade = models.CharField(max_length=30)  

    def __str__(self):
        return f"{self.nome} - {self.especialidade}"

class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    data = models.DateField()
    horario = models.TimeField()
    avaliacao = models.PositiveSmallIntegerField(
        null=True, blank=True,
        choices=[(i, f"{i} Estrela{'s' if i > 1 else ''}") for i in range(1, 6)]
    )

    @property
    def tipo(self):
        return self.medico.especialidade


    def __str__(self):
        return f"{self.tipo} - {self.paciente} com {self.medico} em {self.data} às {self.horario}"
