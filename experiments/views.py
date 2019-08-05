from django.views.generic import DetailView, CreateView, ListView
from django.urls import reverse_lazy

from experiments.models import Experiment
from experiments.forms import ExperimentForm


class ExperimentDetailView(DetailView):
    model = Experiment


class ExperimentCreateView(CreateView):
    model = Experiment
    form_class = ExperimentForm
    success_url = reverse_lazy('home')

    def get_initial(self):
        initial = super().get_initial()
        initial['author'] = self.request.user.pk
        return initial
