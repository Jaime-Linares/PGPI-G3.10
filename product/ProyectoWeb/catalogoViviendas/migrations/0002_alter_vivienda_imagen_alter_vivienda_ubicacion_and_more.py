# Generated by Django 5.1.2 on 2024-11-14 13:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogoViviendas', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='vivienda',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='viviendas'),
        ),
        migrations.AlterField(
            model_name='vivienda',
            name='ubicacion',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('precio_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('creada', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vivienda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservas', to='catalogoViviendas.vivienda')),
            ],
        ),
    ]
