# Generated by Django 2.0 on 2017-12-26 21:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('channels_core', '0003_auto_20171226_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupoevento',
            name='id',
            field=models.UUIDField(default=uuid.UUID('b2a54188-09b9-4485-9637-18a10f2bc460'), editable=False, primary_key=True, serialize=False),
        ),
    ]
