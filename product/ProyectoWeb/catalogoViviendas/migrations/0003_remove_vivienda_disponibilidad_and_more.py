# Generated by Django 5.1.2 on 2024-11-14 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogoViviendas', '0002_alter_vivienda_imagen_alter_vivienda_ubicacion_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vivienda',
            name='disponibilidad',
        ),
        migrations.RemoveField(
            model_name='vivienda',
            name='fecha_disponible_desde',
        ),
        migrations.RemoveField(
            model_name='vivienda',
            name='fecha_disponible_hasta',
        ),
    ]
