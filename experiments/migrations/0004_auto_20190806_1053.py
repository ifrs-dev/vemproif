# Generated by Django 2.2.3 on 2019-08-06 13:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0003_remove_experiment_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='materials',
            field=models.TextField(default='', help_text='Exemplo: 2 mesas e uma fonte de energia', verbose_name='Materiais Necessários'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='experiment',
            name='supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supervised_experiments', to=settings.AUTH_USER_MODEL, verbose_name='Orientador'),
        ),
    ]
