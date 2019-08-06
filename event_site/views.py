from django.views.generic import TemplateView, FormView
from django.shortcuts import reverse

from event_site.forms import ImportFormSIGAA, ImportFormSIA, ImportFormServ
from experiments.models import Experiment

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["experiments"] = Experiment.objects.all()
        return context


class SiaImporterView(FormView):
    template_name = 'importer.html'
    form_class = ImportFormSIA

    def get_success_url(self):
        return reverse('home')


class SigaaImporterView(FormView):
    template_name = 'importer.html'
    form_class = ImportFormSIGAA

    def get_success_url(self):
        return reverse('home')


class ServImporterView(FormView):
    template_name = 'importer.html'
    form_class = ImportFormServ

    def get_success_url(self):
        return reverse('home')
