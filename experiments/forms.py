from django import forms
from django_select2.forms import Select2Widget, Select2MultipleWidget
from django.contrib.auth.models import User

from experiments.models import Experiment


class ExperimentForm(forms.ModelForm):

    class Meta:
        model = Experiment
        exclude = ('status',)
        widgets = {
            'supervisor': Select2Widget,
            'co_authors': Select2MultipleWidget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = User.objects.filter(is_superuser=False)
        self.fields['co_authors'].choices = [(u.id, u.get_full_name()) for u in users]
        self.fields['supervisor'].choices = [(u.id, u.get_full_name()) for u in users.filter(groups__name='servidores')]
        self.fields['supervisor'].choices += [('', '--------')]
