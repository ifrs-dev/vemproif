import csv

from django import forms


def validate_file_extension(value):
        if not value.name.endswith('.csv'):
            raise forms.ValidationError("Apenas arquivos csv são aceitos.")

class ImportForm(forms.Form):
    docfile = forms.FileField(label='Selecionar Arquivo',validators=[validate_file_extension])

    def clean_docfile(self):
        docfile = self.cleaned_data['docfile'].read().decode('utf-8')
        data = csv.reader(docfile, delimiter=',', quotechar='"')
        for a in data:
            print(a)
        raise forms.ValidationError("Apenas arquivos csv são aceitos.")
        return docfile