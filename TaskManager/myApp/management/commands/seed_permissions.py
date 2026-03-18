from django.core.management import BaseCommand
from myApp.models import Permission, RolePermission, Role

class Command(BaseCommand):
    help = 'seed initial permissions, roles and role permissions'

    def handle(self,*args,**kwargs):
        permissions = [
            'create_task',
            'view_task',
            'update_task',
            'delete_task',
            'assign_task',
            'change_task_status',
            'create_user',
            'update_user',
            'update_password',
            'delete_user',
            'view_users'
        ]
        roles = [
            'Manager',
            'Member'
        ]

        role_permissions = {
            'Manager': [
                'create_task',
                'view_task',
                'update_task',
                'delete_task',
                'assign_task',
                'change_task_status',
                'create_user',
                'update_user',
                'update_password',
                'delete_user',
                'view_users'
            ],
            'Member': [
                'create_task',
                'view_task',
                'update_password',

            ]
        }
        for permission in permissions:
            obj, created = Permission.objects.get_or_create(
                name=permission,
                codename=permission
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created permission: {permission}"))


        for role in roles:
            obj, created = Role.objects.get_or_create(name=role)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created role: {role}"))

        for role_name, permission_list in role_permissions.items():
            role = Role.objects.get(name=role_name)
            for permission_name in permission_list:
                permission_obj = Permission.objects.get(codename=permission_name)
                obj,created=RolePermission.objects.get_or_create(
                    role=role,
                    permission=permission_obj)

                self.stdout.write(self.style.SUCCESS(f"Assigned permission: {permission_name}"))

# def seed_permissions():
#     permissions = [
#         'create_task',
#         'view_task',
#         'update_task',
#         'delete_task',
#         'assign_task',
#         'change_task_status',
#         'create_user',
#         'update_user',
#         'update_password',
#         'delete_user',
#         'view_users'
#     ]



