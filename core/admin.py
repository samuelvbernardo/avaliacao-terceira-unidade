from django.contrib import admin
from .models import Paciente, Medico, Consulta

# Registrando os modelos no Django Admin
admin.site.register(Paciente)
admin.site.register(Medico)
admin.site.register(Consulta)