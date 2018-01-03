# Generated by Django 2.0 on 2018-01-03 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_tipoprenda_url_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caracteristica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caracteristica', models.CharField(max_length=60)),
                ('descricao', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='CaracteristicaPrenda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.CharField(max_length=100)),
                ('caracteristica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Caracteristica')),
                ('prenda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Prenda')),
            ],
        ),
        migrations.AlterField(
            model_name='evento',
            name='data_evento',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='prenda',
            name='caracteristicasPrenda',
            field=models.ManyToManyField(through='core.CaracteristicaPrenda', to='core.Caracteristica'),
        ),
    ]
