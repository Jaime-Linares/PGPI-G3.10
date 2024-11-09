from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group


@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    roles = ['Cliente', 'Propietario']
    for role in roles:
        if not Group.objects.filter(name=role).exists():
            Group.objects.create(name=role)
            print(f"Rol '{role}' creado exitosamente.")
