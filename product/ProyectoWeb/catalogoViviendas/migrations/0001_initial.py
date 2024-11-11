from django.db import migrations, models
from django.utils import timezone
from django.conf import settings
import django.db.models.deletion

def create_initial_properties(apps, schema_editor):
    Vivienda = apps.get_model("catalogoViviendas", "Vivienda")
    User = apps.get_model("auth", "User")

    try:
        propietario = User.objects.get(username="userPropietario")
    except User.DoesNotExist:
        print("El usuario 'userPropietario' no existe. Asegúrate de crearlo antes de ejecutar esta migración.")
        return 

    propiedades = [
        {
            "nombre": "El Molino",
            "descripcion": "La sala de estar dispone de TV de pantalla plana, mesa de comedor y sofá...",
            "ubicacion": "Monte Pueblo,29,38730 Villa de Mazo, España",
            "precio_por_dia": 80.00,
            "fecha_disponible_desde": timezone.datetime(2024, 11, 20),
            "fecha_disponible_hasta": timezone.datetime(2024, 12, 5),
            "propietario": propietario,
        },
        {
            "nombre": "Casa Atilano",
            "descripcion": "Casa Atilano Las Puntas La Frontera El Hierro ofrece terraza y vistas al mar...",
            "ubicacion": "Las Puntas, España",
            "precio_por_dia": 100.00,
            "fecha_disponible_desde": timezone.datetime(2024, 11, 12),
            "fecha_disponible_hasta": timezone.datetime(2024, 11, 15),
            "propietario": propietario,
        },
    ]

    for propiedad_data in propiedades:
        Vivienda.objects.get_or_create(**propiedad_data)

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
                ('precio_por_dia', models.DecimalField(max_digits=10, decimal_places=2)),
                ('ubicacion', models.CharField(max_length=255)),  # Nuevo campo
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viviendas', to=settings.AUTH_USER_MODEL)),
                    ],
            options={
                'verbose_name': 'vivienda',
                'verbose_name_plural': 'viviendas',
            },
        ),
        migrations.RunPython(create_initial_properties),
    ]
