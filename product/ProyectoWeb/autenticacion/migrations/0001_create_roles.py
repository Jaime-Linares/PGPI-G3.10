from django.db import migrations

def create_roles(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    roles = ['Cliente', 'Propietario']
    for role in roles:
        if not Group.objects.filter(name=role).exists():
            Group.objects.create(name=role)

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_roles),
    ]
