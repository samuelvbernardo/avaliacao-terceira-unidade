from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Consulta, Medico, Paciente
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

def home(request):
    return render(request, "core/pages/home.html")

class MedicoCreateView(CreateView):
    model = Medico
    template_name = "core/pages/cadastro_medico.html"
    fields = ["nome", "especialidade"]
    
    def form_valid(self, form):
        self.object = form.save()
        return self.render_to_response(
        self.get_context_data(
        sucesso=True,
        medico=self.object,
        form=self.get_form(),
        medicos=self.get_queryset()
        )
    )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["medicos"] = self.get_queryset()
        return context
    
class MedicoListView(ListView):
    model = Medico
    template_name = "core/pages/medico/lista_medicos.html"
    context_object_name = "medicos"
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ConsultaCreateView(CreateView):
    model = Consulta
    template_name = "core/pages/consulta/criar_consulta.html"
    fields = ["paciente", "medico", "data", "horario", "avaliacao"]
    
    def form_valid(self, form):
        self.object = form.save()
        return self.render_to_response(
        self.get_context_data(
        sucesso=True,
        consulta=self.object,
        form=self.get_form(),
        consultas=self.get_queryset()
        )
    )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["consultas"] = self.get_queryset()
        context["medicos"] = Medico.objects.all()
        context["pacientes"] = Paciente.objects.all()
        queryset = Consulta.objects.all().order_by("-data", "-horario")
        termo = self.request.GET.get("q")
        if termo:
            queryset = queryset.filter(
                Q(paciente__nome__icontains=termo) |
                Q(medico__nome__icontains=termo) |
                Q(medico__especialidade__icontains=termo)
            )
        context["consultas"] = queryset
        return context 
    
class ConsultaUpdateView(UpdateView):
    model = Consulta
    template_name = "core/pages/consulta/editar_consulta.html"
    fields = ["paciente", "medico", "data", "horario", "avaliacao"]
    success_url = reverse_lazy("criar_agendamento")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["medicos"] = Medico.objects.all()
        context["pacientes"] = Paciente.objects.all()
        context["editando"] = True
        return context
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class ConsultaListView(ListView):
    model = Consulta
    template_name = "core/pages/consulta/lista_consultas_historico.html"
    context_object_name = "consultas"
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["medicos"] = Medico.objects.all()
        context["pacientes"] = Paciente.objects.all()
        return context
    
class ConsultaDeleteView(DeleteView):
    model = Consulta
    template_name = "core/pages/consulta/confirmar_exclusao.html"
    success_url = reverse_lazy("criar_agendamento")

def buscar_consultas(request):
    termo = request.GET.get("q", "")
    consultas = Consulta.objects.all().order_by("-data", "-horario")
    if termo:
        consultas = consultas.filter(
            Q(paciente__nome__icontains=termo) |
            Q(medico__nome__icontains=termo) |
            Q(medico__especialidade__icontains=termo)
        )
    html = render_to_string("core/partials/tabela_consultas.html", {"consultas": consultas})
    return JsonResponse({"html": html})
