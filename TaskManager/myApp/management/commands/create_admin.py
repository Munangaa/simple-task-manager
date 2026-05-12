from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from myApp.models import Role

class Command(BaseCommand):
    help = 'Create superuser with staff access'

    def handle(self, *args, **kwargs):
        self.stdout.write('=== CREATE ADMIN STARTED ===')
        User = get_user_model()


        try:
            role = Role.objects.get(name='Manager')
        except Role.DoesNotExist:
            self.stdout.write(' Manager role not found!')
            return


        # if User.objects.filter(username='admin').exists():
        User.objects.filter(username='admin').delete()
        self.stdout.write('Deleted existing admin')

        # if not User.objects.filter(username='admin').exists():
        try:
            user = User.objects.create_superuser(
                username='admin',
                email='admin@taskit.com',
                password = 'Admin1234!',
                user_role=role,
            )

            self.stdout.write('Superuser created!')
            self.stdout.write(f'is_staff: {user.is_staff}')
            self.stdout.write(f'is_superuser: {user.is_superuser}')
            self.stdout.write(f'is_active: {user.is_active}')
        except Exception as e:
            self.stdout.write(f'error{e}')
        #     user.user_role = role
        #     user.is_staff=True,
        #     user.is_superuser= True,
        #     user.is_active=True,
        #
        #     # user.set_password('Admin1234!')
        #     user.save()
        #     # self.stdout.write(' Superuser created!')
        # # else:
        # #     user = User.objects.get(username='admin')
        # #     user.is_staff = True
        # #     user.is_superuser = True
        # #     user.user_role = role
        # #     user.set_password('Admin1234!')
        # #     user.save()
        # #     self.stdout.write(' Superuser updated!')
        # self.stdout.write(f'Superuser created!')
        # self.stdout.write(f'is_staff: {user.is_staff}')
        # self.stdout.write(f'is_superuser: {user.is_superuser}')
        # self.stdout.write(f'is_active: {user.is_active}')