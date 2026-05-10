from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from myApp.models import Role

class Command(BaseCommand):
    help = 'Create superuser with staff access'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # ✅ Get Manager role
        try:
            role = Role.objects.get(name='Manager')
        except Role.DoesNotExist:
            self.stdout.write(' Run seed_permissions first!')
            return

        if not User.objects.filter(username='admin').exists():
            user = User(
                username='admin',
                email='admin@taskit.com',
                is_staff=True,
                is_superuser=True,
                user_role=role,
            )
            user.set_password('Admin1234!')
            user.save()
            self.stdout.write(' Superuser created!')
        else:
            user = User.objects.get(username='admin')
            user.is_staff = True
            user.is_superuser = True
            user.user_role = role
            user.set_password('Admin1234!')
            user.save()
            self.stdout.write(' Superuser updated!')