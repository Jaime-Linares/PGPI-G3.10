from django.db import migrations, models
from django.utils import timezone
from django.conf import settings
import django.db.models.deletion

import os
from django.conf import settings

def create_initial_properties(apps, schema_editor):
    Vivienda = apps.get_model("catalogoViviendas", "Vivienda")
    User = apps.get_model("auth", "User")

    try:
        propietario = User.objects.get(username="userPropietario")
    except User.DoesNotExist:
        print("El usuario 'userPropietario' no existe.")
        return 

    propiedades = [
        {
            "nombre": "El Molino",
            "descripcion": "El Molino cuenta con una terraza y jardines con vistas al océano Atlántico. Esta casa de 3 dormitorios está ubicada en Villa de Mazo, en un edificio del siglo XVIII que cuenta con suelo y techos de madera original. La sala de estar dispone de TV de pantalla plana, mesa de comedor y sofá, mientras que la cocina está equipada con horno, lavadora, microondas y utensilios de cocina. El baño incluye ducha y secador de pelo. La casa tiene 1 dormitorio con 1 cama doble, 1 dormitorio con 2 camas individuales y 1 dormitorio individual. Se ofrece conexión Wi-Fi gratuita y hay una barbacoa y tumbonas en el jardín. El centro de artesanía El Molino, que ofrece elementos de cerámica elaborados de forma tradicional, se encuentra junto a la casa. Santa Cruz de la Palma está a 12 km del establecimiento y el aeropuerto de La Palma se sitúa a 4,5 km.",
            "ubicacion": "Monte Pueblo, Villa de Mazo",
            "precio_por_dia": 80.00,
            "imagen": os.path.join(settings.MEDIA_URL, 'viviendas/el_molino.jpg'),
            "wifi": True,
            "piscina": False,
            "parking": False,
            "aire_acondicionado": True,
            "barbacoa": True,
            "ducha": True,
            "cocina": True,
            "propietario": propietario,
        },
        {
            "nombre": "Casa Atilano",
            "descripcion": "Casa Atilano Las Puntas La Frontera El Hierro ofrece terraza y vistas al mar. Se encuentra en Las Puntas, a 27 km de Roque de la Bonanza y a 30 km de Faro de Orchilla. El alojamiento, que está a 13 km de Playa del Verodal, ofrece jardín y parking privado gratis.Esta casa o chalet de 3 dormitorios dispone de wifi gratis, TV de pantalla plana, lavadora y cocina con nevera y microondas. Hay toallas y ropa de cama en la casa o chalet. El aeropuerto (Aeropuerto de El Hierro) está a 20 km.",
            "ubicacion": "Las Puntas, España",
            "precio_por_dia": 100.00,
            "imagen": os.path.join(settings.MEDIA_URL, 'viviendas/casa_atilano.jpg'),
            "wifi": True,
            "piscina": True,
            "parking": True,
            "aire_acondicionado": True,
            "barbacoa": True,
            "ducha": True,
            "cocina": True,
            "propietario": propietario,
        },
    ]

    for propiedad_data in propiedades:
        imagen_path = os.path.join(settings.MEDIA_ROOT, propiedad_data["imagen"].replace(settings.MEDIA_URL, ''))
        if os.path.exists(imagen_path):
            propiedad_data["imagen"] = propiedad_data["imagen"].replace(settings.MEDIA_URL, '')
            Vivienda.objects.get_or_create(**propiedad_data)
        else:
            print(f"Imagen no encontrada: {imagen_path}")


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
                ('precio_por_dia', models.DecimalField(max_digits=10, decimal_places=2)),
                ('ubicacion', models.CharField(max_length=255)),
                ('wifi', models.BooleanField(default=False)),
                ('piscina', models.BooleanField(default=False)),
                ('parking', models.BooleanField(default=False)),
                ('aire_acondicionado', models.BooleanField(default=False)),
                ('barbacoa', models.BooleanField(default=False)),
                ('ducha', models.BooleanField(default=False)),
                ('cocina', models.BooleanField(default=False)),
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