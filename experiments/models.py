from django.db import models
from django.contrib.auth.models import User

CHOICES_STATUS_EVENT = (
    (1, "Submetido"),
    (2, "Aprovado"),
    (3, "Não aprovado"),
    (3, "Não Apresentado"),
)


class Experiment(models.Model):

    class Meta:
        verbose_name = "Trabalho"
        verbose_name_plural = "Trabalhos"

    title = models.CharField(max_length=100, verbose_name='Título')
    description = models.TextField(verbose_name='Resumo (Breve descrição)', help_text='Paragráfo único com no máximo 50 palavras.')
    materials = models.TextField(verbose_name='Materiais Necessários', help_text='Exemplo: 2 mesas e uma fonte de energia')
    goal = models.CharField(max_length=150, verbose_name='Objetivo')
    status = models.IntegerField(choices=CHOICES_STATUS_EVENT, default=1, verbose_name='Status')
    author = models.OneToOneField(User, verbose_name='Autor', on_delete=models.PROTECT, related_name='author_experiments')
    co_authors = models.ManyToManyField(User, verbose_name='Co-autores', related_name='co_authors_experiments', blank=True)
    supervisor = models.ForeignKey(User, verbose_name='Orientador', on_delete=models.PROTECT, related_name='supervised_experiments', blank=True, null=True)
    #attachment = models.FileField(blank=True, null=True, upload_to=True, verbose_name='Anexo')

    def __str__(self):
        return self.title

    def get_author(self):
        authors = [self.author.get_full_name()]
        authors += [u.get_full_name() for u in self.co_authors.all()]
        if self.supervisor:
            authors += [self.supervisor.get_full_name()]
        return ', '.join(authors)
