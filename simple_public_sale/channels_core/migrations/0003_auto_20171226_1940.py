# Generated by Django 2.0 on 2017-12-26 19:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('channels_core', '0002_auto_20171221_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupoevento',
            name='id',
            field=models.UUIDField(default=uuid.UUID('bffc0749-aa64-4e62-81c5-1e97d8d7ad58'), editable=False, primary_key=True, serialize=False),
        ),
    ]