import csv

from django import forms
from django.contrib.auth.models import User, Group



def validate_file_extension(value):
        if not value.name.endswith('.csv'):
            raise forms.ValidationError("Apenas arquivos csv são aceitos.")

class ImportForm(forms.Form):
    docfile = forms.FileField(label='Selecionar Arquivo',validators=[validate_file_extension])


class ImportFormSIGAA(ImportForm):

    def clean_docfile(self):
        csv_file = self.cleaned_data['docfile']
        lines = csv_file.read().decode("utf-8").split("\n")
        for line in lines[1:]:
            try:
                fields = line.split(",")
                username = fields[2].replace('"', '')
                first_name = fields[0].replace('"', '')
                password = fields[4].replace('"', '')
                user, created = User.objects.get_or_create(username=username, first_name=first_name)
                if created:
                    user.set_password(password)
                    user.save()
            except:
                break
        return csv_file


class ImportFormSIA(ImportForm):

    def clean_docfile(self):
        csv_file = self.cleaned_data['docfile']
        lines = csv_file.read().decode("utf-8").split("\n")
        for line in lines[1:]:
            try:
                fields = line.split(",")
                cpf = fields[7].replace('"', '')
                username = '%s.%s.%s-%s' % (cpf[0:3], cpf[3:6], cpf[6:9], cpf[9:11])
                first_name = fields[1].replace('"', '')
                password = fields[0].replace('"', '')
                password = password
                user, created = User.objects.get_or_create(username=username, first_name=first_name)
                if created:
                    user.set_password(password)
                    user.save()
            except:
                break
        return csv_file


class ImportFormServ(ImportForm):

    def clean_docfile(self):
        csv_file = self.cleaned_data['docfile']
        lines = csv_file.read().decode("utf-8").split("\n")
        serv_group, created = Group.objects.get_or_create(name='servidores')
        for line in lines[1:]:
            fields = line.split(",")
            username = fields[2].replace('"', '').strip()
            first_name = upper(fields[1].replace('"', '').strip())
            password = fields[0].replace('"', '').strip()
            user, created = User.objects.get_or_create(username=username, first_name=first_name)
            serv_group.user_set.add(user)
            if created:
                user.set_password(password)
                user.save()
        return csv_file
