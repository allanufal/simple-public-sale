# Generated by Django 2.0 on 2017-12-21 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channels_core', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='grupo',
            field=models.OneToOneField(blank=True, null=True, on_delete=True, to='channels_core.GrupoEvento'),
        ),
    ]
