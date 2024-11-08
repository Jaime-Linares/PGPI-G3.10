# Generated by Django 5.1.2 on 2024-11-08 09:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vivienda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('imagen', models.ImageField(upload_to='viviendas')),
                ('disponibilidad', models.BooleanField(default=True)),
                ('fecha_disponible_desde', models.DateField()),
                ('fecha_disponible_hasta', models.DateField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viviendas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'vivienda',
                'verbose_name_plural': 'viviendas',
            },
        ),
    ]
