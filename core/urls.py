from django.urls import path
from . import views
from .views import MedicoCreateView
from .views import ConsultaCreateView
from .views import ConsultaUpdateView
from .views import ConsultaListView
from .views import ConsultaDeleteView


urlpatterns = [
    path("", views.home, name="home"),
    path("cadastro", MedicoCreateView.as_view(),  name="cadastro_medico"),
    path("agendamento", ConsultaCreateView.as_view(), name="criar_agendamento"),
    path('consulta/<int:pk>/editar/', ConsultaUpdateView.as_view(), name='editar_agendamento'),
    path("historico", ConsultaListView.as_view(), name="historico"),
    path("consulta/<int:pk>/excluir/", ConsultaDeleteView.as_view(), name="excluir_agendamento"),
    path("buscar-consultas/", views.buscar_consultas, name="buscar_consultas"),
]