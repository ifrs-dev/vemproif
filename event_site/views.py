from django.views.generic import TemplateView, FormView

from event_site.forms import ImportForm

class HomeView(TemplateView):
    template_name = 'home.html'


class SiaImporterView(FormView):
    template_name = 'importer.html'
    form_class = ImportForm


class SigaaImporterView(FormView):
    template_name = 'importer.html'
    form_class = ImportForm
