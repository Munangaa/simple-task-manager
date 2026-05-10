from django.core.management import BaseCommand
from django.utils.translation.trans_null import activate
from myApp.models import Permission, RolePermission, Role

from TaskManager.myApp.models import States


class Command(BaseCommand):
    help = 'seed initial permissions, roles and role permissions'

    def handle(self,*args,**kwargs):


        states_data = [
            ('ACTIVE', 'Active'),
            ('DISABLED', 'Disabled'),
            ('PENDING', 'Pending'),
            ('APPROVED', 'Approved'),
            ('REJECTED', 'Rejected'),
            ('DELETED', 'Deleted'),
            ('IN_PROGRESS', 'In Progress'),
            ('DONE', 'Done'),
        ]

        for status_type,name in states_data:
            state, created = States.objects.get_or_create(
                status_type=status_type,
                defaults={'name':name}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created state: {name}'))

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

        for permission in permissions:
            obj, created = Permission.objects.get_or_create(
                name=permission,
                codename=permission
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created permission: {permission}"))

        roles = [
            'Manager',
            'Member'
        ]
        active_state = States.objects.get(status_type = 'ACTIVE')

        for role in roles:
            obj, created = Role.objects.get_or_create(
                name=role,
                defaults={'state':active_state}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created role: {role}"))

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

        for role_name, permission_list in role_permissions.items():
            role = Role.objects.get(name=role_name)
            for permission_name in permission_list:
                permission_obj = Permission.objects.get(codename=permission_name)
                obj,created=RolePermission.objects.get_or_create(
                    role=role,
                    permission=permission_obj)
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Assigned permission: {permission_name}"))

            self.stdout.write(self.style.SUCCESS('DATABASE seeded successfully'))

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



