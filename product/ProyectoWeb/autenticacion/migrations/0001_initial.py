from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_roles_and_users(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    User = apps.get_model('auth', 'User')

    roles = ['Cliente', 'Propietario']
    created_groups = {}
    for role in roles:
        group, _ = Group.objects.get_or_create(name=role)
        created_groups[role] = group

    users = [
        {"username": "userCliente", "email": "cliente@example.com", "password": "12345678!Aa", "group": created_groups['Cliente']},
        {"username": "userPropietario", "email": "propietario@example.com", "password": "12345678!Aa", "group": created_groups['Propietario']},
    ]

    for user_data in users:
        user, created = User.objects.get_or_create(
            username=user_data["username"],
            defaults={
                "email": user_data["email"],
                "password": make_password(user_data["password"])
            }
        )
        if created:
            user.groups.add(user_data["group"])

    admin_user, admin_created = User.objects.get_or_create(
        username="admin",
        defaults={
            "email": "admin@example.com",
            "password": make_password("admin"),
            "is_superuser": True,
            "is_staff": True
        }
    )

class Migration(migrations.Migration):

    dependencies = []  

    operations = [
        migrations.RunPython(create_roles_and_users),
    ]
