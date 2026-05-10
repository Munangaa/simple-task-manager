from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create superuser with staff access'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_superuser(
                username='admin',
                email='admin@taskit.com',
                password='Admin1234!'
            )
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write('Superuser created successfully!')
        else:
            # ✅ Update existing admin to have staff access
            user = User.objects.get(username='admin')
            user.is_staff = True
            user.is_superuser = True
            user.set_password('Admin1234!')
            user.save()
            self.stdout.write('Superuser updated successfully!')